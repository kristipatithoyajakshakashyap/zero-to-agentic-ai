# Support Vector Machines - Classification

**MLCourse · Machine Learning · supervised · classification · 03_svm**

## The idea in one sentence
Find the separating line (hyperplane) that leaves the **widest possible margin**
between the two classes - the "safest street" through the data.

## Math intuition (gentle)

Decision: $\hat y = \text{sign}(w^Tx+b)$ - a weighted sum like linear regression,
but we only care WHICH SIDE of zero it lands on.

Training maximizes the street width $\frac{2}{\lVert w\rVert}$ subject to every
point being outside/on the curb:

$$y_i(w^Tx_i + b) \ge 1$$

Only the points ON the curbs matter - the **support vectors**. Delete everything
else and the boundary doesn't move.

### Soft margin & C
Real data overlaps. Parameter `C` prices violations:
- **small C** = wide street, tolerant of strays → simpler, underfit risk
- **large C** = narrow street, chases every point → overfit risk

### The Kernel Trick
When a straight street can't work, map points into a richer space where it can -
computed WITHOUT ever building that space:

| kernel | draws |
|---|---|
| `linear` | straight hyperplane |
| `rbf` (default) | smooth curved bubbles; `gamma` = bubble tightness |
| `poly` | polynomial curved surfaces |

`gamma` small ⇒ far-reaching smooth curves; `gamma` large ⇒ tight wiggly islands.

## When / how to use
✅ small-to-medium datasets · clear-margin problems · high-dimensional but
low-sample (text, genomics).
❌ big n (>~100k trains slowly) · heavy noise overlap · when you need fast
probabilities or feature importances.

## Key sklearn parameters
| param | meaning |
|---|---|
| `C` | violation price (inverse regularization) |
| `kernel` | linear / rbf / poly |
| `gamma` | rbf/poly curvature reach |

ALWAYS scale features (margins are distance-based).

## Contents
- `01_theory_and_mathematics.ipynb` - margin geometry drawn on real penguins
- `02_model_development_workflow.ipynb` - C/gamma sweeps + grid search on breast cancer
- `projects/` - 🟢 penguins boundary · 🟡 heart kernels · 🔴 german credit costs

## Cheat sheet
```python
Pipeline([("sc", StandardScaler()),
          ("svm", SVC(kernel="rbf", C=10, gamma="scale"))])
```
