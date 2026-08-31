# Naive Bayes - Classification

**MLCourse · Machine Learning · supervised · classification · 04_naive_bayes**

## The idea in one sentence
Pick the class that makes the observed features most probable, assuming features
are **independent given the class** - the "naive" part.

## Math intuition (gentle)

Bayes' theorem flips the question from "which class?" to "which class best
explains what I saw?":

$$P(\text{class} \mid x) \propto P(\text{class}) \times P(x_1\mid\text{class}) \times P(x_2\mid\text{class}) \cdots$$

- $P(\text{class})$ = prior (base rate)
- Each $P(x_j\mid\text{class})$ = one-feature likelihood, learned by counting
- Multiply everything -> biggest product wins

The independence assumption is usually WRONG in reality - yet the classifier
still works because only the ARGmax ranking must be right.

### Three flavors
| Variant | Feature type | Likelihood model |
|---|---|---|
| `GaussianNB` | continuous numbers | bell curve per feature per class |
| `MultinomialNB` | word/term COUNTS | how often terms appear |
| `BernoulliNB` | binary flags | presence/absence |

## When / how to use
 text classification (spam!) with counts · tiny training data · instant
training & retraining · strong first baseline.
 correlated numeric features (double-counting evidence) · calibrated
probabilities required · fairness-sensitive priors left unexamined.

## Key sklearn parameters
| param | note |
|---|---|
| `var_smoothing` (Gaussian) | numerical stabilizer; rarely tuned |
| `alpha` (Multinomial/Bernoulli) | Laplace smoothing for unseen words; 1.0 default |

No scaling needed; GaussianNB is scale-invariant.

## Pitfalls
- zero-frequency trap -> keep `alpha ≥ 1`
- probabilities are over-confident but rankings remain useful
- don't feed one-hot dummies AND their source column together

## Contents
- `01_theory_and_mathematics.ipynb` - Bayes computed BY HAND on Titanic counts
- `02_model_development_workflow.ipynb` - GaussianNB vs logistic on breast cancer + MultinomialNB taste
- `projects/` -  titanic ·  SMS spam ·  20-newsgroups routing

## Cheat sheet
```python
from sklearn.naive_bayes import MultinomialNB
Pipeline([("bow", CountVectorizer()), ("nb", MultinomialNB(alpha=1.0))])
```
