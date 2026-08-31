# Gradient Boosting Classifier - Projects

**MLCourse · Machine Learning · projects/** - 4 real datasets, rising difficulty.
Every project: business question -> EDA -> prep -> staged tuning -> evaluation.
The recurring theme is `staged_predict`: watching the ensemble improve round by
round, and stopping when it stops.

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `titanic.csv` | can sequentially-corrected trees beat the logistic and forest baselines from earlier modules? |
| 02 | Medium | `pima.csv` | zeros-to-median plus missing flags, then choosing a threshold by screening economics |
| 03 | Hard | `german_credit.csv` | watch AUC evolve per boosting round, then price each candidate policy in dollars |
| 04 | Advanced | `adult_income.csv` (~48k rows, OpenML `adult`) | the largest tabular set in the track: mixed types, ~24% positive class, plus a fairness cut on group accuracy |

## Rules of engagement

- Attempt each phase before reading the next cell.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.
- Grade with the rubric in the module README one level up.

Datasets live in the shared `02_machine_learning/data/` folder; anything missing is downloaded once on first run and cached there. Start at Project 01!
