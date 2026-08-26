# Gradient Boosting - Classifier

**MLCourse · Machine Learning · supervised · classification · 08_gradient_boosting**

## The idea in one sentence
Build shallow trees **sequentially**, where each new tree is trained to predict
the *mistakes* (gradients) left by the team so far, then nudges the ensemble
forward with a small, shrunk step.

## Math intuition (gentle)

Current ensemble score after m rounds:

$$F_m(x) = F_{m-}(x) + \nu \cdot h_m(x)$$

- $h_m$ = the NEW small tree
- $\nu$ = `learning_rate` (shrink every contribution)
- For log-loss, $h_m$'s training target is the residual-like quantity
  $y_i - p_i$ (truth minus current probability) - literally *"how wrong are we,
  per row"*

Contrast with AdaBoost: AdaBoost **re-weights rows**; GBM **fits residuals**.
Same greedy spirit, different mechanics.

## When / how to use
 tabular accuracy workhorse · mixed scales natively (trees!) · `staged_*`
APIs give learning curves free.
 noisy labels amplify overfitting -> tune depth(2-4)+lr together · no
extrapolation · slower than XGBoost at scale.

## Key sklearn parameters
| param | meaning | start |
|---|---|---|
| `n_estimators` | number of trees | 00-500 |
| `learning_rate` | step size ν | 0.03-0. |
| `max_depth` | per-tree complexity | 2-4 |
| `subsample` | rows per tree (< = stochastic) | 0.8 |

Golden rule: lower lr => more trees => better generalization (until time hurts).

## Pitfalls
- deep trees + high lr = instant overfit; sweep them TOGETHER
- raw probabilities skew confident -> calibrate before risk pricing
- single-threaded sklearn version lags XGB/LightGBM on huge data

## Contents
- `0_theory_and_mathematics.ipynb` - residuals fitted BY HAND on real tips
- `02_model_development_workflow.ipynb` - staged curves + lr×depth×subsample grid
- `projects/` -  titanic ·  pima ·  credit-g staged ·  adult income

## Cheat sheet
```python
GradientBoostingClassifier(n_estimators=300, learning_rate=0.05,
                           max_depth=3, subsample=0.8, random_state=42)
```
