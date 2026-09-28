import pytest

@pytest.fixture
def numbers():
    return [1,2,3]

def test_sum(numbers):
    assert sum(numbers) == 6

@pytest.mark.parametrize("a,b,expected", [(1,2,3),(2,3,5)])
def test_add(a,b,expected):
    assert a + b == expected