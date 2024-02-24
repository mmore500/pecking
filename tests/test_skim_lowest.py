from pecking import skim_lowest


def test_skim_lowest_two_groups_signif():
    group1 = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4]
    group2 = [5, 5, 5, 6, 6, 6, 7, 7, 7, 8]

    samples = [group1, group2]
    labels = ["Lower", "Higher"]

    assert skim_lowest(samples, labels) == ["Lower"]


def test_skim_lowest_two_groups_insig():
    group1 = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4]
    group2 = [2, 2, 2, 3, 3, 3, 4, 4, 4, 5]

    samples = [group1, group2]

    assert skim_lowest(samples) == []


def test_skim_lowest_three_groups_signif1():
    group1 = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4]
    group2 = [4, 4, 4, 5, 5, 5, 6, 6, 6, 7]
    group3 = [7, 7, 7, 8, 8, 8, 9, 9, 9, 10]

    samples = [group1, group2, group3]
    labels = ["Bottom", "Middle", "Top"]

    assert skim_lowest(samples, labels) == ["Bottom"]


def test_skim_lowest_three_groups_signif2():
    group1 = [1, 1, 4, 2, 2, 2, 3, 3, 3, 4]
    group2 = [1, 1, 2, 2, 2, 2, 3, 4, 3, 4]
    group3 = [8, 8, 8, 9, 9, 9, 10, 10, 10, 11]

    samples = [group2, group3, group1]

    assert set(skim_lowest(samples)) == {0, 2}


def test_skim_lowest_three_groups_insig():
    group1 = [1, 1, 4, 2, 2, 2, 3, 3, 3, 4]
    group2 = [1, 1, 2, 2, 2, 2, 3, 4, 3, 4]
    group3 = [1, 0, 2, 4, 2, 2, 3, 4, 3, 4]

    samples = [group1, group2, group3]
    labels = ["Bottom", "Middle", "Top"]

    assert skim_lowest(samples, labels) == []


def test_skim_lowest_singular():
    group1 = [1, 1, 1]
    group2 = [1, 1, 1]

    samples = [group1, group2]
    labels = ["Bottom", "Middle"]

    assert skim_lowest(samples, labels) == []
