# MLCourse - Zero to Advanced

A structured, hands-on curriculum covering Data Science Foundations, Machine
Learning, and Agentic AI. Every topic is delivered as Jupyter notebooks with
dense instructional comments, supported by standalone Markdown reference guides
per section.

## Repository layout

```
MLCourse/
├── 0_data_science_foundations/     NumPy · Pandas · Matplotlib · Seaborn
│                                    + Data Preprocessing + Capstone Projects
├── 02_machine_learning/
│   ├── data/                        shared dataset hub (auto-downloaded)
│   ├── 0_supervised/
│   │   ├── 0_classification/       logistic · knn · svm · naive bayes
│   │   │                            · decision tree · random forest
│   │   │                            · adaboost · gradient boosting · xgboost
│   │   └── 02_regression/           linear (+ Ridge/Lasso/ElasticNet) · knn
│   │                                · svr · decision tree · random forest
│   │                                · adaboost · gradient boosting · xgboost
│   └── 02_unsupervised/             k-means · hierarchical clustering
│                                    · silhouette evaluation lab
└── 03_agentic_ai/                   LLM agents, tool use, RAG, multi-agent
                                     systems                          (planned)
```

## Environment setup

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps        # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Select the `.venv` Python kernel inside Jupyter so notebooks resolve the
installed packages. If script activation is blocked, run
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once.

## Learning path

Work top-to-bottom within each track. Times assume focused part-time study.

| Order | Section | Time | Outcome |
|---|---|---|---|
|  | `foundations/0_numpy` | ~6 h | Arrays, broadcasting, vectorization |
| 2 | `foundations/02_pandas` | ~8 h | Cleaning, groupby, merging, time series |
| 3 | `foundations/03_matplotlib` | ~5 h | Full plotting control, dashboards |
| 4 | `foundations/04_seaborn` | ~5 h | Statistical graphics |
| 5 | `foundations/05_preprocessing` | ~6 h | Missing/numeric/categorical/text pipelines |
| 6 | `foundations/06_capstones` | ~0 h | Five end-to-end projects |
| 7 | `ml/classification` | ~6 h | Nine classifiers with graded projects |
| 8 | `ml/regression` | ~3 h | Eight regressors with graded projects |
| 9 | `ml/unsupervised` | ~6 h | Clustering plus silhouette evaluation |

Study discipline matters more than speed: read the section reference first,
execute every cell, attempt exercises before solutions, and inspect errors
deliberately.

## Datasets

All data is real. Seaborn built-ins, sklearn loaders, and stable public mirrors
are fetched by download-once helpers inside the notebooks and cached locally;
the machine-learning track consolidates them under `02_machine_learning/data/`.
After the initial fetches the entire course runs offline.

## Troubleshooting

| Problem | Resolution |
|---|---|
| Module not found in a notebook | Switch the kernel to this repository's `.venv` Python |
| seaborn dataset fails to load | Connect once; results cache locally afterwards |
| NLTK LookupError | Run the guarded `nltk.download(...)` cell in that notebook |
| Plots do not render | Ensure the `%matplotlib inline` cell executed |
| Notebook behaves inconsistently | Restart the kernel and run all cells in order |

## Note for contributors

Standards that keep this repository maintainable:

. **Notebooks only.** Content ships as self-contained `.ipynb` files; no
   companion `.py` scripts. A notebook is accepted only if it executes
   top-to-bottom from a fresh kernel without errors.
2. **Comment density is part of the contract.** Every non-trivial line or block
   carries an explanatory comment aimed at a learner seeing the concept for the
   first time.
3. **Data handling.** Datasets are never committed. Fetch them at runtime with
   the established download-once helper and store them in the track's `data/`
   directory; synthetic arrays may appear only to illustrate mathematics inside
   theory notebooks.
4. **Module structure.** New algorithm modules follow the existing layout:
   `README.md` reference, theory notebook, development-workflow notebook, and
   three-to-four graded project notebooks ordered by difficulty.
5. **Documentation sync.** Adding or renaming a module requires updating the
   affected section README and the learning-path table above in the same change.

Keep prose plain, precise, and free of decoration; clarity is the product.
