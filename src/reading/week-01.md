This week we open the box that an n8n AI node hides. A call to Claude is one HTTP request with a handful of fields, and one JSON response with a handful more. This reading walks through both, explains why a reply can be cut off while the call still "succeeds", shows how tokens turn into money, and then looks at what LangChain adds on top. Everything you build later (tools, loops, graphs, audits) is made of these requests, so the time spent here pays back every week.

### One call is one HTTP request

When an n8n Anthropic node runs, it sends an HTTPS `POST` to Anthropic's Messages API with your key in a header and a JSON body, waits, and receives a JSON response. There is no session, no connection kept open between calls, and no memory on the other side. The Anthropic Python SDK does the same thing with nicer syntax: it reads your key from the `ANTHROPIC_API_KEY` environment variable (set from Colab Secrets), builds the JSON body from your arguments, sends it, and turns the JSON reply into a Python object.

Here is the call from step 1 of the lab:

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model=MODEL,                       # ct.MODELS["haiku"], i.e. "claude-haiku-4-5"
    max_tokens=300,
    system="You are an accounts-payable expert. Answer in plain English.",
    messages=[{"role": "user", "content": "In two sentences, what is a three-way match?"}],
)
```

Notice that there is no key anywhere in the code. `anthropic.Anthropic()` finds it in the environment. That is the pattern for the whole course.

### Anatomy of a request

Five fields do almost all the work.

- **`model`** names which model answers. The course keeps model IDs in one place, `ct.MODELS`, so a change of model is a change to one dictionary, not a search through notebooks. Haiku is the cheap, fast tier; Sonnet the middle; Opus the most capable and most expensive.
- **`system`** is the system prompt: standing instructions about role, tone and rules. It sits outside the conversation and applies to the whole request.
- **`messages`** is the conversation so far, as a list of `{"role": ..., "content": ...}` items. Roles alternate between `"user"` and `"assistant"`, and the list normally ends with a user message that the model answers. `content` can be a plain string, as here, or a list of content blocks (text, images, tool results) as you will see in Weeks 2 and 3.
- **`max_tokens`** is a hard cap on the length of the reply. It is required. It is not a target: the model does not try to fill it. When the reply reaches it, generation simply stops.
- **`temperature`** (optional, between 0 and 1) controls how much randomness goes into choosing each next token. Lower values make the output more repeatable. Even at 0 you should not expect identical output on every run, so never build a check that depends on the exact wording of a reply.

In n8n these are the node's fields and "Options". In code, you can see all of them in one place, which is why printing the request is the first debugging habit.

### The response and its content blocks

![How a Claude response is created: your code names three things, the library sends one HTTPS POST, Anthropic's server runs the model and fills in a fixed reply form; fields it knows are filled, unused features come back as None](/images/week-01/week-01-step-03-response.webp)

Printing `response.model_dump_json(indent=2)` shows the whole object. It looks like this (the numbers and text are illustrative):

```json
{
  "id": "msg_01XyZ...",
  "type": "message",
  "role": "assistant",
  "model": "claude-haiku-4-5",
  "content": [
    {
      "type": "text",
      "text": "A three-way match compares the purchase order, the goods receipt and the supplier invoice before payment. The invoice is paid only if quantities and prices agree across all three."
    }
  ],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 34,
    "output_tokens": 41,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0
  }
}
```

The reply is not a string. It is `content`, a **list of blocks**, and each block has a `type`. Here there is one text block, so the text is at `response.content[0].text`. Next week a request will carry image blocks; in Week 3 a response will carry `tool_use` blocks, where the model asks your code to run a tool. This is the reason `output[0].content[0].text` appears in n8n expressions: the node is showing you the list structure you are now reading directly.

The SDK gives you attributes rather than dictionary keys: `response.content[0].text`, `response.stop_reason`, `response.usage.input_tokens`.

**You sent three things; you got back a dozen.** Your call named only `model`, `max_tokens` and `messages`. Every other field comes from Anthropic, not from your code:

- The reply is a **fixed form**, the same for every call. The SDK's `Message` class lists every box on it, so printing it shows them all.
- The **server fills in** what it knows about this reply: `id`, `role`, `model`, `content`, `stop_reason`, `usage`. `model` names the exact snapshot that answered, for example `claude-haiku-4-5-20251001`.
- Boxes for **features you did not use** come back empty (`null` in JSON, `None` in Python): `stop_sequence`, `container`, `citations` and others.

In n8n, the HTTP Request node's output panel works the same way: a few inputs, the API's whole response out. Two fields you will use constantly: `role`, because you append the reply to `messages` so the next call sees it, and `stop_reason`, next.

### Stop reasons, and the reply that "succeeds" while broken

`stop_reason` says why the model stopped writing. The values you will meet in this course:

| `stop_reason` | Meaning |
| --- | --- |
| `"end_turn"` | The model finished its answer naturally. |
| `"max_tokens"` | The reply hit your `max_tokens` cap and was cut off. |
| `"stop_sequence"` | The reply reached one of the stop strings you supplied (`stop_sequence` shows which). |
| `"tool_use"` | The model wants your code to run a tool (Week 3). |

(There are others, such as `"refusal"`, which you are unlikely to meet with this dataset.)

The important row is `"max_tokens"`. When a reply is cut off, the API does **not** return an error. The HTTP status is 200, the SDK raises nothing, and `content[0].text` holds a perfectly readable string that simply ends early. If you only read the text, a truncated answer looks like a short answer. In n8n the node goes green.

For a chat reply that is an annoyance. For a harness it is a silent data error: next week, a truncated transcription of a two-page invoice loses the lines on page 2, and everything downstream calculates from an incomplete invoice without complaint. So every function that calls a model must check the stop reason and **fail loudly** on truncation. That is what `ask()` does in step 3, and what `TruncatedOutputError` is for: it gives the failure a name, so later code (and later you) can tell "cut off" apart from every other problem.

A small point for when you write `ask`: only include `system` in the request when one was given. The pattern of building a dictionary of arguments and passing it with `**kwargs` is common for exactly this reason.

### Tokens: what you are charged for

Models read and write **tokens**, pieces of text that are often a word or part of a word. As a rough guide, English prose averages around four characters per token; numbers, codes like `SBP/26-27/0412` and Indian-formatted amounts like `1,22,400.00` usually take more tokens than their length suggests.

`usage` reports two numbers that matter now:

- **`input_tokens`**: everything you sent, which is the system prompt plus every message in the list (and, later, images and tool definitions).
- **`output_tokens`**: everything the model wrote.

They are priced separately, and output costs more per token. The course price table, in USD per million tokens:

| Model | Input | Output |
| --- | --- | --- |
| Haiku 4.5 (`claude-haiku-4-5`) | 1 | 5 |
| Sonnet 5.5 (`claude-sonnet-5-5`) | 2 | 10 |
| Opus 5.5 (`claude-opus-5-5`) | 4 | 20 |

These figures are in `ct.PRICES_PER_MTOK` and were checked in September 2026. Prices change: re-check them on Anthropic's site before relying on them.

### Estimating cost

The arithmetic is simple, and doing it by hand once makes `cost_of` easy to write and easy to test. Take the illustrative call above on Haiku: 34 input tokens and 41 output tokens.

- Input: 34 × USD 1 / 1,000,000 = USD 0.000034
- Output: 41 × USD 5 / 1,000,000 = USD 0.000205
- Total: about USD 0.00024 per call

That looks like nothing, which is the trap. Architects think in volume: at 10,000 calls a month the same call costs about USD 2.40 on Haiku and about USD 9.60 on Opus. Then remember that a real invoice call sends page images and long prompts, and an agent makes many calls per invoice. The lab's resource meter cell asks you to do this extrapolation on your own numbers.

Two habits come from this. First, cap `max_tokens` on every call, at a level that fits the task and no higher: it limits cost, and with the stop-reason check it turns an over-long reply into a named error. Second, you can **count tokens before sending**: `client.messages.count_tokens(...)` takes the same `model` and `messages` and returns the input token count without generating a reply. You will use it next week to compare an invoice as an image with the same invoice as text.

For `cost_of`, note that the SDK gives you `usage` as an object with attributes, while LangChain (below) gives you a plain dictionary. Your function has to accept both.

### The message array is the whole memory

The model is **stateless**. Each request stands alone. If you call it twice, the second call knows nothing about the first unless you put the first exchange into the `messages` list yourself. A "conversation" is your code re-sending the whole history every time:

```python
messages = [
    {"role": "user", "content": "Which supplier issued invoice SBP/26-27/0412?"},
    {"role": "assistant", "content": "Sahyadri Beverages Pvt Ltd."},
    {"role": "user", "content": "Which purchase order does it quote?"},
]
```

Three consequences follow. Memory is something the harness builds, not something the model has. Every turn re-sends, and re-pays for, everything before it, so input tokens grow as a conversation or agent loop goes on (you will measure this in Week 3). And when an agent does something strange, the first question is always "what exactly was in the message array?" Printing it is the first debugging step, before changing the prompt or the model.

### What LangChain's `init_chat_model` adds and hides

Step 4 repeats the same call through LangChain:

```python
from langchain.chat_models import init_chat_model

llm = init_chat_model(MODEL, model_provider="anthropic", max_tokens=300)
msg = llm.invoke([("system", "You are an accounts-payable expert. Answer in plain English."),
                  ("human", "In two sentences, what is a three-way match?")])
```

Underneath, it sends the same HTTP request. What comes back is an `AIMessage`, and the fields have moved:

- `msg.content` holds the text. For a text-only reply it is a plain string, not a list of blocks.
- `msg.response_metadata` is a dictionary of provider details, including `stop_reason`.
- `msg.usage_metadata` is a dictionary with `input_tokens`, `output_tokens` and `total_tokens`, in the same shape for every provider.

**What it adds.** One interface across providers: changing `model_provider` and the model name switches vendors without rewriting the call. Standard message types that the rest of LangChain and LangGraph understand. Helpers you will use soon, such as structured output (Week 2) and tool binding (Week 3).

**What it hides.** The content-block list is flattened for you, which is convenient until a reply contains more than text. The stop reason has moved into a metadata dictionary, where it is easy never to look, so a truncated reply is just as silent here as in the SDK. You also depend on one more library's version and defaults. None of this makes LangChain a bad choice. It means you should know where to look when it misbehaves, which is the point of ADR 1: raw SDK, LangChain or n8n, judged on transparency, portability, lock-in and learning cost.

### Three nested crafts

The course separates three kinds of work that are often blurred together.

- **Prompt engineering** shapes one input: the wording of a system prompt or a question.
- **Context engineering** decides what goes into the whole message array for each call: which history, which documents, which tool results, and what to leave out.
- **Harness engineering** builds the machinery around both: tools, state, checks, approvals, retries, logging and cost control.

Each contains the one before. This week you touched all three in miniature: you wrote a system prompt, you saw that the message array is the model's entire world, and you wrote `ask`, the first piece of harness, which refuses to pass on a truncated answer.

### Why the resource meter starts now

It is tempting to measure cost later, once something works. The course starts in Week 1 because of how agents spend tokens. In the Odysseus tutorials' reference run, agents read about 20 times more tokens than they wrote (roughly 20 million in against under 1 million out, across 25 projects). Every turn re-sends the growing history, tool results and documents; the replies are short. So even though input tokens are the cheaper kind, **input usually dominates the bill**, and the levers that matter most (sending less, caching, using a cheaper model for simple steps, replacing a model step with code) are about what you send, not what you receive. You cannot pull those levers without numbers, so from this week every model call records its usage by stage.

### Bring to the live session

- Find an n8n workflow of yours that uses an AI node. What would its `max_tokens` be, and what happens today if the reply is cut off?
- Where in your own work would a conversation's growing history quietly multiply cost?
- Raw SDK or LangChain for the rest of Act 1: what would make you choose one over the other?

### Self-quiz

**1. Predict the output.** Assume `ask` is written as in step 3 and uses Haiku.

```python
ask("Our supplier code for Sahyadri Beverages is S01. Please remember it.")
print(ask("What is our supplier code for Sahyadri Beverages?"))
```

What does the second call print?

<details><summary>Answer</summary>

The model cannot know. Each call to `ask` sends a new request whose `messages` list holds only that call's prompt, so the second request contains no trace of the first. Expect a reply saying it does not have that information (or, worse, a guess). To "remember", your code must include the earlier exchange in the message array, or store the fact somewhere and put it into the request itself.

</details>

**2. What is wrong with this snippet?** A colleague prices a Haiku call:

```python
# usage: input_tokens=1850 output_tokens=120, model claude-haiku-4-5
cost = (usage.input_tokens + usage.output_tokens) / 1_000_000 * 5.00
print(f"USD {cost:.5f}")      # USD 0.00985
```

<details><summary>Answer</summary>

It charges every token at the output price. Input and output tokens are priced separately: on Haiku, 1,850 input tokens at USD 1 per million is USD 0.00185, and 120 output tokens at USD 5 per million is USD 0.0006, a total of USD 0.00245. The snippet overstates the cost by four times, and the error grows as calls become more input-heavy, which agent calls are. It also hard-codes a price instead of looking it up in `ct.PRICES_PER_MTOK`, so it breaks silently when the model changes.

</details>
