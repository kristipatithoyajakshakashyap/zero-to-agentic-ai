# Data Preprocessing - The Section Reference Book

> **MLCourse · Data Science Foundations · 05_data_preprocessing**

Welcome to the preprocessing track. This book is the **single reference** for everything
in section 05: it explains the concepts, shows every technique twice (manual
pandas/NumPy first, then its scikit-learn equivalent), and collects the rules of thumb
you will actually remember six months from now.

The companion notebooks put these ideas into your hands:

| Notebook | Title | Focus |
|---|---|---|
| `0_missing_data.nb.py` | Handling Missing Data | NaN semantics, MCAR/MAR/MNAR, deletion vs imputation, `SimpleImputer`, leakage |
| `02_numerical_data.nb.py` | Processing Numerical Data | Scaling trio, skew fixes, binning, outliers |
| `03_categorical_data.nb.py` | Encoding Categorical Data | Label/ordinal/one-hot/frequency encoding, dummy trap, datetime features |
| `04_text_fundamentals.nb.py` *(sibling track)* | Text Cleaning & Tokenization | Regex cleaning, tokenizing, stopwords, stemming vs lemmatization with NLTK |
| `05_text_vectorization.nb.py` *(sibling track)* | From Text to Numbers | Bag-of-Words and TF-IDF, vocabulary limits, n-grams |
| `06_pipelines.nb.py` *(sibling track)* | Preprocessing Pipelines | `Pipeline` + `ColumnTransformer`: bundling every transform so it can never leak |
| `08_exercises.nb.py` *(sibling track)* | Consolidation Exercises | Applied practice on messy datasets |

>  **Pro tip:** Read chapters 0-4 before opening the notebooks; use chapters 5-8 as
> lookup material while you work.

---

## Table of contents

. [Chapter 0 - The preprocessing mindset](#chapter-0--the-preprocessing-mindset)
2. [Chapter  - Order of operations](#chapter---order-of-operations)
3. [Chapter 2 - Missing data](#chapter-2--missing-data)
4. [Chapter 3 - Numerical data](#chapter-3--numerical-data)
5. [Chapter 4 - Categorical data](#chapter-4--categorical-data)
6. [Chapter 5 - Text data (summary)](#chapter-5--text-data-summary)
7. [Chapter 6 - Pipelines tie it together](#chapter-6--pipelines-tie-it-together)
8. [Chapter 7 - The end-to-end workflow checklist](#chapter-7--the-end-to-end-workflow-checklist)
9. [Chapter 8 - Cheat sheets](#chapter-8--cheat-sheets)

---

## Chapter 0 - The preprocessing mindset

**Preprocessing is not chores before the fun part. It is the model.** A linear model fed
unscaled features where one column ranges 0-00,000 and another 0-5 is not "a model with
a scaling problem" - it is a broken optimization. Preprocessing decisions routinely move
accuracy more than the choice of algorithm does.

Three beliefs drive this whole track:

. **Models eat numbers, only numbers.** Every raw input - text, categories, dates,
   missing cells - must become a well-behaved numeric matrix. The *art* is choosing a
   transformation that keeps the signal while making the math well-behaved.
2. **Every transform has two verbs: `fit` and `transform`.**
   - `fit(data)` = *learn parameters from data* (the mean, the min/max, the category
     list, the vocabulary).
   - `transform(data)` = *apply those learned parameters*.
   Manual pandas code mixes both steps invisibly; scikit-learn separates them. That
   separation is what makes train/test honesty enforceable.
3. **Anything fitted on test data is leaked.** If your scaler saw the test set, your
   evaluation is optimistic fiction. We will flag this in every chapter because it is
   the single most common beginner bug - and it silently passes code review.

### The manual-vs-sklearn pairing

Each notebook follows one rhythm:

```python
# MANUAL: you see the arithmetic
z_manual = (x - x.mean()) / x.std(ddof=0)

# SKLEARN: same math, but fit/transform separated and reusable
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
z_sklearn = scaler.fit_transform(x.values.reshape(-, ))
```

Why learn both? The manual version builds intuition; the sklearn version is what ships:
it remembers its parameters (`scaler.mean_`), applies them identically to new data, and
slots into pipelines.

---

## Chapter  - Order of operations

Preprocessing steps are **not commutative**. Log-transforming then imputing gives a
different answer than imputing then log-transforming (log of NaN is still NaN, but log
of an imputed zero is not). Use this canonical order:

```
. Split protocol decided FIRST (train/test indices fixed, test set untouched)
2. Structural cleaning      -> dtypes, duplicates, impossible values, units
3. Missing data handling    -> mechanism-aware strategy (Ch. 2)
4. Outlier policy           -> detect, decide cause, treat or keep (Ch. 3.4)
5. Skew fixes               -> log / PowerTransformer (Ch. 3.2)
6. Scaling                  -> Standard / MinMax / Robust (Ch. 3.)   [fit on TRAIN]
7. Encoding categoricals    -> ordinal / one-hot / frequency (Ch. 4)   [fit on TRAIN]
8. Datetime expansion       -> calendar + cyclical features (Ch. 4.5)
9. Wrap in Pipeline         -> freeze the order so serving matches training (Ch. 6)
0. Validate                -> cross-validate the WHOLE pipeline, not the bare model
```

>  **Common pitfall:** Steps 6-8 are *parameters learned from data* (means, category
> lists). They must be fitted **inside cross-validation folds**, never once on the full
> dataset. This is exactly what notebook 06's `Pipeline` automates.

---

## Chapter 2 - Missing data

Full hands-on treatment: notebook `0_missing_data.nb.py`.

### 2. Why missingness matters

Most sklearn estimators raise `ValueError: Input contains NaN`. Pandas is friendlier -
it silently skips NaN in `sum()`, `mean()`, `groupby()` - which is convenient for
exploration and dangerous for modeling: silent skipping hides how much information is
gone. Also memorize the semantics:

- `np.nan != np.nan` is `True` - you cannot test equality, use `df.isna()`.
- A column of floats with even one NaN stays `float64`; NaN in an int column forces
  float; in an object column it coexists with strings.
- pandas ≥ .0 also has the nullable `pd.NA` scalar for proper integer/text missingness.

### 2.2 The three mechanisms (this dictates everything)

| Mechanism | Meaning | Relatable example | Safe strategies |
|---|---|---|---|
| **MCAR** - Missing Completely At Random | P(missing) unrelated to anything | A scanner randomly failed on 3% of forms | Deletion OK if < ~5%; any imputation unbiased |
| **MAR** - Missing At Random | P(missing) explained by *other observed* columns | Older customers decline to type their age online -> age missing depends on signup channel | Imputation using those other columns (group-wise, KNN); deletion biases results |
| **MNAR** - Missing Not At Random | P(missing) depends on the *missing value itself* | Very high incomes under-reported on surveys | Nothing fully fixes it; median > mean, model the mechanism, be honest about limits |

The practical triage question is always: *"Can I explain the gaps with columns I still
have?"* Yes -> MAR, exploit those columns. No, and rich/poor rows look equally gappy ->
MCAR. Gaps concentrated at extreme values -> suspect MNAR.

### 2.3 Detection toolkit

```python
df.isna().sum()                      # absolute count per column
df.isna().mean().mul(00).round()   # percentage per column
df.info()                            # non-null counts + dtypes in one view
plt.imshow(df.isna(), aspect="auto") # nullity matrix - white/black wall of gaps
df.isna().sum().plot.bar()           # missingness per column at a glance
```

Look at patterns, not just totals: sort rows by a suspicious column and re-`imshow` -
if gaps line up with another column's values, that is MAR staring at you.

### 2.4 Deletion rules

| Tool | Use when |
|---|---|
| `df.dropna()` (rows, any-NaN) | MCAR and total loss < ~5% of rows |
| `df.dropna(subset=["target"])` | Target missing = unusable row, always drop |
| `df.dropna(thresh=k)` | Keep rows that have at least k observed values |
| `df.drop(columns=col)` | Column mostly empty (>60-80%) AND low predictive value (e.g. Titanic `deck`, 77% missing) |

>  **Common pitfall:** In the Titanic demo, naive `dropna()` deletes ~40%+ of rows
> because three columns each lose 0-45%. Row deletion compounds multiplicatively across
> columns. Always measure `len(df)` before/after.

Deletion is not just about sample size - under MAR/MNAR it *biases* the remaining sample
(e.g., dropping unknown ages removes all third-class passengers disproportionately).

### 2.5 Imputation strategies

| Strategy | Code (manual) | Code (sklearn) | Best for |
|---|---|---|---|
| Constant sentinel | `df.fillna("Unknown")`, numeric `-` | `SimpleImputer(strategy="constant", fill_value=...)` | Categoricals where "missing" may itself be informative |
| Mean | `df.fillna(df.x.mean())` | `SimpleImputer(strategy="mean")` | Symmetric, MCAR-ish numerics |
| Median | `df.fillna(df.x.median())` | `SimpleImputer(strategy="median")` | Skewed numerics, outlier-robust (default choice) |
| Mode | `df.fillna(df.x.mode()[0])` | `SimpleImputer(strategy="most_frequent")` | Categoricals |
| ffill/bfill | `df.ffill()` / `df.bfill()` | - (pandas-only) | Sorted time series; carry last observation forward |
| Group-wise | `df.x.fillna(df.groupby(g).x.transform("median"))` | - (compose yourself) | MAR - lets related columns pick the fill value |
| K-neighbors | - | `KNNImputer(n_neighbors=5)` | Rows resemble rows; scale features first! |
| Iterative | - | `IterativeImputer` (experimental) | Multivariate regression-style fill; powerful, slower |

Group-wise deserves emphasis because it is pure pandas and often beats fancy methods:
impute age by the median age of *that passenger class and sex*, and the fills inherit
real structure instead of one global number.

>  **Common pitfall - DATA LEAKAGE:** Fit every imputer on the **training split
> only**, then `transform` the test split. Computing the mean on train+test smuggles
> test-set information into training. Notebook 0 demonstrates the wrong way and the
> right way side by side.

---

## Chapter 3 - Numerical data

Full hands-on treatment: notebook `02_numerical_data.nb.py`.

### 3. The scaling trio

Why scale at all? (a) distance-based models (KNN, SVM, k-means) are dominated by the
widest-range feature; (b) gradient descent converges faster on round-ish loss surfaces;
(c) regularization penalizes coefficients fairly only when features share a scale.
Trees don't care - splits are per-feature thresholds.

| Scaler | Formula | Resulting range | Robust to outliers? | Use when |
|---|---|---|---|---|
| **StandardScaler** | z = (x − μ) / σ | mean 0, std  | No (μ, σ shift) | Default for linear models, logistic regression, PCA, neural nets |
| **MinMaxScaler** | x' = (x − min) / (max − min) | [0, ] | **No - catastrophic**: one huge value squashes everyone into a sliver | Bounded inputs needed: image pixels, NN input layers, when you know true bounds |
| **RobustScaler** | x' = (x − median) / IQR | centered on median, IQR =  | **Yes** | Data with outliers or heavy tails; default companion to tree-free models on dirty data |

Manual equivalents (note the `ddof=0` - NumPy's default, matching sklearn):

```python
z      = (x - x.mean()) / x.std(ddof=0)          # StandardScaler
minmax = (x - x.min())  / (x.max() - x.min())    # MinMaxScaler
robust = (x - np.median(x)) / (np.percentile(x, 75) - np.percentile(x, 25))  # RobustScaler
```

Two facts beginners must internalize:

- **Scaling preserves shape.** A right-skewed distribution scaled by any of the three
  is still right-skewed - scaling shifts/stretches axes, it does not bend the curve.
  Fix shape with §3.2 *first*, then scale.
- **`Normalizer` is a different beast.** It scales each *row* to unit length
  (L2), not each column. Used for text vectors and direction-only data. Do not confuse
  it with the scalers above.

### 3.2 Fixing skew

Detect: `df.col.skew()` (roughly: > + strong right skew, < − strong left) plus a
histogram/KDE. Right-skewed money-like variables (salary, fare, house prices, durations)
are everywhere.

| Fix | Handles negatives? | Notes |
|---|---|---|
| `np.logp` (= log(+x)) | No (NaN for x < 0) | One-liner; near-normalizes lognormal data; invert with `np.expm` |
| Box-Cox (`PowerTransformer(method="box-cox")`) | No - strictly positive | Classic power family, λ fitted from data |
| Yeo-Johnson (`PowerTransformer(method="yeo-johnson")`) | **Yes** | Default choice; sklearn fits λ like any estimator |

Rule of thumb: try `logp` for quick exploration; ship `PowerTransformer` in pipelines
because it learns λ on train only and handles zeros/negatives.

### 3.3 Binning / discretization

```python
pd.cut(age,  bins=[0, 8, 35, 60, 20], labels=False)          # equal WIDTH (you choose edges)
pd.qcut(fare, q=4, labels=["Q","Q2","Q3","Q4"])               # equal FREQUENCY (quantiles)
```

- `cut`: interpretable edges ("child/adult/senior"), but counts per bin can be wildly
  unequal on skewed data.
- `qcut`: balanced bins guaranteed (great for skewed variables), but edges become
  data-dependent numbers - another thing to fit on train and reuse.

Why bin at all? Linear/logistic models can then fit a step per bin - cheap
non-linearity. Trees don't need scaling, and they find their own bins, so this is a
linear-model tool. Cost: you throw away within-bin detail.

### 3.4 Outliers: detect, diagnose, treat

Detection (complementary views):

```python
z = (x - x.mean()) / x.std()
outliers_z  = x[np.abs(z) > 3]                                     # assumes roughly normal
q, q3 = x.quantile([0.25, 0.75]); iqr = q3 - q
lo, hi = q - .5 * iqr, q3 + .5 * iqr
outliers_iqr = x[(x < lo) | (x > hi)]                              # boxplot fences, no normality needed
```

Treatment decision table - **cause decides cure**:

| Cause | Treatment |
|---|---|
| Data-entry/measurement error, verifiable | Remove (or fix at source) |
| Genuine heavy tail (income, claims) | Transform (log) or cap at fences (**winsorize**: `x.clip(lo, hi)`) |
| Genuine extremes that ARE the phenomenon (fraud, VIPs) | Leave them; switch to robust scalers/models |

Compare mean/std/skew after each option on the same series - capping changes tails,
removal changes n and moments, transforms change everything smoothly.

>  **Pro tip:** Winsorizing = clipping to the IQR fences. It keeps every row (no
> sample-size loss) while defusing leverage points - a great default for skewed
> business data.

---

## Chapter 4 - Categorical data

Full hands-on treatment: notebook `03_categorical_data.nb.py`.

### 4. The fundamental split

- **Nominal** - no inherent order (city, color, blood type).
- **Ordinal** - real ranking (t-shirt S<M<L, contract tier Bronze<Silver<Gold).

Everything downstream follows from asking this one question.

### 4.2 Encoding decision table

| Technique | Nominal? | Ordinal? | k columns out | Watch out for |
|---|---|---|---|---|
| Label encoding (arbitrary ints) |  risky |  fine |  | Fakes an order: linear/distance models read `blue(2) > red(0)`; trees tolerate it |
| Explicit ordinal mapping |  |  correct tool |  | You must supply the true order (`{"S":0,"M":,"L":2}`); sklearn `OrdinalEncoder(categories=[[...]])` |
| One-hot (`get_dummies` / `OneHotEncoder`) |  gold standard | wasteful | k (or k−) | Dummy trap; unseen categories at predict time; high cardinality explodes width |
| Frequency/count encoding |  compact | - |  | Frequencies must come from TRAIN only; collisions (two cities, same count) |
| Target encoding |  compact, strong | - |  | **Severe leakage risk** - needs CV-safe schemes (see §4.4) |

### 4.3 The dummy variable trap

One-hot with all k dummies + an intercept creates perfect multicollinearity:
`d_red + d_green + d_blue ==  == intercept`. For ordinary least squares the design
matrix becomes singular. Drop one level (`drop_first=True`) and the remaining
coefficients read naturally as "difference from the dropped baseline". Regularized
models (ridge/lasso, most gradient boosting) handle the redundant column fine - but
k− is never wrong, so make it a habit for interpretability.

### 4.4 Production concerns

- **Unseen categories:** `pd.get_dummies` produces whatever columns exist *in that
  dataframe* - feed it a test batch containing `"Berlin"` when training saw only
  Paris/Tokyo/Dubai and the feature matrices misalign and the model crashes.
  `OneHotEncoder(handle_unknown="ignore")` encodes the stranger as all-zeros instead -
  production-safe.
- **Fit on train, always:** the encoder's remembered category list (`categories_`) is a
  learned parameter. Refitting on live data later silently reshuffles columns.
- **Sparse output:** modern sklearn uses `sparse_output=False` for dense arrays
  (pre-.2 name was `sparse`). Dense is easier to inspect; sparse saves memory for very
  wide text-ish encodings.
- **High cardinality:** 00 cities -> 00 one-hot columns; 50k product IDs -> unusable.
  Reach for frequency encoding, hashing, or target encoding.
- **Rare levels:** merge levels below a support threshold into `"Other"` with
  `np.where(s.isin(rare_levels), "Other", s)` - stabilizes one-hot and prevents
  overfitting to categories seen twice.

### 4.5 Datetime features + cyclical encoding

Dates are gold mines: extract `year`, `month`, `dayofweek`, `hour`,
`is_weekend=(dow>=5)`, `quarter` via the `.dt` accessor. Then close the circle
literally - the clock wraps around:

```python
hour = df.time.dt.hour
df["hour_sin"] = np.sin(2 * np.pi * hour / 24)
df["hour_cos"] = np.cos(2 * np.pi * hour / 24)
```

Raw `hour` tells a linear model that 23:00 and 00:00 are maximally different; the
sin/cos pair puts them adjacent on a circle (scatter plot proves 23 ≈ 0). Same trick
for month (period 2) and day-of-week (period 7).

>  **Common pitfall:** Extracted components like `year` are technically numeric but
> act as categories/trends depending on the horizon - think before you scale or
> one-hot them blindly.

---

## Chapter 5 - Text data (summary)

Deep dives live in sibling notebooks `04_text_fundamentals.nb.py` and
`05_text_vectorization.nb.py`; here is the conceptual spine so the book is complete.

Text cannot feed a model until it becomes a numeric matrix. The standard assembly line:

```
raw text
  └─ . CLEAN        lowercase, strip HTML/punctuation/URLs, normalize whitespace
  └─ 2. TOKENIZE     sentence -> word tokens (NLTK word_tokenize)
  └─ 3. STOPWORDS    remove high-information-free glue words ("the", "is", "and")
  └─ 4. NORMALIZE    stem (crude suffix chop -> "runn") or lemmatize
                     (dictionary-aware -> "running" -> "run")
  └─ 5. VECTORIZE    Bag-of-Words: one column per vocabulary token, value = count
                     TF-IDF:    downweight tokens common across documents,
                                upweight rare-but-in-this-document tokens
```

Key intuitions to carry into those notebooks:

- BoW ignores word order entirely ("dog bites man" == "man bites dog"); TF-IDF adds
  *which words are distinctive*; both produce wide sparse matrices - exactly the case
  where `OneHotEncoder`-style sparsity and `Normalizer` (row-unit-length) shine.
- The vocabulary is **learned from train only** (`CountVectorizer.fit` on train) -
  the same fit/transform discipline, third verse.
- Stemming is fast and dumb; lemmatization is slower and smarter. Choose stemming for
  search-style recall, lemmatization when readable features matter.

---

## Chapter 6 - Pipelines tie it together

Sibling notebook `06_pipelines.nb.py` is where every technique above stops being a pile
of cells and becomes one deployable object. Conceptually:

- A `Pipeline` chains steps as `(name, transformer_or_model)` pairs; calling `.fit(X, y)`
  runs each transformer's fit+transform in sequence and finally fits the model.
- A `ColumnTransformer` routes *different columns* to *different sub-pipelines*
  (median-impute + robust-scale numerics; most-frequent-impute + one-hot categoricals)
  and stitches the outputs back together, with `get_feature_names_out()` for inspection.
- The killer property: cross-validation now fits every preprocessing parameter *inside
  each fold*. Leakage becomes structurally impossible rather than a matter of discipline.
- The deployed pickle is one artifact - train and serve can never drift apart.

If notebooks 0-03 taught the moves, notebook 06 teaches choreography.

---

## Chapter 7 - The end-to-end workflow checklist

Print this. Tape it to your monitor.

. **Fix the evaluation protocol before touching data** - define target, holdout/CV
   split, metric. The test set is cryogenically frozen from now on.
2. **Audit:** `shape`, `dtypes`, `head()`, `describe(include="all")`, duplicates,
   constant/degenerate columns, ID-like columns (drop them - pure noise/leak risk).
3. **Structural repair:** fix types (dates parsed as dates, numbers stored as strings),
   unify units/casing, resolve impossible values (age = 250).
4. **Missing data:** classify mechanisms (MCAR/MAR/MNAR), choose per-column strategy
   (drop / sentinel / median / mode / group-wise / KNN). Fit imputers on train only.
5. **Outlier policy:** detect (z-score + IQR), diagnose cause, choose remove / cap /
   transform / leave. Document the decision.
6. **Numerical shaping:** logp or PowerTransformer for skew; then Standard/Robust/
   MinMax scaling - fitted on train, applied everywhere.
7. **Categorical encoding:** nominal->one-hot (or frequency for high cardinality),
   ordinal->explicit mapping; group rare levels; plan for unseen categories.
8. **Datetime engineering:** decompose dates, add cyclical sin/cos pairs.
9. **Assemble a `ColumnTransformer` + `Pipeline`** reproducing steps 4-8 exactly.
0. **Cross-validate the whole pipeline;** tune; evaluate ONCE on the frozen test set;
    persist the fitted pipeline for serving.

---

## Chapter 8 - Cheat sheets

### 8. Missing data

| Situation | First move |
|---|---|
| <5% rows affected, MCAR | `dropna()` |
| Column >70% empty + low value | `drop(columns=...)` |
| Numeric, skewed | median (or group-median) imputation |
| Numeric, symmetric | mean imputation |
| Categorical | mode or `"Unknown"` sentinel |
| Time series | `ffill` after sorting |
| Rows resemble rows | `KNNImputer` (scale first) |
| Anything going to production | wrap in `Pipeline` + fit on train only |

### 8.2 Scaling

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, Normalizer
StandardScaler()            # z-score, default for linear/NN/PCA
MinMaxScaler(feature_range=(0, ))   # bounded, outlier-fragile
RobustScaler()              # median/IQR, outlier-safe default for dirty data
Normalizer()                # ROW-wise unit norm - different beast!
```

### 8.3 Skew & outliers

```python
np.logp(x)                                   # quick de-right-skew (x >= 0)
PowerTransformer(method="yeo-johnson")        # learned power transform, negatives OK
x.clip(q - .5*iqr, q3 + .5*iqr)            # winsorize
```

### 8.4 Encoding

```python
df["tier"] = df["tier"].map({"Bronze": 0, "Silver": , "Gold": 2})       # ordinal, explicit
pd.get_dummies(df, columns=["city"], prefix="city", drop_first=True)     # quick EDA
OneHotEncoder(handle_unknown="ignore", sparse_output=False)              # production
df["city_freq"] = df["city"].map(train["city"].value_counts(normalize=True))  # cardinality
np.where(df["city"].isin(rare), "Other", df["city"])                     # rare grouping
np.sin(2*np.pi*df.hour/24); np.cos(2*np.pi*df.hour/24)                   # cyclical hour
```

### 8.5 The golden rules

. Fit on train, transform everywhere else. No exceptions.
2. Ask nominal-or-ordinal before choosing an encoder.
3. Scale ≠ reshape: fix skew first, scale second.
4. Median beats mean whenever money or outliers are involved.
5. If you typed the same three preprocess lines twice, you wanted a `Pipeline`.

*End of the reference book - open notebook 0 and get your hands dirty.*
