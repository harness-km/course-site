This week you write an agent by hand. There is no framework: just the Anthropic SDK, four read-only tools over the procure-to-pay tables, and a loop of about 30 lines. By the end of the reading you should be able to say what the model sees when it "uses a tool", what your code must send back, and why the loop needs a hard stop. Those three ideas explain most of the agent behaviour you have seen in n8n, good and bad, and they are the foundation for everything that follows in the course.

### A tool is a function plus a manual

A tool has two halves. One half is an ordinary Python function that runs on your machine, such as `get_supplier(supplier_ref)`. The other half is a short manual that you send to the model: a name, a description and an input schema. The model never sees your Python. It never reads your docstring, your regular expressions or your SQL. It reads the manual, decides whether to ask for the tool, and writes the arguments.

Here is the manual for the worked example in the notebook:

```python
{"name": "get_supplier",
 "description": "Look up a supplier in the supplier master by supplier ID (like S01) or GSTIN.",
 "input_schema": {"type": "object",
                  "properties": {"supplier_ref": {"type": "string"}},
                  "required": ["supplier_ref"]}}
```

The description is doing real work. `get_supplier` accepts either a supplier ID or a GSTIN, and the only way the model can know that is the phrase "by supplier ID (like S01) or GSTIN". An invoice from Sahyadri Beverages prints a GSTIN, `29GHTWA4257Z1ZH`, not `S01`. If the description said only "Look up a supplier", a reasonable model might pass the supplier's name, "Sahyadri Beverages Pvt Ltd", and get an error back. Nothing in your code would be wrong; the manual would be.

So write descriptions for a reader who has nothing else. Say what the tool returns, what the argument looks like (with an example), and when to use it rather than a neighbouring tool. Keep them short, because the whole list of tool definitions is sent again on every call. A description is not written once and forgotten: you pay for its tokens on every turn of every run.

In n8n, the AI Agent node builds this manual for you from the tool node's name, its description field and any `$fromAI` placeholders. The mechanism is the same. The difference is that you can now print exactly what was sent.

### Required and optional arguments

The `required` list in the schema tells the model which arguments it must supply. It is tempting to mark everything as required, to be safe. It has the opposite effect.

Suppose a hypothetical tool for searching the catalogue were defined like this:

```python
"input_schema": {"type": "object",
                 "properties": {"supplier_id": {"type": "string"},
                                "hsn_code":    {"type": "string"},
                                "max_price":   {"type": "number"}},
                 "required": ["supplier_id", "hsn_code", "max_price"]}
```

Ask the agent "what does Kaveri Foods supply?" and it has a supplier but no HSN code and no price limit. The schema says it must provide all three, so it will invent them: an HSN code that looks plausible, a round number for the price. The query then runs with filters nobody asked for, returns a narrower list than the truth, and the answer looks confident.

The rule is to require only what the function cannot work without. In the lab, `find_similar_invoices(supplier_id, amount=None)` needs the supplier, and the amount is an optional filter. Your Python signature and your schema should agree: a parameter with a default in Python is usually an optional property in the schema.

### The loop, one turn at a time

The model cannot run a tool. When it wants one, it stops and says so. Your code runs the tool, sends the result back, and calls the model again. That cycle is the whole agent.

Each response has a `stop_reason`. If it is `"end_turn"`, the model has finished and replied in text. If it is `"tool_use"`, the response content contains one or more `tool_use` blocks, each with a type, an id, the tool name and the arguments. Your loop must then:

1. Append the assistant's response, unchanged, to the message list.
2. Run every tool the model asked for.
3. Send back exactly one `tool_result` for each `tool_use`, matched by id, all inside one user message.
4. Call the model again with the longer message list.

Here is a shortened trace for the question in the lab, "Has PO-1001 been fully received, and has it been invoiced?". The ids are abbreviated, and the model may choose a different order on your run.

```text
[0] user       "Has PO-1001 been fully received, and has it been invoiced?"

[1] assistant  stop_reason = "tool_use"
               {type: "text", text: "I'll start with the purchase order."}
               {type: "tool_use", id: "toolu_01A", name: "get_purchase_order",
                input: {"po_id": "PO-1001"}}

[2] user       {type: "tool_result", tool_use_id: "toolu_01A",
                content: '{"po_id": "PO-1001", "supplier_id": "S01", "status": "open", "lines": [...]}',
                is_error: false}

[3] assistant  stop_reason = "tool_use"
               {type: "tool_use", id: "toolu_01B", name: "get_goods_receipt",
                input: {"po_id": "PO-1001"}}
               {type: "tool_use", id: "toolu_01C", name: "find_similar_invoices",
                input: {"supplier_id": "S01"}}

[4] user       {type: "tool_result", tool_use_id: "toolu_01B", content: '{... "fully_received": true}', is_error: false}
               {type: "tool_result", tool_use_id: "toolu_01C", content: '{"supplier_id": "S01", "invoices": [...]}', is_error: false}

[5] assistant  stop_reason = "end_turn"
               {type: "text", text: "PO-1001 is fully received: 120 cases of Instant Coffee and
                80 cases of Soda Water. None of S01's recorded invoices refers to PO-1001."}
```

Three things are worth noticing. First, in message 3 the model asked for two tools in one turn. Both results go back together in message 4, one per id. Second, the model learned the supplier ID `S01` from the first result and used it in the third call. It did not guess it; the tool told it. Third, the tool results travel in a message with the role `user`. There is no separate "tool" role in the Messages API.

The ids are how the API keeps the conversation consistent. If a `tool_use` has no matching `tool_result` in the next message, the API rejects the whole request. One of the stretch steps asks you to delete the line that appends the results and read that error; it is worth doing once so you recognise it later.

The message list is the agent's memory. The model does not remember message 2 when it writes message 5; your code re-sends it. When a run behaves strangely, print the message list first. The notebook has a cell that does this.

### Failure becomes information

Tools fail. A PO number is mistyped, a supplier is missing from the master, a query hits a column that was renamed. What your loop does next decides whether the agent is robust or fragile.

The fragile version lets the Python exception escape. The loop crashes, the run is lost, and the model never learns what happened. The robust version catches the exception and turns it into a tool result flagged as an error. The pattern looks like this:

```python
{"type": "tool_result", "tool_use_id": block.id,
 "content": "Tool get_goods_receipt failed: KeyError: 'qty_received'",
 "is_error": True}
```

Now the failure is part of the conversation. The model can try another argument, try another tool, or explain in its final answer that one lookup failed. This is the first appearance of a principle that runs through the whole course: failure becomes information. A crash tells nobody anything; an error result tells the model, and later a person, what went wrong.

There is a second kind of failure that is harder to spot: a result that is empty but looks valid. Imagine `get_purchase_order("PO-9999")` returned `{"po_id": "PO-9999", "lines": []}`. To the model this reads as "a real purchase order with no lines", and it may reason from there to a wrong answer. The lab asks for explicit errors instead, and the provided `get_supplier` shows the style:

```python
if row is None:
    return {"error": f"Supplier {supplier_ref} not found in the supplier master. Treat as an unknown supplier."}
```

A good error message says what happened and what to do next. "Not found. Check the PO number on the invoice, or ask a person" gives the model a sensible next step. "Invalid input" does not. The self-check looks for the exact phrase `PO-9999 not found`, so keep that wording at the start of your message.

### Ending well: step limits and the status report

A loop that runs until the model says it is done has handed the exit to the model. Most of the time that is fine. Sometimes the model keeps calling tools: it retries a failing lookup, or it wanders through every past invoice for a supplier. Without a limit, each extra turn costs money and time, and the run may never finish.

So `run_agent` takes `max_steps`. When the limit is reached, the loop does not simply stop. It adds a short text block to the last user message asking for a status report (what was found, what is still unknown) and makes one final call in which the model cannot use tools. Two details matter here. The request goes after the tool results in that message, because tool results must come first in a user message. And the final call must be one that cannot ask for another tool, or the report may be another tool request.

The rule "never end a run without a report" exists because a silent stop is the worst outcome for the person relying on the agent. They cannot tell a finished run from an abandoned one.

The opposite failure also happens. A model sometimes writes "I'll now check the goods receipt." and stops, with `stop_reason == "end_turn"` and no `tool_use` block. Your loop sees a text reply and returns it, correctly: prose without a tool call ends the loop. The agent announced an action instead of taking it. The system prompt in the lab asks the model to use the tools and to reply with a summary only when it has the answer, which reduces this, but you should be able to recognise it in a trace. The short name for the habit you want from the model is "act, don't narrate".

### The message list grows, and so does the bill

Look at the input tokens the loop prints at each step. They go up every turn, and the reason is simple arithmetic. Each call sends the system prompt, every tool definition, the original question, every assistant message so far and every tool result so far. The API also adds its own instructions for tool use, which count as input. Nothing is dropped between turns.

That has two consequences. First, a four-turn run does not cost four times a one-turn run; it costs more, because the later turns carry the earlier ones. Second, the size of your tool results matters. If `get_purchase_order` returned every column of every joined row, those tokens would be re-sent on every later turn. This is why the lab asks for a small dict of named fields rather than whole rows. Compact results are the resource meter's optimisation this week.

Record the input tokens per turn for the PO-1001 question. You will compare them with the Week 4 graph, which does the same lookups with far fewer model calls.

### Blast radius: what is the worst each tool can do?

Giving a model tools gives it agency. The security question for every tool is: if the model, or someone steering it through an invoice or a chat message, called this tool with the worst possible arguments, what could happen? That is the tool's blast radius. The threat category is excessive agency: more capability than the task needs.

The lab narrows the blast radius in three layers.

**A read-only connection.** The notebook opens the database with `mode=ro`:

```python
con = sqlite3.connect(f"file:{env.db}?mode=ro", uri=True)
```

Any attempt to insert, update or delete through this connection fails, whatever SQL reaches it. The lookup tools do not need to write, so they are not allowed to. This is least privilege, applied at the lowest level available.

**Validate IDs before they reach SQL.** Supplier IDs must match `^S\d{2}$` and PO numbers `^PO-\d{4}$`. Anything else is refused with an explicit error before a query is built. This stops malformed input early and also produces a helpful message for the model.

**Parameterised SQL.** The value goes in as a parameter, marked by `?`, never pasted into the SQL text:

```python
# Unsafe: the value becomes part of the SQL
con.execute(f"select * from purchase_orders where po_id = '{po_id}'")

# Safe: the value is passed separately and is only ever treated as data
con.execute("select * from purchase_orders where po_id = ?", (po_id,))
```

With the f-string, an ID of `PO-1001' OR '1'='1` turns the query into `... where po_id = 'PO-1001' OR '1'='1'`. The condition is true for every row, so the tool returns every purchase order in the database. With the placeholder, the database looks for a PO whose ID is literally that whole string, finds none, and returns nothing. In the lab, the pattern check refuses the ID even before that.

Why two defences for one attack? Because each one can fail on its own. A pattern can be written too loosely, or skipped in a hurry in the next tool someone adds. Placeholders are the defence that holds even when the input check is wrong. The read-only connection is a third layer: even a successful injection cannot change data. When you fill in the threat-model rows this week, write down the layer each defence belongs to.

### Bring to the live session

- Your trace for the PO-1001 question: which tools were called, in what order, and did the model ever call one it did not need?
- Your input tokens per turn. Which tool result added the most?
- ADR 3 asks whether the model or code should choose which tools to call. For invoice processing, what would you lose by letting code decide?

### Self-quiz

**1. Predict the output.** Using the provided `get_supplier`, what do these two lines print?

```python
print(get_supplier("s01"))
print(get_supplier("S09"))
```

<details><summary>Answer</summary>

```text
{'error': "'s01' is not a supplier ID (like S01) or a GSTIN."}
{'error': 'Supplier S09 not found in the supplier master. Treat as an unknown supplier.'}
```

`"s01"` fails the pattern check (`^S\d{2}$` needs a capital S), so no SQL runs at all. `"S09"` passes the pattern but there is no such supplier: the dataset has S01 to S08. Both are explicit errors, and both tell the model something it can act on. Neither returns an empty dict that could be mistaken for a real supplier.

</details>

**2. What is wrong with this trace?** The next API call failed.

```text
[3] assistant  stop_reason = "tool_use"
               {type: "tool_use", id: "toolu_01B", name: "get_goods_receipt", input: {"po_id": "PO-1001"}}
               {type: "tool_use", id: "toolu_01C", name: "find_similar_invoices", input: {"supplier_id": "S01"}}

[4] user       {type: "tool_result", tool_use_id: "toolu_01B", content: '{... "fully_received": true}', is_error: false}
```

<details><summary>Answer</summary>

The model asked for two tools, but only one result came back. `toolu_01C` has no matching `tool_result`, so the API rejects the conversation. The usual cause is a loop that returns or breaks after the first `tool_use` block instead of running every block in the response. The fix is to build one result per `tool_use` id and send them all together in the same user message. If `find_similar_invoices` had raised an exception, the answer is the same: it still needs a result, flagged `is_error`.

</details>
