from datetime import datetime


def normalize_registration(plate):
    """Normalize a registration number safely."""
    if plate is None:
        return ""

    try:
        plate = str(plate).strip().upper()
        for ch in [' ', '-', '.']:
            plate = plate.replace(ch, '')
        return plate
    except Exception:
        return ""


def total_claim_amount(text):
    """Add valid non-negative integer claim amounts."""
    if text is None:
        return 0

    try:
        amounts = str(text).split(';')
    except Exception:
        return 0

    total = 0

    for amount in amounts:
        try:
            value = int(amount.strip())
            if value >= 0:
                total += value
        except (ValueError, TypeError, OverflowError):
            continue

    return total


def driver_age(dob, current_year=2026):
    """Calculate age safely from a DD/MM/YYYY date."""
    try:
        if not isinstance(dob, str):
            return -1

        if not isinstance(current_year, int) or isinstance(current_year, bool):
            return -1

        dob = dob.strip()
        parsed_date = datetime.strptime(dob, "%d/%m/%Y")

        if parsed_date.strftime("%d/%m/%Y") != dob:
            return -1

        if parsed_date.year > current_year:
            return -1

        return current_year - parsed_date.year

    except Exception:
        return -1


def main():
    print("==== Running normalize_registration ====")
    value = input("Enter a registration number (e.g. ka 01 ab 1234): ")
    print("Normalized registration:", normalize_registration(value))

    print("\n==== Running total_claim_amount ====")
    value = input("Enter past claim amounts separated by ; (e.g. 12000;4500;800): ")
    print("Total claimed:", total_claim_amount(value))

    print("\n==== Running driver_age ====")
    value = input("Enter the driver's date of birth as DD/MM/YYYY (e.g. 14/08/1999): ")
    print("Driver age in 2026:", driver_age(value))


if __name__ == "__main__":
    main()
