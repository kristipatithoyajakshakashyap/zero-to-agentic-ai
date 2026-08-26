# Seaborn - The Complete Reference (Module 04)

> **MLCourse · Data Science Foundations · 04_seaborn**
> A standalone reference for statistical visualization with seaborn: the two-level API, every plot family with when-to-use guidance, palettes, theming, matplotlib interop, and a one-page cheat sheet.

Companion notebooks in this folder:

| File | Contents |
|---|---|
| `01_seaborn_foundations.nb.py` | Philosophy, themes, relational/distributional/categorical basics, palettes |
| `02_seaborn_advanced.nb.py` | Regression, heatmaps & clustering, joint/pair grids, FacetGrid masterclass, interop, saving |
| `03_seaborn_exercises.nb.py` | 12 graded challenges (4 Easy / 5 Medium / 3 Hard), no answers |
| `04_seaborn_solutions.nb.py` | Fully commented standalone solutions |

---

## Table of contents

1. [Mental model](#1-mental-model)
2. [The two-level API](#2-the-two-level-api)
3. [Setup conventions](#3-setup-conventions)
4. [Relational family](#4-relational-family)
5. [Distributional family](#5-distributional-family)
6. [Categorical family](#6-categorical-family)
7. [Regression family](#7-regression-family)
8. [Matrix family](#8-matrix-family)
9. [Grids: FacetGrid, PairGrid, JointGrid](#9-grids-facetgrid-pairgrid-jointgrid)
10. [Palette guide](#10-palette-guide)
11. [Styling and theming guide](#11-styling-and-theming-guide)
12. [Matplotlib interop recipes](#12-matplotlib-interop-recipes)
13. [Saving and exporting](#13-saving-and-exporting)
14. [Performance and etiquette](#14-performance-and-etiquette)
15. [Cheat sheet](#15-cheat-sheet)

---

## 1. Mental model

Seaborn is a **dataset-oriented** interface on top of matplotlib:

```python
import seaborn as sns
sns.set_theme()                      # do this ONCE, near the top
ax = sns.scatterplot(data=tips, x="total_bill", y="tip", hue="time")
```

Three commitments define it:

- **Pass DataFrames + column names**, not arrays. Labels, legends, and axis
  titles come from your columns automatically.
- **Statistics are built in.** Repeated y-values get averaged with bootstrap
  confidence bands (`lineplot`, `barplot`); fits come with uncertainty
  (`regplot`); distributions estimate densities honestly (`kdeplot`).
- **Defaults look good.** Themes and perceptually-uniform palettes mean the
  gap between "quick look" and "report-ready" is a few parameters.

Seaborn does not replace matplotlib - every seaborn call returns or populates
real matplotlib artists, so matplotlib knowledge remains fully applicable.

## 2. The two-level API

This is the single most important structural fact about seaborn.

### Axes-level functions

Return a single matplotlib `Axes`. They accept an existing axes via `ax=`,
compose into arbitrary subplot grids, and never create figures themselves.

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
sns.boxplot(data=tips, x="day", y="tip", ax=axes[0])
sns.violinplot(data=tips, x="day", y="tip", ax=axes[1])
```

### Figure-level functions

Own their entire figure (a seaborn `FacetGrid` object). They ignore `ax=`,
create a new window on each call, and provide native faceting via `col=`/`row=`.

```python
g = sns.catplot(data=tips, kind="bar",
                x="day", y="tip", col="time", height=3)
g.figure.suptitle("Faceted in one call", y=1.03)
```

### Function table

| Family | Axes-level | Figure-level | Figure-level superpower |
|---|---|---|---|
| Relational | `scatterplot`, `lineplot` | `relplot` | `hue`/`size`/`style` + `col`/`row` facets |
| Distributional | `histplot`, `kdeplot`, `ecdfplot`, `rugplot` | `displot` | stacked/filled/faceted distributions |
| Categorical | `stripplot`, `swarmplot`, `boxplot`, `violinplot`, `boxenplot`, `pointplot`, `barplot`, `countplot` | `catplot` | `kind=` switch + facets |
| Regression | `regplot`, `residplot` | `lmplot` | per-facet fits |
| Matrix | `heatmap` | `clustermap` | dendrograms |
| Grids | - | `jointplot`, `pairplot`, `FacetGrid`, `PairGrid`, `JointGrid` | composite multi-panel layouts |

Decision rule: **faceting or quick exploration → figure-level; custom layout,
dashboards, layered panels → axes-level.**

## 3. Setup conventions

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

sns.set_theme()                                  # style + context + palette at once

tips = sns.load_dataset("tips")                  # wrap in try/except offline!
```

Built-in practice datasets used throughout this module: `tips`, `titanic`,
`penguins`, `mpg`, `flights`, `iris`, `diamonds`.

## 4. Relational family

Question answered: **how do numeric variables relate, conditionally on others?**

### scatterplot / relplot(kind="scatter")

```python
sns.scatterplot(data=mpg, x="horsepower", y="mpg",
                hue="origin",            # color by category
                size="weight",           # area by magnitude
                style="origin",          # marker shapes survive grayscale
                alpha=0.7, palette="colorblind")
```

When to use: moderate n (< ~2000 points), group separation, outlier spotting.
Beyond that: hexbin/jointplot, or sample.

### lineplot / relplot(kind="line")

Aggregates repeated y per x into a mean plus a **95% bootstrap CI band**.

```python
sns.lineplot(data=readings, x="day", y="value")          # band appears if repeats exist
sns.lineplot(data=df, x="day", y="value",
             errorbar=("sd", 2), err_style="bars")       # spread instead of CI
sns.lineplot(data=df, x="day", y="value", errorbar=None) # raw lines, fast
```

Error-bar spec tuples: `("ci", 95)`, `("pi", 90)` (percentile interval),
`("sd", k)`, `("se", k)`. One observation per x ⇒ no band (nothing to aggregate).

When to use: trends over ordered x (time, dose, year). Aggregate upstream first
if x values are dense.

## 5. Distributional family

Question answered: **what does one variable's distribution look like?**

### histplot

```python
sns.histplot(data=penguins, x="body_mass_g", bins=30,
             kde=True, hue="species", multiple="layer")
```

Knobs: `bins`/`binwidth`, `stat` (`"count"`, `"density"`, `"probability"`),
`element` (`"bars"`, `"step"`, `"poly"`), `multiple`
(`"layer"`, `"stack"`, `"fill"`, `"dodge"`), `common_norm=False` to compare
group shapes fairly. Always try 2-3 bin widths before trusting a shape.

### kdeplot

```python
sns.kdeplot(data=penguins, x="body_mass_g", bw_adjust=1, cut=0, fill=True)
sns.kdeplot(data=penguins, x="bill_length_mm", y="bill_depth_mm",
            fill=True, cmap="crest", levels=10)
```

`bw_adjust < 1` wigglier, `> 1` smoother; `cut=0` stops invented tails on
bounded quantities. 2-D form gives topographic density contours.

### ecdfplot

```python
sns.ecdfplot(data=penguins, x="body_mass_g", hue="species")
```

No tuning parameters; y at any x IS "fraction of data below x". Ideal for
threshold/SLA questions and clean group overlays.

### rugplot

One tick per observation along an edge; layer onto ECDF/KDE for raw-data texture.

### displot (figure-level)

Wraps all of the above with `kind=` and facet support (`col=`, `row=`).

## 6. Categorical family

Question answered: **how does a distribution or aggregate compare across groups?**

| Function | Shows | Use when |
|---|---|---|
| `stripplot` | jittered raw points | n small-medium, show evidence |
| `swarmplot` | non-overlapping points | n ≤ ~2000/category; shape for free |
| `boxplot` | median, IQR, whiskers (1.5×IQR), fliers | robust summary; small multiples |
| `violinplot` | mirrored KDE (+ `inner=`) | n ≥ ~50/group, shape matters |
| `boxenplot` | nested letter-value boxes | large n, tail structure |
| `countplot` | row frequencies | category sizes |
| `barplot` | mean (default) + bootstrap CI | aggregated comparisons |
| `pointplot` | estimates joined within `hue` | interactions (parallel-lines test) |

Essentials:

```python
order = tips["day"].value_counts().index              # frequency ordering trick
sns.countplot(data=tips, x="day", order=order)

sns.barplot(data=tips, x="day", y="tip",
            estimator=np.median, errorbar=("sd", 1))  # legacy ci= -> errorbar=("ci",95)

sns.pointplot(data=tips, x="day", y="tip", hue="smoker", dodge=0.35)
```

Power combo - context + evidence on one axes:

```python
ax = sns.violinplot(data=tips, x="day", y="tip", inner=None, color="#dddddd")
sns.swarmplot(data=tips, x="day", y="tip", size=3, color="#333333", ax=ax)
```

Bar-chart honesty: bars start at 0 (seaborn enforces this for length encodings);
label whether error bars are CI-of-mean or SD-of-data.

## 7. Regression family

Question answered: **what is the trend, how sure are we, and what did we miss?**

### regplot (axes-level)

```python
sns.regplot(data=tips, x="total_bill", y="tip",
            order=2,                       # polynomial curvature
            logistic=True,                 # binary y S-curve (with y_jitter=.03)
            logx=True,                     # straightens power-law-ish skewed x
            ci=None,                       # skip bootstrap band: fast exploration
            scatter_kws={"alpha": .4}, line_kws={"color": "crimson"})
```

`robust=True` downweights outliers (slower). CI band = bootstrapped fit
uncertainty, not data spread.

### lmplot (figure-level)

Per-facet/per-hue fits in one call:

```python
g = sns.lmplot(data=mpg, x="horsepower", y="mpg", col="origin", hue="origin",
               height=3.2, scatter_kws={"alpha": .5})
```

Check per-facet counts before trusting slopes on thin groups.

### residplot

Residuals = signal left behind. Flat zero-centered noise = good model;
curvature → raise `order`; funnel → transform y; waves → missing predictor.

```python
sns.residplot(x=x_observed, y=y_observed, lowess=True)
```

## 8. Matrix family

Question answered: **what structure lives in a rows × columns numeric table?**

### heatmap

```python
corr = penguins[num_cols].corr(numeric_only=True)
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)

sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
            annot_kws={"fontsize": 9}, linewidths=.5, linecolor="white",
            cmap="vlag", center=0, vmin=-1, vmax=1, square=True)
```

Rules: diverging cmaps need a meaningful `center` (0 for correlations);
sequential cmaps for magnitudes; mask symmetric matrices; pin `vmin/vmax`.
Extract insights programmatically too (`corr.stack().sort_values()`).

### clustermap

Heatmap + hierarchical clustering dendrograms on rows/columns:

```python
sns.clustermap(iris_sample.iloc[:, :4], cmap="mako",
               row_colors=labels.map(palette_dict), figsize=(7, 6))
```

Standardize mixed-unit features first (`standard_scale=1` or `z_score=1`) so
large units don't dominate distances.

## 9. Grids: FacetGrid, PairGrid, JointGrid

### jointplot - bivariate + marginals

```python
sns.jointplot(data=diamonds_sample, x="carat", y="price",
              kind="hex", marginal_ticks=True, joint_kws={"gridsize": 30})
```

`kind=` ∈ `scatter` (default), `kde`, `hex` (big n), `reg`, `resid`.
Marginals answer "is the cluster difference along x, y, or both?"

### pairplot - scatterplot matrix

```python
sns.pairplot(penguins, vars=num_cols, hue="species",
             diag_kind="kde", corner=True,
             plot_kws={"s": 18, "alpha": .65})
```

`corner=True` halves panels beyond ~5 variables; `diag_kind="hist"` for counts.

### PairGrid - bespoke matrices

Different plot per triangle:

```python
pg = sns.PairGrid(penguins, vars=num_cols, hue="species", diag_sharey=False)
pg.map_diag(sns.kdeplot, fill=True, common_norm=False)
pg.map_upper(sns.scatterplot, s=12, alpha=.55)
pg.map_lower(sns.regplot, scatter=False)
pg.add_legend()
```

### FacetGrid - full manual control

```python
def mark_mean(data, y, **kws):
    ax = plt.gca()
    ax.axhline(data[y].mean(), ls="--", color="crimson")

g = sns.FacetGrid(tips, row="time", col="sex",
                  margin_titles=True, height=2.8, aspect=1.3,
                  sharex=True, sharey=True)
g.map_dataframe(sns.scatterplot, x="total_bill", y="tip", alpha=.55)
g.map_dataframe(mark_mean, y="tip")
g.refline(y=tips["tip"].mean(), color="gray", ls=":")
g.set_titles(row_template="{row_name}", col_template="{col_name}")
g.add_legend()
```

Contract for mapped functions: receive the facet's data subset, draw on the
current axes. Free scales via `sharex/sharey=False` (warn readers!),
reflow with `col_wrap=n`, individual facets via `g.axes_dict`.

## 10. Palette guide

Choose color by *meaning*:

### Qualitative - categories without order

| Name | Character |
|---|---|
| `deep` | seaborn default, balanced saturation |
| `muted` | deep, slightly desaturated |
| `pastel` | light, low-saturation fills |
| `bright` | punchy, high contrast |
| `dark` | muted-dark, good on white |
| `colorblind` | Okabe-Ito-style safe set - default for public work |
| `Set2` / `tab10` | classic categorical standards |

### Sequential - ordered magnitude

| Name | Character |
|---|---|
| `rocket`, `mako`, `flare`, `crest` | seaborn signature ramps |
| `viridis` | perceptually uniform classic |
| `Blues` / `Greens` | single-hue, print-friendly |
| `cubehelix` | grayscale-safe spiral ramp |

### Diverging - deviation around a midpoint

| Name | Character |
|---|---|
| `vlag` | blue↔red, seaborn-tuned |
| `RdBu_r` / `coolwarm` | scientific standard red-blue |
| `Spectral` | multihue diverging |
| `icefire` | dark-centered dramatic option |

Usage patterns:

```python
sns.color_palette("deep")                        # list of RGB tuples
sns.color_palette("viridis", as_cmap=True)       # colormap object for heatmaps/KDE
sns.palplot(sns.color_palette("colorblind"))     # preview swatches

sns.barplot(..., palette="flare")                # per-call (preferred)
sns.set_palette("colorblind")                    # global until changed back
sns.diverging_palette(220, 20, as_cmap=True)     # custom diverging build
```

Accessibility: ~1 in 12 men has color-vision deficiency; avoid red/green pairs
and rainbow maps - make `"colorblind"` your public default.

## 11. Styling and theming guide

### Styles (background furniture)

| Style | Look | Typical use |
|---|---|---|
| `darkgrid` | gray bg + white grid (default) | exploration |
| `whitegrid` | white bg + light grid | value reading on print |
| `dark` | charcoal bg | dashboards |
| `white` | bare white | minimal reports |
| `ticks` | white + ticks only | publication, pair with `despine` |

```python
sns.set_theme(style="ticks")
sns.despine(offset=10, trim=True)
```

### Contexts (font/line scaling)

`paper` < `notebook` < `talk` < `poster` - same chart, scaled for destination.

```python
with sns.plotting_context("talk"):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=tips, x="day", y="tip", ax=ax)
```

### Persistent fine-tuning via rc

```python
sns.set_theme(style="white",
              rc={"axes.spines.top": False, "axes.spines.right": False,
                  "figure.dpi": 110})
```

Remember: `set_theme()` resets style + context + palette together; reapply
targeted tweaks after calling it.

## 12. Matplotlib interop recipes

Everything seaborn draws is matplotlib - so these all just work:

**Recipe 1 - annotate a seaborn axes afterwards**

```python
ax = sns.histplot(data=tips, x="total_bill", bins=30)
ax.annotate("long right tail", xy=(46, 8), xytext=(30, 40),
            arrowprops=dict(arrowstyle="->", color="crimson"))
```

**Recipe 2 - resize figure-level output after creation**

```python
g = sns.relplot(data=tips, x="total_bill", y="tip", hue="time", height=3.5)
g.figure.set_size_inches(9, 3.6)        # modern accessor (legacy: g.fig)
```

**Recipe 3 - correct titling levels**

```python
ax.set_title("panel title")              # one axes-level panel
g.figure.suptitle("whole grid title")   # FacetGrid window
```

**Recipe 4 - move any legend**

```python
sns.move_legend(ax, "upper left", frameon=False)
sns.move_legend(g, "lower center", bbox_to_anchor=(0.5, -0.08), ncol=3)
```

**Recipe 5 - mix engines on one canvas**

```python
fig, ax = plt.subplots()
sns.kdeplot(data=bill, x="bill_length_mm", y="bill_depth_mm",
            fill=True, cmap="crest", ax=ax)
ax.scatter(sub.x, sub.y, s=10, c="k", alpha=.4)   # raw mpl on seaborn axes
```

**Recipe 6 - reach individual facets of a grid**

```python
g.axes_dict["Dinner"]            # dict keyed by facet variable
g.axes                           # numpy array of Axes
```

## 13. Saving and exporting

```python
fig.savefig("chart.png", dpi=150, bbox_inches="tight")   # axes-level path
g.savefig("facets.svg")                                   # figure-level path
```

- `dpi=150` screens/slides · `dpi=300` print · `svg`/`pdf` vector for reports.
- `bbox_inches="tight"` crops whitespace; `transparent=True` drops background.
- Set once globally: `sns.set_theme(rc={"savefig.dpi": 200})`.

## 14. Performance and etiquette

1. **Sample reproducibly**: `diamonds.sample(5000, random_state=42)` looks like
   54k rows at a fraction of the cost.
2. **Explore without CIs**: `ci=None` / `errorbar=None` removes the expensive
   bootstrap; restore for finals.
3. **Cost curves**: KDE ≈ O(n·grid²)/dim; swarm ≈ quadratic - no swarms past a
   few thousand points/category.
4. **Close windows**: `plt.close("all")` inside exploration loops caps memory.
5. **Label uncertainty**: say whether bars/bands show CI-of-mean or SD-of-data.
6. **Order categories from data** (`value_counts().index` or sorted groupby),
   never alphabetically-by-accident.

### Pitfall gallery

| Pitfall | Symptom | Fix |
|---|---|---|
| Calling `set_theme()` mid-notebook | earlier styling silently reverts | call once at top; tweak via `axes_style`/`plotting_context` context managers afterwards |
| Trusting one bin width | histogram shape changes wildly | try 2-3 `binwidth` values; prefer ECDF for threshold claims |
| KDE beyond reality | density below zero for prices/masses | `cut=0` on bounded quantities |
| Violin on tiny groups | invented shapes from smoothing | n < ~50/group → boxplot or strip/swarm |
| Swarm on big data | minutes-long render, failed placement | sample first or switch to strip/hex |
| Reading bar error bars as spread | overconfident group comparisons | they are bootstrap CIs of the mean; label them |
| Rainbow/jet colormap | fake visual boundaries | sequential (`viridis`, `crest`) or diverging with real center |
| Diverging scale without `center=` | midpoint lands on arbitrary value | pass `center=0` (or grand median) explicitly |
| Unmasked correlation matrix | duplicated triangles waste attention | `mask=np.triu(np.ones_like(corr, bool), k=1)` |
| Figure-level call expecting `ax=` | confusing errors / stray windows | figure-level owns its figure; use axes-level for grids |
| Facets with free scales | silent incomparable panels | `sharey=False` only with a caption warning |
| Regression on thin facets | wild slopes from n=8 groups | check `value_counts()` per facet first |

## 15. Cheat sheet

| Task | One-liner |
|---|---|
| Quick theme reset | `sns.set_theme()` |
| Scatter with groups | `sns.scatterplot(df, x=, y=, hue=)` |
| Trend + CI band | `sns.lineplot(df, x=, y=)` |
| Histogram + smooth overlay | `sns.histplot(df, x=, bins=30, kde=True)` |
| Smooth density, bounded data | `sns.kdeplot(df, x=, cut=0, fill=True)` |
| Fraction-below-threshold | `sns.ecdfplot(df, x=, hue=)` |
| Grouped box summary | `sns.boxplot(df, x=cat, y=num)` |
| Density by group, split halves | `sns.violinplot(df, x=, y=, hue=bin, split=True)` |
| Large-n quantiles | `sns.boxenplot(df, x=, y=)` |
| Raw points, no overlap | `sns.swarmplot(df, x=, y=, size=3)` |
| Category frequencies | `sns.countplot(df, x=cat, order=value_counts().index)` |
| Group means + CI | `sns.barplot(df, x=cat, y=num, errorbar=("ci", 95))` |
| Interaction check | `sns.pointplot(df, x=a, y=num, hue=b)` |
| Linear fit + band | `sns.regplot(df, x=, y=)` |
| Fit diagnostics | `sns.residplot(df, x=, y=, lowess=True)` |
| Per-group fits, faceted | `sns.lmplot(df, x=, y=, col=g, hue=g)` |
| Correlation matrix, masked | `sns.heatmap(corr, mask=triu, annot=True, center=0)` |
| Clustered matrix | `sns.clustermap(matrix, cmap="mako")` |
| Bivariate + marginals | `sns.jointplot(df, x=, y=, kind="hex")` |
| All-pairs matrix | `sns.pairplot(df, vars=v, hue=g, corner=True)` |
| Custom facet overlay | `g.map_dataframe(fn)` after `sns.FacetGrid(...)` |
| Categorical facets | `sns.catplot(df, kind="bar", col=g, row=h)` |
| Move a legend | `sns.move_legend(ax_or_g, "upper left")` |
| Save anything | `fig.savefig("f.png", dpi=300)` / `g.savefig("f.svg")` |

Quick FAQ:

- *Which level should I start with?* Figure-level while exploring (`relplot`,
  `catplot`, `lmplot`); switch to axes-level the moment you compose layouts.
- *Where did my styling go?* A later `sns.set_theme()` reset it - reapply.
- *Why no CI band on my lineplot?* One observation per x: nothing to aggregate.

---

*End of the Seaborn reference. Pair it with notebooks 01-04 in this folder for
guided walkthroughs and graded practice.*
