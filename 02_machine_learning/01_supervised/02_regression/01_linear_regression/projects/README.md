# Linear Regression - Capstone Projects

**MLCourse · Machine Learning · projects/** - five real datasets, rising difficulty.
Each notebook: business question -> EDA -> justified preprocessing -> modeling
(scratch + sklearn where marked) -> evaluation -> assumption checks -> findings.

| # | Difficulty | Dataset | New skills spotlight |
|---|---|---|---|
| 01 |  Beginner | seaborn `tips` | dual-solver proof, dummy encoding, coefficient reading |
| 02 |  Easy | seaborn `penguins` | categorical-heavy design, controlled vs raw effects |
| 03 |  Medium | seaborn `mpg` | real missing data, collinearity insurance (RidgeCV), CV |
| 04 |  Hard | `insurance.csv` (downloaded once, cached in `02_machine_learning/data/`) | skewed target via log1p->expm1, interaction features from EDA |
| 05 |  Advanced | `fetch_california_housing` | winsorization policy, VIF, full L/N/E/I assumption audit |

## Rules of engagement

- Attempt each phase BEFORE reading the next cell's solution.
- Re-run top-to-bottom (`Kernel -> Restart & Run All`) before declaring done.
- Extend every project with ONE question of your own.
- Grade yourself with the rubric in the section README.

Datasets cache automatically: seaborn and sklearn download theirs once, and P04
caches `insurance.csv` into the shared `02_machine_learning/data/` folder.
Start at Project 01 - good luck!
