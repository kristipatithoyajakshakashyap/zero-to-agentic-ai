# [Step 5 - Document Loaders] Turning raw files into Document objects

> **MLCourse - Agentic AI - Module 05: Document Loaders**

> Stage in the capstone: stage 1 INGEST: the capstone reads user-supplied documents with exactly these loaders

## What you'll learn

- the anatomy every loader shares: `Document(page_content=..., metadata=...)`
- which loader fits which format, and the few arguments that actually matter
- how to inspect, filter, and reshape Documents before anything downstream runs
- the failure modes of each loader: internet needs, encodings, granularity traps

## 1. The Document object: two fields that carry the whole pipeline

Every loader in LangChain - no matter the format - emits instances of one tiny
class:

```python
from langchain_core.documents import Document

doc = Document(
    page_content="All text a model may ever read lives here.",  # str
    metadata={"source": "reports/q3.txt", "page": 3},           # dict
)
```

- `page_content` - the payload. Exactly the string that later gets chunked,
  embedded, and retrieved. Nothing more, nothing less.
- `metadata` - the address label. Where it came from, which page, which row,
  which JSON key. It never gets embedded, but it decides what you can FILTER
  on, what you can CITE, and how you debug retrieval later.

Loaders differ in two dimensions only: what they put into those two fields,
and at what GRANULARITY they emit Documents (one doc per file, per page, per
row, per record, or per site). Keep that lens and the whole module collapses
into one idea.

## 2. Loader decision table

| Format | Loader class | Typical use-case | Key arguments | Gotchas |
|---|---|---|---|---|
| `.txt` | `TextLoader` | notes, logs, books, exported chats | `encoding="utf-8"`, `autodetect_encoding=True` | one Document per FILE; BOM or latin-1 bytes crash strict decoding |
| `.md` | `TextLoader` (light) or `UnstructuredMarkdownLoader` | documentation, wikis, these very course notes | `encoding` | the light route keeps `#` header lines as plain text; the structured route needs the heavy `unstructured` dependency |
| `.csv` | `CSVLoader` | tabular knowledge (products, metrics, FAQs) | `source_column`, `content_columns`, `metadata_columns`, `csv_args={"delimiter": ";"}` | row-vs-document choice is YOURS; wrong delimiter silently merges a whole file into one row |
| `.json` | `JSONLoader` | API dumps, nested records | `jq_schema`, `content_key`, `metadata_func` | requires the optional `jq` package; the schema string decides document granularity |
| `.pdf` | `PyPDFLoader` | papers, reports, manuals | file path only | page granularity (sections rarely align with pages); scanned PDFs return empty text - `pypdf` has no OCR |
| web page | `WebBaseLoader` | live pages, wikis, blog posts | `web_path`, `requests_per_second` | needs internet; JavaScript-heavy sites come back nearly empty; nav/boilerplate noise rides along |
| folder | `DirectoryLoader` | bulk ingest of a directory tree | `glob`, `loader_cls`, `loader_kwargs`, `recursive`, `silent_errors` | one bad file can abort the run; `silent_errors=True` skips files quietly - data loss you cannot see |

## 3. When and how to pick a loader

Pick by STRUCTURE, not by file extension alone:

```text
Is the file plain prose?              -> TextLoader
Does meaning live in headers?         -> markdown route (light now, header-aware splitting in module 06)
Are there repeating records?          -> CSVLoader or JSONLoader (one doc per record)
Is it binary paginated?               -> PyPDFLoader (one doc per page)
Does it live on the web?              -> WebBaseLoader (one doc per URL)
Do you have MANY files at once?       -> DirectoryLoader wrapping any loader above
```

Then always inspect before trusting:

```python
docs = loader.load()
print(len(docs))                    # how many Documents?
print(docs[0].metadata)             # what did it record about origin?
print(docs[0].page_content[:300])   # does the content look sane?
```

That three-line ritual catches ninety percent of ingestion bugs before they
reach chunking, embeddings, or retrieval.

## 4. Pitfalls

- **Pitfall - web loaders need internet and bring boilerplate**: `WebBaseLoader`
  fetches live HTML, so results change between runs and navigation menus,
  footers, and cookie banners ride along in `page_content`. Budget a cleaning
  step, and be polite: honor `robots.txt`, throttle with `requests_per_second`.
- **Pitfall - PDF granularity is the PAGE, not the idea**: a section may span
  five pages and one page may hold three sections. Keep `metadata["page"]` so
  answers can cite their exact location, and remember scanned PDFs yield empty
  strings from `pypdf` - they need OCR before any loader helps.
- **Pitfall - CSV row-vs-document is a design decision**: one Document per row
  is great for lookup questions and terrible for questions needing many rows.
  Decide deliberately using `source_column` / `metadata_columns`, and always
  pass the true delimiter (`csv_args={"delimiter": ";"}` for semicolon files).
- **Pro-tip - cache downloads, never re-fetch**: every notebook in this track
  uses a download-once helper writing into `03_agentic_ai/data`. Public servers
  deserve politeness, and offline reruns should just work.

## 5. Contents

| Notebook | Teaches |
|---|---|
| [01_text_loader.ipynb](01_text_loader.ipynb) | TextLoader basics, inspection ritual, Gutenberg boilerplate strip |
| [02_markdown_loader.ipynb](02_markdown_loader.ipynb) | loading markdown as text, headers survive, light vs unstructured trade-off |
| [03_csv_loader.ipynb](03_csv_loader.ipynb) | CSVLoader delimiters, `content_columns` / `metadata_columns`, filtering by metadata |
| [04_json_loader.ipynb](04_json_loader.ipynb) | JSONLoader jq schemas, two granularities, `metadata_func`, graceful jq fallback |
| [05_pdf_loader.ipynb](05_pdf_loader.ipynb) | PyPDFLoader page Documents, metadata, page concatenation |
| [06_web_base_loader.ipynb](06_web_base_loader.ipynb) | WebBaseLoader, metadata, boilerplate cleaning, web etiquette |
| [07_directory_loader.ipynb](07_directory_loader.ipynb) | DirectoryLoader globs, progress, per-file error behavior |

## Summary

- Everything a loader produces is a `Document`: `page_content` plus `metadata`.
- Loaders vary only in field contents and emission granularity - reason in
  those terms and any new loader becomes obvious.
- Inspect count, metadata, and a content preview immediately after every load.
- Know each loader's failure mode BEFORE it reaches your vector store: web
  needs network, PDF thinks in pages, CSV makes you choose row-vs-doc, and
  DirectoryLoader can fail loudly or skip silently - pick on purpose.
