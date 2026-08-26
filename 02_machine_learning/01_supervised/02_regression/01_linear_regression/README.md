# Linear Regression - Section Guide

**MLCourse · Machine Learning · 0_linear_regression**

Eleven notebooks take you from raw calculus to five audited real-data projects.
Everything runs offline after first-time dataset caching; no .py scripts needed -
every model class lives inside its notebook.

## Study order

| # | Notebook | Focus | Time |
|---|---|---|---|
|  | `0_theory_and_math` | hypothesis -> MSE -> Normal Equation -> GD -> LINE+M assumptions -> metrics | ~2.5 h |
| 2 | `02_from_scratch_oop` | `MyLinearRegression` class, both solvers, verified vs sklearn | ~.5 h |
| 3 | `03_sklearn_implementation` | Pipeline/CV/diagnostics workflow on diabetes | ~.5 h |
| 4 | `04_ridge_regression` | L2 math + when-to-use + diabetes project | ~ h |
| 5 | `05_lasso_regression` | L/sparsity + geometry + diamonds project | ~ h |
| 6 | `06_elasticnet` | mixed penalty + decision flowchart + expanded-housing project | ~.2 h |
| 7- | `projects/0…05` |  tips ·  penguins ·  mpg ·  insurance ·  california | ~6 h |

## Datasets you will touch (all REAL)

- seaborn cached: `tips`, `penguins`, `mpg`, `diamonds`
- sklearn bundled/downloaded: `load_diabetes`, `fetch_california_housing`
- web CSV (cached locally): medical `insurance.csv`

## The one-page mental model

$$h_\theta(x)=X\theta \quad\to\quad J(\theta)=\lVert X\theta-y\rVert^2+\alpha R(\theta)$$

- No penalty ($\alpha=0$): OLS - notebooks 0-03, project baselines.
- $R=\lVert\theta\rVert_2^2$ -> **Ridge**: keep everything, shrink together.
- $R=\lVert\theta\rVert_$ -> **Lasso**: select a sparse subset.
- Mixed -> **ElasticNet**: correlated groups + noise.

## Self-review rubric for every project notebook

. Business question stated up front?
2. Every cleaning/imputation choice justified?
3. Split before ANY fitted statistic?
4. Train/CV/test reported together?
5. Coefficients translated to plain language?
6. Assumption diagnostics run and READ?
7. Limitations admitted honestly?

*Start -> `0_theory_and_math.ipynb`*
