from unittest.mock import Mock
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

from app.db.mongo import DB

def test_cleanup_ok():
    db = DB({
        "url": "mongodb://localhost:27017",
        "timeout": "1000",
        "mongo_history_days": "7"
    })
    db.daysold = 7

    delete_result = Mock()
    delete_result.deleted_count = 2
    
    mock_collection = Mock()
    

    mock_collection.delete_many.return_value = delete_result
    db.collection = mock_collection

    result = db.cleanup()
    
    assert result == 2
    mock_collection.delete_many.assert_called_once()

def test_cleanup_failure():
    db = DB({
        "url": "mongodb://localhost:27017",
        "timeout": "1000",
        "mongo_history_days": "7"
    })
    db.daysold = 7

    delete_result = Mock()
    delete_result.deleted_count = -1
    
    mock_collection = Mock()
    

    mock_collection.delete_many.side_effect = OperationFailure("Delete records failed")
    db.collection = mock_collection

    result = db.cleanup()
    
    assert result == -1
    mock_collection.delete_many.assert_called_once()

def test_cleanup_timeout():
    db = DB({
        "url": "mongodb://localhost:27017",
        "timeout": "1000",
        "mongo_history_days": "7"
    })
    db.daysold = 7
    db.timeout = 1000
    db.mongo_host = "localhost"
    db.mongo_port = 27017

    delete_result = Mock()
    delete_result.deleted_count = -1
    
    mock_collection = Mock()
    

    mock_collection.delete_many.side_effect = ServerSelectionTimeoutError("Database connection timed out")
    db.collection = mock_collection

    result = db.cleanup()
    
    assert result == -1
    mock_collection.delete_many.assert_called_once()