[
![PyPi](https://img.shields.io/pypi/v/pecking.svg?)
](https://pypi.python.org/pypi/pecking)
[
![CI](https://github.com/mmore500/pecking/actions/workflows/ci.yaml/badge.svg)
](https://github.com/mmore500/pecking/actions)
[
![GitHub stars](https://img.shields.io/github/stars/mmore500/pecking.svg?style=round-square&logo=github&label=Stars&logoColor=white)](https://github.com/mmore500/pecking)
[![DOI](https://zenodo.org/badge/760949154.svg)](https://zenodo.org/doi/10.5281/zenodo.10701184)

:hatching_chick: **_pecking_** identifies the set of lowest-ranked groups and set of highest-ranked groups in a dataset using nonparametric statistical tests.

- Free software: MIT license
- Repository: <https://github.com/mmore500/pecking>
- Documentation: <https://github.com/mmore500/pecking/blob/master/README.md>

## Install

`python3 -m pip install pecking`

## Example Usage

```python3
>>> import pecking
>>> samples = [[1, 2, 3, 4, 5], [2, 3, 4, 4, 4], [8, 9, 7, 6, 4]]
>>> labels = ['Group 1', 'Group 2', 'Group 3']
>>> pecking.skim_highest(samples, labels)
['Group 1']
```

---

```python3
import functools
from matplotlib import pyplot as plt
import pecking
import seaborn as sns

g = peckplot(
    sns.load_dataset("titanic"),
    score="age",
    x="who",
    y="age",
    hue="class",
    col="survived",
    legend_kws=dict(prop={"size": 8}, bbox_to_anchor=(0.88, 0.5)),
    skimmers=(
        functools.partial(
            skim_highest, alpha=0.05, min_obs=8, nan_policy="omit"
        ),
        functools.partial(
            skim_lowest, alpha=0.05, min_obs=8, nan_policy="omit"
        ),
    ),
    skim_labels=["Oldest", "Youngest"],
    palette=sns.color_palette("tab10")[:3],
)
assert g is not None
g.map_dataframe(
    sns.stripplot,
    x="who",
    y="age",
    hue="class",
    s=2,
    color="black",
    dodge=True,
    jitter=0.3,
)

plt.show()
```

![Example Plot](docs/assets/test_peckplot_titanic.png)

## API

See function docstrings for full parameter and return value descriptions.

### `pecking.skim_lowest`/`pecking.skim_highest`

Direct interface to the underlying statistical tests.

```python3
def skim_highest(
    samples: typing.Sequence[typing.Sequence[float]],
    labels: typing.Optional[typing.Sequence[typing.Union[str, int]]] = None,
    alpha: float = 0.05,
) -> typing.List[typing.Union[str, int]]:
    """Identify the set of highest-ranked groups that are statistically
    indistinguishable amongst themselves based on a Kruskal-Wallis H-test
    followed by multiple Mann-Whitney U-tests."""
```

```python3
def skim_highest(
    samples: typing.Sequence[typing.Sequence[float]],
    labels: typing.Optional[typing.Sequence[typing.Union[str, int]]] = None,
    alpha: float = 0.05,
) -> typing.List[typing.Union[str, int]]:
    """Identify the set of lowest-ranked groups that are statistically
    indistinguishable amongst themselves based on a Kruskal-Wallis H-test
    followed by multiple Mann-Whitney U-tests."""
```

### `pecking.mask_skimmed_rows`

Tidy-data interface to calculate the results of `skim_lowest`/`skim_highest` among row groups in a DataFrame.

```python3
def mask_skimmed_rows(
    data: pd.DataFrame,
    score: str,
    groupby_inner: typing.Union[typing.Sequence[str], str],
    groupby_outer: typing.Union[typing.Sequence[str], str] = tuple(),
    skimmer: typing.Callable = skim_highest,
    **kwargs: dict,
) -> pd.Series:
    """Create a boolean mask for a DataFrame, identifying rows within
    significantly outstanding groups.

    This function applies a two-level grouping to the input DataFrame: an outer
    grouping ('groupby_outer') followed by an inner grouping ('groupby_inner').
    For each inner group, it uses a 'skimmer' function to determine which rows
    are part of significantly outstanding groups based on a specified 'score'
    column. Only inner groups within the same outer group are compared.

    Rows identified as members of significantly outstanding inner groups are
    marked True in the returned Series, while all others are marked False."""
```

### `pecking.peckplot`

Wraps `seaborn.catplot` to add hatched backgrounds behind the best and worst groups within the each `row`/`col` facet.
(Comparison scope/pooling can be controlled with `*_group` parameters.)

```python3
def peckplot(
    data: pd.DataFrame,
    score: str,
    x: typing.Optional[str] = None,
    y: typing.Optional[str] = None,
    hue: typing.Optional[str] = None,
    col: typing.Optional[str] = None,
    row: typing.Optional[str] = None,
    x_group: typing.Literal["inner", "outer", "ignore"] = "inner",
    y_group: typing.Literal["inner", "outer", "ignore"] = "inner",
    hue_group: typing.Literal["inner", "outer", "ignore"] = "inner",
    col_group: typing.Literal["inner", "outer", "ignore"] = "outer",
    row_group: typing.Literal["inner", "outer", "ignore"] = "outer",
    skimmers: typing.Sequence[typing.Callable] = (
        functools.partial(skim_highest, alpha=0.05),
        functools.partial(skim_lowest, alpha=0.05),
    ),
    skim_hatches: typing.Sequence[str] = ("*", "O.", "xx", "++"),
    skim_labels: typing.Sequence[str] = ("Best", "Worst"),
    skim_title: typing.Optional[str] = "Rank",
    orient: typing.Literal["v", "h"] = "v",
    **kwargs: dict,
) -> sns.FacetGrid:
    """Boxplot the distribution of a score across various categories,
    highlighting the best (and/or worst) performing groups.

    Uses nonparametric `skim_highest`/`skim_lowest` to distinguish the sets of
    groups with statistically indistinguishable highest/lowest scores. Uses
    `backstrip`'s `backplot` to add hatched backgrounds behind the best and
    worst groups."""
```

## Citing

If pecking contributes to a scientific publication, please cite it as

> Matthew Andres Moreno. (2024). mmore500/pecking. Zenodo. https://doi.org/10.5281/zenodo.10701185

```bibtex
@software{moreno2024pecking,
  author = {Matthew Andres Moreno},
  title = {mmore500/pecking},
  month = feb,
  year = 2024,
  publisher = {Zenodo},
  doi = {10.5281/zenodo.10701185},
  url = {https://doi.org/10.5281/zenodo.10701185}
}
```

Consider also citing [matplotlib](https://matplotlib.org/stable/users/project/citing.html), [seaborn](https://seaborn.pydata.org/citing.html), and [SciPy](https://scipy.org/citing-scipy/).
And don't forget to leave a [star on GitHub](https://github.com/mmore500/pecking/stargazers)!
