# Module 02 - Prompt Templates

> **MLCourse - Agentic AI - Prompt Templates**

> Stage in the capstone: the R and A prompts of retrieval-augmented answering - one
> template formats what you send to the retriever, the other assembles context plus
> question for the model that writes the final answer.

Prompts are programs written in natural language. Change a word and behavior changes,
so treating prompts as copy-pasted strings scattered through your code is how projects
rot. LangChain's `ChatPromptTemplate` turns them into versionable, testable, reusable
objects with declared inputs - the same discipline variables and functions gave your
Python code.

## Why prompts are programs

- A prompt encodes *behavior*: role, rules, output shape, tone. That is source code
  whose interpreter happens to be a language model.
- Small wording changes produce large output changes, which means prompts need the
  things real code gets: names instead of magic strings, one definition reused in
  many places, and diffs you can review.
- Templates separate the fixed skeleton from the per-request data (`{topic}`,
  `{question}`, `{context}`), so application logic never does fragile string surgery.

## Roles explained

| Role | Who writes it | Job in the conversation |
|---|---|---|
| `system` | The developer | Sets persistent identity, rules, and constraints. The steering wheel - put policy here once, not in every turn. |
| `human` | The end user (or your app on their behalf) | Carries the actual request or question for this turn. |
| `ai` | The model (or replayed by you) | Previous replies. You inject these deliberately during few-shotting and when rebuilding history. |
| tool | Tool results (later modules) | Structured data returned by tools an agent called. |

The template renders to a plain list of LangChain message objects
(`SystemMessage`, `HumanMessage`, `AIMessage`) - exactly what module 01 sent to the models.

## Variables and few-shot: when to use what

- **Plain variables** (`{question}`): any value that changes per request. Declared via
  `input_variables`, supplied at `.invoke({"question": ...})`.
- **`MessagesPlaceholder`**: a slot for a whole LIST of messages - conversation history
  now, chat memory later in module 11. Mark it `optional=True` so the chain also runs
  before any history exists.
- **Few-shot examples**: when describing the behavior is weaker than showing it. Tone
  conversion, strict output formats, domain jargon - two to five worked examples beat a
  paragraph of instructions. Implemented with `FewShotChatMessagePromptTemplate`.
- **`partial_variables`**: values known at build time rather than call time - a persona
  line, today's date (a callable works too), an audience level. They disappear from
  `input_variables`, so callers only supply what actually varies.

### Key parameters and attributes

| Name | What it does | Notes and gotchas |
|---|---|---|
| `messages` | The skeleton: role/text tuples, templates, placeholders | Passed to `ChatPromptTemplate.from_messages([...])`; accepts mixed types. |
| `input_variables` | Read-only list of values you must supply | Placeholders count too; check it before wiring chains. |
| `optional_variables` | Variables allowed to be missing | Set via `MessagesPlaceholder(..., optional=True)`; render skips them if absent. |
| `partial_variables` | Pre-filled constants merged at format time | Values may be static strings OR zero-argument callables evaluated lazily at invoke time. |
| `.partial(**kw)` | Returns a NEW template with some variables pre-filled | Original stays untouched - partialing is non-destructive. |
| FewShot: `examples` + `example_prompt` | Data rows and the mini-template rendering each row | Each example dict must contain exactly the example_prompt's variables. |
| Literal braces | To emit a real `{` or `}` double it: `{{...}}` | Otherwise Python's formatter reads it as a variable name and raises KeyError at invoke. |

## Common pitfalls

- **Instruction dilution**: burying the three rules that matter inside twelve. Models
  weight instructions unevenly; keep system prompts short, ordered by importance, with
  critical rules first AND last.
- **Conflicting instructions**: "be concise" plus "write a detailed essay". The model
  resolves ties unpredictably - audit prompts for contradictions like contradictory
  lengths, tones, or audiences.
- Unescaped braces around literal JSON examples - crashes with a KeyError at invoke time.
- Putting per-turn user data into the system message: it belongs in the human turn;
  system content is often cached and should stay stable across requests.
- Too many near-duplicate few-shot examples: the model starts parroting their surface
  phrasing instead of learning the transformation.
- Forgetting that formatting a template NEVER calls a model - rendering is free and
  offline, so print rendered prompts liberally while debugging.

## Contents

1. `01_prompts_and_few_shot.ipynb` - roles and `ChatPromptTemplate.from_messages`,
   variables, literal-brace escaping, `MessagesPlaceholder`, a full few-shot tone
   conversion with `FewShotChatMessagePromptTemplate`, `partial_variables`, and the
   dilution/conflict pitfalls demonstrated side by side.

Later modules build directly on this one: module 04 pipes these templates into models
with LCEL, module 10 adds the retrieval context block, and the capstone combines both
into the final RAG answer prompt.
