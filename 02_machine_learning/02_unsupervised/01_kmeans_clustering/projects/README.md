# K-Means Clustering - Projects

**MLCourse · Machine Learning · projects/** - 3 real datasets, rising difficulty.
No labels, no accuracy score. Every project: business question -> EDA -> scale
-> choose k with elbow and silhouette -> profile the clusters -> findings AND
limitations.

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `mall_customers.csv` | own a clustering task end to end and turn the segments into concrete marketing recommendations |
| 02 | Medium | `iris.csv` | cluster blind, then use true species only post-hoc (crosstab + Adjusted Rand Index) and explain why two species merge |
| 03 | Hard | `winequality-red.csv` | 11-dimensional chemistry where the elbow gets genuinely hard to read; do chemistry-only clusters differ in measured quality? |

## Rules of engagement

- Cluster BLIND. Any ground-truth column is for evaluation only - it must never
  reach the scaler or `fit()`.
- Scale before you measure distance, and scale once so every candidate model
  sees identical coordinates.
- Justify k with evidence (elbow, silhouette), not with the answer you wanted.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.

Datasets live in the shared `02_machine_learning/data/` folder; anything missing is downloaded once on first run and cached there. Start at Project 01!
