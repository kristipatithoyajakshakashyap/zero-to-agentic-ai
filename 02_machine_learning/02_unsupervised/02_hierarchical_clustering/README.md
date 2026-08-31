# Hierarchical Clustering - The Complete Reference

**MLCourse · Machine Learning · unsupervised · 02_hierarchical_clustering**

Hierarchical clustering builds a **tree of clusters** (a dendrogram) instead of
one flat partition. Bottom-up *agglomerative* versions start with every point
alone and repeatedly glue the two closest clusters together until one giant
cluster remains. You then CHOOSE where to cut the tree - which means you can
look at the whole nested structure BEFORE committing to a number of clusters.
This book covers the merge logic, the linkage zoo, dendrogram reading, and the
traps.

**Contents**
1. [The idea in words](#1-the-idea-in-words-agglomerative)
2. [Linkage types](#2-linkage-types-how-is-cluster-distance-defined)
3. [Reading a dendrogram](#3-reading-a-dendrogram)
4. [Scaling is mandatory](#4-scaling-is-mandatory)
5. [When to use / when to avoid](#5-when-to-use--when-to-avoid)
6. [Key parameters](#6-key-parameters-sklearn--scipy)
7. [Common pitfalls](#7-common-pitfalls)
8. [Module map](#8-module-map)
9. [Cheat sheet](#9-cheat-sheet)

---

## 1. The idea in words (agglomerative)

```
start:  every point is its own tiny cluster (n clusters)
repeat: find the TWO CLOSEST clusters (per the linkage rule)
        merge them into one; record their distance (= merge height)
        now one fewer cluster
stop:   when a single cluster holds everything -> full tree
cut:    slice the tree horizontally at height h -> k clusters fall out
```

It is LEGO in reverse: keep snapping the nearest bricks together while writing
down at which "height" each snap happened. The recorded heights become the y-axis
of the dendrogram; longer branches = more dissimilar merges = stronger evidence
of separate groups.

>  **Why it's loved:** the tree shows ALL granularities at once - executives
> can argue about 3 macro-segments while analysts inspect 12 micro-segments
> from the same fit.

## 2. Linkage types - how is "cluster distance" defined?

Once two points become two CLUSTERS, "closest pair" is ambiguous. Each linkage
answers differently:

| Linkage | Distance between clusters A,B | Minimizes / behavior |
|---|---|---|
| `ward` (default) | increase in within-cluster variance if merged | tight, spherical, similar-size clusters - usually the best default |
| `complete` (max) | FARTHEST pair distance | minimizes cluster diameter -> compact blobs |
| `average` | MEAN over all cross pairs | compromise between complete & single |
| `single` (min) | CLOSEST pair distance | minimizes nearest-neighbour gap -> can "chain" into long snakes |

Rules of thumb: blob-shaped data -> `ward`; noisy elongated truth you want
respected -> try `average`/`complete`; avoid `single` unless you specifically
want chain-like clusters (it is the classic "chaining" failure mode).

## 3. Reading a dendrogram

```python
from scipy.cluster.hierarchy import linkage, dendrogram
Z = linkage(X_scaled, method="ward")       # Z rows = merges: [id_a, id_b, dist, size]
dendrogram(Z)                              # full tree plot
```

- Each leaf = one observation; each U = one merge event.
- **y-value of a U = the linkage distance at which those branches fused.**
- Draw a horizontal line ("cut") at height h -> the vertical lines it crosses =
  your clusters. Tall U's below your cut = robust separation; cutting through
  short U's = arbitrary grouping.
- Long vertical stretches with NO merges (big gaps between fusion heights) mark
  natural cut positions.

 Dendrograms get unreadable past a few hundred leaves - use
`truncate_mode="level", p=3` to show only the top of the tree, or
`no_labels=True`.

## 4. Scaling is mandatory

Every merge decision is a distance computation, exactly like K-Means. Raw
units with different magnitudes silently decide all merges:

```python
from sklearn.preprocessing import StandardScaler
X_scaled = StandardScaler().fit_transform(X)
```

## 5. When to use / when to avoid

 **Use hierarchical clustering when…**
- **k is unknown** and you want to see structure before choosing it
- you need a **taxonomy / nested categories** (product catalog, species,
  org-level segmentation)
- dataset is **small-to-medium** (up to a few thousand rows comfortably)
- stakeholders debate granularity - one tree serves many cuts

 **Avoid when…**
- **n is large**: naive algorithms cost O(n²) memory (distance matrix!) and
  ~O(n² log n) time - 100k rows will hurt
- you must **assign NEW points later**: `AgglomerativeClustering` has NO
  `.predict()` - the tree is built once for the data it saw (K-Means wins here)
- you need guaranteed convex, re-seedable partitions -> K-Means

## 6. Key parameters (`sklearn` + `scipy`)

### `sklearn.AgglomerativeClustering`

| Parameter | Default | Meaning |
|---|---|---|
| `n_clusters` | 2 | how many clusters after the (implicit) cut |
| `linkage` | `"ward"` | merge rule: ward / complete / average / single |
| `metric` | `"euclidean"` (was `affinity`) | distance used; ward REQUIRES euclidean |
| `distance_threshold` | None | cut by height instead of count (then `n_clusters=None`) |

### `scipy.cluster.hierarchy`

| Function | Job |
|---|---|
| `linkage(X, method, metric)` | build the merge table Z |
| `dendrogram(Z, truncate_mode, p, ...)` | draw the tree |
| `fcluster(Z, t, criterion="maxclust")` | extract flat labels: k=t clusters |

 sklearn gives labels; scipy gives the tree + flexible cuts. Pros often do
both: scipy to LOOK, sklearn to LABEL.

## 7. Common pitfalls

1. **Wrong linkage for the shape** - `single` chains noise into mega-clusters;
   `ward` shatters elongated truths. Compare linkages before believing any tree.
2. **Unscaled features** - biggest-unit column dictates every early merge.
3. **Memory blow-up** - the pairwise-distance approach is O(n²); subsample for
   big data.
4. **Cut position is a DECISION, not a discovery** - justify it (gap in merge
   heights, silhouette, business sense).
5. **No new-point assignment** - plan a workaround (nearest-centroid mapping)
   if you'll score future records.
6. **Cluster IDs arbitrary again** - same naming discipline as K-Means.

## 8. Module map

```
02_hierarchical_clustering/
├── README.md                            <- this reference book
├── 01_theory_and_mathematics.ipynb      <- merge 6 customers BY HAND + dendrogram
├── 02_model_development_workflow.ipynb  <- penguins: dendrogram, cut, sanity check
└── projects/
    ├── 01_easy_mall_dendrogram.ipynb    <- PROJECT: mall segments via ward tree
    ├── 02_medium_penguins_discovery.ipynb <- PROJECT: linkage face-off on penguins
    └── 03_hard_wine_linkages.ipynb      <- PROJECT: method x k silhouette grid
```

Datasets: Mall Customers, Penguins, Wine Quality (red).

## 9. Cheat sheet

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

Xs = StandardScaler().fit_transform(df[num_cols])       # 1. ALWAYS scale

Z = linkage(Xs, method="ward")                          # 2. merge table (scipy view)
dendrogram(Z, truncate_mode="level", p=3)               #    readable top-of-tree

labels = AgglomerativeClustering(n_clusters=3,          # 3. flat labels (sklearn)
                                 linkage="ward").fit_predict(Xs)
alt_labels = fcluster(Z, t=3, criterion="maxclust")     #    equivalent cut via scipy

sil = silhouette_score(Xs, labels)                      # 4. judge the cut
profile = df.assign(c=labels).groupby("c").mean()       # 5. interpret segments
```

| Need | One-liner |
|---|---|
| merge table | `Z = linkage(Xs, "ward")` - rows: id_a, id_b, dist, size |
| show only top levels | `dendrogram(Z, truncate_mode="level", p=3)` |
| cut at k clusters | `fcluster(Z, t=k, criterion="maxclust")` |
| cut at height h | `fcluster(Z, t=h, criterion="distance")` |
| sklearn labels only | `AgglomerativeClustering(n_clusters=k, linkage="ward").fit_predict(Xs)` |
| number of clusters in Z | `len(np.unique(labels))` or count crossings at your cut |

*Next: perform three merges with pen-and-paper numpy in
`01_theory_and_mathematics.ipynb`.*
