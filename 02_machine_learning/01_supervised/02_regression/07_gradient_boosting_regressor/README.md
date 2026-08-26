# Gradient Boosting Regressor - Section Guide

> **MLCourse · Machine Learning · supervised · regression**

Gradient boosting is the idea that won Kaggle after Kaggle: build a regression model
**slowly**, each new small tree trained to predict the **residuals** the current model
still leaves behind, then added in with a shrinkage factor:

$$F_m(x) \;=\; F_{m-}(x) \;+\; \nu \cdot h_m(x), \qquad 0 < \nu \le $$

## What you'll learn

- Why "fit the residuals" and "descend the gradient" are THE SAME statement
- Why shrinkage (`learning_rate`, ν) turns a wild chaser into a careful learner
- What `loss="huber"` / `"absolute_error"` buy you on outlier-heavy targets
- The staged API: how to find the best number of trees BEFORE overfitting starts
- Practical knobs, honest pitfalls, and two worked notebooks + four real-data projects

## The loop in words

. Start with a constant: $F_0(x) = \bar y$ (the mean minimises squared error).
2. Compute residuals $r_i = y_i - F_{m-}(x_i)$.
3. Fit a shallow tree $h_m$ to those residuals (features -> *error corrections*).
4. Add it in shrunk: $F_m = F_{m-} + \nu\, h_m$.
5. Repeat `n_estimators` times. Predictions are just the final accumulated $F_M(x)$.

### Why residuals ARE gradients (the one-line calculus)

For squared-error loss $\frac{1}{2}(y - F)^2$, the gradient with respect to the
prediction is

$$\frac{\partial}{\partial F}\,\tfrac{1}{2}\bigl(y-F\bigr)^2 \;=\; -(y-F).$$

So "the negative gradient" - the direction of steepest DESCENT in prediction space -
is exactly the residual. Fitting a tree to residuals **is** taking a gradient step,
where each leaf outputs the step size. Change the loss and the pseudo-residuals change
(absolute error -> sign of residual; huber -> residual clipped at δ); the machinery
never changes. That generality is why this family is called gradient boosting.

### Shrinkage (why ν matters)

Without shrinkage (ν=) each tree fully "corrects" the residuals - including noise -
and the train MSE plummets while test error balloons. Small ν (0.0-0.3) makes each
round a cautious nudge; errors decay smoothly and many rounds average out noise.
The classic recipe: **small learning_rate + more trees + early stopping.**

### Loss options for regression

| `loss` | pseudo-residual | use when |
|---|---|---|
| `"squared_error"` (default) | residual $y - F$ | generic, symmetric errors |
| `"absolute_error"` | $\mathrm{sign}(y-F)$ | heavy-tailed outliers; optimises the median |
| `"huber"` | residual clipped at δ | best of both: quadratic near 0, linear far out |

## When to reach for GradientBoostingRegressor

- Tabular data, small-to-medium size, where you want top accuracy without deep tuning.
- Non-linear signals + interactions that linear models miss.
- You want `staged_predict` to pick the optimal number of trees empirically.
- Mixed-scale features WITHOUT preprocessing (trees don't care about units).

When NOT to:

- Huge data -> prefer `HistGradientBoostingRegressor` (or XGBoost/LightGBM).
- Need extrapolation beyond training ranges (all tree ensembles fail there).
- Ultra-noisy labels with no cleaning possible - boosting will fit the noise eventually.

## How to use it well

- Start: `n_estimators` generous (500-2000), `learning_rate=0.05`,
  `max_depth=2-3`, `subsample=0.8`, then let staged validation find the stop point.
- Use `staged_predict` on a VALIDATION split to choose the round count honestly.
- Keep trees shallow: depth 2-3 captures interactions without memorising rows.
- Compare against `DummyRegressor` and a linear model so "hard-won" gains are real.

## Key parameters

| Parameter | Default | What it does |
|---|---|---|
| `learning_rate` (ν) | `0.` | shrinkage per tree; smaller = safer, needs more trees |
| `n_estimators` | `00` | number of sequential trees (M) |
| `max_depth` | `3` | depth of each small tree; 2-4 is the sweet spot |
| `subsample` | `.0` | fraction of rows per tree; `<` adds stochasticity (variance (down), speed (up)) |
| `loss` | `'squared_error'` | also `'absolute_error'`, `'huber'` for robustness |
| `init` | mean Dummy | the starting constant model $F_0$ |
| `random_state` | `None` | reproducibility of subsampling |

Useful extras: `staged_predict()` (prediction after every round),
`train_score_`/`validation_fraction`+`n_iter_no_change` (built-in early stopping),
`feature_importances_`.

## Pitfalls

-  **Overfits by design if unchecked**: train MSE falls every single round; only a
  held-out curve tells you when to STOP adding trees.
-  **lr × n_estimators are coupled**: changing ν without retuning M invalidates
  comparisons.
-  **No extrapolation**: predictions are sums of bounded leaf values - the model can
  never output beyond the range seen during training.
-  Sensitive to duplicated/leaky columns: boosting will happily latch onto leakage
  and report glorious CV numbers until deployment humbles everyone.
-  Sequential by nature - no easy parallelism across trees (unlike forests).

## Contents

| File | Focus |
|---|---|
| `0_theory_and_mathematics.nb.py` | manual 4-round residual loop (bmi), verified == sklearn; ν comparison |
| `02_model_development_workflow.nb.py` | insurance: log-target, `staged_predict` best-round, lr×depth grid, importances |
| `projects/0_easy_diabetes_gbm.nb.py`  | baseline vs tuned, staged peak, bmi/s5 drivers |
| `projects/02_medium_white_wine_gbm.nb.py`  | UCI white wine quality: baselines, MAE/RMSE/R², alcohol/density |
| `projects/03_hard_insurance_log_gbm.nb.py`  | log-charges pipeline, $-metrics, smoker×bmi partial dependence |
| `projects/04_advanced_california_staged.nb.py`  | 8k-row California: staged early-stop, subsample study, error hotspots |

## Cheat sheet

```python
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV

gbm = GradientBoostingRegressor(
    n_estimators=500,       # plenty of rope...
    learning_rate=0.05,     # ...but tiny steps
    max_depth=3,            # shallow interaction-capturing trees
    subsample=0.8,          # stochastic rounds: variance down
    random_state=42,
).fit(X_train, y_train)

# staged API: predictions after EVERY round -> pick the validation optimum
for m, pred in enumerate(gbm.staged_predict(X_valid), start=):
    ...
best_round = int(np.argmin([mse(y_valid, p) for p in gbm.staged_predict(X_valid)])) +
final = GradientBoostingRegressor(n_estimators=best_round, **same_kwargs).fit(X_trval, y_trval)
```

*Next section -> `08_xgboost_regressor` - the industrial-strength descendant.*
