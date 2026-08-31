# Random Forest - Classifier

**MLCourse · Machine Learning · supervised · classification · 06_random_forest**

## The idea in one sentence
Train many slightly-different decision trees on random slices of data and
features, then let them **vote** - the crowd cancels each tree's quirks.

## Math intuition (gentle)

Each tree t gets its own personality via two injections of randomness:
1. **Bootstrap rows** - sample n rows WITH replacement (some duplicated, ~37%
   left out = the tree's personal "out-of-bag" exam set)
2. **Random feature subset per split** (~√n_features) - no single strong
   feature dominates every tree

Prediction = $\text{argmax}_c \sum_t 1[\text{tree}_t(x)=c]$ (or averaged
probabilities).

Why it works: trees make UNCORRELATED mistakes; averaging uncorrelated errors
shrinks variance dramatically while keeping low bias.

**OOB score** = free test set: every row is predicted by the ~37% of trees that
never saw it.

## When / how to use
 tabular data default · mixed feature types · need importance estimates with
no preprocessing gymnastics · resistant to overfitting as trees grow.
 extrapolation beyond training range (trees output constants!) · tiny data ·
when you need one interpretable rule (use a single pruned tree instead) · very
large datasets where boosting wins accuracy-per-byte.

## Key sklearn parameters
| param | meaning | sensible start |
|---|---|---|
| `n_estimators` | number of trees | 200-500 (more never hurts accuracy, only time) |
| `max_depth` / `min_samples_leaf` | per-tree pruning | leave None/1; RF self-regularizes |
| `max_features` | features tried per split | "sqrt" for classification |
| `oob_score` | free validation | True when n_estimators decent |
| `class_weight` | imbalance help | "balanced" if skewed |

## Pitfalls
- importances favor high-cardinality/continuous columns (same caveat as trees)
- cannot predict values outside seen target ranges (regression cousin!)
- many trees on huge data -> memory & latency

## Contents
- `01_theory_and_mathematics.ipynb` - bootstrap & vote mechanics by hand
- `02_from_scratch_oop.ipynb` - pure-NumPy `MyRandomForestClassifier` implementation
- `03_sklearn_implementation.ipynb` - OOB, tuning grid, importances on breast cancer
- `projects/` -  penguins ·  heart ·  credit-g with permutation audit

## Cheat sheet
```python
RandomForestClassifier(n_estimators=400, max_features="sqrt",
                       oob_score=True, n_jobs=-1, random_state=42)
```
