from carapace import (Data)

def test_subset():
    assert Data.subset(True, True)
    assert Data.subset([1, 2, 3, 4], [1, 2, 3, 4])
    assert Data.subset(dict(a=1), dict(a=1, b=2))
    assert Data.subset(dict(a=dict(a=1), b=2), dict(a=dict(a=1, b=2), b=2, c=3))
    assert Data.subset([dict(a=1), 2], [dict(a=1, b=2), 2])

    assert not Data.subset(False, True)
    assert not Data.subset([1, 2, 3], [1, 2, 3, 4])
    assert not Data.subset(dict(a=2), dict(a=1))
    assert not Data.subset(dict(a=1, b=2), dict(a=1))
    assert not Data.subset([dict(a=1), 2], [dict(b=2), 2])

def test_deep_append():
    assert Data.deep_append([1, 2, 3], 4) == [1, 2, 3, 4]
    assert Data.deep_append([1, 2, 3], [4, [5, 6], 7]) == [1, 2, 3, 4, 5, 6, 7]