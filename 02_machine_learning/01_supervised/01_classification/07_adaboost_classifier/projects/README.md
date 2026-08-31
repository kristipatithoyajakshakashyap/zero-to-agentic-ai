# AdaBoost Classifier - Projects

**MLCourse · Machine Learning · projects/** - 3 real datasets, rising difficulty.
Every project: fit hundreds of re-weighted stumps, then ask the honest
question - did sequential correction actually beat the simpler model?

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `penguins.csv` | three-way benchmark against the single tree and the random forest on an identical split |
| 02 | Medium | `heart.csv` | tuning learning rate x rounds while scoring on RECALL rather than accuracy, so the search optimizes the clinical goal |
| 03 | Hard | `pima.csv` | boosted stumps on data with hidden zeros-as-missing, threshold sweep, delivered screening operating point |

## Rules of engagement

- Attempt each phase before reading the next cell.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.
- Grade with the rubric in the module README one level up.

Datasets live in the shared `02_machine_learning/data/` folder; anything missing is downloaded once on first run and cached there. Start at Project 01!
