import os
import logging
import re
import time
from pymongo import MongoClient
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

logging.getLogger(__name__)

class DB:
  '''
  Database class for maintaining MongoDB operations

  Attributes
  ----------
  mongo_host : str
    MongoDB server DNS name
  mongo_port : str
    MongoDB server tcp port  
  connection : str
    MongoDB server connection string
  timeout : str
    Database connection timeout in milliseconds
  daysold : str
    How old data should be kept in database
  client : obj
    MongoDB database client instance
  db : obj
    Database instance object

  Methods
  -------
  '''
  
  def __init__(self, conf: dict) -> None:
    '''
    Object constructor. Generates attributes based on conf object
    
    :param conf: Configuration object from main function
    :type conf: dict
    '''
    
    m = re.search(r'@(.+?):(\d+)\/', conf["url"])
    
    try:
      self.mongo_host = m.group(1)
      self.mongo_port = m.group(2)
      
      self.connection = conf["url"]
      self.timeout = conf["timeout"]
      self.daysold = conf["mongo_history_days"]

      self.client = MongoClient(self.connection, timeoutMS=self.timeout)
      self.db = self.client[os.path.basename(self.connection)]

      # Find a collection with given name, create one if it does not exist
      collections = self.db.list_collection_names()
      for c in collections:
        if c == conf["collection"]:
          self.collection = self.db[c]
          break
      else:
        self.collection = self.db.create_collection(conf["collection"])

    except OperationFailure as e:
      logging.error("Operation error")
      return None
    except ServerSelectionTimeoutError as e:
      logging.error(f"Database connection timed out ({int(self.timeout/1000)}s): {self.mongo_host}:{self.mongo_port}")
      return None
    except Exception as e:
      logging.error("Other error")
      return None

  def insert(self, data: dict) -> dict:
    '''
    Inserts data JSON object to a database and returns object with id of inserted data
    
    :param data: JSON data to insert into database
    :type data: dict
    :return: Object with id of inserted data
    :rtype: dict
    '''
    try:
      item = self.collection.insert_one(data)
      logging.debug(str(item))
      return {"id": str(item)}
    
    except OperationFailure as e:
      logging.error(e)
    except ServerSelectionTimeoutError as e:
      logging.error(e)
  
  def collect(self) -> list:
    '''
    Function forms MongoDB query to pick only latest record from database.
    Query result will be sent to prometheus
    
    :return: Latest backup information
    :rtype: list
    '''
    try:
      query = [
        # Select latest data
        { "$sort": {"timestamp": -1} },
        { "$group": {
            "_id": "$vmid",
            "vmid": {"$first": "$vmid"},            # VM ID (number)
            "name": {"$first": "$name"},            # VM name
            "size": {"$first": "$size"},            # Backup size in bytes
            "duration": {"$first": "$duration"},    # backup job duration in seconds 
            "timestamp": {"$first": "$timestamp"},  # timestamp for data processing in grafana
            "status": {"$first": "$status"}         # Backup job status (ok or error)
          }
        }]
      return list(self.collection.aggregate(query))
    
    except OperationFailure as e:
      logging.error(e)
      return []
    except ServerSelectionTimeoutError as e:
      logging.error(f"Database connection timed out ({int(self.timeout/1000)}s): {self.mongo_host}:{self.mongo_port}")
      return []
    except Exception as e:
      logging.error(e)
      return []
    
  def ping(self) -> str:
    '''
    function sends ping command to MongoDB.
    This function is used at application startup to ensure database is available
    
    :return: 'ok' string when database is alive, otherwise None
    :rtype: str
    '''
    try:
      status = [key for key in self.db.command('ping').keys()]
      return status[0]
    except OperationFailure as e:
      return None
    except ServerSelectionTimeoutError as e:
      return None
    except Exception as e:
      return None
  
  def cleanup(self) -> int:
    '''
    Function removes old database records, to keep database small 
    
    :return: Number of deleted records on -1 on error
    :rtype: int
    '''
    try:
      today = time.time()
      shift = today - (86400*self.daysold)

      query = {"timestamp": {"$lt": shift }}
      result = self.collection.delete_many(query)
      
      return result.deleted_count
    except OperationFailure as e:
      return -1
    except ServerSelectionTimeoutError as e:
      logging.error(f"Database connection timed out ({int(self.timeout/1000)}s): {self.mongo_host}:{self.mongo_port}")
      return -1
    except Exception as e:
      return -1
    