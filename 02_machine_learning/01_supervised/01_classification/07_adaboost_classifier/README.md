# AdaBoost - Classifier

**MLCourse · Machine Learning · supervised · classification · 07_adaboost**

## The idea in one sentence
Train a long line of WEAK learners (usually depth-1 "stumps"); after each round,
**increase the weight of the rows the previous model got wrong**, forcing the
next learner to focus on them; finally let all stumps vote with their earned
trust.

## Math intuition (gentle)

Round t with row-weights $w_i$:

. fit stump on weighted rows -> weighted error $\epsilon_t$
2. learner's say: $\alpha_t = \tfrac{1}{2}\ln\frac{1-\epsilon_t}{\epsilon_t}$
   (better-than-coin-flip -> positive say)
3. re-weight wrong rows by $e^{\alpha_t}$ (right rows shrink)

Final: $H(x)=\text{sign}\big(\sum_t \alpha_t h_t(x)\big)$ - weighted committee.

Intuition: hard examples get louder voices until someone explains them.

## When / how to use
 small-to-medium tabular · as a teaching bridge to gradient boosting ·
stumps give coarse-but-stable boundaries.
 very noisy labels (re-weighting amplifies noise!) · big data (GBM/XGB faster
and stronger) · high-cardinality categoricals without encoding care.

## Key sklearn parameters
| param | meaning | start |
|---|---|---|
| `n_estimators` | number of stumps | 100-400 |
| `learning_rate` | shrinks each α_t (needs more rounds) | 0.5-1.0 |
| `estimator` | weak learner | default depth-1 tree |

Scaling unnecessary; watch for `SAMME` deprecation notes in old tutorials.

## Pitfalls
- noisy outliers get exponentially louder -> cap n_estimators, inspect errors
- learning_rate & n_estimators trade off (lower rate => need more rounds)
- don't deep-tree the base learner ("weak" is the point)

## Contents
- `01_theory_and_mathematics.ipynb` - α and weight updates computed BY HAND on real rows
- `02_model_development_workflow.ipynb` - staged-error curve + tuning on breast cancer
- `projects/` -  penguins ·  heart ·  pima screening

## Cheat sheet
```python
AdaBoostClassifier(n_estimators=200, learning_rate=0.8, random_state=42)
```
