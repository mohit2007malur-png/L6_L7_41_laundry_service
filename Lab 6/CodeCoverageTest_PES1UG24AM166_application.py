
import pytest

from laundry_service import (
    extra_weight_charge,
    order_acceptable,
    dropoff_status,
)


# -------------------------------
# EXTRA WEIGHT CHARGE TESTS
# -------------------------------

def test_within_included_weight():
    assert extra_weight_charge("regular", 4, "standard", False) == 0


def test_unknown_garment_type():
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("unknown", 5, "standard", False)


def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -1, "standard", False)


def test_member_gets_extra_included_weight():
    assert extra_weight_charge("regular", 8, "standard", True) == 30


def test_bedding_member_does_not_get_extra_allowance():
    assert extra_weight_charge("bedding", 9, "standard", True) == 30


def test_standard_extra_weight_charge():
    assert extra_weight_charge("regular", 10, "standard", False) == 150


def test_express_extra_weight_charge():
    assert extra_weight_charge("regular", 10, "express", False) == 250


def test_other_speed_extra_weight_charge():
    assert extra_weight_charge("regular", 10, "economy", False) == 250


def test_standard_charge_above_10kg_extra():
    assert extra_weight_charge("regular", 16, "standard", False) == 495


def test_express_charge_above_10kg_extra():
    assert extra_weight_charge("regular", 16, "express", False) == 825


def test_other_speed_charge_above_10kg_extra():
    assert extra_weight_charge("regular", 16, "economy", False) == 715


# -------------------------------
# ORDER ACCEPTABILITY TESTS
# -------------------------------

def test_delicate_order_accepted():
    assert order_acceptable(10, 5, True) is True


def test_delicate_order_rejected():
    assert order_acceptable(10, 6, True) is False


def test_non_delicate_order_weight_exceeded():
    assert order_acceptable(26, 10, False) is False


def test_non_delicate_order_accepted():
    assert order_acceptable(25, 40, False) is True


def test_non_delicate_order_items_exceeded():
    assert order_acceptable(20, 41, False) is False


# -------------------------------
# DROPOFF STATUS TESTS
# -------------------------------

def test_bedding_order_accepted():
    assert dropoff_status(90, True, False) == "accepted"


def test_bedding_order_late():
    assert dropoff_status(80, True, False) == "late"


def test_bedding_order_rejected():
    assert dropoff_status(69, True, False) == "rejected"


def test_non_bedding_order_accepted():
    assert dropoff_status(60, False, False) == "accepted"


def test_non_bedding_order_late():
    assert dropoff_status(40, False, False) == "late"


def test_non_bedding_order_rejected():
    assert dropoff_status(39, False, False) == "rejected"


def test_express_order_cutoff():
    assert dropoff_status(90, False, True) == "accepted"
