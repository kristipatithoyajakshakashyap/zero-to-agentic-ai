# AdaBoost Regressor - Section Guide

> **MLCourse · Machine Learning · supervised · regression**

AdaBoost (**Ada**ptive **Boost**ing) was the algorithm that made "boosting" famous.
The regressor version, **AdaBoost.R2**, builds a strong regressor out of many *weak*
ones by running **weighted rounds**: every new weak learner is forced to stare at the
rows the previous learners got wrong.

## What you'll learn

- The AdaBoost.R2 loop **in words**: why each round re-weights rows toward big residuals
- Why the weak learner stays tiny (depth-1 / depth-2 trees) and why that is a feature
- What the `loss` parameter (`"linear"` / `"square"` / `"exponential"`) changes
- How the final prediction is a **weighted median** of all the weak trees
- Practical knobs, honest pitfalls, and two worked notebooks + three real-data projects

## The loop in words (the heart of it)

AdaBoost.R2 trains trees **one after another**, and after each round it re-scales how
much each row "matters":

1. Give every row equal weight `w_i = 1/n`.
2. Fit a shallow tree `h_m` respecting the current weights.
3. Score every row's error, then **divide by the worst error** so all errors land in `[0, 1]`
   (this scaling is what lets regression borrow boosting machinery built for 0/1 mistakes).
4. Convert errors to a `loss` in `[0, 1]` - see table below - and average them with the
   current weights to get the round's quality score `err_m` (smaller is better).
5. Turn that into an **estimator weight** `alpha_m = ln((1 - err_m)/err_m)`:
   a round that predicts well earns a loud voice; a coin-flip round is silenced
   (if `err_m >= 0.5` the tree is thrown away entirely and boosting stops early!).
6. **Re-weight the rows:** well-predicted rows lose weight, poorly-predicted rows keep
   (or gain) relative weight - e.g. for the linear loss the update is
   `w_i *= exp(alpha_m * |err_i| / max_err)`, then everything is renormalised.
   This is THE move: round `m+1` cannot just repeat round `m`.
7. Repeat for `n_estimators` rounds. Predict by taking the **weighted median**
   of all tree predictions (robust to one crazy tree).

 Intuition: it is a tutoring loop. After each quiz (round), the tutor spends the next
lesson mostly on the questions the student missed.

## Why weak depth-1 / depth-2 trees?

- A depth-1 tree (a "stump") asks ONE yes/no question about one feature - barely better
  than guessing. Boosting's whole job is turning "barely better than guessing" into
  "very good", so keeping learners weak keeps the *adaptive* part meaningful.
- Shallow trees are extremely fast to fit, and you fit hundreds of them.
- They have low variance individually, so the ensemble's main job is reducing **bias**
  (opposite role to Random Forest, which averages low-bias deep trees to kill variance).

## The `loss` parameter (how errors are reshaped)

After scaling errors to `[0, 1]` via division by the maximum error `D`:

| `loss` | per-row loss `L_i` | character |
|---|---|---|
| `"linear"` (default) | `\|err_i\| / D` | democratic - all sizes matter proportionally |
| `"square"` | `(\|err_i\| / D)^2` | punishes big misses harder |
| `"exponential"` | `1 - exp(-\|err_i\| / D)` | compresses; most forgiving -> rounds survive longest |

 In practice `"exponential"` often lets boosting run many more rounds before the
`err_m >= 0.5` early stop kicks in - try it when your run "stops early".

## When to reach for AdaBoost.R2

- Tabular data of small-to-medium size where you want strong accuracy from tiny trees.
- You suspect some rows are systematically harder and want the model to *focus* on them.
- As the classic baseline between "one decision tree" and gradient boosting.
- Teaching/interpreting: the weight dynamics are very visual (see notebook 01).

When NOT to:

- Very noisy targets / heavy label noise - re-weighting noisy rows **amplifies noise**.
- Huge datasets needing raw speed - prefer `HistGradientBoostingRegressor`.
- You need extrapolation outside the training range - ALL tree ensembles fail there.

## How to use it well

- Start `max_depth=1` or `2` on the base tree; deeper stumps defeat the purpose.
- Keep `learning_rate <= 1.0`; it shrinks every `alpha_m` (gentler re-weighting).
- Watch `len(model.estimators_)`: if it is far below `n_estimators`, boosting stopped
  early - switch `loss="exponential"` or reduce depth.
- Always compare against a single tree of the SAME depth: that gap IS what boosting buys.
- Tune `n_estimators` and `learning_rate` together; more rounds want smaller steps.

## Key parameters

| Parameter | Default | What it does |
|---|---|---|
| `estimator` | `DecisionTreeRegressor(max_depth=3)` | the weak learner; pass `DecisionTreeRegressor(max_depth=1)` for true stumps |
| `n_estimators` | `50` | max boosting rounds (may end EARLY if a round hits `err >= 0.5`) |
| `learning_rate` | `1.0` | shrinks each tree's voice `alpha_m`; smaller = safer, needs more rounds |
| `loss` | `'linear'` | how scaled errors become per-row losses: `'linear'`, `'square'`, `'exponential'` |
| `random_state` | `None` | fixes the weighted bootstrap sampling -> reproducible rounds |

Useful fitted attributes: `estimator_weights_` (voice of each round),
`estimator_errors_` (quality of each round), `feature_importances_`.

## Pitfalls (read before trusting a result!)

-  **Noise amplification:** rows with wrong/noisy labels get MORE attention each
  round - AdaBoost can chase outliers into absurdity. Inspect the highest-weight rows.
-  **Silent early stopping:** if `err_m >= 0.5`, sklearn discards the tree and stops;
  your `n_estimators=300` may really be 21. Check `len(estimators_)`.
-  Weighted-median prediction means individual trees disagree a lot; a single-tree
  interpretation is meaningless.
-  Like every tree ensemble: no extrapolation, and importances are biased toward
  high-cardinality / wide-range features.

## Contents

| File | Focus |
|---|---|
| `01_theory_and_mathematics.ipynb` | hand-run 3 weighted rounds on diabetes (s5), weight-shift visuals, verified vs sklearn internals |
| `02_model_development_workflow.ipynb` | full workflow on diabetes: rounds curve, lr × loss grid, importances |
| `projects/01_easy_diabetes_adaboost.ipynb`  | EDA -> tuned AdaBoost vs single stump table |
| `projects/02_medium_mpg_adaboost.ipynb`  | messy mpg: median-fill, one-hot, rounds curve, residual diagnostics |
| `projects/03_hard_california_staged.ipynb`  | 6k-row California: R²-vs-rounds curve, lr race, extrapolation limits |

## Cheat sheet

```python
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.model_selection import GridSearchCV

ada = AdaBoostRegressor(
    estimator=DecisionTreeRegressor(max_depth=1),  # the weak learner (a stump)
    n_estimators=300,        # MAX rounds - may stop earlier on its own!
    learning_rate=0.5,       # shrink each round's vote
    loss="exponential",      # try when "linear" stops too early
    random_state=42,
).fit(X_train, y_train)

print(len(ada.estimators_), "rounds survived")   # early-stopping detector
y_pred = ada.predict(X_test)                      # weighted median of the trees
GridSearchCV(AdaBoostRegressor(DecisionTreeRegressor(max_depth=1), random_state=42),
             {"n_estimators": [100, 300], "learning_rate": [0.05, 0.3, 1.0],
              "loss": ["linear", "square", "exponential"]}, cv=5)
```

*Next section -> `07_gradient_boosting_regressor` - the same "focus on errors" idea,
rebuilt as gradient descent in function space.*
