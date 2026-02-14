from unittest.mock import Mock
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

from app.db.mongo import DB # zaimportuj swoją klasę


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
    db_instance = DB(mock_conf_value)
    db_instance.collection = mock_collection # wstrzykujemy mocka

    test_data = {"vmid": "123", "name": "testvm"}
    
    # 3. Akcja
    result = db_instance.insert(test_data)

    # 4. Asercja
    assert result == {"id": "12345qwerty"}
    mock_collection.insert_one.assert_called_once_with(test_data)

def test_insert_operation_failure():
    # 1. Przygotowanie mocka, który rzuca wyjątek
    mock_collection = Mock()
    # side_effect sprawia, że przy wywołaniu insert_one zostanie rzucony błąd
    mock_collection.insert_one.side_effect = OperationFailure("Błąd autoryzacji lub uprawnień")

    mock_conf_value = {
        "url": "http",
        "timeout": "1000",
        "mongo_history_days": "7"
    }

    # 2. Inicjalizacja
    db_instance = DB(mock_conf_value)
    db_instance.collection = mock_collection

    test_data = {"vmid": "123", "name": "testvm"}

    # 3. Akcja
    # Wywołujemy metodę - dzięki try/except w kodzie, aplikacja nie powinna "scrashować"
    result = db_instance.insert(test_data)

    # 4. Asercja
    # Jeśli w kodzie zwracasz None lub pusty dict w except, sprawdź to tutaj:
    assert result is None or result == {}
    mock_collection.insert_one.assert_called_once()

def test_insert_timeout_error():
    # 1. Przygotowanie mocka rzucającego Timeout
    mock_collection = Mock()
    # Symulujemy, że baza nie odpowiedziała w wyznaczonym czasie
    mock_collection.insert_one.side_effect = ServerSelectionTimeoutError("Zbyt długi czas oczekiwania na serwer")

    mock_conf_value = {
        "url": "mongodb://localhost:27017",
        "timeout": "1000",
        "mongo_history_days": "7"
    }

    # 2. Inicjalizacja
    db_instance = DB(mock_conf_value)
    db_instance.collection = mock_collection

    test_data = {"vmid": "999", "name": "timeout_vm"}

    # 3. Akcja
    # Zakładamy, że Twoja metoda insert ma blok: 
    # except ServerSelectionTimeoutError as e:
    result = db_instance.insert(test_data)

    # 4. Asercja
    # Sprawdzamy, czy metoda zwróciła pusty słownik zamiast wybuchnąć błędem
    assert result == None
    # Opcjonalnie: sprawdź czy logging.error został wywołany (wymaga mockowania loggera)
    mock_collection.insert_one.assert_called_once()