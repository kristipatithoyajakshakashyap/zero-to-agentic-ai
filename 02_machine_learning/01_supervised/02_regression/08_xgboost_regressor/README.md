# XGBoost - Regressor

**MLCourse · Machine Learning · supervised · regression · 08_xgboost**

## The idea in one sentence
Gradient boosting rebuilt for discipline: second-order gradients pick smarter
leaf weights, λ/γ penalties sit INSIDE the split-gain formula itself, missing
values are routed natively instead of imputed, and early stopping ends the
"how many trees?" guessing game - the industry default for tabular regression.

## Math intuition (gentle)

Same additive recipe as GBM: $F_m = F_{m-1}+\nu h_m$, but each tree $h_m$ is
grown against a closed-form score built from gradient sums $G$ and hessian
sums $H$, with regularization wired into the split decision:

$$\text{gain} = \underbrace{\tfrac{1}{2}\frac{G_L^2}{H_L+\lambda}}_{left}
+\underbrace{\tfrac{1}{2}\frac{G_R^2}{H_R+\lambda}}_{right}
-\underbrace{\tfrac{1}{2}\frac{(G_L+G_R)^2}{H_L+H_R+\lambda}}_{parent}
-\gamma$$

- For `reg:squarederror`: $G$ = residual sum, $H$ = row count (hessian = 1)
- `reg_lambda` (λ) shrinks each leaf's confidence; `gamma` (γ) is the price
  of adding one more leaf - a split only happens if gain > 0
- Second-order information -> per-leaf step sizes that plain GBM has to
  approximate with its learning rate alone

## When / how to use
 medium/large tabular data · mixed scales & outliers · columns with gaps
(native NaN routing) · you want accuracy AND speed · early stopping to pick
round count automatically.
 tiny datasets (<~500 rows - linear models/RF usually win, boosting just
finds noise faster) · raw image/text inputs · when regulators demand a
fully interpretable model (use linear models or a single tree).

## Key parameters (sklearn API)
| param | meaning | start |
|---|---|---|
| `objective` | loss being boosted | `"reg:squarederror"` |
| `n_estimators` | boosting rounds (trees) | 500-2000 *with* early stopping |
| `learning_rate` | step shrinkage ν | 0.05-0.1 |
| `max_depth` | tree depth | 3-6 |
| `subsample` | row fraction per tree | 0.8-0.9 |
| `colsample_bytree` | feature fraction per tree | 0.8-0.9 |
| `reg_lambda` | L2 penalty on leaf weights | 1 |
| `early_stopping_rounds` | patience on eval metric | 50-100 |

 **Version churn alert**: in xgboost ≥ 1.6 (and all of 3.x),
`early_stopping_rounds` and `eval_metric` belong in the CONSTRUCTOR,
`eval_set` rides in `fit(..., verbose=False)`, `evals_result()` is a METHOD,
and `trees_to_dataframe()` returns CAPITALIZED column names. Older tutorials
that pass `early_stopping_rounds=` to `fit()` will crash on modern installs.

## Pitfalls
- forgetting `eval_set=[(X_val, y_val)]` in `fit()` - early stopping silently
  does nothing without something to watch
- `get_booster().get_score(importance_type="gain")` may return keys like
  `f0, f1, …` when you fit on NumPy arrays - map them back to column names
- tiny-data overkill: on `n < ~500`, prefer Ridge/RandomForest; XGB's capacity
  becomes a liability
- extrapolation: trees can't predict outside the training range (and capped
  targets, like California's 5.00001 ceiling, cap predictions forever)

## Contents
- `01_theory_and_mathematics.ipynb` - one split's gain priced BY HAND, λ sweep, NaN-routing autopsy
- `02_model_development_workflow.ipynb` - early stopping + gain audit on California housing
- `projects/` -  diabetes progression ·  insurance costs (log-target) ·  California early-stop deep dive

## Cheat sheet
```python
from xgboost import XGBRegressor

model = XGBRegressor(
    n_estimators=1500, learning_rate=0.06, max_depth=5,
    subsample=0.85, colsample_bytree=0.85, reg_lambda=1.0,
    early_stopping_rounds=60,          # constructor, NOT fit() - 3.x style
    eval_metric="rmse", objective="reg:squarederror", random_state=42)

model.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=False)
print(model.best_iteration)            # the REAL tree count, chosen by data
pred = model.predict(X_test)
```
