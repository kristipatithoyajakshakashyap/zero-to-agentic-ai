# Unsupervised Learning

**MLCourse · Machine Learning · 02_unsupervised**

No labels at all - the algorithm discovers structure on its own.

```
02_unsupervised/
├── 0_kmeans_clustering/               assign points to k group centers
├── 02_hierarchical_clustering/         build a tree of nested groups (dendrogram)
└── 03_cluster_evaluation_silhouette/   how do we KNOW clustering is any good?
```

| Module | One-liner | Use when |
|---|---|---|
| K-Means | "k centroids pull their nearest points" | you know roughly how many segments; big data |
| Hierarchical | merge/split clusters into a tree | you don't know k; want taxonomy/dendrogram |
| Silhouette lab | measure cohesion vs separation per point | choosing k; comparing clusterings |

Real datasets used: Mall Customers (classic segmentation), Iris & Penguins
(discovering known species blind), UCI Wholesale Customers.

Key habit: **always scale features before distance-based clustering**, and never
trust a clustering without a silhouette or domain sanity-check.
