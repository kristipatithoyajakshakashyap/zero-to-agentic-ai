# XGBoost - Classifier

**MLCourse · Machine Learning · supervised · classification · 09_xgboost**

## The idea in one sentence
Gradient boosting rebuilt for speed and discipline: second-order gradients,
built-in regularization, clever splitting, and native missing-value handling -
the industry default for tabular competitions and production.

## Math intuition (gentle)

Same additive recipe as GBM: $F_m = F_{m-1}+\nu h_m$, but each tree $h_m$ is
fit to a smoothed objective that ADDS penalties inside the split search:

$$\text{gain} = \underbrace{\tfrac{1}{2}\frac{G_L^2}{H_L+\lambda}}_{left}
+\underbrace{\tfrac{1}{2}\frac{G_R^2}{H_R+\lambda}}_{right}
-\underbrace{\tfrac{1}{2}\frac{(G_L+G_R)^2}{H_L+H_R+\lambda}}_{parent}
-\gamma$$

- $G$ = gradient sums, $H$ = hessian (curvature) sums -> smarter steps than GBM
- `reg_lambda` (λ) shrinks leaf weights; `gamma` (γ) prices each extra leaf

## When / how to use
 medium/large tabular data · need speed + accuracy together · sparse/missing
values natively · early stopping built in.
 tiny datasets (overkill; logistic/RF fine) · image/text raw inputs · when
strict interpretability required (use linear models or single tree).

## Key parameters (sklearn API)
| param | meaning | start |
|---|---|---|
| `n_estimators` | trees | 300-800 with early stopping |
| `learning_rate` | step ν | 0.05-0.1 |
| `max_depth` | tree depth | 3-6 |
| `subsample`, `colsample_bytree` | row/feature sampling | 0.8 |
| `reg_lambda` | L2 on leaf weights | 1 |
| `early_stopping_rounds` | stop when eval metric stalls | 50 |

## Pitfalls
- forgetting `eval_set` wastes early stopping
- overfitting small data with depth>5
- version churn: sklearn wrapper moves params around across releases

## Contents
- `01_theory_and_mathematics.ipynb` - gain formula by hand + regularization demo
- `02_model_development_workflow.ipynb` - early stopping + tuning on breast cancer
- `projects/` -  titanic ·  heart ·  credit-g ·  adult income

## Cheat sheet
```python
XGBClassifier(n_estimators=500, learning_rate=0.06, max_depth=4,
              subsample=0.8, colsample_bytree=0.8,
              early_stopping_rounds=50, random_state=42)
```
