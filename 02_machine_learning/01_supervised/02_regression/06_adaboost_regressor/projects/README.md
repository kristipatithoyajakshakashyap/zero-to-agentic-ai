# AdaBoost Regressor - Projects

**MLCourse · Machine Learning · projects/** - 3 real datasets, rising difficulty.
Boosting re-weights the examples it got wrong. Every project asks whether many
tiny trees really beat one tiny tree - and shows the round-by-round evidence.

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `diabetes.csv` | pre-standardised features and no missing values, so the only question is modelling: boosted stumps vs a single stump |
| 02 | Medium | `mpg.csv` | genuinely messy input - missing horsepower, a categorical `origin`, strong multicollinearity - with the split done FIRST |
| 03 | Hard | `california_housing.csv` (6,000-row sample) | an R2-versus-rounds curve, a learning-rate race, and a hard look at boosting's early-stop behaviour and trees' inability to extrapolate |

## Rules of engagement

- Attempt each phase before reading the next cell.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.
- Grade with the rubric in the module README one level up.

Datasets live in the shared `02_machine_learning/data/` folder; anything missing is downloaded once on first run and cached there. Start at Project 01!
