Last week the model decided which lookups to run and when to stop. This week you take that decision away from it. You rebuild the same lookups as a LangGraph `StateGraph`, where your code fixes the order of the steps and the model is used only where it is needed: reading the invoice and structuring it. The reading covers the question behind the whole week (who owns the exit?), the handful of LangGraph ideas you need, how to design the state, and why a graph cannot be talked out of a step the way a prompted agent can.

### Who owns the exit?

"Agent" and "workflow" are often used as if they were different technologies. The more useful distinction is simpler: who decides what happens next, and who decides when the work is done?

In the Week 3 loop, the model owns both. It chooses the next tool, and the run ends when it replies in text instead of asking for a tool. Your code only provides the tools and a step limit. That is the right design when you cannot know the steps in advance. A coding agent asked to "fix this failing test" might need to read three files or thirty; the Odysseus reference agent lets the model own the loop for exactly this reason.

Invoice processing is different. Every invoice goes through the same steps in the same order: read it, structure it, find the supplier, find the purchase order, find the goods receipt, then match. Nothing about a particular invoice changes that order. When the order is known, code should own it. The model still does what only a model can do, turning a PDF into text and text into fields, but it no longer decides the route.

This is not a rule that graphs are better than agents. It is a question to ask about each process: is the path known in advance, or discovered as you go? Many real systems are hybrids, with a fixed graph and one node inside it that runs a small agent loop for an open-ended sub-task. ADR 4 asks you to make this call for invoices and give reasons.

### LangGraph in six ideas

LangGraph gives you a small vocabulary for writing a process as a graph. You need six ideas this week.

**State.** One object that holds everything the run knows so far. You declare its shape up front as a `TypedDict`:

```python
class InvoiceState(TypedDict, total=False):
    file: str
    raw_text: str
    ...
```

`total=False` means no key is required to be present. That matters because the run starts with almost nothing, just `{"file": ".../INV-A.pdf"}`, and fields fill in as nodes run. Note that a `TypedDict` describes the shape for you and your editor; it does not check values at runtime. The guide allows a Pydantic model as state instead, which does validate; the lab uses `TypedDict` to keep things light.

**Nodes.** A node is a plain Python function that takes the current state and returns a dict of only the fields it changes. It does not return the whole state, and it should not modify the state it was given. The provided `read` node is the pattern:

```python
def read(state: InvoiceState) -> dict:
    try:
        return {"raw_text": read_invoice(state["file"])}
    except Exception as e:
        return fail(state, "error", f"read: {type(e).__name__}: {e}")
```

LangGraph takes the returned dict and merges it into the state before the next node runs. By default a returned value simply replaces the old value for that key.

**Edges.** A normal edge says "after this node, always go to that one": `builder.add_edge("lookup_grn", END)`.

**Conditional edges.** A conditional edge calls a routing function after a node and uses its return value to choose the next node. The routing function reads the state and returns a label; a dict maps each label to a node:

```python
def route(state: InvoiceState) -> str:
    return state.get("status") if state.get("status") in ("error", "exception") else "next"

builder.add_conditional_edges("read", route,
                              {"next": "structure", "error": "error", "exception": "exception"})
```

In the lab, one routing function is reused after every step. Either the step went well and the run continues, or it set a status and the run goes to a terminal node.

**START and END.** Two special nodes mark where a run enters and where it finishes. Every path through the graph must eventually reach `END`.

**Compile and invoke.** `builder.compile()` turns the description into a runnable graph and checks the wiring, for example that every edge points at a node that exists. `graph.invoke(initial_state, config={"recursion_limit": 20})` runs it and returns the final state as a dict.

The recursion limit caps how many steps a single run may take. If a run exceeds it, LangGraph raises an error instead of carrying on. This week's graph has no loops, so a correct graph never gets near the limit. It is a safety net for the day someone adds a cycle by mistake, and next week you add a loop on purpose. A limit that stops a runaway run is a cost control as well as a correctness one; this is the security lens for the week.

### Designing the state

The lab's state has these fields: `file`, `raw_text`, `invoice`, `supplier`, `purchase_order`, `goods_receipt`, `errors` and `status`. Before you type them, work through two questions for each field.

**What does each node need?** `structure` needs `raw_text`. `lookup_supplier` needs the invoice's GSTIN, so it needs `invoice`. `lookup_po` needs the PO reference from the invoice, and also the supplier, because it checks that the PO belongs to that supplier. `lookup_grn` needs the purchase order's ID. If you can list each node's inputs, you can see the order of the graph, and you can see what would break if a node were skipped.

**Who may write each field?** Ideally each field has one owner. Only `read` writes `raw_text`. Only `structure` writes `invoice`. Only the supplier lookup writes `supplier`. When a field has one writer, a wrong value has one place to look. The exceptions are `status` and `errors`, which any node may write when something goes wrong, and which is why the notebook routes all such writes through one helper:

```python
def fail(state: InvoiceState, status: str, message: str) -> dict:
    return {"status": status, "errors": state.get("errors", []) + [message]}
```

Compare this with n8n, where each node sees whatever the previous node emitted, and reaching back to an earlier node's output needs an expression like `$('Node name').item.json`. A LangGraph state is one declared object that every node reads. Nothing disappears because a node in the middle reshaped the data.

### Errors and business exceptions

The lab separates two kinds of early stop, and the distinction is worth more than it first appears.

An **error** means something technical failed: the reading call was truncated, the structured output failed validation, the API timed out. The invoice may be perfectly fine. The right response is to look at the pipeline, fix or retry, and run it again. Status `"error"`.

An **exception** means the pipeline worked and found something that needs a person. The invoice was read and structured correctly, but it cannot go forward on its own. The course dataset has one of each kind you need to handle:

- **Unknown supplier.** INV-15 is from Nandi Trading Co. Its GSTIN has a valid format, but it is not in the supplier master. `get_supplier` returns its explicit not-found error.
- **No PO reference.** INV-07 from Malnad Home Care prints an empty "PO Ref". There is nothing to look up.
- **PO not found.** INV-16 from Coromandel Snacks quotes PO-9999, which does not exist.
- **PO of another supplier.** The PO exists but was raised with a different supplier. This is the case people forget, and it matters: a supplier who quotes someone else's open PO should not be matched against it.

Why keep them apart? Because they go to different people and are measured differently. Errors go to whoever runs the harness and should trend towards zero as the pipeline improves. Exceptions go to accounts payable, and a steady rate of them is normal business. If both are counted as "failed", neither team can see its own problem. When you write your lookup nodes, make each one return the right status with a message a person could act on, reusing the error text the Week 3 tools already produce.

### Why the graph cannot skip a step

This week's break-it asks you to persuade the Week 3 agent to skip the goods-receipt lookup. It is usually not hard. The system prompt says to use the tools, but a user message that sounds urgent and authoritative competes with it, and the model is trying to be helpful. It confirms the PO exists and declares the invoice payable without ever checking what arrived.

The graph has no such weakness, and it is worth being precise about why. After `lookup_po` succeeds, the routing function returns `"next"`, and the edge for `"next"` goes to `lookup_grn`. That is a line of Python. No text in any message is consulted when that decision is made. The model is not asked whether the goods receipt matters; it is not asked anything at all after `structure`. The only ways to reach `END` are through `lookup_grn`, `error` or `exception`.

This is a principle you will meet again: if it must always happen, it belongs in code, not in a prompt. A prompt is a request. An edge is a guarantee. The prompt should still be well written, because it shapes the model's work inside its node. But anything that must hold every time, whatever the input says, is enforced by structure.

### Fewer model calls, and what the numbers mean

Count the model calls in the graph for INV-A. There are two: `read` sends the page image to Sonnet and gets the transcription back, and `structure` turns that text into an `Invoice`. The three lookups are plain Python calling the Week 3 functions directly. They cost no tokens, take milliseconds, and give the same answer every time. The self-check expects exactly two calls.

In Week 3, each lookup was a model turn: the model asked for a tool, your code ran it, and the whole growing message list went back to the model. Even if the model asks for all three lookups in one turn, it needs a call to request them and another to answer, and in practice it often takes one lookup per turn. Each call re-sends the tool definitions and is larger than the last.

Step 5 asks you to compare the two, and it is worth reading the comparison carefully rather than just the ratio. The graph's two calls include reading the PDF with vision and structuring the result, both on Sonnet. The agent in the comparison is given the text already and only does lookups, on Haiku. So the two numbers are not measuring identical work. Ask yourself what each side includes before you draw a conclusion, and say so in your ADR. Being precise about what a measurement covers is part of the architect's job.

The model calls you removed are the ones that were deciding a route that was never in doubt. That is this week's resource meter optimisation: replace model-chosen steps with fixed edges.

### Drawing the graph

A compiled graph can describe itself. `graph.get_graph().draw_mermaid()` returns the graph as Mermaid text, and the notebook tries to render it as an image. The diagram is generated from the code, so it cannot drift from what actually runs. Paste the Mermaid text into your ADR 4: a reviewer can check the routes at a glance, and so can you, in three months' time.

When you look at the diagram, check three things: every node has a way to `END`, every conditional edge has a branch for each label your routing function can return, and there is no path that reaches `lookup_grn` without passing `lookup_po`.

### Stretch: reducers

By default, a node's returned value replaces the old value. A reducer changes that for one field. If you declare

```python
from typing import Annotated
import operator

errors: Annotated[list[str], operator.add]
```

then LangGraph adds each node's returned list to the existing one instead of replacing it. The main use is when several nodes, possibly running in parallel, all contribute to the same list.

If you try this, notice a knock-on effect: `fail` currently returns the whole list with the new message appended. With the reducer in place, that would add the old messages a second time. With a reducer, a node returns only what it is adding. State design and node code have to agree.

### Bring to the live session

- Your model calls, time and cost for INV-A, graph versus agent, and what each number includes.
- One invoice from the dataset that you think should be an error rather than an exception, or the other way round.
- For ADR 4: name one step in invoice processing where you would accept an agent loop inside the graph.

### Self-quiz

**1. Predict the output.** What does the last line print?

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class S(TypedDict, total=False):
    errors: list[str]

def first(state: S) -> dict:
    return {"errors": ["first"]}

def second(state: S) -> dict:
    return {"errors": ["second"]}

b = StateGraph(S)
b.add_node("first", first)
b.add_node("second", second)
b.add_edge(START, "first")
b.add_edge("first", "second")
b.add_edge("second", END)
print(b.compile().invoke({})["errors"])
```

<details><summary>Answer</summary>

`['second']`. Without a reducer, each node's returned value replaces the previous one, so `first`'s message is lost. This is why the lab's `fail` helper builds the new list from `state.get("errors", [])` plus the new message. If `errors` were declared as `Annotated[list[str], operator.add]`, the output would be `['first', 'second']`. Also note that `invoke({})` is allowed because `total=False` makes every key optional.

</details>

**2. What is wrong with this snippet?** INV-A runs end to end, but INV-07 fails.

```python
builder.add_conditional_edges("lookup_supplier", route,
                              {"next": "lookup_po", "error": "error"})
builder.add_conditional_edges("lookup_po", route,
                              {"next": "lookup_grn", "error": "error"})
```

<details><summary>Answer</summary>

The path maps have no `"exception"` entry. `route` returns `"exception"` when a lookup node sets that status, which is exactly what happens for INV-07 (no PO reference), INV-15 and INV-16. There is no node mapped to that label, so the run fails with an error instead of ending at the `exception` node. INV-A never takes that branch, so a test on the clean invoice alone would not catch it. Every label the routing function can return needs an entry in the map, and a drawn graph makes a missing branch easy to see.

</details>
