# Gradient Boosting Regressor - Projects

**MLCourse · Machine Learning · projects/** - 4 real datasets, rising difficulty.
Each tree fits the previous ensemble's residuals. The recurring tool here is
the staged API, which tells you exactly how many trees were enough.

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `diabetes.csv` | a three-way split so `staged_predict` can pick the round count honestly |
| 02 | Medium | `winequality-white.csv` | quality as a regression target, honest baselines, and the lab measurements that drive taste |
| 03 | Hard | `insurance.csv` | encoding inside a leak-proof `Pipeline`, staged round selection, dollar metrics, and a smoker x BMI partial-dependence read |
| 04 | Advanced | `california_housing.csv` | staged early stopping, a controlled `subsample` experiment, and an error-hotspot audit |

## Rules of engagement

- Attempt each phase before reading the next cell.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.
- Grade with the rubric in the module README one level up.

Datasets live in the shared `02_machine_learning/data/` folder; anything missing is downloaded once on first run and cached there. Start at Project 01!
