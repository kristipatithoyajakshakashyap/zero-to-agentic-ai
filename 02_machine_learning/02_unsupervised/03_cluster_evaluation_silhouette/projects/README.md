# Cluster Evaluation with Silhouette - Projects

**MLCourse · Machine Learning · projects/** - 3 real datasets, rising difficulty.
This module is about judging clusterings rather than producing them. Every
project sweeps candidates, reads the silhouette evidence, crowns a winner, and
defends the choice.

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `mall_customers.csv` | sweep k=2..10, draw side-by-side silhouette diagrams for k=3/5/7, and let the evaluation - not habit - pick the winner |
| 02 | Medium | `iris.csv` | a diagram gallery for k=2..6, then an honest explanation of why even good iris clusterings score low: overlap, not incompetence |
| 03 | Hard | `penguins.csv` | select the algorithm AND the granularity together - K-Means vs ward vs average across k=2..6 - from one 3x5 silhouette table |

## Rules of engagement

- Cluster BLIND. Any ground-truth column is for evaluation only - it must never
  reach the scaler or `fit()`.
- Scale before you measure distance, and scale once so every candidate model
  sees identical coordinates.
- Justify k with evidence (elbow, silhouette), not with the answer you wanted.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.

Datasets live in the shared `02_machine_learning/data/` folder; anything missing is downloaded once on first run and cached there. Start at Project 01!
