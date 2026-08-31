# k-Nearest Neighbors (Classification) - Projects

**MLCourse · Machine Learning · projects/** - 3 real datasets, rising difficulty.
Every project: business question -> EDA -> justified prep (scaling matters
enormously here) -> tuned k -> honest evaluation -> findings.

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `iris.csv` | first distance-based classifier, stratified split, scaling inside a `Pipeline`, grid-search k & weights |
| 02 | Medium | `winequality-red.csv` (UCI, `;`-separated) | engineering a binary target from a score, noisy and collinear features, class imbalance |
| 03 | Hard | `breast_cancer.csv` (OpenML `breast-w`) | 30-feature clinical data, recall on the malignant class as the metric that matters |

## Rules of engagement

- Attempt each phase before reading the next cell.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.
- Grade with the rubric in the module README one level up.

Datasets live in the shared `02_machine_learning/data/` folder; anything missing is downloaded once on first run and cached there. Start at Project 01!
