# Pandas - The Complete Reference
#
# **MLCourse · Data Science Foundations · 02_pandas**

Pandas is Python's table engine: labeled rows and columns, heterogeneous types,
missing-value awareness, and hundreds of vectorized operations. If NumPy is the
engine, Pandas is the cockpit. This book covers everything taught in the three
teaching notebooks - use it as your lookup reference.

**Contents**
. [Core objects](#-core-objects)
2. [Creating & loading data](#2-creating--loading-data)
3. [Inspecting](#3-inspecting)
4. [Selection & filtering](#4-selection--filtering)
5. [Sorting & ranking](#5-sorting--ranking)
6. [Missing data](#6-missing-data)
7. [Dtypes](#7-dtypes)
8. [apply / map family](#8-apply--map-family)
9. [Binning](#9-binning)
0. [Groupby: split-apply-combine](#0-groupby-split-apply-combine)
. [Reshaping](#-reshaping)
2. [Combining tables](#2-combining-tables)
3. [Time series](#3-time-series)
4. [MultiIndex](#4-multiindex)
5. [Categoricals](#5-categoricals)
6. [String methods](#6-string-methods)
7. [Method chaining style](#7-method-chaining-style)
8. [Copies, views & memory](#8-copies-views--memory)
9. [Styling & export](#9-styling--export)
20. [Cheat sheet](#20-cheat-sheet)

---

## . Core objects

| Object | Dimensionality | Think of it as |
|---|---|---|
| `Series` | -D | one labeled column (values + index) |
| `DataFrame` | 2-D | dict of Series sharing an index |
| `Index` | -D labels | immutable axis used by both |

```python
s = pd.Series([0, 20, 30], index=["a", "b", "c"])
df = pd.DataFrame({"city": ["Rome", "Oslo"], "pop": [4_300_000, 700_000]})
```

>  **Common pitfall:** Series operations ALIGN ON INDEX. Adding two Series with
> different indexes produces NaN wherever labels don't match:

```python
a = pd.Series([, 2], index=["x", "y"])
b = pd.Series([, 2], index=["y", "z"])
a + b        # x->NaN, y->3, z->NaN
```

## 2. Creating & loading data

```python
pd.read_csv("f.csv", dtype={"id": str}, na_values=["NA", "-"],
            parse_dates=["date"], index_col=0)
pd.read_excel("f.xlsx", sheet_name="Sales")
df.to_csv("out.csv", index=False)          # almost always drop the index!
```

From in-memory structures:

```python
pd.DataFrame({"col": [...], ...})          # dict of lists/Series
pd.DataFrame(records_list_of_dicts)        # JSON-ish rows
```

## 3. Inspecting

| Method | Purpose |
|---|---|
| `head(n)` / `tail(n)` / `sample(n)` | eyeball rows |
| `shape`, `columns`, `index` | dimensions & axes |
| `info()` | dtypes + non-null counts + memory |
| `describe(include="all")` | numeric AND categorical summaries |
| `value_counts(dropna=False)` | frequency per value |
| `nunique()`, `memory_usage(deep=True)` | cardinality & footprint |

## 4. Selection & filtering

| Goal | Use | Example |
|---|---|---|
| pick column(s) | `[]` | `df["age"]`, `df[["a","b"]]` |
| label-based rows/cols | `.loc` | `df.loc[3]`, `df.loc[3:5, "a":"c"]` |
| position-based | `.iloc` | `df.iloc[:5, 0]` |
| fast scalar | `.at` / `.iat` | `df.at[7, "fare"]` |
| boolean mask | inside `[]`/`.loc` | `df[df.age > 30]` |
| declarative | `.query()` | `df.query("age > 30 and sex=='F'")` |
| membership | `isin`, `between` | `df[df.day.isin(["Sat","Sun"])]` |

Boolean rules: combine with `& | ~` and **parenthesize each condition**.
Label slices in `.loc` are INCLUSIVE; positional slices in `.iloc` are exclusive.

>  Dot-access (`df.age`) works but breaks when names collide with methods or
> contain spaces - prefer brackets in real code.

## 5. Sorting & ranking

```python
df.sort_values(["day", "tip"], ascending=[True, False], na_position="last")
df.sort_index()
s.rank(method="dense")                     # ties handled explicitly
df.nlargest(5, "fare"); df.nsmallest(3, "age")
```

## 6. Missing data

Detection & counts:

```python
df.isna().sum()                            # per-column count
df.isna().mean().mul(00).round()         # per-column %
```

Deletion:

```python
df.dropna()                                # any NaN in row -> gone
df.dropna(how="all")                       # only fully-empty rows
df.dropna(subset=["embarked"], thresh=None)
df.dropna(thresh=0)                       # keep rows having ≥0 non-nulls
```

Imputation:

```python
df.fillna(0)                               # constant
df["age"].fillna(df["age"].median())       # robust central fill
df["town"].fillna(df["town"].mode()[0])    # categorical mode fill
df["price"].ffill()                        # forward-fill ordered data
df["price"].bfill()
```

Strategy selection:

| Situation | Strategy |
|---|---|
| >70-80% missing, low value | drop column |
| few % missing, MCAR | mean/median/mode or row-drop |
| skewed numeric | median |
| time-ordered | ffill/bfill |
| group structure exists | group-wise median (`groupby+transform`) |

## 7. Dtypes

```python
df.dtypes                                  # inspect
df["pclass"].astype("int8")                # downcast integers
df["sex"].astype("category")               # huge memory win, enables ordering
pd.to_numeric(df["bad"], errors="coerce")  # dirty strings -> NaN
pd.to_datetime(df["when"], errors="coerce")
```

## 8. apply / map family

| Tool | Level | Vectorized? | Use for |
|---|---|---|---|
| arithmetic / `.str` | element |  | always prefer first |
| `Series.map(func/dict)` | element |  | per-item transforms, recode maps |
| `DataFrame.apply(func, axis)` | row/col |  | multi-column logic last resort |
| `replace(mapping)` | values |  | targeted recodes |

>  **Pro tip:** every `apply(lambda x: x.a + x.b)` should make you reach for
> direct column math instead.

## 9. Binning

```python
pd.cut(ages, bins=[0, 8, 35, 60, 20],               # fixed-width bins
       labels=["minor", "young", "adult", "senior"])
pd.qcut(fares, q=4, labels=["Q","Q2","Q3","Q4"])     # equal-COUNT bins
```

`cut` = equal width; `qcut` = equal frequency (better for skewed data).

## 0. Groupby: split-apply-combine

Mental model: **split** rows by key -> **apply** a reduction per group ->
**combine** results back into a frame.

```python
g = df.groupby("class", observed=True)

g["fare"].mean()                                   # Series out
g.agg({"fare": "mean", "age": ["min","max"]})      # dict form

# NAMED AGGREGATION - clean column names, production style:
(df.groupby("class", observed=True)
   .agg(passengers=("survived", "size"),
        survival_rate=("survived", "mean"),
        avg_fare=("fare", "mean")))
```

The three siblings:

| Method | Output shape | Typical job |
|---|---|---|
| `agg` | one row per group | summarize |
| `transform` | same shape as input | group-wise feature (e.g., z-score within group, group-median imputation) |
| `filter` | subset of rows | keep groups passing a test |

Group-wise median imputation:

```python
df["age"] = df.groupby(["class","sex"])["age"] \
              .transform(lambda s: s.fillna(s.median()))
```

## . Reshaping

| Op | Direction |
|---|---|
| `pivot(index, columns, values)` | long -> wide |
| `pivot_table(..., aggfunc, margins)` | long -> wide WITH aggregation |
| `melt(id_vars, var_name, value_name)` | wide -> long |
| `stack()` / `unstack()` | columns ↔ innermost index level |
| `crosstab(a, b, normalize="index")` | frequency/proportion tables |

## 2. Combining tables

```python
pd.concat([df, df2], axis=0, ignore_index=True)   # stack rows (or cols axis=)
```

`merge` - SQL-style joins:

| how= | keeps |
|---|---|
| `"inner"` | keys present in BOTH |
| `"left"` | all left + matches |
| `"right"` | all right + matches |
| `"outer"` | everything, NaN-filled gaps |

```python
orders.merge(customers, on="cust_id", how="left",
             suffixes=("_o", "_c"), indicator=True, validate="m:")
df.join(other, how="left")          # convenience join on INDEX
```

>  **Common pitfall:** unintended many-to-many merges silently explode row
> counts. Guard with `validate="m:"` / `":"` and check shapes after merging.

## 3. Time series

```python
df["d"] = pd.to_datetime(df["d"], format="%Y-%m-%d", errors="coerce")
ts = df.set_index("d").sort_index()

ts.loc["2023"]                      # whole year
ts.loc["2023-03":"2023-05"]         # inclusive range
ts.index.year; ts.index.month; ts.index.dayofweek   # components

ts.resample("MS").mean()            # MS=month start (stable alias), QE, YE...
ts.rolling(window=30).mean()        # trailing window; min_periods tames edge-NaNs
ts.expanding().mean()               # cumulative window
ts.shift(); ts.pct_change(); ts.diff()              # lags & deltas
```

Frequency aliases: `D` day · `B` business · `W` week · `MS` month-start ·
`QE` quarter-end · `YE` year-end.

## 4. MultiIndex

```python
multi = df.groupby(["region", "dept"])["rev"].sum()
multi.loc[("East", "Sales")]         # exact tuple
multi.loc["East"]                    # outer slice
multi.xs("Sales", level="dept")      # deep-level cross-section
wide = multi.unstack()               # inner level -> columns
back = wide.stack()
```

## 5. Categoricals

```python
sizes = pd.Categorical(s, categories=["S","M","L","XL"], ordered=True)
s.astype("category")                       # quick conversion
s.cat.rename_categories({...}); s.cat.add_categories([...])
```

Benefits: correct ORDERED sorting/comparisons, big memory savings,
fast groupby on categories.

## 6. String methods

Everything via `.str.` (vectorized, regex-aware):

| Task | Call |
|---|---|
| case/trim | `lower upper title strip` |
| search | `contains(r"\d{3}", regex=True)` |
| capture | `extract(r"@(\w+)\.")` |
| split+pick | `split("@").str[0]` |
| replace | `replace(r"\D", "", regex=True)` |
| length/join | `len cat(sep=", ")` |
| dummies | `str.get_dummies(sep=";")` |

Escape regex metachars (`. ^ $ * + ? ( ) [ ] { } |`) with `\`.

## 7. Method chaining style

```python
result = (
    tips.query("total_bill < 40")
        .assign(tip_pct=lambda d: d.tip / d.total_bill * 00)
        .groupby("day", observed=True)["tip_pct"]
        .mean().round(2)
        .sort_values()
)
```

Rules of thumb: parentheses + one step per line · `assign` for new columns ·
`pipe(fn)` to slot in custom functions.

## 8. Copies, views & memory

```python
sub = df[df.fare > 50].copy()      # filter then COPY - kills the ambiguity
sub["flag"] =                     # safe now
pd.set_option("mode.copy_on_write", True)   # modern pandas default behavior
```

Memory diet: `category` for repeats -> `int8/int6` via astype -> float32 via
`to_numeric(downcast=...)`; audit with
`df.memory_usage(deep=True).sort_values()`.

## 9. Styling & export

```python
(df.groupby("day", observed=True)["tip"].mean().to_frame()
   .style.bar(color="#5fba7d")
   .background_gradient(cmap="Blues")
   .format("{:.2f}"))
df.to_csv("out.csv", index=False)
df.to_parquet("out.parquet")       # preserves dtypes, compressed, fast
```

## 20. Cheat sheet

| Need | One-liner |
|---|---|
| top-k rows by col | `df.nlargest(k, col)` |
| % missing | `df.isna().mean()*00` |
| group summary (clean names) | named `.agg(a=("b","mean"), ...)` |
| group-wise fill | `groupby(keys)[c].transform(lambda s: s.fillna(s.median()))` |
| survival-style rate table | `crosstab(a, b, normalize="index")` |
| long <-> wide | `melt` <-> `pivot_table` |
| month series from parts | `to_datetime(y.astype(str)+"-"+m+"-0")` |
| lag feature | `s.shift()` |
| rolling average | `s.rolling(w).mean()` |
| top-n per group | sort_values -> `groupby(k).head(n)` |
| dedupe keeping latest | `drop_duplicates(subset=id, keep="last")` |
| email username | `email.str.split("@").str[0]` |
| quantile bins | `qcut(x, 4, labels=...)` |
| safe scalar get/set | `.at[i, c]` / `.iat[i, j]` |

*End of the Pandas reference book - now run the notebooks and break things.*
