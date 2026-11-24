
import pytest
from hypothesis import given, strategies as st

from laundry_service import (
    parse_order,
    weight_average,
    payable_charge,
)


# -----------------------------------------
# 1. FUZZ TESTING: parse_order()
# -----------------------------------------

@given(
    garment=st.text(
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
        min_size=0,
        max_size=30,
    ),
    weight=st.floats(
        min_value=-100000,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_parse_order_no_crash(garment, weight):
    text = f"{garment}:{weight!r}"

    result = parse_order(text)

    assert result == (garment.strip().title(), weight)


def test_parse_order_missing_separator():
    with pytest.raises(ValueError):
        parse_order("regular6")


def test_parse_order_multiple_separators():
    with pytest.raises(ValueError):
        parse_order("regular:6:extra")


def test_parse_order_invalid_weight():
    with pytest.raises(ValueError):
        parse_order("regular:abc")


# -----------------------------------------
# 2. FUZZ TESTING: weight_average()
# -----------------------------------------

@given(
    weights=st.lists(
        st.integers(min_value=-100000, max_value=100000),
        min_size=1,
        max_size=100,
    )
)
def test_weight_average_no_crash(weights):
    weights_csv = ",".join(map(str, weights))

    result = weight_average(weights_csv)

    expected = sum(weights) // len(weights)

    assert result == expected


def test_weight_average_empty_input():
    with pytest.raises(ValueError):
        weight_average("")


def test_weight_average_invalid_value():
    with pytest.raises(ValueError):
        weight_average("3,abc,8")


def test_weight_average_trailing_comma():
    with pytest.raises(ValueError):
        weight_average("3,5,8,")


# -----------------------------------------
# 3. FUZZ TESTING: payable_charge()
# -----------------------------------------

@given(
    charge=st.floats(
        min_value=-100000,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False,
    ),
    discount=st.floats(
        min_value=-100000,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_payable_charge_no_crash(charge, discount):
    text = f"{charge!r}|{discount!r}"

    result = payable_charge(text)

    expected = max(charge * 1.18 - discount, 0)

    assert result == pytest.approx(expected)
    assert result >= 0


def test_payable_charge_zero_floor():
    assert payable_charge("100|500") == 0


def test_payable_charge_positive_result():
    assert payable_charge("300|40") == pytest.approx(314)


def test_payable_charge_missing_separator():
    with pytest.raises(ValueError):
        payable_charge("30040")


def test_payable_charge_invalid_charge():
    with pytest.raises(ValueError):
        payable_charge("abc|40")


def test_payable_charge_invalid_discount():
    with pytest.raises(ValueError):
        payable_charge("300|abc")
