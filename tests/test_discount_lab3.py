"""Lab 3 - my boundary tests."""
import pytest

from app.tasks import calculate_discount


def test_case1_negative():
    with pytest.raises((ValueError, TypeError)):
        calculate_discount(-1, True)


def test_case2_zero():
    assert calculate_discount(0, False) == 0


def test_case3_small():
    assert calculate_discount(0.01, True) == pytest.approx(0.008)


def test_case4_normal_premium():
    assert calculate_discount(100, True) == 80


def test_case5_normal_regular():
    assert calculate_discount(100, False) == 100


def test_case6_below_max():
    assert calculate_discount(9999.99, True) == pytest.approx(7999.992)


def test_case7_max():
    assert calculate_discount(10000, True) == 8000


def test_case8_over_max():
    with pytest.raises((ValueError, TypeError)):
        calculate_discount(10000.01, False)


def test_case9_string_price():
    with pytest.raises(TypeError):
        calculate_discount("100", True)


def test_case10_int_flag():
    with pytest.raises(TypeError):
        calculate_discount(100, 1)


def test_case11_none_flag():
    with pytest.raises(TypeError):
        calculate_discount(100, None)
