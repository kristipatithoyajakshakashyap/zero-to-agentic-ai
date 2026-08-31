# Support Vector Regression - Projects

**MLCourse · Machine Learning · projects/** - 3 real datasets, rising difficulty.
SVR forgives small errors inside an epsilon-tube. Every project contrasts that
philosophy with squared-error thinking and shows when it pays off.

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `tips.csv` | the SVR tube vs the OLS line on one feature - two different definitions of a "good" prediction |
| 02 | Medium | `winequality-white.csv` (`;`-separated) | treating a 3-9 sensory score as a NUMBER so predictions rank batches by closeness to great |
| 03 | Hard | `insurance.csv` | a right-skewed dollar target modelled as `log1p`, then transformed back with `expm1` for honest dollar metrics |

## Rules of engagement

- Attempt each phase before reading the next cell.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.
- Grade with the rubric in the module README one level up.

Datasets live in the shared `02_machine_learning/data/` folder; anything missing is downloaded once on first run and cached there. Start at Project 01!
