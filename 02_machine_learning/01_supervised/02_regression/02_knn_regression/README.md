# k-Nearest Neighbors - Regression

**MLCourse · Machine Learning · supervised · regression · 02_knn**

## The idea in one sentence
To predict a NUMBER for a new point, find the **k closest rows** and output
their **average target value**. No training happens at all - the "model"
IS the dataset, and fitting is just remembering it.

## Math intuition (gentle)

Distance between two rows (Euclidean):

$$d(a,b)=\sqrt{(a_1-b_1)^2+(a_2-b_2)^2+\cdots}$$

Prediction = the mean of the targets of the k rows with the smallest distances
(optionally a *weighted* mean with weights `1/d`, so closer neighbors count more):

$$\hat{y}(q)=\frac{1}{k}\sum_{i \in \text{kNN}} y_i \quad\text{or}\quad \hat{y}(q)=\frac{\sum_i y_i/d_i}{\sum_i 1/d_i}$$

Classification votes; regression averages. Everything else is identical.

**Why scaling is MANDATORY:** a feature in people-per-household (0-10) is
silently crushed by a feature in dollars (0-50,000) inside that square root.
Always wrap `StandardScaler` + `KNeighborsRegressor` in a `Pipeline`.

## The one knob: k
| k | behavior | risk |
|---|---|---|
| too small (1-3) | prediction jumps around, chases noise | overfit (high variance) |
| balanced (10-50) | smooth local averages | sweet spot |
| too large (~n) | predicts nearly the global mean everywhere | underfit (high bias) |

Pick k by cross-validation curve - shown in `03_sklearn_implementation.ipynb`.

## When / how to use
 small-to-medium tabular data · fast baseline before boosting/tree models ·
locally-smooth relationships (price by neighborhood, dosage by weight) ·
zero training time, instant re-fit when data changes.
 big datasets (every PREDICTION scans all n rows) · high dimensions
(distances stop distinguishing - curse of dimensionality) · sharp global
trends/extrapolation (k-NN can only interpolate between seen neighbors).

## Key sklearn parameters
| param | meaning |
|---|---|
| `n_neighbors` | k - tune with CV |
| `weights` | `"uniform"` (plain mean) or `"distance"` (closer counts more) |
| `metric` | distance rule, default euclidean (`minkowski`, p=2) |

## Pitfalls
- forgetting the scaler -> one wide-range feature hijacks every distance
- judging speed by fit-time: k-NN pays at PREDICT time instead
- predicting far outside the training cloud - neighbors simply don't exist there
- even k is fine for regression (averages break ties naturally), but tiny k
  still makes predictions jumpy

## Contents
- `01_theory_and_mathematics.ipynb` - distances & neighbor-averaging by hand on real penguins
- `02_from_scratch_oop.ipynb` - pure-NumPy `MyKNNRegressor` implementation
- `03_sklearn_implementation.ipynb` - end-to-end sklearn workflow on California housing
- `projects/` -  penguin body mass ·  MPG fuel efficiency ·  California housing deep-dive

## Cheat sheet
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor

pipe = Pipeline([("sc", StandardScaler()),
                 ("knn", KNeighborsRegressor(n_neighbors=15, weights="distance"))])
pipe.fit(X_train, y_train)      # "training" = storing the rows
pred = pipe.predict(X_test)     # = weighted average of the 15 nearest rows
```
