# Classification Track

**MLCourse - Machine Learning - supervised - classification**

Predicting categories. Modules in recommended study order:

| Folder | Model in one line | Superpower |
|---|---|---|
| `01_logistic_regression` | weighted sum -> sigmoid probability | interpretable risk scores |
| `02_knn_classification` | "you look like your neighbors" | zero training, intuitive |
| `03_svm_classification` | widest street between classes | strong on small clean data |
| `04_naive_bayes` | multiply per-feature evidence | blazing fast on text counts |
| `05_decision_tree_classifier` | 20 questions game | human-readable rules |
| `06_random_forest_classifier` | many trees vote | robust default for tabular |
| `07_adaboost_classifier` | fix mistakes sequentially | sharpens weak rules |
| `08_gradient_boosting_classifier` | each tree fits previous errors | top accuracy on tabular |
| `09_xgboost_classifier` | industrial gradient boosting | speed + regularized power |

Inside every module you will find the same rhythm:

- `README.md` - the intuition and the maths, written to be read before you code.
- `01_theory_and_mathematics.ipynb` - the algorithm worked by hand on a small,
  real dataset, then checked against scikit-learn.
- `02_from_scratch_oop.ipynb` - pure-NumPy implementation of the algorithm.
- `03_sklearn_implementation.ipynb` - the full end-to-end workflow: split,
  preprocess, tune, evaluate, interpret.
- `projects/` - 3-4 graded notebooks (easy -> hard) with their own README.

`01_logistic_regression` is the exception, and deliberately so: because it is the
module where you learn what a classifier *is*, it splits the material across
`01_theory_made_simple.ipynb`, `02_from_scratch_oop.ipynb` (build one yourself
with NumPy), `03_sklearn_implementation.ipynb` and
`04_evaluation_and_thresholds.ipynb`.

Metrics you must know before starting: accuracy is NOT enough - read
`01_logistic_regression/04_evaluation_and_thresholds.ipynb` for confusion
matrices, precision/recall and ROC-AUC. Every project here uses them.

