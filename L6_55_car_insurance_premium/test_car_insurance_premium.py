import pytest

from car_insurance_premium import (
    annual_premium,
    no_claim_bonus,
    claim_payout,
)


# -------------------------------
# Annual premium tests
# -------------------------------

def test_sedan_no_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600


def test_unknown_car_type():
    with pytest.raises(ValueError, match="unknown car type"):
        annual_premium("truck", 30, 0, False)


def test_driver_below_18():
    with pytest.raises(ValueError, match="driver too young"):
        annual_premium("sedan", 17, 0, False)


def test_young_driver_surcharge_and_anti_theft():
    assert annual_premium("sedan", 24, 1, True) == 15500


def test_senior_driver_surcharge():
    assert annual_premium("suv", 60, 1, False) == 17000


def test_hatchback_with_no_claims():
    assert annual_premium("hatchback", 30, 0, False) == 6400


def test_more_than_two_claims():
    assert annual_premium("sedan", 30, 3, False) == 24000


def test_anti_theft_discount():
    assert annual_premium("hatchback", 30, 1, True) == 7500


def test_two_claims_no_claim_discount_or_doubling():
    assert annual_premium("sedan", 30, 2, False) == 12000


# -------------------------------
# No-claim bonus tests
# -------------------------------

def test_negative_claim_free_years():
    with pytest.raises(ValueError, match="invalid years"):
        no_claim_bonus(-1)


def test_no_bonus():
    assert no_claim_bonus(0) == 0


def test_one_year_bonus():
    assert no_claim_bonus(1) == 20


def test_three_year_bonus():
    assert no_claim_bonus(3) == 35


def test_five_year_bonus():
    assert no_claim_bonus(5) == 50


# -------------------------------
# Claim payout tests
# -------------------------------

def test_negative_damage_cost():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(-1, 10000, 500, False)


def test_negative_deductible():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(1000, 10000, -1, False)


def test_total_loss():
    assert claim_payout(8000, 10000, 500, True) == 10000


def test_damage_equal_to_deductible():
    assert claim_payout(500, 10000, 500, False) == 0


def test_damage_below_deductible():
    assert claim_payout(300, 10000, 500, False) == 0


def test_normal_claim_payout():
    assert claim_payout(2000, 10000, 500, False) == 1500


def test_payout_cannot_exceed_insured_value():
    assert claim_payout(8000, 5000, 1000, False) == 5000