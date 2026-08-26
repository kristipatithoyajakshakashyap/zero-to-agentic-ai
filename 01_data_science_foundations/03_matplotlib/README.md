# Matplotlib - The Complete Reference

**MLCourse · Data Science Foundations · 03_matplotlib**

Matplotlib is the graphics engine every Python viz library builds on (seaborn,
pandas plotting). This book covers the full journey taught in the two teaching
notebooks: mental model -> chart types -> composition -> polish.

**Contents**
. [The anatomy](#-the-anatomy)
2. [Two interfaces](#2-two-interfaces)
3. [Chart type cookbook](#3-chart-type-cookbook)
4. [Text, legends & annotations](#4-text-legends--annotations)
5. [Axes control: limits, scales, ticks](#5-axes-control-limits-scales-ticks)
6. [Layout & multiple plots](#6-layout--multiple-plots)
7. [Dual & secondary axes](#7-dual--secondary-axes)
8. [Images & 2-D fields](#8-images--2-d-fields)
9. [Uncertainty visualization](#9-uncertainty-visualization)
0. [Colormaps](#0-colormaps)
. [Styles & rcParams](#-styles--rcparams)
2. [Pandas integration](#2-pandas-integration)
3. [Saving figures](#3-saving-figures)
4. [Cheat sheet](#4-cheat-sheet)

---

## . The anatomy

```
Figure  ──────────────────────────────── canvas / window
 ├── Axes  (the plot area; a Figure may hold many)
 │    ├── XAxis, YAxis          number lines: ticks + labels
 │    │     └── Tick, ticklabel artists
 │    ├── spines                the 4 border lines
 │    ├── title, labels, legend artists
 │    └── data artists: Line2D, Rectangle (bars), PathCollection (scatter)...
```

>  **Pro tip:** "Axes" = *the plot*, "Axis" = *a number line*. 90% of beginner
> confusion dies when this distinction sticks.

## 2. Two interfaces

| | pyplot (`plt.plot`) | OO (`fig, ax = plt.subplots()`) |
|---|---|---|
| style | implicit "current figure" | explicit objects |
| good for | quick exploration | scripts, dashboards, anything > plot |
| mapping | `plt.title` ↔ `ax.set_title`, `plt.xlim` ↔ `ax.set_xlim`, `plt.xticks` ↔ `ax.set_xticks`, `plt.legend` ↔ `ax.legend` | |

**Default to OO.** One-liner batch setters:

```python
ax.set(xlim=(0, 0), ylim=(-, ), xlabel="t", ylabel="v", title="signal")
```

## 3. Chart type cookbook

| Function | Shows | Key params |
|---|---|---|
| `ax.plot(x, y)` | trends/relations over ordered x | `color ls lw marker alpha label markevery` |
| `ax.scatter(x, y)` | point cloud, 4-D possible | `s c cmap alpha edgecolors` |
| `ax.bar / barh` | category comparison | `width bottom`(stacking) `yerr` |
| `ax.hist(x, bins)` | one-variable distribution | `bins density cumulative histtype range` |
| `ax.boxplot(data_list)` | median/quartiles/outliers per group | `patch_artist tick_labels vert` |
| `ax.pie(sizes)` | ≤5 dominant shares | `autopct explode startangle wedgeprops` |
| `ax.errorbar` | estimate ± uncertainty | `yerr fmt capsize ecolor` |
| `ax.fill_between(x, lo, hi)` | uncertainty band / area | `alpha color step` |
| `ax.hexbin / hist2d` | dense scatter density | `gridsize bins cmap` |
| `ax.imshow(M)` | matrix as image/heatmap | `cmap extent origin interpolation` |
| `ax.contourf(X,Y,Z)` | smooth 2-D field levels | `levels cmap` |
| `ax.plot_surface(X,Y,Z)` | 3-D surface | `cmap rstride/cstride` (needs `projection="3d"`) |

Grouped bars pattern (memorize!):

```python
x = np.arange(len(cats))
ax.bar(x - w/2, series_a, w, label="A")
ax.bar(x + w/2, series_b, w, label="B")
ax.set_xticks(x, cats)
```

Stacked bars: second call gets `bottom=series_a`.
Histogram fairness rule: same explicit `bins=` for every series you compare.

## 4. Text, legends & annotations

```python
ax.set_title("...", fontsize=4, fontweight="bold", loc="left")
fig.suptitle("board title")                 # whole-Figure heading
ax.legend(loc="upper left", ncols=2, frameon=False)
ax.axhline(y, color="red", ls="--"); ax.axvspan(x0, x, alpha=.5)   # refs/bands
ax.annotate("peak", xy=(x_pt, y_pt), xytext=(x_txt, y_txt),           # data coords
            arrowprops=dict(arrowstyle="->"))
ax.text(x, y, "note", fontsize=9, color="dimgray")
```

Legend `loc`: `best upper/lower left/center/right` or 2-tuple of axes fractions.
Merging twin-axis legends: concatenate both `(handles, labels)` pairs.

## 5. Axes control: limits, scales, ticks

```python
ax.set_xlim(a, b); ax.set_ylim(a, b)
ax.set_xscale("log")        # semilogx/loglog/symlog variants
ax.grid(axis="y", which="major", alpha=.35)
ax.tick_params(axis="x", rotation=45, labelsize=9)
ax.minorticks_on()
```

Log-log straight line => power law y=A·x^b with **slope b**:
`b, logA = np.polyfit(np.log0(x), np.log0(y), )`.

Despine recipe:

```python
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
```

## 6. Layout & multiple plots

```python
fig, axes = plt.subplots(2, 3, figsize=(2, 6), sharex=True)
for ax in axes.flat: ...                    # flatten-and-loop pattern

fig, m = plt.subplot_mosaic([["A","B"],      # ASCII layout design!
                             ["C","C"]],
                            gridspec_kw={"width_ratios": [2, ]})
m["A"].plot(...)
fig.tight_layout()          # or constrained_layout=True at creation
```

## 7. Dual & secondary axes

```python
ax_r = ax_t.twinx()                                  # shared x, new y-scale
sec = ax.secondary_xaxis(-0.28, functions=(fwd, inv))# unit converter strip
```

Color-match each axis' label/ticks to its series to avoid misreads.

## 8. Images & 2-D fields

```python
im = ax.imshow(matrix, cmap="viridis", extent=[x0,x,y0,y], origin="lower")
fig.colorbar(im, ax=ax, shrink=.8, label="value")
```

Dense scatter fixes: `alpha≤0.05` -> still blob? -> `hist2d(bins=60)` or
`hexbin(gridsize=45)`, always with a colorbar.

## 9. Uncertainty visualization

```python
ax.errorbar(x, mean, yerr=sem, fmt="o-", capsize=4)
ax.fill_between(x, mean-2*sem, mean+2*sem, alpha=.8, label="±2 SE")
```

Never show a bare forecast line without a widening band - honesty is cheap.

## 0. Colormaps

| Data kind | Family | Safe picks |
|---|---|---|
| magnitude 0->max | sequential | viridis, plasma, Blues, crest |
| signed around 0 | diverging | coolwarm, RdBu_r, Spectral |
| categories | qualitative | tab0, Set2, colorblind |

Rules: perceptually uniform only (never `jet`) · diverging needs symmetric
`vmin/vmax` · discrete N colors via `plt.get_cmap("viridis", N)`.

## . Styles & rcParams

```python
plt.style.available                       # inventory
with plt.style.context("ggplot"): ...     # temporary theme block
plt.rcParams.update({"font.size": ,
                     "axes.spines.top": False})    # persistent defaults
plt.rcParams.update(plt.rcParamsDefault)           # reset
```

## 2. Pandas integration

```python
df.plot(figsize=(9,4))                    # thin wrapper, quick looks
for key, grp in df.groupby("cat"):        # full-control alternative
    ax.plot(grp.index, grp.val, label=key)
```

## 3. Saving figures

```python
fig.savefig("out.png", dpi=200, bbox_inches="tight")   # raster for slides
fig.savefig("out.svg")                                 # vector for papers
```

Order matters: savefig BEFORE plt.show(); keep the `fig` handle alive.

## 4. Cheat sheet

| Need | Call |
|---|---|
| fresh figure+axes | `fig, ax = plt.subplots(figsize=(w,h))` |
| grid of plots | `plt.subplots(r, c)` then `axes.flat` loop |
| custom layout | `subplot_mosaic([[..],[..]], width_ratios=..)` |
| second y-axis | `ax.twinx()` |
| shade a period | `ax.axvspan(t0, t, alpha=.2)` |
| annotate max point | `ax.annotate(txt, xy=(x,y), xytext=offset...)` |
| comparable histograms | same `bins=`, `density=True` |
| donut chart | `pie(..., wedgeprops=dict(width=.4))` |
| heatmap from matrix | `imshow` + `fig.colorbar(im)` |
| power-law exponent | polyfit on log0s; slope=b |
| despine | hide top/right spines |
| temporary theme | `with plt.style.context("..."):` |

*End of the Matplotlib reference book - go make something beautiful.*
