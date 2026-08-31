# Track 02 - Machine Learning

Classical machine learning built directly on the foundations track. Each
algorithm lives in its own module with a consistent structure:

```
<module>/
├── README.md                        reference sheet: intuition, when/how to use
├── 01_theory_and_mathematics.ipynb  gentle math demonstrated on real data
├── 02_model_development_workflow.ipynb  end-to-end sklearn workflow
└── projects/                        3-4 graded notebooks, easy -> advanced
```

## Layout

```
02_machine_learning/
├── data/                            shared dataset hub (downloaded once)
├── 01_supervised/
│   ├── 01_classification/
│   │   ├── 01_logistic_regression       includes evaluation-and-thresholds lab
│   │   ├── 02_knn_classification
│   │   ├── 03_svm_classification
│   │   ├── 04_naive_bayes
│   │   ├── 05_decision_tree_classifier
│   │   ├── 06_random_forest_classifier
│   │   ├── 07_adaboost_classifier
│   │   ├── 08_gradient_boosting_classifier
│   │   └── 09_xgboost_classifier
│   └── 02_regression/
│       ├── 01_linear_regression         includes Ridge / Lasso / ElasticNet
│       ├── 02_knn_regression
│       ├── 03_svm_regression
│       ├── 04_decision_tree_regressor
│       ├── 05_random_forest_regressor
│       ├── 06_adaboost_regressor
│       ├── 07_gradient_boosting_regressor
│       └── 08_xgboost_regressor
└── 02_unsupervised/
    ├── 01_kmeans_clustering
    ├── 02_hierarchical_clustering
    └── 03_cluster_evaluation_silhouette
```

## Study order

1. Linear regression module and its regularization trilogy; then its projects.
2. Logistic regression module and the evaluation lab; then its projects.
3. Classification trees and forests (`05`, `06`), followed by boosting (`07`-`09`).
4. Regression twins of whichever classifiers you liked best.
5. The unsupervised trio, finishing with the silhouette evaluation lab.

## Datasets

All training data is real and cached under `data/`: seaborn exports
(titanic, tips, penguins, mpg, iris, diamonds), sklearn sets loaded once to CSV
(breast cancer, diabetes, California housing), UCI mirrors (wine quality),
and web-hosted CSVs (heart disease, Pima diabetes, German credit, adult income,
SMS spam, mall customers). Notebooks download automatically on first run and
work offline afterwards.

## Coming next

Deep learning fundamentals, model deployment, and MLOps basics.
