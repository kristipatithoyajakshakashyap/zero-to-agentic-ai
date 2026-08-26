# Cluster Evaluation & Silhouette - The Complete Reference

**MLCourse · Machine Learning · unsupervised · 03_cluster_evaluation_silhouette**

K-Means gives you inertia; hierarchies give you trees. But how do you know a
clustering is actually GOOD - or pick between two candidate k values fairly?
The **silhouette** answers per-point: *how well does each observation fit its
own cluster compared to the next-best alternative?* This book explains the
formula, how to read it, why it beats inertia for choosing k, and where it
cheats.

**Contents**
. [The coefficient, point by point](#-the-coefficient-point-by-point)
2. [Interpretation bands](#2-interpretation-bands)
3. [Why mean-silhouette beats inertia for choosing k](#3-why-mean-silhouette-beats-inertia-for-choosing-k)
4. [The sklearn API](#4-the-sklearn-api)
5. [Reading the silhouette DIAGRAM](#5-reading-the-silhouette-diagram)
6. [When to use / when to avoid](#6-when-to-use--when-to-avoid)
7. [Common pitfalls](#7-common-pitfalls)
8. [Module map](#8-module-map)
9. [Cheat sheet](#9-cheat-sheet)

---

## . The coefficient, point by point

For each single point i:

```
a = mean distance from i to all OTHER points in ITS OWN cluster   (cohesion)
b = min over other clusters C of: mean distance from i to C       (separation)

        b − a
s(i) = ─────────      ∈ [-, +]
       max(a, b)
```

Intuition: `b − a` is "far from neighbours elsewhere" minus "close to mates at
home". Dividing by `max(a,b)` squashes it into [-, ] regardless of scale.

| Situation | a | b | s |
|---|---|---|---|
| deep inside a tight island | small | large | -> + |
| exactly on a boundary | ≈ b | ≈ a | ≈ 0 |
| nearer a foreign cluster than its own | large | small | NEGATIVE |

>  s is defined PER POINT. The "silhouette score" you usually quote is just
> the MEAN over all points - and means hide distributions (§5).

## 2. Interpretation bands

| Mean s | Verdict |
|---|---|
| 0.70 - .00 | strong structure, well separated |
| 0.50 - 0.69 | reasonable, usable |
| 0.25 - 0.49 | weak; overlap heavy - inspect diagram before shipping |
| < 0.25 | dubious; maybe wrong k, wrong algorithm, or no clusters exist |
| any negative s(i)'s | points likely MISASSIGNED - find them, don't average them away |

Bands are heuristics for tabular/scaled data; high-dimensional data lives lower.

## 3. Why mean-silhouette beats inertia for choosing k

Inertia (WCSS) **monotonically decreases** with k: add clusters, everything
gets closer to some centroid, score always improves - k=n gives zero. Useless
for fair comparison across k.

Silhouette instead REWARDS cohesion AND penalizes fragmentation: split a tight
true cluster in half and the two halves see each other across the new boundary
-> b shrinks toward a -> s drops. That built-in penalty makes scores COMPARABLE
across different k, so argmax is meaningful:

```python
scores = {k: silhouette_score(Xs, km_k.labels_) for k in range(2, )}
best_k = max(scores, key=scores.get)     # legitimate: comparable across k
```

 Still pair it with the elbow/business constraints - silhouette favors
convex blobs and can miss domain reasons to prefer fewer segments.

## 4. The sklearn API

```python
from sklearn.metrics import silhouette_score, silhouette_samples

score = silhouette_score(X_scaled, labels)        # ONE number (the mean)
samples = silhouette_samples(X_scaled, labels)    # PER-POINT array, same order as X
```

- Both accept ANY clustering (`km.labels_`, agglomerative labels, fcluster
  output…) - they only consume coordinates + labels.
- `silhouette_score(..., sample_size=0_000)` subsamples big data.
- Works for evaluating TRUE labels too (e.g., species): measures how
  geometrically coherent the given partition is.

## 5. Reading the silhouette DIAGRAM

The classic diagnostic (built manually in our notebooks with `plt.barh`):

```
cluster  | ████████████████
          | █████████████              <- sorted s(i) bars, one per point
          | ████
          | ┆ dashed line = cluster MEAN s
cluster 2 | ██████████████████████
          | ██████
          | ██  <- short/negative tail = misfit members
          |─────── red line = GLOBAL mean s ───────
```

Healthy diagram: wide bands of similar thickness, cluster-mean lines near the
global mean, tails rarely negative. Unhealthy: razor-thin bands (over-fragmented
k), wildly unequal widths (one mega-cluster), long negative tails (badly placed
members).

## 6. When to use / when to avoid

 **Use silhouette when…**
- choosing k among candidates (fairer than inertia)
- comparing ALGORITHMS on the same data (K-Means vs ward vs …)
- hunting misassigned points via `silhouette_samples` < 0
- validating an unsupervised segmentation before deployment

 **Avoid / distrust when…**
- n is huge without sampling - cost is **O(n²)** distances (50 points fine;
  M rows painful)
- truth is non-convex (rings, moons) - silhouette structurally prefers convex
  cuts and will slander DBSCAN's snake clusters
- clusters are expected to be very unequal in size/density
- you need domain meaning - geometry score ≠ business value

## 7. Common pitfalls

. **Trusting the mean alone** - a 0.55 can hide half great / half terrible.
   Always draw the diagram.
2. **O(n²) amnesia** - computing it on millions of rows will melt your laptop;
   use `sample_size`.
3. **Convexity bias** - rings/moons score badly even when clustered PERFECTLY.
4. **Comparing scores across DIFFERENT scalings/features** - silhouettes are
   only comparable on identical coordinate systems.
5. **Maximizing into over-simplification** - k=2 often wins mechanically;
   weigh usefulness, not just the number.
6. **Negative samples ignored** - they're the most informative rows you have.

## 8. Module map

```
03_cluster_evaluation_silhouette/
├── README.md                            <- this reference book
├── 0_theory_and_mathematics.nb.py      <- compute s(i) BY HAND for 5 iris flowers
├── 02_model_development_workflow.nb.py  <- elbow+silhouette combo, diagrams k=5/k=2
├── 0_easy_mall_ksweep.nb.py            <- PROJECT: sweep k, diagram k=3/5/7
├── 02_medium_iris_diagrams.nb.py        <- PROJECT: honest low scores explained
└── 03_hard_penguins_compare.nb.py       <- PROJECT: k AND algorithm selection
```

Datasets: Mall Customers, Iris, Penguins.

## 9. Cheat sheet

```python
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.cluster import KMeans

Xs = StandardScaler().fit_transform(df[num_cols])       # same coords for all trials!
rows = []
for k in range(2, ):
    lab = KMeans(n_clusters=k, n_init=0, random_state=42).fit_predict(Xs)
    rows.append((k, silhouette_score(Xs, lab)))         # comparable across k
best_k = max(rows, key=lambda t: t[])[0]

samples = silhouette_samples(Xs, final_labels)          # per-point diagnosis
worst = df.loc[samples.argsort()[:0]]                  # 0 least-at-home points
neg_share = (samples < 0).mean()                        # % likely misassigned
```

| Need | One-liner |
|---|---|
| one quality number | `silhouette_score(Xs, labels)` |
| per-point scores | `silhouette_samples(Xs, labels)` |
| share of bad assignments | `(silhouette_samples(...) < 0).mean()` |
| evaluate true labels' coherence | same calls with true labels |
| fast on big data | `silhouette_score(Xs, labels, sample_size=0_000, random_state=42)` |
| diagram data | sort `samples` within each label, plot `barh` |

*Next: hand-compute five flowers' silhouettes in
`0_theory_and_mathematics.nb.py`.*
