# tests/test_tracker.py
import pytest
import os
import tempfile
from tracker_logic import calculate_total, validate_amount, save_to_csv, load_from_csv

# --- Total Calculation Tests ---
def test_total_empty():
    assert calculate_total([]) == 0.0

def test_total_single():
    assert calculate_total([{"amount": 9.99}]) == 9.99

def test_total_multiple():
    expenses = [{"amount": 10.0}, {"amount": 5.5}, {"amount": 3.75}]
    assert calculate_total(expenses) == 19.25

def test_total_rounding():
    expenses = [{"amount": 0.1}, {"amount": 0.2}]
    assert calculate_total(expenses) == 0.3  # float precision handled

# --- Invalid Input Tests ---
def test_validate_valid_amount():
    assert validate_amount("25.50") == 25.50

def test_validate_negative_raises():
    with pytest.raises(ValueError):
        validate_amount("-10")

def test_validate_zero_raises():
    with pytest.raises(ValueError):
        validate_amount("0")

def test_validate_string_raises():
    with pytest.raises(ValueError):
        validate_amount("abc")

def test_validate_empty_raises():
    with pytest.raises(ValueError):
        validate_amount("")

# --- CSV Save/Load Tests ---
SAMPLE = [
    {"description": "Coffee", "category": "Food", "amount": 4.5},
    {"description": "Bus", "category": "Transport", "amount": 2.0},
]

def test_csv_save_and_load():
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        path = f.name
    try:
        save_to_csv(SAMPLE, path)
        loaded = load_from_csv(path)
        assert len(loaded) == 2
        assert loaded[0]["description"] == "Coffee"
        assert loaded[1]["amount"] == 2.0
    finally:
        os.unlink(path)

def test_load_nonexistent_file():
    result = load_from_csv("nonexistent_file.csv")
    assert result == []

def test_csv_round_trip_total():
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        path = f.name
    try:
        save_to_csv(SAMPLE, path)
        loaded = load_from_csv(path)
        assert calculate_total(loaded) == 6.5
    finally:
        os.unlink(path)

