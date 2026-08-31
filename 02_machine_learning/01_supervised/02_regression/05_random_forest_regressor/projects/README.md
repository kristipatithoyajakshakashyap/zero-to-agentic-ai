# Random Forest Regressor - Projects

**MLCourse · Machine Learning · projects/** - 4 real datasets, rising difficulty.
Each project repeats a decision-tree project with a committee of trees, using
the same cleaning recipe so the comparison is genuinely apples-to-apples.

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `penguins.csv` | the classic head-to-head - single tree vs forest - plus permutation importances |
| 02 | Medium | `mpg.csv` | light tuning of `max_features` and leaf size; the forest's residuals should be visibly tighter than the tree's |
| 03 | Hard | `insurance.csv` | forest on a log target, with the smoker x BMI interaction showing up in permutation importances |
| 04 | Advanced | `california_housing.csv` (fixed 5,000-row sample) | a full audit: OOB curve, permutation importances, error hotspots, and a demonstration that forests cannot extrapolate |

## Rules of engagement

- Attempt each phase before reading the next cell.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.
- Grade with the rubric in the module README one level up.

Datasets live in the shared `02_machine_learning/data/` folder; anything missing is downloaded once on first run and cached there. Start at Project 01!
