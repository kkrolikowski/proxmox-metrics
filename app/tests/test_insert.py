from unittest.mock import Mock
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

from app.db.mongo import DB


def test_insert_ok():
    mock_result = Mock()
    mock_result = "12345qwerty"
    
    mock_collection = Mock()
    mock_collection.insert_one.return_value = mock_result

    mock_conf_value = Mock()
    mock_conf_value = {
        "url": "http",
        "timeout": "1000",
        "mongo_history_days": "7"
    }

    db_instance = DB(mock_conf_value)
    db_instance.collection = mock_collection

    test_data = {"vmid": "123", "name": "testvm"}
    
    result = db_instance.insert(test_data)

    assert result == {"id": "12345qwerty"}
    mock_collection.insert_one.assert_called_once_with(test_data)

def test_insert_operation_failure():
    mock_collection = Mock()
    mock_collection.insert_one.side_effect = OperationFailure("Insert operation failed")

    mock_conf_value = {
        "url": "http",
        "timeout": "1000",
        "mongo_history_days": "7"
    }

    db_instance = DB(mock_conf_value)
    db_instance.collection = mock_collection

    test_data = {"vmid": "123", "name": "testvm"}

    
    result = db_instance.insert(test_data)

    assert result is None or result == {}
    mock_collection.insert_one.assert_called_once()

def test_insert_timeout_error():
    mock_collection = Mock()
    mock_collection.insert_one.side_effect = ServerSelectionTimeoutError("Database connection timed out")

    mock_conf_value = {
        "url": "mongodb://localhost:27017",
        "timeout": "1000",
        "mongo_history_days": "7"
    }

    db_instance = DB(mock_conf_value)
    db_instance.collection = mock_collection

    test_data = {"vmid": "999", "name": "timeout_vm"}


    result = db_instance.insert(test_data)

    assert result == None
    
    mock_collection.insert_one.assert_called_once()

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