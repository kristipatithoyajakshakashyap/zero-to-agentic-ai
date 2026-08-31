# Supervised Learning

**MLCourse · Machine Learning · 01_supervised**

Supervised models learn from **labeled examples**: every row carries the answer
(target) you want to predict. Split by task type:

```
01_supervised/
├── 01_classification/    predict a CATEGORY   (spam? disease? which species?)
└── 02_regression/        predict a NUMBER     (price, weight, charges)
```

## The shared workflow (memorize once, reuse everywhere)

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=..., random_state=42)

pipe = Pipeline([("scaler", StandardScaler()),      # when the model needs it
                 ("model", SomeAlgorithm())])
pipe.fit(X_train, y_train)
cross_val_score(pipe, X_train, y_train, cv=5)
# evaluate on test -> interpret -> check errors
```

## Model lineup

| Classification | Regression |
|---|---|
| 01 Logistic regression  | 01 Linear regression (+ Ridge/Lasso/ElasticNet)  |
| 02 k-Nearest Neighbors | 02 k-Nearest Neighbors |
| 03 Support Vector Machines | 03 SVR |
| 04 Naive Bayes | - (no standard NB regressor) |
| 05 Decision Tree | 04 Decision Tree |
| 06 Random Forest | 05 Random Forest |
| 07 AdaBoost | 06 AdaBoost |
| 08 Gradient Boosting | 07 Gradient Boosting |
| 09 XGBoost | 08 XGBoost |

## Choosing a starter model (rule of thumb)

1. Always run the simple baseline first (logistic / linear).
2. Tabular data with mixed types -> tree ensembles (RF, then boosting).
3. Small clean data needing smooth boundaries -> SVM / KNN.
4. Text counts -> Naive Bayes.
Every module's README has its own "when to use" table.
