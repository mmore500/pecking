import functools
import typing
import warnings

from backstrip import backplot
import numpy as np
import pandas as pd
import seaborn as sns

from ._mask_skimmed_rows import mask_skimmed_rows
from ._skim_highest import skim_highest
from ._skim_lowest import skim_lowest


def peckplot(
    data: pd.DataFrame,
    score: str,
    x: typing.Optional[str] = None,
    y: typing.Optional[str] = None,
    hue: typing.Optional[str] = None,
    col: typing.Optional[str] = None,
    row: typing.Optional[str] = None,
    order: typing.Optional[typing.Sequence[str]] = None,
    hue_order: typing.Optional[typing.Sequence[str]] = None,
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
    worst groups.

    Parameters
    ----------
    data : pd.DataFrame
        Input dataset, where each row is an observation and each column is a feature.
    score : str
        Column name in `data` representing the score to rank groups by.

        Usually this will be the same column name as `x` (if vertical) or `y`
        (if horizontal).
    x, y : Optional[str], default=None
        Column names in `data` for the x and y axes.

        Equivalent interpretation to `x` and `y` in `seaborn.catplot`.
    hue : Optional[str], default=None
        Column name in `data` for coloring elements based on its values.

        Equivalent interpretation to `hue` in `seaborn.catplot`.
    col, row : Optional[str], default=None
        Column names for facet wrapping the plot grid.

        Equivalent interpretation to `col`/`row` in `seaborn.catplot`.
    order : Optional[Sequence[str]], default=None
        Order of the x or y axis levels.

        Equivalent interpretation to `order` in `seaborn.catplot`.
    hue_order : Optional[Sequence[str]], default=None
        Order of the hue levels.

        Equivalent interpretation to `hue_order` in `seaborn.catplot`.
    x_group, y_group, hue_group : {'inner', 'outer', 'ignore'}, default='inner'
        Grouping strategies for x, y, and hue variables.

        By default, `skim_highest`/`skim_lowest` comparison is made among all
        individually boxplotted groups within the same facet. To only compare
        among hue sets, set `x_group` (if vertical) or `y_group` (if
        horizontal) to 'outer'. To pool hue sets together, set `hue_group` to
        'ignore'.
    col_group, row_group : {'inner', 'outer', 'ignore'}, default='outer'
        Grouping strategies col, and row variables.

        By default, `skim_highest`/`skim_lowest` comparisons are made
        independently within each facet. To make comparison span across all
        facets, set `col_group` and `row_group` to 'inner'.
    skimmers : Sequence[Callable], default=(skim_highest, skim_lowest)
        Functions to identify top and bottom groups based on `score`.

        Use `functools.partial` to pass non-default kwargs to the skimming
        functions.
    skim_hatches : Sequence[str], default=("*", "O.", "xx", "++")
        Hatch patterns for highlighting skimmer-identified groups.

        Default patterns are Star for "Best" group and concentric circles for
        "Worst" group.
    skim_labels : Sequence[str], default=("Best", "Worst")
        Labels for the skimmer-identified groups.
    skim_title : Optional[str], default="Rank"
       Legend title for skimmer-identified group hatchings.
    orient : {'v', 'h'}, default='v'
        Orientation of the plot ('v' for vertical, 'h' for horizontal).

        Equivalent interpretation to `orient` in `seaborn.catplot`.
    **kwargs : dict
        Additional keyword arguments passed to `backstrip.backplot`.

    Returns
    -------
    sns.FacetGrid
        A figure-level seaborn FacetGrid object.
    """
    if len(data) == 0:
        raise ValueError("Data must not be empty.")

    xy = {"v": x, "h": y}[orient]
    if xy is not None and order is None:
        order = sorted(data[xy].unique())
    if hue is not None and hue_order is None:
        hue_order = sorted(data[hue].unique())

    all_mask = pd.Series(data=True, index=data.index)
    data = data[
        (data[xy].isin(order) if xy is not None else all_mask)
        & (data[hue].isin(hue_order) if hue is not None else all_mask)
    ].reset_index(drop=True)

    groupby_inner = []
    groupby_outer = []
    if xy is not None:
        group = {"v": x_group, "h": y_group}[orient]
        {"inner": groupby_inner, "outer": groupby_outer, "ignore": list()}[
            group
        ].append(xy)
    if hue is not None and hue_group != "ignore":
        {"inner": groupby_inner, "outer": groupby_outer}[hue_group].append(hue)
    if col is not None and col_group != "ignore":
        {"inner": groupby_inner, "outer": groupby_outer}[col_group].append(col)
    if row is not None and row_group != "ignore":
        {"inner": groupby_inner, "outer": groupby_outer}[row_group].append(row)

    if len(groupby_inner) == 0:
        raise ValueError("At least one inner grouping variable must be used.")

    masks = [
        mask_skimmed_rows(
            data=data,
            score=score,
            groupby_inner=groupby_inner,
            groupby_outer=groupby_outer,
            skimmer=skimmer,
        )
        for skimmer in skimmers
    ]

    if "_" in skim_labels:
        raise ValueError("The label '_' is reserved for unskimmed groups.")

    mask_overlaps = np.stack(masks).sum(axis=0)
    assert len(mask_overlaps) == len(data)
    if (mask_overlaps > 1).any():
        max_overlap = mask_overlaps.max()
        num_overlapping_rows = mask_overlaps.astype(bool).sum()
        warnings.warn(
            f"{num_overlapping_rows} rows overlap between skimmers, with rows "
            f"overlapped between at most {max_overlap} skimmers.",
        )

    if mask_overlaps.any():
        # if there are any overlapping skims, create an independent copy of the
        # data for each skim label and with column masking just that skim
        # ... backplot combines overlapping hatches if a group has multiple
        # style values, and a boxplot with the duplicated or triplicated etc.
        # data will lay out the same way as the just original data
        concat = []
        for i, label in enumerate(skim_labels):
            data_ = data.copy()
            data_[skim_title] = pd.Series(
                [label if tup[i] else "_" for tup in zip(*masks)],
                dtype="string",
                index=data_.index,
            )
            concat.append(data_)
        data = pd.concat(concat, ignore_index=True)
    else:
        data = data.copy()
        data[skim_title] = pd.Series(
            [
                skim_labels[tup.index(True)] if any(tup) else "_"
                for tup in zip(*masks)
            ],
            dtype="string",
            index=data.index,
        )

    return backplot(
        data=data,
        x=x,
        y=y,
        hue=hue,
        col=col,
        row=row,
        order=order,
        hue_order=hue_order,
        style=skim_title,
        style_order=skim_labels,
        hatches=skim_hatches,
        orient=orient,
        **kwargs,
    )
