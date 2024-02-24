import typing

import pandas as pd

from ._robust_groupby import robust_groupby
from ._skim_highest import skim_highest


def mask_skimmed_rows(
    data: pd.DataFrame,
    score: str,
    groupby_inner: typing.Sequence[str],
    groupby_outer: typing.Sequence[str] = tuple(),
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
    groupby_inner : Sequence[str]
        A sequence of column names in 'data' used for the inner grouping
        operation.

        Each unique combination of values in these columns defines an inner
        group.
    groupby_outer : Sequence[str], optional
        A sequence of column names in 'data' used for the outer grouping
        operation.

        Each unique combination of values in these columns defines an outer
        group. If not provided, no outer grouping is performed.
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
    mask = pd.Series(False, index=data.index)
    if len(data) == 0:
        return mask

    for _key, outer_group in robust_groupby(data, by=groupby_outer):
        outer_group_df = outer_group.reset_index()

        inner_groupby = outer_group_df.groupby(groupby_inner)
        __, inner_groups = zip(*inner_groupby[score])
        inner_group_indices = [
            *outer_group_df.groupby(groupby_inner).indices.values(),
        ]
        skimmed = skimmer(inner_groups, inner_group_indices, **kwargs)
        for skim in skimmed:
            mask.loc[skim] = True

    return mask
