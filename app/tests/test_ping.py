from unittest.mock import Mock
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

from app.db.mongo import DB

def test_ping_ok():
    expected_result = "ok"

    db = DB({
        "url": "mongodb://localhost:27017",
        "timeout": "1000",
        "mongo_history_days": "7"
    })

    mock_db = Mock()
    mock_db.command.return_value = {"ok": 1.0}
    
    db.db = mock_db
    
    result = db.ping()

    assert result == expected_result
    mock_db.command.assert_called_once_with("ping")


def test_ping_failure():
    db = DB({
        "url": "mongodb://localhost:27017",
        "timeout": "1000",
        "mongo_history_days": "7"
    })

    mock_db = Mock()
    mock_db.command.side_effect = OperationFailure("Ping failed")
    
    db.db = mock_db
    
    result = db.ping()

    assert result is None
    mock_db.command.assert_called_once_with("ping")
  
def test_ping_timeout():
    db = DB({
        "url": "mongodb://localhost:27017",
        "timeout": "1000",
        "mongo_history_days": "7"
    })

    mock_db = Mock()
    mock_db.command.side_effect = ServerSelectionTimeoutError("Timeout error")
    
    db.db = mock_db
    
    result = db.ping()

    assert result is None
    mock_db.command.assert_called_once_with("ping")