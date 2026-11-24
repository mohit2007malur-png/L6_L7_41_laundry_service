
import pytest

from laundry_service import (
    extra_weight_charge,
    order_acceptable,
    dropoff_status,
)


# EXTRA WEIGHT CHARGE: decision branches

def test_unknown_garment():
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("unknown", 5, "standard", False)


def test_valid_garment():
    assert extra_weight_charge("regular", 5, "standard", False) == 0


def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -1, "standard", False)


def test_non_negative_weight():
    assert extra_weight_charge("regular", 5, "standard", False) == 0


def test_member_regular():
    assert extra_weight_charge("regular", 8, "standard", True) == 30


def test_non_member_regular():
    assert extra_weight_charge("regular", 6, "standard", False) == 30


def test_member_bedding():
    assert extra_weight_charge("bedding", 9, "standard", True) == 30


def test_no_extra_weight():
    assert extra_weight_charge("regular", 5, "standard", False) == 0


def test_extra_weight_standard():
    assert extra_weight_charge("regular", 10, "standard", False) == 150


def test_extra_weight_express():
    assert extra_weight_charge("regular", 10, "express", False) == 250


def test_extra_weight_other_speed():
    assert extra_weight_charge("regular", 10, "economy", False) == 250


def test_extra_above_10_standard():
    assert extra_weight_charge("regular", 16, "standard", False) == 495


def test_extra_above_10_express():
    assert extra_weight_charge("regular", 16, "express", False) == 825


def test_extra_above_10_other_speed():
    assert extra_weight_charge("regular", 16, "economy", False) == 715


# ORDER ACCEPTABILITY: decision branches

def test_delicate_items_within_limit():
    assert order_acceptable(10, 5, True) is True


def test_delicate_items_over_limit():
    assert order_acceptable(10, 6, True) is False


def test_non_delicate_weight_over_limit():
    assert order_acceptable(26, 10, False) is False


def test_non_delicate_weight_at_limit():
    assert order_acceptable(25, 40, False) is True


def test_non_delicate_items_over_limit():
    assert order_acceptable(20, 41, False) is False


# DROPOFF STATUS: decision branches

def test_bedding_accepted():
    assert dropoff_status(90, True, False) == "accepted"


def test_bedding_late():
    assert dropoff_status(80, True, False) == "late"


def test_bedding_rejected():
    assert dropoff_status(69, True, False) == "rejected"


def test_non_bedding_accepted():
    assert dropoff_status(60, False, False) == "accepted"


def test_non_bedding_late():
    assert dropoff_status(40, False, False) == "late"


def test_non_bedding_rejected():
    assert dropoff_status(39, False, False) == "rejected"


def test_express_cutoff():
    assert dropoff_status(90, False, True) == "accepted"


def test_express_bedding_cutoff():
    assert dropoff_status(120, True, True) == "accepted"
