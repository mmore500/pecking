import itertools as it
import typing

import pandas as pd

from ._skim_highest import skim_highest


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
    marked True in the returned Series, while all others are marked False.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame on which the masking operation will be performed.
    score : str
        The name of the column in 'data' that should be used to compare groups.
    groupby_inner : Union[Sequence[str], str]
        Column name(s) in 'data' used for the inner grouping operation.

        The inner grouping operation determines the groups of rows that will be
        compared by `skimmer`. Each unique combination of values in these
        columns defines an inner group.
    groupby_outer : Union[Sequence[str], str], optional
        Column name(s) in 'data' used for the outer grouping operation.

        The outer grouping splits the dataset into independent parts, within
        each of which separate comparisons are made by `skimmer` between inner
        groups. Each unique combination of values in these columns defines an
        outer group. If not provided, no outer grouping is performed.
    skimmer : Callable, default `pecking.skim_highest`
        A function that identifies significant rows within each inner group.

        Use 'skim_highest', 'skim_lowest', or a custom function that takes a
        sequence of samples and a sequence of labels, and returns a sequence of
        selected labels.
    **kwargs : dict
        Additional keyword arguments passed to the 'skimmer' function

    Returns
    -------
    pd.Series
        A boolean Series with the same index as 'data'.

        True values indicate that the corresponding row in 'data' is part of a
        significantly outstanding group as determined by the 'skimmer'
        function.
    """
    if len(data) == 0:
        return pd.Series(False, index=data.index)

    if isinstance(groupby_inner, str):
        groupby_inner = [groupby_inner]

    if isinstance(groupby_outer, str):
        groupby_outer = [groupby_outer]

    if len(groupby_inner) == 0:
        raise ValueError("At least one inner grouping variable must be used.")

    data = data.copy()
    data["_pecking_mask"] = False

    def skim_transform(outer_group: pd.DataFrame) -> pd.DataFrame:
        outer_group["_pecking_index"] = outer_group.index
        inner_groups = outer_group.groupby(groupby_inner, as_index=False)
        inner_scores = [g for _k, g in inner_groups[score]]
        inner_indices = [g for _k, g in inner_groups["_pecking_index"]]

        skimmed_indices = skimmer(inner_scores, inner_indices, **kwargs)
        flat_indices = [*it.chain(*skimmed_indices)]
        outer_group.loc[flat_indices, "_pecking_mask"] = True
        return outer_group

    if groupby_outer:
        grouped_data = data.groupby(
            groupby_outer, as_index=False, group_keys=False
        ).apply(
            skim_transform,
        )
    else:
        grouped_data = skim_transform(data)

    return grouped_data["_pecking_mask"]
