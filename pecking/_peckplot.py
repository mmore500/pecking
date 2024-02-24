import functools
import typing

from backstrip import backplot
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
    if len(data) == 0:
        raise ValueError("Data must not be empty.")

    groupby_inner = []
    groupby_outer = []
    if {"v": x, "h": y}[orient] is not None:
        group = {"v": x_group, "h": y_group}[orient]
        {"inner": groupby_inner, "outer": groupby_outer, "ignore": list()}[
            group
        ].append({"v": x, "h": y}[orient])
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
    if any(sum(tup) > 1 for tup in zip(*masks)):
        raise ValueError("Overlapping groups were identified by the skimmers.")

    if "_" in skim_labels:
        raise ValueError("The label '_' is reserved for unskimmed groups.")

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
        style=skim_title,
        style_order=skim_labels,
        hatches=skim_hatches,
        orient=orient,
        **kwargs,
    )
