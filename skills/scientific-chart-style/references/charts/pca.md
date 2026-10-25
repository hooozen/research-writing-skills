# PCA scores (`pca`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use PCA scores for a descriptive low-dimensional view of multivariate observations. A two-dimensional projection may conceal substantial variation. Visible group separation is not a classification test or proof of causal clusters.

## Minimal inputs

`values` is a finite sample-by-feature matrix; `feature_names` matches columns and `groups` matches rows. This runnable example requires `preprocessing: "standardize"`: center each feature and divide by sample SD. Constant features need removal or justification before this reference.

The optional runner supports up to three group identities; extend or facet deliberately when more are needed.

## Encoding and calculation

Fit SVD to the standardized matrix. Scores use the same fitted components; eigenvalues are singular values squared/(n−1), and axis percentages are each eigenvalue divided by their sum. Group labels only distinguish the unsupervised projection with color and point shape.

## Interpretation limits

PCA does not universally require standardization; for a different protocol, adapt preprocessing and its caption explicitly. Predictive evaluation must fit transformations only on allowed development data. Do not add unsupported ellipses or compare independently fitted PC axes.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart pca --example --output-dir /tmp/pca-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'values': [[1.1, 2.4, 3.2, 1.8],
            [1.5, 2.0, 2.9, 2.2],
            [1.9, 2.8, 3.5, 2.0],
            [2.1, 2.2, 3.0, 2.7],
            [3.0, 3.1, 2.4, 3.8],
            [3.5, 2.9, 2.0, 4.1],
            [3.2, 3.8, 2.6, 3.5],
            [3.9, 3.4, 1.8, 4.6]],
 'groups': ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B'],
 'feature_names': ['F1', 'F2', 'F3', 'F4'],
 'preprocessing': 'standardize'}
render_chart("pca", data, "/tmp/pca-example")
```

**References:** [exact input](../examples/pca.json) · [editable SVG](../examples/pca.svg) · [PNG visual fallback](../examples/pca.png). All example values are synthetic.

**Definition source:** [Official PCA definition](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html).
