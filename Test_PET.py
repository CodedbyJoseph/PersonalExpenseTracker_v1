import pytest
import json
from PersonalExpenseTracker_v1 import log_expense, view_summary

def test_log_expense(monkeypatch, tmp_path):
    # simulate user typing "20", "Food", "lunch" when input() is called
    inputs = iter(["20", "Food", "lunch"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # create a temporary json file so the real data.json is not touched
    temp_file = tmp_path / "data.json"
    real_open = open
    # redirect any open() call to use the temp file instead of data.json
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: real_open(temp_file, "w"))

    # start with an empty expenses list and call the function
    expenses = []
    log_expense(expenses)

    # load the temp file back as a python list to check what was written
    with real_open(temp_file, "r") as file:
        data = json.load(file)

    # check that exactly one expense was added with the correct values
    assert len(data) == 1
    assert data[0]["category"] == "Food"
    assert data[0]["amount"] == "20"
    assert data[0]["description"] == "lunch"


def test_view_summary(capsys, monkeypatch):
    expenses = [
        {"year": 2026, "month": "June", "category": "Food", "amount": "15"},
        {"year": 2026, "month": "June", "category": "Transportation", "amount": "5"},
    ]

    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: __import__("io").StringIO("500"))

    view_summary(expenses)

    captured = capsys.readouterr()
    assert "Spent: 20" in captured.out
    assert "Budget: 500" in captured.out
    assert "Remaining this month: 480" in captured.out
