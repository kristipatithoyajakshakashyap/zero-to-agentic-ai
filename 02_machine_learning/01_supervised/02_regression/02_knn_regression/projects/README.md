# k-Nearest Neighbors (Regression) - Projects

**MLCourse · Machine Learning · projects/** - 3 real datasets, rising difficulty.
Predicting numbers by averaging the neighbors. Every project: question -> EDA
-> prep (scaling is not optional) -> tuned k and weighting -> MAE/RMSE/R2 -> findings.

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `penguins.csv` | predict body mass from non-invasive measurements, dummies for sex/species, scaling inside a `Pipeline` |
| 02 | Medium | `mpg.csv` | real missing horsepower values filled with a train-only median, correlated engine specs |
| 03 | Hard | `california_housing.csv` (6,000-block subsample) | an explicit why-scaling-is-critical proof, joint k x weights grid, and an error-by-income-segment fairness cut |

## Rules of engagement

- Attempt each phase before reading the next cell.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.
- Grade with the rubric in the module README one level up.

Datasets live in the shared `02_machine_learning/data/` folder; anything missing is downloaded once on first run and cached there. Start at Project 01!
