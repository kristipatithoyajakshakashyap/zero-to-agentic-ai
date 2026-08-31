# Naive Bayes - Projects

**MLCourse · Machine Learning · projects/** - 3 real datasets, rising difficulty.
Every project: business question -> EDA -> prep -> fit (which is just counting)
-> evaluation -> findings. The fastest honest baseline in machine learning.

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `titanic.csv` | `GaussianNB` on continuous features, impute + encode, measured against a lazy baseline |
| 02 | Medium | `sms.tsv` | `MultinomialNB` on Bag-of-Words counts, alpha smoothing sweep, precision-first spam policy, readable token table |
| 03 | Hard | 20 Newsgroups (fetched by scikit-learn) | TF-IDF features, four-way routing, multiclass confusion matrix, per-topic vocabularies |

## Rules of engagement

- Attempt each phase before reading the next cell.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.
- Grade with the rubric in the module README one level up.

Projects 01 and 02 read from `02_machine_learning/data/`. Project 03 uses
scikit-learn's own downloader, which caches under `~/scikit_learn_data` after the
first pull. Start at Project 01!
