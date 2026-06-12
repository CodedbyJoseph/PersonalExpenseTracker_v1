import pytest
import json
import io
from datetime import datetime
from PersonalExpenseTracker_v1 import (
    log_expense, view_summary, view_breakdown, main, current_total_spent, remove_expense
)

def test_current_spent():
    year = datetime.now().year
    month = datetime.now().strftime("%B")
    prev_month = datetime(datetime.now().year, datetime.now().month - 1, 1).strftime("%B")

    expenses = [
        {"year": year, "month": month, "category": "Food", "amount": "60"},
        {"year": year, "month": month, "category": "Transport", "amount": "40"},
        {"year": year, "month": prev_month, "category": "Food", "amount": "50"},
    ]

    assert current_total_spent(expenses) == 100

    # assert that the current expense total is correct based on mock expense list

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

    assert data[0]["year"] == datetime.now().year
    assert data[0]["month"] == datetime.now().strftime("%B")
    assert data[0]["category"] == "Food"
    assert data[0]["amount"] == "20"
    assert data[0]["description"] == "lunch"

    # assert that exactly one expense was added, with the correct values, based on mock logged expense

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
    assert "Remaining this month: 480.0" in captured.out

    # assert summary displays correct amount spent, budget, and remaining for current period based on mock expenses

def test_breakdown(capsys):
    year = datetime.now().year
    month = datetime.now().strftime("%B")
    prev_month = datetime(datetime.now().year, datetime.now().month - 1, 1).strftime("%B")

    expenses = [
        {"year": year, "month": month, "category": "Food", "amount": "60"},
        {"year": year, "month": month, "category": "Food", "amount": "10"},
        {"year": year, "month": month, "category": "Transport", "amount": "40"},
        {"year": year, "month": prev_month, "category": "Food", "amount": "50"},
    ]

    view_breakdown(expenses)

    captured = capsys.readouterr()
    assert f"{month} {year} Breakdown" in captured.out
    assert "Food" in captured.out
    assert "Transport" in captured.out
    assert "70.0" in captured.out
    assert "40.0" in captured.out
    assert "50.0" not in captured.out

    # assert that correct categories and their amounts are displayed for current period using mock expenses list

def test_remove_expense(monkeypatch, tmp_path, capsys):
    year = datetime.now().year
    month = datetime.now().strftime("%B")
    prev_month = datetime(datetime.now().year, datetime.now().month - 1, 1).strftime("%B")

    expenses = [
        {"year": year, "month": month, "category": "Food", "amount": "60"},
        {"year": year, "month": month, "category": "Transport", "amount": "40"},
        {"year": year, "month": prev_month, "category": "Food", "amount": "50"},
    ]

    monkeypatch.setattr("builtins.input", lambda _: "2")

    temp_file = tmp_path / "data.json"
    real_open = open
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: real_open(temp_file, "w"))
    
    remove_expense(expenses)

    assert expenses == [
        {"year": year, "month": month, "category": "Food", "amount": "60"},
        {"year": year, "month": prev_month, "category": "Food", "amount": "50"},
    ]

    captured = capsys.readouterr()

    before_current = [
        {"year": year, "month": month, "category": "Food", "amount": "60"},
        {"year": year, "month": month, "category": "Transport", "amount": "40"},
    ]
    for index, expense in enumerate(before_current):
        assert f"{index+1} {expense}" in captured.out

    expected_current = [
        {"year": year, "month": month, "category": "Food", "amount": "60"},
    ]
    for index, expense in enumerate(expected_current):
        assert f"{index+1} {expense}" in captured.out

    with real_open(temp_file, "r") as file:
        data = json.load(file)

    assert data == expenses

    # this test asserts that original and then current expenses are printed
    # correct expense is removed from expenses
    # we use a dummy expenses list as to not alter real user data within the json

def test_main_budget_warning(capsys, monkeypatch):
    # mock expenses totalling 350 out of 400 budget, leaving less than 20% left
    expenses = [
        {"year": 2026, "month": "June", "category": "Food", "amount": "100"},
        {"year": 2026, "month": "June", "category": "Transport", "amount": "150"},
        {"year": 2026, "month": "June", "category": "Shopping", "amount": "50"},
        {"year": 2026, "month": "June", "category": "Bills", "amount": "50"},
    ]

    # makes os.path.exists return True for all files so the json appears to exist and calls open()
    monkeypatch.setattr("os.path.exists", lambda path: True)

    # redirect all open() calls to read a fake file containing int 400 and return it
    # this is the budget I will set for this test
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: io.StringIO("400"))

    # redirect json.load to return mock expenses instead of mock json file contents (400)
    monkeypatch.setattr("json.load", lambda file: expenses)

    # make input() return invalid number to cause exit() which ends main()
    monkeypatch.setattr("builtins.input", lambda _: "q")

    # while expecting a SystemExit, call main()
    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "Be careful. Budget remaining: 50.0" in captured.out

    # assert that warning message is displayed due to <= 20% budget left

def test_main_no_budget_warning(capsys, monkeypatch):
    # mock expenses totalling 300 out of 400 budget, leaving more than 20% left
    expenses = [
        {"year": 2026, "month": "June", "category": "Food", "amount": "50"},
        {"year": 2026, "month": "June", "category": "Transport", "amount": "150"},
        {"year": 2026, "month": "June", "category": "Shopping", "amount": "50"},
        {"year": 2026, "month": "June", "category": "Bills", "amount": "50"},
    ]

    monkeypatch.setattr("os.path.exists", lambda path: True)

    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: io.StringIO("400"))

    monkeypatch.setattr("json.load", lambda file: expenses)

    monkeypatch.setattr("builtins.input", lambda _: "q")

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "Be careful" not in captured.out

    # assert that warning message is not displayed
