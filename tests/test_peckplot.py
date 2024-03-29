import functools
import os

from matplotlib import pyplot as plt
import pandas as pd
import pytest
import seaborn as sns

from pecking import peckplot, skim_highest, skim_lowest


def test_peckplot_empty():
    plt.clf()
    df = pd.DataFrame({"A": [], "B": []})
    with pytest.raises(ValueError):
        peckplot(df, score="B", x="A", y="B")


def test_peckplot_singleton():
    plt.clf()
    df = pd.DataFrame({"A": ["A"], "B": [0]})
    g = peckplot(df, score="B", x="A", y="B")
    assert g is not None


def test_peckplot1():
    plt.clf()
    df = pd.DataFrame(
        {
            "A": [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
            "B": [5, 6, 7, 8, 9, 9, 9, 9, 1, 2, 3, 4, 5, 5, 3, 5],
            "C": [5, 6, 7, 8, 9, 9, 9, 9, 1, 2, 3, 4, 5, 5, 3, 5],
        }
    )
    g = peckplot(df, score="C", y="B", col="A", col_group="inner")
    assert g is not None

    plt.savefig("/tmp/test_peckplot1.png")


def test_peckplot2():
    plt.clf()
    df = pd.DataFrame(
        {
            "A": [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
            "B": [5, 6, 7, 8, 9, 9, 9, 9, 1, 2, 3, 4, 5, 5, 3, 5],
            "C": [5, 6, 7, 8, 9, 9, 9, 9, 1, 2, 3, 4, 5, 5, 3, 5],
        }
    )
    g = peckplot(df, score="C", y="B", hue="A")
    assert g is not None

    plt.savefig("/tmp/test_peckplot2.png")


def test_peckplot3():
    plt.clf()
    df = pd.DataFrame(
        {
            "A": [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
            "B": [5, 6, 7, 8, 9, 9, 9, 9, 1, 2, 3, 4, 5, 5, 3, 5],
            "C": [5, 6, 7, 8, 9, 9, 9, 9, 1, 2, 3, 4, 5, 5, 3, 5],
        }
    )
    g = peckplot(df, score="C", y="B", x="A")
    assert g is not None

    plt.savefig("/tmp/test_peckplot3.png")


def test_peckplot4():
    plt.clf()
    df = pd.DataFrame(
        {
            "A": [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
            "B": [5, 6, 7, 8, 9, 9, 9, 9, 1, 2, 3, 4, 5, 5, 3, 5],
            "C": [5, 6, 7, 8, 9, 9, 9, 9, 1, 2, 3, 4, 5, 5, 3, 5],
        }
    )
    g = peckplot(df, score="C", y="B", x="A", hue="A")
    assert g is not None

    plt.savefig("/tmp/test_peckplot4.png")


def test_peckplot_neutral():
    plt.clf()
    df = pd.DataFrame(
        {
            "A": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
            ],
            "B": [
                -10,
                -9,
                -8,
                -5,
                -4,
                -9,
                -7,
                -6,
                5,
                6,
                7,
                8,
                9,
                9,
                9,
                9,
                1,
                2,
                3,
                4,
                5,
                5,
                3,
                5,
            ],
        }
    )
    g = peckplot(df, score="B", y="B", hue="A", x="A")
    assert g is not None

    plt.savefig("/tmp/test_peckplot_neutral.png")


def test_peckplot_fail():
    plt.clf()
    df = pd.DataFrame(
        {
            "A": [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
            "B": [5, 6, 7, 8, 9, 9, 9, 9, 5, 6, 7, 8, 9, 9, 9, 9],
        }
    )
    g = peckplot(df, score="B", y="B", x="A", hue="A")
    assert g is not None

    plt.savefig("/tmp/test_peckplot_fail.png")


def test_peckplot_outer():
    plt.clf()
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
    g = peckplot(
        concat,
        score="B",
        x="A",
        y="B",
        hue="A",
        col="outer",
        palette=sns.color_palette("tab10")[:2],
    )
    assert g is not None

    plt.savefig("/tmp/test_peckplot_outer.png")


def test_peckplot_outer_neutral():
    plt.clf()
    df = pd.DataFrame(
        {
            "A": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                3,
                3,
                3,
                3,
                3,
                3,
                3,
                3,
                4,
                4,
                4,
                4,
                4,
                4,
                4,
                4,
            ],
            "B": [
                -10,
                -9,
                -8,
                -5,
                -4,
                -9,
                -7,
                -6,
                -10,
                -9,
                -8,
                -5,
                -4,
                -9,
                -7,
                -6,
                5,
                6,
                7,
                8,
                9,
                9,
                9,
                9,
                5,
                6,
                7,
                8,
                9,
                9,
                9,
                9,
                1,
                2,
                3,
                4,
                5,
                5,
                3,
                5,
                1,
                2,
                3,
                4,
                5,
                5,
                3,
                5,
                -10,
                -9,
                -8,
                -5,
                -4,
                -9,
                -7,
                -6,
            ],
        },
    )
    df_a = df.copy()
    df_a["outer"] = "a"
    df_b = df.copy()
    df_b["outer"] = "b"
    concat = pd.concat([df_a, df_b])
    g = peckplot(
        concat,
        score="B",
        x="A",
        y="B",
        hue="A",
        col="outer",
        palette=sns.color_palette("tab10")[:5],
        skim_labels=["Worst", "Best"],
        skim_hatches=[".O", "*"],
    )
    assert g is not None

    plt.savefig("/tmp/test_peckplot_outer_neutral.png")


def test_peckplot_titanic():
    plt.clf()
    data = sns.load_dataset("titanic")
    g = peckplot(
        data,
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

    plt.savefig("/tmp/test_peckplot_titanic.png")


def test_peckplot_order():
    df = pd.read_csv(f"{os.path.dirname(__file__)}/assets/hstrat-sample.csv")

    x_order = [
        "surf-steady",
        "surf-hybrid",
        "surf-tilted",
    ]
    hue_order = [
        "npop4096-ngen100000",
        "npop65536-ngen100000",
    ]

    peckplot(
        data=df.reset_index(drop=True),
        kind="box",
        score="value",
        x="Algorithm",
        y="value",
        col="Scenario",
        row="variable",
        hue="Scale",
        x_group="outer",
        hue_group="inner",
        order=x_order,
        hue_order=hue_order,
        margin_titles=True,
        legend_width_inches=3,
    )

    plt.savefig("/tmp/test_peckplot_order.png")


def test_peckplot_overlapped_skims():
    df = pd.read_csv(f"{os.path.dirname(__file__)}/assets/hstrat-sample.csv")

    hue_order = [
        "surf-steady",
        "surf-hybrid",
        "surf-tilted",
    ]
    x_order = ["Triplet\nDistance", "Inner\nNode\nLoss"]

    peckplot(
        data=df,
        score="value",
        x="variable",
        y="value",
        col="Scenario",
        row="Scale",
        hue="Algorithm",
        x_group="outer",
        hue_group="inner",
        order=x_order,
        hue_order=hue_order,
        skim_hatches=("..OO", "*"),
        skim_labels=("Worst", "Best"),
        margin_titles=True,
        legend_width_inches=3,
    )

    plt.savefig("/tmp/test_peckplot_hstrat.png")
