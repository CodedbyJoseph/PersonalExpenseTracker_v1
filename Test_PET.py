import pytest
from PersonalExpenseTracker_v1 import log_expense

def test_log_expense(monkeypatch, tmp_path):
    inputs = iter(["20", "Food", "lunch"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    temp_file = tmp_path / "data.txt"
    real_open = open
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: real_open(temp_file, "a"))
    
    log_expense()
    
    content = temp_file.read_text()
    assert "Food" in content
    assert "20" in content
    assert "lunch" in content
