# tracker_logic.py
import csv
import os

def calculate_total(expenses: list[dict]) -> float:
    """Sum all expense amounts."""
    return round(sum(e["amount"] for e in expenses), 2)

def validate_amount(value: str) -> float:
    """Raise ValueError on invalid input."""
    amount = float(value)
    if amount <= 0:
        raise ValueError("Amount must be positive.")
    return round(amount, 2)

def save_to_csv(expenses: list[dict], filepath: str) -> None:
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["description", "category", "amount"])
        writer.writeheader()
        writer.writerows(expenses)

def load_from_csv(filepath: str) -> list[dict]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        expenses = []
        for row in reader:
            row["amount"] = float(row["amount"])
            expenses.append(row)
    return expenses