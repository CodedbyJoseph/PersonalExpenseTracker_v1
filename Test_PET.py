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
    assert data[0]["year"] == datetime.now().year
    assert data[0]["month"] == datetime.now().strftime("%B")
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
    assert "Remaining this month: 480.0" in captured.out

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

def test_remove_expense(monkeypatch, tmp_path):
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

    # this test asserts that the correct entry is removed
    # we use a dummy expenses list as to not alter real user data within the json


def test_main_budget_warning(capsys, monkeypatch):
    # 4 expenses totalling 450, leaving only 50 of 500 budget (10%, under 20% threshold)
    expenses = [
        {"year": 2026, "month": "June", "category": "Food", "amount": "100"},
        {"year": 2026, "month": "June", "category": "Transport", "amount": "150"},
        {"year": 2026, "month": "June", "category": "Shopping", "amount": "100"},
        {"year": 2026, "month": "June", "category": "Bills", "amount": "100"},
    ]

    # both files appear to exist so main skips creating defaults
    monkeypatch.setattr("os.path.exists", lambda path: True)
    monkeypatch.setattr("os.path.getsize", lambda path: 3)

    # return the expenses list for data.json and "500" for budget.txt
    def fake_open(filename, *args, **kwargs):
        if "data.json" in str(filename):
            return io.StringIO(json.dumps(expenses))
        return io.StringIO("500")

    monkeypatch.setattr("builtins.open", fake_open)

    # any input triggers the else branch which calls exit()
    monkeypatch.setattr("builtins.input", lambda _: "q")

    # exit() raises SystemExit, catch it so the test doesn't crash
    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "Be careful. Budget remaining: 50.0" in captured.out


def test_main_no_budget_warning(capsys, monkeypatch):
    # 4 expenses totalling 399, leaving 101 of 500 budget (over 20% threshold, no warning)
    expenses = [
        {"year": 2026, "month": "June", "category": "Food", "amount": "100"},
        {"year": 2026, "month": "June", "category": "Transport", "amount": "150"},
        {"year": 2026, "month": "June", "category": "Shopping", "amount": "100"},
        {"year": 2026, "month": "June", "category": "Bills", "amount": "49"},
    ]

    monkeypatch.setattr("os.path.exists", lambda path: True)
    monkeypatch.setattr("os.path.getsize", lambda path: 3)

    def fake_open(filename, *args, **kwargs):
        if "data.json" in str(filename):
            return io.StringIO(json.dumps(expenses))
        return io.StringIO("500")

    monkeypatch.setattr("builtins.open", fake_open)
    monkeypatch.setattr("builtins.input", lambda _: "q")

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "Be careful" not in captured.out
