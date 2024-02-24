[
![PyPi](https://img.shields.io/pypi/v/pecking.svg?)
](https://pypi.python.org/pypi/pecking)
[
![CI](https://github.com/mmore500/pecking/actions/workflows/ci.yaml/badge.svg)
](https://github.com/mmore500/pecking/actions)
[
![GitHub stars](https://img.shields.io/github/stars/mmore500/pecking.svg?style=round-square&logo=github&label=Stars&logoColor=white)](https://github.com/mmore500/pecking)

_pecking_ identifies the set of lowest-ranked groups and set of highest-ranked groups in a dataset using nonparametric statistical tests.

- Free software: MIT license
- Repository: <https://github.com/mmore500/pecking>

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

See function docstrings for full parameter and return value descriptions.
