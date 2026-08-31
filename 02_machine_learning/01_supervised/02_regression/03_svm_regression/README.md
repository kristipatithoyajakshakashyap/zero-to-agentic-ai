# Support Vector Regression (SVR)

**MLCourse · Machine Learning · supervised · regression · 03_svm**

## The idea in one sentence
Fit a line (or curve) through the data but declare a tolerance tube of width
±ε around it: **errors INSIDE the tube cost nothing**, so only the points
OUTSIDE the tube - the **support vectors** - shape the model.

## Math intuition (gentle)

Ordinary least squares punishes *every* residual by squaring it. SVR says:
"stay within ε of every point if you can; pay only for violations":

$$\min \tfrac{1}{2}\|w\|^2 + C\sum_i(\xi_i + \xi_i^*) \quad\text{s.t.}\quad |y_i - w^\top x_i - b| \le \varepsilon + \xi_i$$

- Flat street = the prediction line; **ε-tube** = the asphalt you're allowed to miss by.
- Curb stones holding the street = support vectors (`model.support_`).
- **Kernel trick**: replace $w^\top x$ with a kernel $K(x_i,x_j)$ and the same
  flat-street logic bends into curves - without ever computing features
  explicitly. `kernel="rbf"` is the everyday choice.

## The two knobs that matter
| knob | too small | too large |
|---|---|---|
| `C` | wide margin, many points outside -> flexible, risks overfit when huge? no - small C = MORE violations tolerated, smoother/underfit | tube enforced strictly -> chases noise, overfit |
| `gamma` (rbf) | each point's reach is long -> nearly-linear curve, underfit | reach tiny -> islands around single points, wild overfit |
| `epsilon` | thin tube -> almost all points become SVs, slow & noisy-fit | fat tube -> few/no SVs, near-constant prediction |

Rule of thumb: start `epsilon` at roughly 10% of the target's standard
deviation, tune C/gamma on a log grid via cross-validation.

## When / how to use
 medium-sized data (~100-10,000 rows) · smooth nonlinear trends · robustness
to moderate noise/outliers (they sit inside ε and are ignored) · regression on
a transformed target (e.g. log-price).
 very large n (training cost grows ~O(n²-n³)) · heteroscedastic noise (one
global tube width can't fit both calm and volatile regions) · when you need
per-feature explanations or lightning-fast predictions.

**Scaling is MANDATORY**: kernels compare rows with inner products/distances;
unscaled features dominate them exactly like in k-NN.

## Key sklearn parameters
| param | meaning |
|---|---|
| `kernel` | `"linear"` (fast, interpretable-ish), `"rbf"` (smooth curves, default) |
| `C` | price of leaving the tube - log-grid [0.1 … 1000] |
| `epsilon` | half-width of the no-penalty tube |
| `gamma` | rbf reach per point - `"scale"` default, then try 0.1× / 10× |

## Pitfalls
- forgetting `StandardScaler` -> silently terrible fits
- `epsilon=0` -> degenerates toward hard-margin chasing of EVERY point
- tuning only C while gamma stays `"scale"` - they interact strongly
- judging SVR on train R²: with small ε it can look perfect yet generalize poorly

## Contents
- `01_theory_and_mathematics.ipynb` - draw the ε-tube on real tips data; count support vectors
- `02_model_development_workflow.ipynb` - kernel shootout + C/gamma grid on California housing
- `projects/` -  tips tube vs OLS ·  white-wine quality as regression ·  insurance charges with log-target

## Cheat sheet
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

pipe = Pipeline([("sc", StandardScaler()),
                 ("svr", SVR(kernel="rbf", C=10, gamma="scale", epsilon=0.1))])
pipe.fit(X_train, y_train)
pred = pipe.predict(X_test)          # smooth nonlinear regression, outliers ignored
```
