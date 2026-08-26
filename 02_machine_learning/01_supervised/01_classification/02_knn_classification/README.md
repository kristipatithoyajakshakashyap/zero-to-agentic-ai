# k-Nearest Neighbors - Classification

**MLCourse · Machine Learning · supervised · classification · 02_knn**

## The idea in one sentence
To classify a new point, look at the **k closest labeled points** and let them
vote. No training happens at all - the "model" IS the dataset.

## Math intuition (gentle)

Distance between two rows (Euclidean):

$$d(a,b)=\sqrt{(a_-b_)^2+(a_2-b_2)^2+\cdots}$$

Prediction = majority class among the k smallest distances (optionally weighted
by `/distance`, so closer votes count more).

**Why scaling is MANDATORY:** a feature in dollars (0-50,000) drowns a feature
in years (0-0) inside that square root. Always `StandardScaler` first.

## The one knob: k
| k | behavior | risk |
|---|---|---|
| too small (-3) | wiggly, chases noise | overfit |
| too large (~n) | predicts the majority class everywhere | underfit |

Pick k odd (avoid ties) via cross-validation - shown in the notebook.

## When / how to use
 small-to-medium data · baseline before fancy models · naturally multi-class ·
low latency training, instant new classes.
 big datasets (prediction cost grows with n!) · high dimensions (distances stop
distinguishing - "curse of dimensionality") · categorical-heavy features.

## Key sklearn parameters
| param | meaning |
|---|---|
| `n_neighbors` | k - tune with CV |
| `weights` | `"uniform"` or `"distance"` |
| `metric` | default euclidean (`minkowski` p=2) |

## Pitfalls
- forgetting the scaler (silently terrible results)
- using even k on binary problems -> tie-breaks by accident
- judging speed by fit-time: KNN pays at PREDICT time instead

## Contents
- `0_theory_and_mathematics.ipynb` - distances & voting by hand on real penguins
- `02_model_development_workflow.ipynb` - end-to-end sklearn workflow on real wine data
- `projects/` -  iris ·  wine quality ·  breast cancer diagnosis

## Cheat sheet
```python
Pipeline([("sc", StandardScaler()),
          ("knn", KNeighborsClassifier(n_neighbors=5, weights="distance"))])
```
