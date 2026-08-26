# Random Forest Regressor

**MLCourse · Machine Learning · supervised · regression**

## The idea in one sentence
Grow many decision trees on random resamples of the data (and random feature
subsets), then predict the **average** of their outputs - a committee that
cancels each member's noise.

## Bootstrap, bagging & OOB explained
- **Bootstrap:** draw n rows *with replacement* from your n-row training set.
  Each tree sees a slightly different dataset → slightly different tree.
  On average ~63.2% of unique rows land in one bootstrap ("in-bag"); the
  remaining **~36.8% are out-of-bag (OOB)** - never seen by that tree.
- **Bagging** (= bootstrap aggregating): fit one tree per bootstrap sample,
  average their predictions for the final answer.
- **OOB score:** because each row is OOB for ≈37% of trees, you can validate
  every row using only trees that never trained on it - a free cross-validation
  pass computed *during* training (`oob_score=True`).

## Why averaging works: variance cancellation
Independent errors average out:
$$Var(\bar{pred}) = \rho\,\sigma^2 + \frac{1-\rho}{B}\,\sigma^2$$
With $B$ trees the second term shrinks toward zero; the first term survives
because trees correlate (they keep picking similar top features). `max_features`
randomises which features each split may consider → decorrelates trees →
shrinks ρ and kills more variance than plain bagging.

## When / how to use
- **Use when:** tabular regression with non-linearities/interactions, you want
  strong out-of-the-box accuracy with almost no scaling/tuning, or a quick
  reliable baseline before boosting.
- **Avoid when:** you need extrapolation beyond training ranges (forests output
  flat plateaus outside them), strict interpretability, or tiny-latency/memory-
  capped deployments.

## Key sklearn parameters
| param | effect |
|---|---|
| `n_estimators` | number of trees; more = smoother/stabler, no overfit risk, just compute |
| `max_features` | features tried per split (`1.0`=bagging only; `"sqrt"`/`0.5`=more diversity) |
| `max_depth` / `min_samples_leaf` | per-tree pruning; shallow-ish leaves often help noisy data |
| `oob_score` | free validation estimate from out-of-bag rows |
| `n_jobs=-1` | parallelise tree building across CPU cores |

## Pitfalls
- ⚠️ **No extrapolation:** predictions flatten beyond the min/max of training
  features - never trust a forest on inputs outside its observed range.
- Impurity importances mislead when features are correlated → prefer permutation importance.
- Big forests are slow to predict and memory-hungry (hundreds of full trees).
- Averaging can't produce values outside the union of leaf means - bounded targets in, bounded predictions out.

💡 Workflow tip: set `n_estimators=300+`, tune `max_features` and leaf size via
CV/OOB, then confirm with a held-out test set.

## Contents
- `01_theory_and_mathematics.nb.py` - hand-built 5-tree forest on penguins,
  OOB ≈37% demonstrated live, single-tree vs forest stability across seeds
- `02_model_development_workflow.nb.py` - California housing: OOB baseline,
  OOB-vs-n_estimators curve, permutation importance, actual-vs-pred scatter
- `projects/` - easy penguins RF · medium mpg RF · hard insurance RF ·
  advanced OOB + error-hotspot audit

## Cheat sheet
```python
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators=300, max_features=0.5,
                           oob_score=True, n_jobs=-1, random_state=42)
rf.fit(X_train, y_train)          # oob_score_ available immediately after fit
```
