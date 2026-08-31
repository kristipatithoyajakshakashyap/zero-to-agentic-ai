# XGBoost Regressor - Projects

**MLCourse · Machine Learning · projects/** - 3 real datasets, rising difficulty.
The closing module of the regression track: early stopping everywhere, gain
importances, and a final look at where the model - and the data - fall down.

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `diabetes.csv` | a validation slice for early stopping, then a gain-importance audit for the clinicians |
| 02 | Medium | `insurance.csv` | `log1p` target justified by skew EDA, `expm1` back-transform, dollar metrics segmented by smoking status |
| 03 | Hard | `california_housing.csv` (all ~20k blocks) | a head-to-head on learning rate (0.05 vs 0.1) - does a smaller rate buy a better floor, and at what round cost? - plus a worst-error investigation |

## Rules of engagement

- Attempt each phase before reading the next cell.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.
- Grade with the rubric in the module README one level up.

Datasets live in the shared `02_machine_learning/data/` folder; anything missing is downloaded once on first run and cached there. Start at Project 01!
