# K-Means Clustering - The Complete Reference

**MLCourse · Machine Learning · unsupervised · 01_kmeans_clustering**

K-Means is THE workhorse of unsupervised learning: give it a number `k`, and it
partitions your data into `k` groups by repeatedly pulling group centers toward
the middle of the points they own. No labels, no training targets - just
geometry. This book explains the loop in words, the math behind it, how to pick
`k`, and every trap waiting for beginners.

**Contents**
1. [The idea in words](#1-the-idea-in-words)
2. [The objective: inertia / WCSS](#2-the-objective-inertia--wcss)
3. [Choosing k: the elbow method](#3-choosing-k-the-elbow-method)
4. [k-means++ seeding](#4-k-means-seeding-k-meansinit)
5. [Scaling is mandatory](#5-scaling-is-mandatory)
6. [When to use / when to avoid](#6-when-to-use--when-to-avoid)
7. [Key parameters](#7-key-parameters-sklearnkmeans)
8. [Common pitfalls](#8-common-pitfalls)
9. [Module map](#9-module-map)
10. [Cheat sheet](#10-cheat-sheet)

---

## 1. The idea in words

K-Means runs a **pull-and-reassign** loop until nothing moves anymore:

```
1. PLACE     drop k centroids into the data (randomly, or smartly - see §4)
2. ASSIGN    every point joins the NEAREST centroid (Euclidean distance)
3. UPDATE    each centroid slides to the MEAN of the points that joined it
4. REPEAT    go to step 2 until assignments stop changing (or max_iter hit)
```

Think of k magnets scattered on a table of iron filings: filings snap to the
closest magnet, each magnet drifts to the balance point of its pile, and piles
re-snap. After a few rounds the magnets settle and the piles ARE your clusters.

>  **Why it works:** every step strictly DECREASES the objective in §2, so
> the loop is guaranteed to converge - but possibly to a *local* optimum
> (see pitfall #1).

## 2. The objective: inertia / WCSS

K-Means minimizes **Within-Cluster Sum of Squares** (a.k.a. inertia):

```
WCSS  =  Σ_c  Σ_{i ∈ cluster c}  ‖ x_i − μ_c ‖²

      μ_c  = mean (centroid) of cluster c
      ‖·‖  = Euclidean distance
```

In words: *how tightly does each point hug its own centroid?* Lower = tighter,
more coherent clusters. `sklearn` exposes it as `km.inertia_`.

>  **Inertia always falls as k grows** - with k = n you get WCSS = 0 (every
> point IS a centroid). That is why raw inertia can never tell you the "right"
> k on its own; see the silhouette module for a fairer judge.

## 3. Choosing k: the elbow method

Plot WCSS against k = 1, 2, 3, … Each added cluster buys less improvement;
the curve bends like an arm. Pick the k at the **elbow** - the point where
adding another cluster stops paying rent.

```python
wcss = [KMeans(n_clusters=k, n_init=10, random_state=42).fit(X).inertia_
        for k in range(1, 11)]
```

Rules of thumb:

| Signal | Meaning |
|---|---|
| steep drop then flattening | elbow - good candidate |
| no visible elbow | data may not be k-means-shaped; try silhouette |
| elbow ambiguous (two candidates) | prefer smaller k unless business value differs |

Pair the elbow with **mean silhouette** (module 03) whenever possible.

## 4. k-means++ seeding (`init="k-means"`)

Random placement can start two centroids in the same blob and split it, while
another blob gets none - a bad local optimum. **k-means++** fixes the odds:
it places the first centroid randomly, then places each NEXT centroid far from
the ones already placed (probability ∝ squared distance). It is sklearn's
default (`init="k-means++"`) and usually worth keeping.

## 5. Scaling is mandatory

K-Means measures Euclidean distance, so a feature measured in large units
(e.g., salary 10,000-100,000) will drown one measured in small units
(e.g., age 18-70). Distance becomes "whoever has the biggest unit wins."

```python
from sklearn.preprocessing import StandardScaler
X_scaled = StandardScaler().fit_transform(X)   # mean 0, std 1 per feature
```

>  **Unscaled K-Means is the #1 beginner bug.** If one feature dominates
> every distance, your "clusters" are really just slices of that one feature.

## 6. When to use / when to avoid

 **Use K-Means when…**
- customer/product/user **segmentation** (the classic marketing play)
- **big n** - fast, scales linearly, `MiniBatchKMeans` for huge data
- clusters are roughly **round, similar-sized blobs** in scaled space
- you need a **simple, explainable** model (centroid = segment prototype)

 **Avoid K-Means when…**
- **unknown k with no elbow** - you must supply k somehow
- **non-convex shapes** (moons, rings, spirals) - K-Means only cuts straight
  Voronoi boundaries; use DBSCAN / spectral instead
- clusters have very different sizes/densities - big blobs swallow small ones
- you need hierarchy/taxonomy -> hierarchical clustering (module 02)

## 7. Key parameters (`sklearn.KMeans`)

| Parameter | Default | What it does | Typical setting |
|---|---|---|---|
| `n_clusters` | 8 | k - number of centroids | from elbow/silhouette/business |
| `init` | `"k-means++"` | seeding strategy; array = exact start points | keep default; array for teaching/repro |
| `n_init` | 10 | independent restarts; best inertia wins | ≥ 10 (older defaults were riskier) |
| `max_iter` | 300 | Lloyd iterations per restart | 300 is plenty; raise for stubborn data |
| `random_state` | None | seed for reproducible runs | fix it (42 in this course) |
| `tol` | 1e-4 | convergence threshold on centroid shift | rarely touched |

Handy attributes after `fit`: `labels_` (cluster per point), `cluster_centers_`,
`inertia_` (WCSS), `n_iter_`.

## 8. Common pitfalls

. **Local optima** -> different seeds, different clusters. Fix: `n_init≥10`
   (sklearn keeps the best-inertia run) and a fixed `random_state`.
2. **No feature scaling** -> distances hijacked by the biggest-unit column (§5).
3. **Interpreting clusters as ground truth** -> clusters are GEOMETRY, not
   reality. Validate with silhouette, business sense, or known labels as a
   sanity check - never treat them as proven categories.
4. **Reading only inertia** -> monotone decreasing; useless alone for choosing k.
5. **Forgetting K-Means assumes convexity** -> always eyeball a 2-D projection
   of the final clustering before shipping it.
6. **Cluster IDs are arbitrary** -> rerun and `3` becomes `0`; never hardcode
   meanings to IDs, map through a named profile table.

## 9. Module map

```
01_kmeans_clustering/
├── README.md                            <- you are here (reference book)
├── 01_theory_and_mathematics.ipynb      <- Lloyd's loop BY HAND + elbow (mall)
├── 02_model_development_workflow.ipynb  <- full scaled workflow + profiles (mall)
└── projects/
    ├── 01_easy_mall_segments.ipynb      <- PROJECT: classic 5-segment story
    ├── 02_medium_iris_blindfolded.ipynb <- PROJECT: rediscover iris w/o labels
    └── 03_hard_wine_red_chemistry.ipynb <- PROJECT: do chemistry clusters track quality?
```

Datasets (auto-downloaded to `02_machine_learning/data/`): Mall Customers,
Iris, Wine Quality (red).

## 10. Cheat sheet

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

Xs = StandardScaler().fit_transform(df[num_cols])          # 1. ALWAYS scale
wcss, sils = [], []
for k in range(2, 11):                                     # 2. sweep k
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(Xs)
    wcss.append(km.inertia_)                               #    elbow fuel
    sils.append(silhouette_score(Xs, km.labels_))          #    silhouette fuel

km = KMeans(n_clusters=5, n_init=10, random_state=42).fit(Xs)   # 3. final fit
df["cluster"] = km.labels_

profile = (df.groupby("cluster")                                  # 4. profile
             .agg(size=("cluster", "size"),
                  income=("income", "mean"),
                  spend=("spend", "mean"))
             .round(1))
```

| Need | One-liner |
|---|---|
| cluster per point | `km.labels_` |
| centroid coordinates | `km.cluster_centers_` |
| WCSS | `km.inertia_` |
| assign NEW points | `km.predict(Xs_new)` |
| centroids back to units | `scaler.inverse_transform(km.cluster_centers_)` |
| one-number quality | `silhouette_score(Xs, km.labels_)` |
| reproducible run | `random_state=42, n_init=10` |

*Next: watch Lloyd's loop crawl in `01_theory_and_mathematics.ipynb` - by hand.*
