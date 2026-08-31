# Hierarchical Clustering - Projects

**MLCourse · Machine Learning · projects/** - 3 real datasets, rising difficulty.
A dendrogram shows every granularity at once. Every project: scale -> build the
tree -> justify where you cut -> profile -> findings AND limitations.

| # | Difficulty | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | Easy | `mall_customers.csv` | the same segmentation as the K-Means module, but as a ward tree the CMO can argue over: 3 campaigns or 5, from one picture |
| 02 | Medium | `penguins.csv` | a controlled linkage face-off (ward vs complete vs average) judged on silhouette, then sanity-checked against species |
| 03 | Hard | `winequality-red.csv` | a systematic 3-linkage x 4-k grid on real chemistry, read as a silhouette heatmap, with the winner cut and profiled |

## Rules of engagement

- Cluster BLIND. Any ground-truth column is for evaluation only - it must never
  reach the scaler or `fit()`.
- Scale before you measure distance, and scale once so every candidate model
  sees identical coordinates.
- Justify k with evidence (elbow, silhouette), not with the answer you wanted.
- Restart kernel & run all cells before declaring victory.
- Add ONE analysis question of your own to every project.

Datasets live in the shared `02_machine_learning/data/` folder; anything missing is downloaded once on first run and cached there. Start at Project 01!
