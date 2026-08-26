# Regression Track

**MLCourse · Machine Learning · supervised · regression**

Predicting numbers. Modules in recommended study order:

| Folder | Model in one line | Superpower |
|---|---|---|
| `0_linear_regression`  (+ Ridge/Lasso/ElasticNet) | weighted sum of features | interpretable baselines |
| `02_knn_regression` | average of nearest neighbors | local, no assumptions |
| `03_svm_regression` | tube around the trend (ε-insensitive) | kernel flexibility |
| `04_decision_tree_regressor` | piecewise constant steps | captures thresholds/jumps |
| `05_random_forest_regressor` | forest averages out noise | strong tabular default |
| `06_adaboost_regressor` | sequential error fixing | boosts shallow trees |
| `07_gradient_boosting_regressor` | fits residuals stepwise | state-of-art tabular accuracy |
| `08_xgboost_regressor` | industrial boosting | fast, regularized, tunable |

Each module: `README.md` (intuition + when/how to use) ·
`0_sklearn_in_action.ipynb` · `projects/` graded .

Evaluation toolkit: MAE, RMSE, R², adjusted R², train-vs-test gap,
residual plots - inherited from `0_linear_regression/0_theory_and_math.ipynb`.
