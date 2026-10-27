
"""Manage pharmacy stock, prescriptions, and dispensing operations."""

import ast
import hashlib
import hmac
import json
import math
import os
import secrets
from datetime import date, datetime
from pathlib import Path

medicines = {}


def add_medicine(
    name, qty=0, price=0.0, expiry="2099-12-31", audit=None
):
    """Add medicine stock and optionally record an audit entry."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Medicine name must be a non-empty string.")
    if not isinstance(qty, int) or isinstance(qty, bool) or qty < 0:
        raise ValueError("Quantity must be a non-negative integer.")
    if not isinstance(price, (int, float)) or isinstance(price, bool):
        raise ValueError("Price must be a number.")
    if not math.isfinite(price) or price < 0:
        raise ValueError("Price must be finite and non-negative.")

    datetime.strptime(expiry, "%Y-%m-%d")
    if audit is None:
        audit = []

    if name not in medicines:
        medicines[name] = {
            "qty": 0,
            "price": price,
            "expiry": expiry,
        }
    else:
        medicines[name]["price"] = price
        medicines[name]["expiry"] = expiry

    medicines[name]["qty"] += qty
    audit.append(
        f"{datetime.now()}: Stocked {qty} units of {name}"
    )
    return audit


def dispense_medicine(name, qty):
    """Dispense medicine only when sufficient stock is available."""
    if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
        raise ValueError("Dispensing quantity must be a positive integer.")
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")
    if medicines[name]["qty"] < qty:
        raise ValueError("Insufficient stock.")

    medicines[name]["qty"] -= qty


def get_quantity(name):
    """Return the available quantity for a medicine."""
    return medicines[name]["qty"]


def is_expired(name):
    """Return whether a medicine's expiry date is in the past."""
    expiry = datetime.strptime(
        medicines[name]["expiry"], "%Y-%m-%d"
    ).date()
    return expiry < date.today()


def bill_amount(prescription):
    """Calculate the total cost of a prescription."""
    total = 0.0
    for name, qty in prescription:
        if name not in medicines:
            raise KeyError(f"Medicine not found: {name}")
        if not isinstance(qty, int) or isinstance(qty, bool) or qty < 0:
            raise ValueError("Prescription quantities must be non-negative.")
        total += medicines[name]["price"] * qty
    return total


def calculate_dosage(formula):
    """Evaluate basic arithmetic without executing arbitrary code."""
    binary_operators = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.FloorDiv: lambda a, b: a // b,
        ast.Mod: lambda a, b: a % b,
    }
    unary_operators = {
        ast.UAdd: lambda value: value,
        ast.USub: lambda value: -value,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if (
            isinstance(node, ast.Constant)
            and type(node.value) in (int, float)
        ):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in binary_operators:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return binary_operators[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in unary_operators:
            return unary_operators[type(node.op)](evaluate(node.operand))
        raise ValueError("Only basic arithmetic expressions are allowed.")

    try:
        tree = ast.parse(formula, mode="eval")
        result = evaluate(tree)
    except (SyntaxError, TypeError, ZeroDivisionError) as exc:
        raise ValueError("Invalid dosage formula.") from exc

    if not isinstance(result, (int, float)) or not math.isfinite(result):
        raise ValueError("Dosage result must be finite.")
    return result


def patient_id(name, phone):
    """Generate a keyed patient identifier using an environment secret."""
    secret = os.environ.get("PATIENT_ID_SECRET")
    if not secret:
        raise RuntimeError(
            "Set PATIENT_ID_SECRET before generating patient IDs."
        )

    message = f"{name}:{phone}".encode("utf-8")
    return hmac.new(
        secret.encode("utf-8"), message, hashlib.sha256
    ).hexdigest()


def generate_rx_number():
    """Generate an unpredictable prescription reference."""
    return f"RX-{secrets.randbelow(900000) + 100000}"


def save_stock(file="pharmacy.json"):
    """Save stock records to a JSON file."""
    with Path(file).open("w", encoding="utf-8") as stock_file:
        json.dump(medicines, stock_file, indent=2)


def load_stock(file="pharmacy.json"):
    """Load and validate stock records from a JSON file."""
    try:
        with Path(file).open("r", encoding="utf-8") as stock_file:
            stock_data = json.load(stock_file)
    except FileNotFoundError:
        return

    if not isinstance(stock_data, dict):
        raise ValueError("Stock file must contain a JSON object.")

    for name, details in stock_data.items():
        if not isinstance(name, str) or not isinstance(details, dict):
            raise ValueError(f"Invalid stock record: {name!r}")

        qty = details.get("qty")
        price = details.get("price")
        expiry = details.get("expiry")

        invalid_qty = (
            not isinstance(qty, int)
            or isinstance(qty, bool)
            or qty < 0
        )
        invalid_price = (
            not isinstance(price, (int, float))
            or isinstance(price, bool)
            or not math.isfinite(price)
            or price < 0
        )
        invalid_expiry = not isinstance(expiry, str)

        if invalid_qty or invalid_price or invalid_expiry:
            raise ValueError(f"Invalid stock record: {name!r}")

        try:
            datetime.strptime(expiry, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError(
                f"Invalid expiry date for {name!r}"
            ) from exc

    medicines.clear()
    medicines.update(stock_data)


def print_label(name):
    """Print a dispensing label without invoking a system shell."""
    print(f"Dispensing label: {name}")


def expiring_soon(days=30):
    """Return medicines expiring within the requested number of days."""
    if not isinstance(days, int) or isinstance(days, bool) or days < 0:
        raise ValueError("Days must be a non-negative integer.")

    today = date.today()
    return [
        name
        for name, details in medicines.items()
        if 0 <= (
            datetime.strptime(details["expiry"], "%Y-%m-%d").date()
            - today
        ).days <= days
    ]


def pharmacist_login(password):
    """Verify a password configured in the environment."""
    expected_password = os.environ.get("PHARMACIST_PASSWORD", "")
    return bool(expected_password) and hmac.compare_digest(
        password, expected_password
    )


def print_stock():
    """Print a report of the current medicine inventory."""
    print("===== Pharmacy Stock Report =====")
    for name, details in medicines.items():
        print(
            f"{name} -> {details['qty']} units, Rs. "
            f"{details['price']} exp {details['expiry']}"
        )


def main():
    """Run a demonstration of pharmacy management features."""
    add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15")
    add_medicine("Cetirizine 10mg", 10, 2.0, "2027-03-31")
    add_medicine("Test Product", 25, 1.0)
    dispense_medicine("Paracetamol 500mg", 30)

    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))
    print(
        "Bill:",
        bill_amount(
            [("Paracetamol 500mg", 10), ("Amoxicillin 250mg", 5)]
        ),
    )
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    print(
        "Login:",
        pharmacist_login(os.environ.get("PHARMACIST_PASSWORD", "")),
    )
    print_label("Paracetamol 500mg")
    save_stock()
    load_stock()
    print_stock()


if __name__ == "__main__":
    main()
