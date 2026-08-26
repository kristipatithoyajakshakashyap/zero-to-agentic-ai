# Decision Tree Regressor

**MLCourse · Machine Learning · supervised · regression**

## The idea in one sentence
Play 20-questions with a number: repeatedly split the rows with yes/no feature
questions so each side gets more homogeneous, then predict each final region's
**mean target** - the result is a **piecewise-constant staircase**, not a smooth curve.

## Piecewise-constant intuition
A fitted tree is just a nested set of `if/else` questions. Every row falls into
exactly one leaf, and the leaf outputs **one flat number** (the average of the
training targets that landed there). Sweep the input from left to right and the
prediction jumps in **steps**: shallow tree = few wide steps; deep tree = many
thin steps that can hug every training point.

## Math intuition (gentle)
At every node the tree asks: *"which single question shrinks squared error the most?"*
For a node holding rows with targets $y_i$:

$$SSE = \sum_{i \in node}(y_i - \bar y)^2 \qquad (\text{best constant} = \text{mean})$$

A candidate split sends $n_L$ rows left / $n_R$ rows right. Score it by the error it removes:

$$\Delta = SSE_{parent} - \left(\frac{n_L}{n}\,SSE_L + \frac{n_R}{n}\,SSE_R\right)$$

The split maximizing $\Delta$ wins; recursion repeats until stopping rules bite.
Since $SSE = n\cdot Var(y)$, this is exactly **variance reduction** - same recipe
as classification trees, with Gini swapped for MSE.

## Overfitting anatomy
An unpruned tree keeps splitting until leaves are nearly singletons:
- **Symptoms:** hundreds of leaves, train R² ≈ 1.0, test R² far lower, staircase with one step per point.
- **Cause:** splits start isolating *noise*, not signal - the model memorizes instead of generalizes.
- **Cure:** prune. Limit depth, fatten leaves, or cut weak branches with cost-complexity pruning.

## Key sklearn parameters (the pruning kit)
| param | effect |
|---|---|
| `max_depth` | hard stop on question-chain length (1-3 = crude steps, ~8 = usually enough on tabular data) |
| `min_samples_leaf` | leaf must hold ≥ this many rows → smooths steps, blocks singleton memorization |
| `min_samples_split` | don't bother splitting nodes smaller than this |
| `ccp_alpha` | cost-complexity penalty: grow full tree, then cut branches whose gain < alpha |
| `max_features` | features considered per split (adds randomness - mostly a forest tool) |

## When / how to use
- **Use when:** interpretability matters (you can print the rule book), mixed
  numeric/categorical features, non-linear thresholds, no scaling needed, fast inference.
- **Avoid when:** you need smooth/extrapolating predictions (trees output flat
  steps bounded by training range) or low-variance standalone accuracy -
  always pair with pruning or upgrade to a random forest.

💡 Tune in this order: `max_depth` sweep → `min_samples_leaf` → `ccp_alpha`.
Validate every choice with cross-validation, never by staring at training error.

## Contents
- `01_theory_and_mathematics.nb.py` - SSE of the root by hand, Δ of a real split,
  proving sklearn's depth-1 tree predicts group means, step-functions at depth 1/3/unlimited
- `02_model_development_workflow.nb.py` - California housing: unpruned baseline,
  depth CV sweep, ccp_alpha path, feature importances
- `projects/` - easy tips tree · medium mpg tree · hard insurance charges tree ·
  advanced underfit-vs-overfit audit

## Cheat sheet
```python
from sklearn.tree import DecisionTreeRegressor, plot_tree
tree = DecisionTreeRegressor(max_depth=6, min_samples_leaf=20, ccp_alpha=1e-3)
tree.fit(X_train, y_train)
plot_tree(tree, feature_names=X.columns, filled=True, rounded=True)
```
