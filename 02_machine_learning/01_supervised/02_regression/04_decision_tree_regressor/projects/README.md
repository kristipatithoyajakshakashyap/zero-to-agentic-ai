# Decision Tree Regressor - Projects

**MLCourse · Machine Learning · projects/** - 4 real datasets, rising difficulty.
Trees predict in flat steps. Every project makes that staircase visible - in
the fitted curve, in the residuals, and in the bias-variance trade-off.

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `tips.csv` | a depth-2 tree whose `plot_tree` output you can read aloud, with its steps overlaid on the raw scatter |
| 02 | Medium | `mpg.csv` | median-imputing horsepower, one-hot encoding origin, tuning depth by CV, spotting the staircase in the residual plot |
| 03 | Hard | `insurance.csv` | a justified `log1p` target, a 2-D `max_depth` x `min_samples_leaf` grid, and dollar-scale reporting |
| 04 | Advanced | `california_housing.csv` (fixed 5,000-row sample) | build an underfit, a balanced and an overfit tree on identical data, diagnose each from train/test R2, then let cost-complexity pruning find the sweet spot |

## Rules of engagement

- Attempt each phase before reading the next cell.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.
- Grade with the rubric in the module README one level up.

Datasets live in the shared `02_machine_learning/data/` folder; anything missing is downloaded once on first run and cached there. Start at Project 01!
