# Regression Track

**MLCourse · Machine Learning · supervised · regression**

Predicting numbers. Modules in recommended study order:

| Folder | Model in one line | Superpower |
|---|---|---|
| `01_linear_regression`  (+ Ridge/Lasso/ElasticNet) | weighted sum of features | interpretable baselines |
| `02_knn_regression` | average of nearest neighbors | local, no assumptions |
| `03_svm_regression` | tube around the trend (ε-insensitive) | kernel flexibility |
| `04_decision_tree_regressor` | piecewise constant steps | captures thresholds/jumps |
| `05_random_forest_regressor` | forest averages out noise | strong tabular default |
| `06_adaboost_regressor` | sequential error fixing | boosts shallow trees |
| `07_gradient_boosting_regressor` | fits residuals stepwise | state-of-art tabular accuracy |
| `08_xgboost_regressor` | industrial boosting | fast, regularized, tunable |

Each module follows the same shape: `README.md` (intuition, maths and when to
reach for the model), `01_theory_and_mathematics.ipynb` (the algorithm worked by
hand, then verified against scikit-learn), `02_from_scratch_oop.ipynb`
(pure-NumPy implementation), `03_sklearn_implementation.ipynb`
(the full end-to-end workflow) and `projects/` (graded notebooks, easy -> hard).

`01_linear_regression` goes deeper, because everything later builds on it: it
adds `02_from_scratch_oop.ipynb`, `03_sklearn_implementation.ipynb` and a
notebook per regulariser - `04_ridge_regression.ipynb`,
`05_lasso_regression.ipynb` and `06_elasticnet.ipynb`.

Evaluation toolkit: MAE, RMSE, R², adjusted R², train-vs-test gap,
residual plots - inherited from `01_linear_regression/01_theory_and_math.ipynb`.
