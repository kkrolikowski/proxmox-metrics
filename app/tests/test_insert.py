from unittest.mock import Mock

def test_insert_ok():
    # 1. Przygotowanie mocków dla PyMongo
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

    # 2. Inicjalizacja Twojej klasy (załóżmy, że nazywa się Database)
    # Zamiast db = Mock(), tworzymy realny obiekt
    from app.db.mongo import DB # zaimportuj swoją klasę
    db_instance = DB(mock_conf_value)
    db_instance.collection = mock_collection # wstrzykujemy mocka

    test_data = {"vmid": "123", "name": "testvm"}
    
    # 3. Akcja
    result = db_instance.insert(test_data)

    # 4. Asercja
    assert result == {"id": "12345qwerty"}
    mock_collection.insert_one.assert_called_once_with(test_data)