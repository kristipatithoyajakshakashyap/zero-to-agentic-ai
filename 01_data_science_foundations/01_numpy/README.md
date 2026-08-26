# NumPy - The Complete Reference (Zero to Advanced)

> **MLCourse · Data Science Foundations · 01_numpy**

NumPy (Numerical Python) is the foundation layer of the entire Python data stack. pandas builds its
DataFrames on NumPy arrays, scikit-learn accepts them as input, Matplotlib plots them, and PyTorch
and TensorFlow borrow their core ideas outright. This book takes you from "what is an array?" all
the way to performance engineering and linear algebra - every idea mirrored in the companion
notebooks `01_numpy_foundations`, `02_numpy_advanced`, `03_numpy_exercises` and
`04_numpy_solutions`.

## Table of contents

1. [Why NumPy exists](#1-why-numpy-exists)
2. [The ndarray vs the Python list](#2-the-ndarray-vs-the-python-list)
3. [Creating arrays](#3-creating-arrays)
4. [Array attributes](#4-array-attributes)
5. [Data types (dtypes)](#5-data-types-dtypes)
6. [Indexing and slicing](#6-indexing-and-slicing)
7. [Views vs copies](#7-views-vs-copies)
8. [Reshaping, transposing, new axes](#8-reshaping-transposing-new-axes)
9. [Broadcasting](#9-broadcasting)
10. [Elementwise operations and ufuncs](#10-elementwise-operations-and-ufuncs)
11. [Aggregations and axis](#11-aggregations-and-axis)
12. [Boolean masking](#12-boolean-masking)
13. [Fancy indexing](#13-fancy-indexing)
14. [The where-family toolkit](#14-the-where-family-toolkit)
15. [Sorting, ranking, top-k](#15-sorting-ranking-top-k)
16. [Unique values and set operations](#16-unique-values-and-set-operations)
17. [Joining, splitting, tiling](#17-joining-splitting-tiling)
18. [Vectorizing your own formulas](#18-vectorizing-your-own-formulas)
19. [Linear algebra essentials](#19-linear-algebra-essentials)
20. [Random numbers done right](#20-random-numbers-done-right)
21. [Performance playbook](#21-performance-playbook)
22. [Saving and loading](#22-saving-and-loading)
23. [Pitfall gallery](#23-pitfall-gallery)
24. [One-page cheat sheet](#24-one-page-cheat-sheet)

---

## 1. Why NumPy exists

Three reasons, in order of importance:

1. **Speed.** NumPy's core routines are compiled C loops (often SIMD-vectorized - several numbers
   processed per CPU instruction). A single call replaces millions of interpreted Python
   iterations.
2. **Memory.** An array of one million float64s is one contiguous 8 MB buffer. A list of the same
   million numbers is an 8 MB pointer table PLUS roughly 28 bytes per boxed int object.
3. **Ecosystem.** pandas, scipy, scikit-learn, matplotlib, statsmodels - they all exchange data as
   ndarrays. Learning NumPy is learning the field's lingua franca.

```python
import numpy as np

a = np.arange(5_000_000)          # five million integers in one buffer
total = a.sum()                   # one compiled pass: typically 100x+ faster than a Python loop
```

> 💡 **Pro tip:** benchmark honestly with `%timeit` inside Jupyter (`%timeit a.sum()`); it repeats
> the measurement until the statistics are trustworthy. Wall-clock guesses lie.

---

## 2. The ndarray vs the Python list

|                | Python `list`              | NumPy `ndarray`                  |
|----------------|----------------------------|----------------------------------|
| contents       | references to any objects  | fixed dtype, dense raw values    |
| memory layout  | scattered pointer table    | one contiguous block             |
| arithmetic     | manual loops               | whole-array operations           |
| missing values | anything you like          | usually encoded as `np.nan`      |

Homogeneity is the feature that buys everything else: because every element occupies exactly the
same number of bytes, element `i` sits at address `base + i * itemsize` - pure pointer arithmetic,
no object chasing.

```python
mixed = np.array([1, 2.5])        # coercion happens silently
print(mixed.dtype)                # float64 - int was promoted
oops = np.array([1, "two"])       # everything becomes '<U3' strings!
```

> ⚠️ **Common pitfall:** mixed inputs never raise; they silently coerce to one dtype. Check
> `.dtype` immediately after building arrays from external data.

---

## 3. Creating arrays

| function                     | purpose                              | example                          |
|------------------------------|--------------------------------------|----------------------------------|
| `np.array(obj)`              | from list / nested lists             | `np.array([[1, 2], [3, 4]])`     |
| `np.zeros(shape)`            | all zeros                            | `np.zeros((2, 3))`               |
| `np.ones(shape)`             | all ones                             | `np.ones(4)`                     |
| `np.full(shape, val)`        | any constant                         | `np.full((2, 2), 7)`             |
| `np.arange(a, b, step)`      | integer range, stop EXCLUSIVE        | `np.arange(0, 10, 2)`            |
| `np.linspace(a, b, n)`       | n points, endpoints INCLUSIVE        | `np.linspace(0, 1, 5)`           |
| `np.eye(n)` / `np.identity(n)` | identity matrix (`eye` allows offset `k`) | `np.eye(3)`          |
| `np.zeros_like(a)` etc.      | same shape/dtype as another array    | `np.ones_like(a)`                |

The classic difference worth memorizing - `arange` counts by STEP and excludes the stop;
`linspace` counts by NUMBER OF POINTS and includes both ends:

```python
np.arange(0, 1, 0.2)     # array([0. , 0.2, 0.4, 0.6, 0.8])  <- 1.0 missing!
np.linspace(0, 1, 5)     # array([0.  , 0.25, 0.5 , 0.75, 1. ])  <- exact endpoints
```

> ⚠️ **Common pitfall:** floating-point steps make `arange` both unpredictable at the endpoint
> and vulnerable to rounding drift. Rule of thumb: `arange` for integer steps, `linspace` for
> floats.

---

## 4. Array attributes

Six metadata fields answer most debugging questions:

| attribute   | meaning                                  | on `(2, 3, 4)` int64 array |
|-------------|------------------------------------------|----------------------------|
| `.shape`    | lengths along each dimension             | `(2, 3, 4)`                |
| `.ndim`     | number of axes                           | `3`                        |
| `.size`     | total elements (= product of shape)      | `24`                       |
| `.dtype`    | element type                             | `int64`                    |
| `.itemsize` | bytes per element                        | `8`                        |
| `.nbytes`   | total bytes (`size * itemsize`)          | `192`                      |

```python
T = np.arange(24).reshape(2, 3, 4)
assert T.nbytes == T.size * T.itemsize
```

---

## 5. Data types (dtypes)

| dtype     | bytes | range / use                                     |
|-----------|-------|-------------------------------------------------|
| `int32`   | 4     | counters; +/- ~2.1 billion                      |
| `int64`   | 8     | general-purpose default integer                 |
| `float32` | 4     | images, deep-learning weights (~7 digits)       |
| `float64` | 8     | scientific workhorse (~15-16 digits)            |
| `bool`    | 1     | masks: True/False                               |

Convert with `.astype()` - it ALWAYS returns a copy:

```python
np.array([1.9, -2.7]).astype(np.int32)    # -> [1, -2]   truncates toward ZERO
np.array([0, 1, 99]).astype(bool)         # -> [False, True, True]
np.float32(np.pi)                          # -> 3.1415927  precision silently dropped
```

> ⚠️ **Common pitfall (overflow):** fixed-width integers wrap around SILENTLY:
>
> ```python
> np.array([100, 120], dtype=np.int8) + np.array([100, 120], dtype=np.int8)
> # -> [-56 -16]   (200 and 240 do not fit; no exception raised!)
> ```
>
> For image math on uint8 pixels, upcast first (`img.astype(np.int32)`), compute, clip, then cast
> back down.

---

## 6. Indexing and slicing

Python slice semantics carry over: `start:stop:step` with stop EXCLUSIVE, negative indices from
the end. Two dimensions are separated by ONE comma: `M[row, col]`.

```python
x = np.arange(10, 20)
x[0]; x[-1]; x[2:5]; x[::2]; x[::-1]      # first, last, slice, strided, reversed

G = np.arange(1, 13).reshape(3, 4)
G[1, 2]        # single cell
G[1]           # whole row 1  (same as G[1, :])
G[:, 1]        # whole column 1 -> array([ 2,  6, 10])
G[0:2, 1:3]    # submatrix: rows 0-1, cols 1-2
G[::-1]        # rows flipped upside down
G[::-1, ::-1]  # 180-degree rotation
```

> ⚠️ **Common pitfall:** prefer `G[1, 2]` over `G[1][2]`. Both work, but the double-bracket form
> creates an intermediate view per bracket pair and hides your intent.
>
> > 💡 **Pro tip:** read selectors aloud - `G[:, 1]` is "all rows, column 1". Saying it prevents
> most axis mix-ups.

---

## 7. Views vs copies

Slicing does NOT copy data; it returns a *view* onto the same buffer. This is why slicing huge
datasets is free - and why mutations leak through unexpectedly.

| operation                        | returns |
|----------------------------------|---------|
| basic slice `a[:]`, `a[1:]`, `a[::2]` | view |
| `reshape(...)`, `ravel()` (when possible) | view |
| `.T` transpose                    | view    |
| fancy indexing `a[[1, 3]]`        | **copy** |
| boolean masking `a[a > 2]`        | **copy** |
| `.copy()`, `flatten()`, `astype()`| **copy** |

```python
a = np.arange(6)
v = a[1:4]
v[0] = 999                 # write through the view...
print(a)                   # ...original shows 999 too!

f = a[[1, 2]]              # fancy indexing: independent COPY
f[0] = -100
print(a)                   # untouched this time
```

Memorize the asymmetry: **basic slices = views, fancy selections = copies.** Verify any suspicion
with `np.shares_memory(x, y)` or by checking whether `x.base` points at another array.

> 💡 **Pro tip:** when independence matters, say so explicitly with `.copy()`. Deliberate code
> beats accidental correctness.

---

## 8. Reshaping, transposing, new axes

Reshaping reinterprets the flat buffer - usually without moving a byte:

```python
r = np.arange(12)
R = r.reshape(3, 4)        # 3x4 grid (view)
R2 = r.reshape(-1, 4)      # -1 = "infer this dimension"
flat = R.ravel()           # back to 1-D: view if possible
flat2 = R.flatten()        # ALWAYS a fresh copy
Ct = R.T                   # transpose: rows <-> columns (view)
```

Add an axis with `np.newaxis` (identical to `None`) - the standard setup for broadcasting:

```python
x = np.arange(4)
x[np.newaxis, :].shape     # (1, 4)  row-like
x[:, np.newaxis].shape     # (4, 1)  column-like
```

> ⚠️ **Common pitfall:** reshape cannot change the element count - 12 values will never fit a
> `(5, 3)` grid; you get `ValueError`. Product of new shape must equal `arr.size`.

---

## 9. Broadcasting

Broadcasting lets binary operators combine different shapes WITHOUT copying data. Three rules,
applied from the LAST dimension backwards:

1. **Pad** - the shape with fewer dimensions gets 1s prepended until ranks match.
2. **Stretch** - dimensions of size 1 expand (for free) to match the other operand.
3. **Fail** - sizes that differ AND neither equals 1 raise `ValueError`.

Resulting dimension = max of the two padded sizes, per axis.

| left shape     | right shape  | result        | why                                    |
|----------------|--------------|---------------|----------------------------------------|
| `(3,)`         | `()` scalar  | `(3,)`        | scalars broadcast into anything        |
| `(3, 4)`       | `(4,)`       | `(3, 4)`      | right pads to `(1, 4)`, stretches down |
| `(3, 1)`       | `(3,)`       | `(3, 3)`      | pad right to `(1, 3)`; stretch BOTH    |
| `(8, 1, 6, 1)` | `(7, 1, 5)`  | `(8, 7, 6, 5)`| pad to `(1, 7, 1, 5)`; stretch all 1s  |
| `(3, 2)`       | `(3,)`       | ERROR         | last dims 2 vs 3, neither is 1         |

Worked diagram for the outer-sum case `(3, 1) + (3,) -> (3, 3)`:

```text
col (3,1)          row (3,) stretched right        result (3,3)
[[0],              [10 20 30 ->  ->                [[10 20 30]
 [1],                                              [11 21 31]
 [2]]                                              [12 22 32]]
```

```python
F = np.ones((3, 2)); g = np.ones(3)
F + g              # ValueError: operands could not be broadcast together
```

> ⚠️ **Common pitfall:** `(n,)` is neither row nor column until YOU decide. For columns use
> `x.reshape(-1, 1)` or `x[:, None]`; orientation bugs produce plausible garbage downstream.
>
> > 💡 **Pro tip:** `np.broadcast_shapes((8, 1, 6, 1), (7, 1, 5))` predicts result shapes without
> computing anything - handy when designing tensor code.

---

## 10. Elementwise operations and ufuncs

All Python operators act ELEMENTWISE; under the hood each is a *universal function* (ufunc) - a
compiled loop over the buffers.

| category  | operators / functions                                        |
|-----------|--------------------------------------------------------------|
| arithmetic| `+  -  *  /  //  %  **`, `np.sqrt`, `np.exp`, `np.log`       |
| trig      | `np.sin`, `np.cos`, `np.tan`, `np.arctan2`                   |
| rounding  | `np.round`, `np.floor`, `np.ceil`                            |
| special   | `np.abs`, `np.sign`, `np.maximum`, `np.minimum`              |
| comparison| `==  !=  <  <=  >  >=`  (return boolean arrays)              |

```python
u = np.array([1., 2., 3.]); w = np.array([10., 20., 30.])
u * w                       # array([10., 40., 90.])  ELEMENTWISE, not dot product!
u @ w                       # 140.0 - matrix/vector product is the @ operator
```

> ⚠️ **Common pitfall:** `*` multiplies elementwise. If you wanted linear-algebra multiplication,
> you wanted `@`. Silent shape-compatible elementwise products are a classic silent bug.

---

## 11. Aggregations and axis

Read `axis=` as **"collapse THIS axis"**:

| call                    | meaning on a 2-D array                    | result shape |
|-------------------------|-------------------------------------------|--------------|
| `A.sum()`               | collapse everything                       | `()` scalar  |
| `A.sum(axis=0)`         | collapse ROWS -> one value per COLUMN     | `(ncols,)`   |
| `A.sum(axis=1)`         | collapse COLUMNS -> one value per ROW     | `(nrows,)`   |
| `A.sum(axis=0, keepdims=True)` | same but keeps a `(1, ncols)` stub | good for broadcasting |

Available reducers: `sum`, `mean`, `std` (ddof=0 default), `var`, `min`, `max`, plus index
versions `argmin`/`argmax` ("where is the extreme?") and cumulative versions `cumsum`/`cumprod`.

```python
A = np.arange(12, dtype=float).reshape(3, 4)
A.mean(axis=0)             # per-column means, shape (4,)
A.argmax(axis=1)           # winning column within each row, shape (3,)
np.cumsum(np.array([3, 5, 2, 8]))    # running totals: [3 8 10 18]
```

Real data has holes; every reducer has a NaN-skipping twin:

```python
readings = np.array([[1., np.nan, 3.], [4., 5., 6.]])
readings.sum()             # nan - infection spreads through any NaN
np.nansum(readings)        # 19.0 - NaN treated as absent
np.nanmean(readings)       # mean over valid cells only
```

> ⚠️ **Common pitfall:** axis confusion is THE beginner bug. Drill the mantra - axis=0 goes down
> the rows, axis=1 goes across the columns - and print `.shape` after reductions until automatic.

---

## 12. Boolean masking

Comparisons produce boolean arrays; masks then count, select and replace - loop-free:

```python
temps = np.array([18, 21, 25, 29, 31, 27, 22, 17, 30, 26])

hot = temps > 25                    # boolean mask
hot.sum()                           # count Trues
temps[hot]                          # filter: only hot values (returns a COPY)
temps[(temps >= 18) & (temps <= 26)]   # combined condition - parentheses REQUIRED
temps[~hot]                         # negation
temps[hot] = 0                      # in-place replacement via mask assignment
```

Combining conditions uses the bitwise operators `&` (and), `|` (or), `~` (not) - NEVER Python's
`and`/`or`/`not`, which demand a single truth value and explode on arrays:

```python
arr = np.arange(1, 10)
arr[(arr > 3) & (arr < 8)]          # correct
arr[arr > 3 & arr < 8]              # WRONG: & binds tighter than comparisons ->
                                    # ValueError about ambiguous truth value
```

> ⚠️ **Common pitfall:** forgetting parentheses in compound masks. Write `(a > 3) & (a < 8)`
> every single time.

---

## 13. Fancy indexing

Select with ARRAYS of integers: arbitrary order, duplicates fine, negatives fine - always a COPY.

```python
a = np.array([10, 20, 30, 40, 50])
a[[3, 0, 3]]                  # [40 10 40]
a[[-1, 1]]                    # [50 20]

G = np.arange(16).reshape(4, 4)
G[[3, 1, 2]]                  # reorder whole rows
G[[0, 1, 2], [1, 2, 3]]       # paired coordinates: cells (0,1), (1,2), (2,3)
G[:, [2, 0]]                  # all rows, two columns swapped
```

Duplicate-index accumulation gotcha - buffered reads mean repeated indices increment once:

```python
counts = np.zeros(5, dtype=int)
counts[[0, 0, 1]] += 1        # [1 1 0 0 0] - lost an increment!
np.add.at(counts, [0, 0, 1], 1)   # [2 1 0 0 0] - unbuffered, every hit lands
```

---

## 14. The where-family toolkit

| function                  | job                                                     |
|---------------------------|---------------------------------------------------------|
| `np.where(cond, x, y)`    | vectorized if/else, elementwise                         |
| `np.where(cond)`          | indices where cond is True (tuple; take `[0]` in 1-D)   |
| `np.clip(a, lo, hi)`      | clamp values into `[lo, hi]`                            |
| `np.count_nonzero(mask)`  | number of Trues (same as `mask.sum()`)                  |
| `np.nonzero(cond)`        | index arrays of Trues (per dimension)                   |
| `mask.any()` / `mask.all()` | at least one / every element True?                    |

```python
vals = np.array([88, 45, 92, 58])
np.where(vals >= 60, "pass", "fail")   # ['pass' 'fail' 'pass' 'fail']
np.where(vals < 60)[0]                 # array([1, 3])
np.clip(vals, 0, 80)                   # [80 45 80 58]
(vals >= 60).any(), bool((vals < 0).all())
```

> ⚠️ **Common pitfall:** one-argument `np.where` returns a TUPLE of arrays. In 1-D grab `[0]`;
> forgetting it poisons shapes downstream.

---

## 15. Sorting, ranking, top-k

| need                                | tool                                |
|-------------------------------------|-------------------------------------|
| sorted VALUES (copy)                | `np.sort(x)`                        |
| sort IN PLACE (returns None!)       | `x.sort()`                          |
| the ORDER that sorts (ranking)      | `np.argsort(x)`                     |
| descending                          | `np.argsort(-x)` or reverse the idx |
| top-k indices, ordered              | `np.argsort(x)[-k:][::-1]`          |
| top/bottom-k values fast, unordered | `np.partition(x, k)`                |

```python
raw = np.array([23, 7, 13, 42, 4, 19])
names = np.array(["ada", "bob", "cy", "dee", "eli", "fay"])

order = np.argsort(raw)            # [4 1 2 5 0 3]
names[order]                       # leaderboard names via fancy indexing
top3_idx = np.argsort(raw)[-3:][::-1]      # [3 0 5] -> 42, 23, 19

part = np.partition(raw, len(raw) - 3)     # O(n): 3rd-largest placed correctly,
part[-3:]                                  # bigger elements to its right (unordered set)
```

> ⚠️ **Common pitfall:** `x = arr.sort()` sets x to None and mutates arr - the method returns
> nothing. Use `np.sort(arr)` when you want a sorted copy.
>
> > 💡 **Pro tip:** ties matter on leaderboards? Pass `kind="stable"` so equal keys keep original
> order.

---

## 16. Unique values and set operations

```python
draws = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])

uniq, cnts = np.unique(draws, return_counts=True)   # frequency table
uniq[cnts.argmax()]                                   # the mode
uniq, first_idx = np.unique(draws, return_index=True) # where each value FIRST appeared

a = np.array([1, 2, 3, 4]); b = np.array([3, 4, 5, 6])
np.intersect1d(a, b)      # [3 4]        in both
np.union1d(a, b)          # [1 2 3 4 5 6]
np.setdiff1d(a, b)        # [1 2]        in a but not b
np.isin(a, [2, 4, 6])     # [False True False True]  elementwise membership
```

---

## 17. Joining, splitting, tiling

| operation                    | function(s)                                            |
|------------------------------|--------------------------------------------------------|
| join along an axis           | `np.concatenate([a, b], axis=0 or 1)`                  |
| stack as rows                | `np.vstack([a, b])` (legacy alias: `row_stack`)        |
| join side-by-side            | `np.hstack([a, b])`                                    |
| 1-D vectors -> columns       | `np.column_stack([x, y])`  (**not hstack!**)           |
| add depth axis               | `np.dstack([a, b])` briefly                            |
| split rows / cols evenly     | `np.vsplit(M, n)` / `np.hsplit(M, n)`                  |
| uneven splitting             | `np.array_split(x, n)`                                 |
| repeat WHOLE pattern         | `np.tile(p, reps)`                                     |
| repeat EACH element          | `np.repeat(p, n)`                                      |

```python
x = np.array([1, 2, 3]); y = np.array([40, 50, 60])
np.hstack([x, y])            # [ 1  2  3 40 50 60]   <- flat!
np.column_stack([x, y])      # [[ 1 40] [ 2 50] [ 3 60]]  <- design-matrix material

p = np.array([1, 2, 3])
np.tile(p, 3)                # [1 2 3 1 2 3 1 2 3]
np.repeat(p, 3)              # [1 1 1 2 2 2 3 3 3]
```

> ⚠️ **Common pitfall:** building feature matrices with `hstack` on 1-D features yields one long
> row vector. Use `column_stack`.
>
> > 💡 **Pro tip:** joining in a loop copies on every iteration. Collect parts in a list, then
> `np.concatenate(parts)` once.

---

## 18. Vectorizing your own formulas

Any formula composed of ufuncs runs at C speed over whole arrays. Write the scalar math, apply it
to arrays - unchanged:

```python
# Compound interest across a rate curve: A = P * (1 + r/n)**(n*t)
P, t, n = 10_000.0, 10, 4
rates = np.linspace(0.01, 0.10, 10)
fv = P * (1 + rates / n) ** (n * t)          # ten answers, zero loops
```

The pairwise-difference broadcasting trick - memorize this sandwich:

```python
xs = np.array([0., 2., 5., 9.])
D = np.abs(xs[:, None] - xs[None, :])        # (4,1)-(1,4) -> (4,4) matrix of |xi-xj|

pts = rng.normal(size=(6, 2))                # N points in D dims
delta = pts[:, None, :] - pts[None, :, :]    # (N, N, D)
dist = np.sqrt((delta ** 2).sum(axis=-1))    # full Euclidean distance matrix
```

`np.vectorize(f)` wraps a scalar-only Python function so it accepts arrays. It is pure CONVENIENCE
- internally it still loops in Python and gives zero speed-up. Use it for string formatting or
bespoke branching, never for arithmetic.

---

## 19. Linear algebra essentials

| task                        | tool                                |
|-----------------------------|-------------------------------------|
| matrix product              | `A @ B` (same as `np.dot(A, B)`)    |
| identity                    | `np.eye(n)` / `np.identity(n)`      |
| diagonal sum                | `np.trace(A)`                       |
| determinant                 | `np.linalg.det(A)`                  |
| inverse (use sparingly)     | `np.linalg.inv(A)`                  |
| solve Ax = b                | `np.linalg.solve(A, b)`             |
| least squares (overdetermined) | `np.linalg.lstsq(A, b)`          |
| vector/matrix norm          | `np.linalg.norm(v)`                 |
| eigenvalues (symmetric)     | `np.linalg.eigvalsh(S)`             |

Worked system:

```text
2x +  y =  5
 x + 3y = 10
```

```python
A = np.array([[2., 1.], [1., 3.]])
b = np.array([5., 10.])
x = np.linalg.solve(A, b)              # -> [1. 3.]
np.allclose(A @ x, b)                  # True - substitute-back verification
```

> ⚠️ **Common pitfall:** `inv(A) @ b` works but squares the condition number and computes entries
> nobody needs. Professional code says `solve` (or `lstsq`) almost exclusively.

---

## 20. Random numbers done right

Modern best practice (NumPy >= 1.17): create ONE seeded Generator and use its methods. Explicit
seed = reproducibility; no hidden global state; better algorithms (PCG64).

| method                                 | draws                                  |
|----------------------------------------|----------------------------------------|
| `rng.integers(low, high, size)`        | uniform ints, high EXCLUSIVE           |
| `rng.uniform(low, high, size)`         | continuous U[low, high)                |
| `rng.normal(loc, scale, size)`         | Gaussian (mean, std)                   |
| `rng.choice(a, size, replace, p)`      | sample with/without replacement, weights|
| `rng.permutation(x)`                   | shuffled COPY                          |
| `rng.shuffle(x)`                       | shuffle IN PLACE (returns None)        |
| `rng.random(size)`                     | U[0, 1) floats                         |

```python
rng = np.random.default_rng(42)               # instantiate once, reuse everywhere
dice = rng.integers(1, 7, size=(1000, 2))     # fair dice, faces 1..6
heights = rng.normal(170, 10, size=5)
lottery = rng.choice(np.arange(1, 50), size=6, replace=False)
deck_copy = rng.permutation(deck)             # original intact
rng.shuffle(deck)                             # deck itself reordered
```

Legacy style - `np.random.seed(42)` followed by `np.random.rand(...)` - seeds hidden GLOBAL state
and still dominates old tutorials. Recognize it; write Generator code instead.

> ⚠️ **Common pitfall:** creating a fresh unseeded generator inside a loop destroys
> reproducibility. Instantiate once (seeded), pass `rng` around like any parameter.

---

## 21. Performance playbook

Why vectorization wins: interpreted Python pays per-element bytecode dispatch, while NumPy runs a
compiled C loop - often SIMD-vectorized, processing multiple lanes per instruction.

Do:

- Replace element loops with ufunc expressions (`np.exp(vals)`, `a @ b`, masked assignments).
- Preallocate output arrays and fill by index instead of appending.
- Aggregate/join ONCE after collecting parts in a Python list.
- Reduce with `axis=` instead of looping over rows/columns.
- Measure with `%timeit`; optimize only what profiling proves slow.

Don't:

- Grow arrays in loops - `np.append` copies EVERYTHING each call (quadratic overall):

```python
def grow_bad(n):
    out = np.empty(0)
    for i in range(n):
        out = np.append(out, i)     # O(total-so-far) copy per call -> O(n^2) overall
    return out

def grow_good(n):
    out = np.empty(n)               # one allocation
    for i in range(n):
        out[i] = i
    return out                      # orders of magnitude faster
```

- Loop over rows "just to be safe": almost every row-loop has a broadcasting equivalent.
- Trust intuition over `%timeit` output - measurements win arguments.

---

## 22. Saving and loading

| format      | write             | read            | notes                                   |
|-------------|-------------------|-----------------|-----------------------------------------|
| `.npy`      | `np.save(path, a)`| `np.load(path)` | ONE array; exact dtype/shape preserved  |
| `.npz`      | `np.savez(path, key=a, ...)` | `np.load(path)` | labeled bundle; lazy dict access via `z["key"]` |
| text/CSV    | `np.savetxt(path, M, delimiter=",")` | `np.loadtxt(path, delimiter=",")` | human-readable; dtype NOT preserved |

```python
matrix = np.arange(12).reshape(3, 4)
np.save("m.npy", matrix)
np.loadtxt  # comes back float64 even if you saved ints - astype(int) if needed
```

> ⚠️ **Common pitfall:** text formats forget dtypes. Anything structural lives happily in
> `.npy`/`.npz` (or pandas parquet); reserve CSV for exchanging with the outside world.

---

## 23. Pitfall gallery

The eight classics, collected from the notebooks above:

1. Mixed-type `np.array([...])` coerces silently - check `.dtype`.
2. Fixed-width integer overflow wraps without error - upcast before heavy integer math.
3. Slices are views; writes leak into parents. Fancy/boolean selections are copies.
4. `axis=0` collapses rows, `axis=1` collapses columns - print `.shape` to confirm.
5. Compound masks NEED parentheses: `(a > 3) & (a < 8)`, and use `&`/`|`/`~`, not `and`/`or`.
6. `arr.sort()` returns None - `np.sort(arr)` for a copy.
7. One-arg `np.where` returns a tuple - index `[0]` in 1-D.
8. Never build arrays with repeated `np.append` - preallocate or convert a list once.

---

## 24. One-page cheat sheet

```python
import numpy as np
rng = np.random.default_rng(42)
```

| I want to...                        | one-liner                                       |
|-------------------------------------|-------------------------------------------------|
| make 0..n-1                         | `np.arange(n)`                                  |
| n evenly spaced incl. endpoints     | `np.linspace(a, b, n)`                          |
| zeros / ones / constant             | `np.zeros(s)`, `np.ones(s)`, `np.full(s, v)`    |
| identity                            | `np.eye(n)`                                     |
| inspect                             | `.shape .ndim .size .dtype .nbytes`             |
| change dtype                        | `a.astype(np.float64)`                          |
| pick cell / row / col               | `M[i, j]`, `M[i]`, `M[:, j]`                    |
| submatrix / reverse                 | `M[0:2, 1:3]`, `M[::-1]`                        |
| reshape / flatten                   | `a.reshape(r, c)`, `a.ravel()` (view), `a.flatten()` (copy) |
| transpose                           | `a.T`                                           |
| add axis                            | `a[:, None]` or `a[np.newaxis, :]`              |
| broadcast-safe stats                | `X.mean(axis=0, keepdims=True)`                 |
| reduce with axis                    | `A.sum(axis=0)` down rows, `axis=1` across cols |
| NaN-safe reduce                     | `np.nansum`, `np.nanmean`, `np.nanmax`          |
| running totals                      | `np.cumsum(x)`                                  |
| mask / filter / count               | `m = x > v`; `x[m]`; `m.sum()`                  |
| combine conditions                  | `(x > a) & (x < b)`, negate with `~m`           |
| vectorized if/else                  | `np.where(cond, x, y)`                          |
| clamp                               | `np.clip(x, lo, hi)`                            |
| positions of Trues                  | `np.where(cond)[0]` / `np.nonzero(cond)`        |
| sort copy / in place                | `np.sort(x)` / `x.sort()`                       |
| ranking / descending                | `np.argsort(x)` / `np.argsort(-x)`              |
| top-k indices                       | `np.argsort(x)[-k:][::-1]`                      |
| fast top-k values                   | `np.partition(x, -k)[-k:]`                      |
| frequency table / mode              | `np.unique(x, return_counts=True)`              |
| set ops                             | `intersect1d union1d setdiff1d isin`            |
| join / stack columns                | `np.concatenate`, `np.vstack`, `np.column_stack`|
| split                               | `np.hsplit`, `np.vsplit`, `np.array_split`      |
| duplicate pattern / elements        | `np.tile(p, n)` / `np.repeat(p, n)`             |
| distance matrix                     | `np.abs(x[:, None] - x[None, :])` (1-D)         |
| matrix product / solve              | `A @ B`, `np.linalg.solve(A, b)`                |
| det / inv / trace / norm            | `np.linalg.det/inv`, `np.trace`, `np.linalg.norm`|
| random ints / normal / choice       | `rng.integers`, `rng.normal`, `rng.choice`      |
| shuffle copy / in place             | `rng.permutation(d)` / `rng.shuffle(d)`         |
| save / load                         | `np.save`, `np.savez`, `np.load`, `savetxt/loadtxt` |

---

## Where next

You now hold the vocabulary underneath pandas (vectorized column ops ARE masking + broadcasting),
scikit-learn (design matrices ARE `column_stack` + z-scoring), and beyond. Continue with the
exercises notebook, check yourself against the solutions, and keep the cheat sheet within reach -
fluency comes from repetition, not reading.
