# Capstone Projects - Prove the Foundations

**MLCourse · Data Science Foundations · 06_capstone_projects**

Five end-to-end analyses chaining **pandas → preprocessing → matplotlib → seaborn**
into stakeholder-grade deliverables. No scaffolding here - you drive.

## The method (use it on every project)

```
1 QUESTION   translate the brief into concrete, answerable questions
2 LOAD       acquire + audit data (shape, dtypes, missing, duplicates)
3 CLEAN      justified per-column strategies - never silent fixes
4 ANALYZE    segment → aggregate → compare; every number earns a sentence
5 VISUALIZE  one coherent dashboard + supporting charts
6 INSIGHT    quantify each finding; state limitations honestly
7 COMMUNICATE findings + recommendations in plain language
```

## The projects

| # | Notebook | Dataset | Skills spotlight |
|---|---|---|---|
| 01 | `titanic_survival_eda` | seaborn titanic | missing-data strategy, feature engineering, survival segmentation dashboard |
| 02 | `restaurant_tips_analytics` | tips | tip-% economics, regression line, Simpson's-paradox hint, business recs |
| 03 | `penguins_statistical_eda` | penguins | species statistics, correlation matrix, IQR outlier audit, dimorphism |
| 04 | `flights_timeseries_dashboard` | flights | datetime index, trend/seasonality decomposition, YoY growth, anomaly flags |
| 05 | `movie_reviews_text_eda` | real IMDB 50k (downloads ~66 MB once) | full text pipeline, n-grams, TF-IDF discriminative words, VADER validation, word clouds |

Datasets load via `sns.load_dataset(...)` (internet needed once, then cached).
Project 05 auto-downloads and caches to `data/imdb_reviews.csv`.

## How to work

- Open the notebook, read the *brief*, then attempt each phase before reading its cells.
- Type your own extra cells - extend every analysis with one question of YOURS.
- Finish by writing the conclusions section as if emailing a non-technical manager.
- Self-review rubric: reproducible top-to-bottom? every chart labeled? every
  insight quantified? limitations stated? recommendations actionable?

*Start with Capstone 01.*
