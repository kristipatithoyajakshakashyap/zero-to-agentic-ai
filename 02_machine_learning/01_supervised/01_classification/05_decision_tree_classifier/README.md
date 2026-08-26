# Decision Tree - Classifier

**MLCourse · Machine Learning · supervised · classification · 05_decision_tree**

## The idea in one sentence
Play 20-questions with the data: repeatedly split rows on the feature/question
that best separates the classes until leaves are (almost) pure.

## Math intuition (gentle)

At every node the tree asks: *"which single question lowers class-mixing the
most?"* Mixing is measured by:

**Gini impurity** - chance two random rows disagree:
$$G = -\sum_c p_c^2 \quad\text{(0 = pure node)}$$

or **entropy** - surprise in bits: $H=-\sum_c p_c\log_2 p_c$.

The split maximizing impurity DROP wins:
$$\Delta = G_{\text{parent}} - \frac{n_L}{n}G_L - \frac{n_R}{n}G_R$$

Trees recurse until stopping rules bite (`max_depth`, `min_samples_leaf`…).

## When / how to use
 interpretability is required (print the tree!) · mixed numeric/categorical
features · non-linear thresholds · fast inference.
 alone on noisy data (overfits wildly) -> always prune or move to forests;
unstable: tiny data change -> different tree.

## Key sklearn parameters (the pruning kit)
| param | effect |
|---|---|
| `max_depth` | hard stop on question chain length |
| `min_samples_leaf` | leaf must hold ≥ this many rows |
| `min_samples_split` | don't bother splitting small nodes |
| `ccp_alpha` | cost-complexity pruning - cut weak branches |
| `criterion` | "gini" (default) or "entropy" |

## Pitfalls
- unconstrained depth memorizes training data (00% train / coin-flip test)
- axis-aligned splits struggle with diagonal relationships
- class imbalance biases default thresholds

## Contents
- `0_theory_and_mathematics.ipynb` - Gini by hand + grow/visualize a real tree
- `02_model_development_workflow.ipynb` - depth tuning, pruning, feature importances
- `projects/` -  titanic readable-tree ·  penguins multiclass ·  credit-g pruning

## Cheat sheet
```python
DecisionTreeClassifier(max_depth=5, min_samples_leaf=20, ccp_alpha=0.002)
```
