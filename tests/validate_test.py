import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.adapters.client_adapter import ClientAdapter


def test_validate_valid_workorder():
    adapter = ClientAdapter()
    
    valid_wo = {
        "orderNo": 1,
        "summary": "Test",
        "creationDate": "2024-12-08T10:00:00Z",
        "lastUpdateDate": "2024-12-08T11:00:00Z"
    }
    
    result = adapter.validate_work_order(valid_wo)
    assert result == True


def test_validate_workorder_missing_field():
    adapter = ClientAdapter()
    
    invalid_wo = {
        "orderNo": 2,
        "summary": "Test"
    }
    
    result = adapter.validate_work_order(invalid_wo)
    assert result == False


def test_validate_workorder_empty_field():
    adapter = ClientAdapter()
    
    empty_wo = {
        "orderNo": 3,
        "summary": "",
        "creationDate": "2024-12-08T10:00:00Z",
        "lastUpdateDate": "2024-12-08T11:00:00Z"
    }
    
    result = adapter.validate_work_order(empty_wo)
    assert result == False
