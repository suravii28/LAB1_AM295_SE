from hypothesis import given, strategies as st

from car_insurance_premium_parser import (
    normalize_registration,
    total_claim_amount,
    driver_age,
)


@given(st.text() | st.none())
def test_normalize_registration_no_crash(s):
    try:
        result = normalize_registration(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"Registration crashed: {e}"


@given(st.text() | st.none())
def test_total_claim_amount_no_crash(s):
    try:
        result = total_claim_amount(s)
        assert isinstance(result, int)
        assert result >= 0
    except Exception as e:
        assert False, f"Claims crashed: {e}"


@given(st.text() | st.none())
def test_driver_age_no_crash(s):
    try:
        result = driver_age(s)
        assert isinstance(result, int)
        assert result == -1 or result >= 0
    except Exception as e:
        assert False, f"Driver age crashed: {e}"


def test_normalize_valid():
    assert normalize_registration(" ka 01-ab.1234 ") == "KA01AB1234"


def test_claims_valid():
    assert total_claim_amount("12000;4500;800") == 17300


def test_age_valid():
    assert driver_age("14/08/1999") == 27
