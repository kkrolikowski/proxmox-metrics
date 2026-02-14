from unittest.mock import Mock
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

from app.db.mongo import DB

def test_collect_ok():
    mock_collection = Mock()
    expected_result = [{
        "vmid": "111",
        "name": "testvm",
        "size": "10000",
        "duration": "111",
        "timestamp": "123",
        "status": "ok"
    }]

    mock_collection.aggregate.return_value = expected_result

    db = DB({
        "url": "mongodb://localhost:27017",
        "timeout": "1000",
        "mongo_history_days": "7"
    })
    db.collection = mock_collection

    result = db.collect()

    assert result == expected_result
    mock_collection.aggregate.assert_called_once()

def test_collect_operation_failure():
    mock_collection = Mock()
    expected_result = []

    mock_collection.aggregate.side_effect = OperationFailure("Error collecting data")

    db = DB({
        "url": "mongodb://localhost:27017",
        "timeout": "1000",
        "mongo_history_days": "7"
    })
    db.collection = mock_collection

    result = db.collect()

    assert result == expected_result
    mock_collection.aggregate.assert_called_once()

def test_collect_timeout():
    mock_collection = Mock()
    expected_result = []

    mock_collection.aggregate.side_effect = ServerSelectionTimeoutError("Database connection timed out")

    db = DB({
        "url": "mongodb://localhost:27017",
        "timeout": "1000",
        "mongo_history_days": "7"
    })
    db.collection = mock_collection

    result = db.collect()

    assert result == expected_result
    mock_collection.aggregate.assert_called_once()