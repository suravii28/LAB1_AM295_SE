# L7 — Car Insurance Premium: Fuzzing for Input Validation Bugs

This folder contains the Lab 7 deliverables for the car insurance premium parser.

## Files

- `car_insurance_premium_parser.py`: hardened parser with safe handling for malformed input.
- `test_car_insurance_premium_parser.py`: three Hypothesis no-crash properties and three regression tests.
- `SRN_NAME_LAB7.pdf`: screenshots SS1–SS4 and viva/reflection notes (to be added after SS4 is captured).

## Run

Install dependencies:

```bash
python3 -m pip install hypothesis pytest
```

Run the application:

```bash
python3 car_insurance_premium_parser.py
```

Run the tests:

```bash
python3 -m pytest -v test_car_insurance_premium_parser.py
```

Invalid-input conventions:
- Registration normalization returns an empty string for `None` or an unconvertible value.
- Claim parsing ignores empty, malformed, and negative entries; `None` returns zero.
- Date parsing returns `-1` for invalid values or invalid calendar dates.
