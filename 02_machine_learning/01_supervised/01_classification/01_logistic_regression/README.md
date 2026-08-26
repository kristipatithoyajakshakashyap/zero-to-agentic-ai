# Logistic Regression - Section Guide

**MLCourse · Machine Learning · 02_logistic_regression**

Classification with the gentlest possible math: one S-curve, one log, and the
gradient-descent loop you already know. Nine notebooks - four teaching labs plus
five graded real-data projects. Zero .py files; every class lives in a notebook.

## Study order

| # | Notebook | Focus | Time |
|---|---|---|---|
| 1 | `01_theory_made_simple` | probability → odds → sigmoid → cross-entropy (story-built) → the familiar gradient | ~2 h |
| 2 | `02_from_scratch_oop` | `MyLogisticRegression`, verified vs sklearn on Titanic | ~1 h |
| 3 | `03_sklearn_implementation` | Pipeline + C-parameter + L1/L2 paragraph on bundled breast-cancer data | ~1 h |
| 4 | `04_evaluation_and_thresholds` | confusion matrix, precision/recall/F1 stories, ROC-AUC, threshold dial, imbalance trap | ~1.5 h |
| 5-9 | `projects/01…05` | 🟢 titanic · 🟢 penguins · 🟡 heart · 🟠 pima · 🔴 sms spam | ~6 h |

## The whole model on a napkin

$$p = \sigma(w_0+w_1x_1+\cdots), \qquad \sigma(z)=\frac{1}{1+e^{-z}},
\qquad w := w-\alpha\,\frac{X^T(p-y)}{m}$$

Same skeleton as linear regression: weighted sum in, average-error-times-inputs
out. Everything else is interpretation craft - which is what notebook 04 teaches.

## Datasets (all real)

- seaborn cached: `titanic`, `penguins`
- sklearn bundled: breast-cancer wisconsin (offline-safe)
- web CSVs cached next to their notebooks: UCI heart, Pima diabetes, SMS spam

## Project rubric (grade yourself)

1. Lazy baseline computed before celebrating accuracy?
2. Every cleaning/imputation choice justified?
3. Confusion matrix READ (which error hurts more here)?
4. Threshold chosen deliberately with numbers, not left at 0.5 by accident?
5. Coefficients translated into plain business/clinical language?
6. Limitations admitted?

*Start → `01_theory_made_simple.ipynb`*
