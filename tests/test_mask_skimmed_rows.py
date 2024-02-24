import pandas as pd

from pecking import mask_skimmed_rows


def test_mask_skimmed_empty():
    df = pd.DataFrame({"A": [], "B": []})
    mask = mask_skimmed_rows(df, score="B", groupby_inner=["A"])
    assert len(mask) == 0


def test_mask_skimmed_singleton():
    df = pd.DataFrame({"A": ["A"], "B": [0]})
    mask = mask_skimmed_rows(df, score="B", groupby_inner=["A"])
    assert mask.to_list() == [False]


def test_mask_skimmed_rows():
    df = pd.DataFrame(
        {
            "A": [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
            "B": [5, 6, 7, 8, 9, 9, 9, 9, 1, 2, 3, 4, 5, 5, 3, 5],
        }
    )
    mask = mask_skimmed_rows(df, score="B", groupby_inner=["A"])
    assert (mask == (df["A"] == 1)).all()


def test_mask_skimmed_rows_fail():
    df = pd.DataFrame(
        {
            "A": [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
            "B": [5, 6, 7, 8, 9, 9, 9, 9, 5, 6, 7, 8, 9, 9, 9, 9],
        }
    )
    mask = mask_skimmed_rows(df, score="B", groupby_inner=["A"])
    assert not mask.any()


def test_mask_skimmed_rows_outer():
    df = pd.DataFrame(
        {
            "A": [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
            "B": [5, 6, 7, 8, 9, 9, 9, 9, 1, 2, 3, 4, 5, 5, 3, 5],
        }
    )
    df_a = df.copy()
    df_a["outer"] = "a"
    df_b = df.copy()
    df_b["outer"] = "b"
    concat = pd.concat([df_a, df_b])
    mask = mask_skimmed_rows(
        concat, score="B", groupby_inner=["A"], groupby_outer=["outer"]
    )
    assert (mask == (concat["A"] == 1)).all()
