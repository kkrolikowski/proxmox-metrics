from prometheus_client import Gauge

class Prometheus:
  '''
  Prometheus class designed for metrics creation

  Attributes
  ----------
  backup_size : object 
    Gauge object for backup size metric of particular VM
  backup_duration : object
    Gauge object for backup duration of particular VM
  backup_timestamp : object 
    Gauge object for backup completion timestamp of particular VM
  backup_status : object 
    Gauge object for backup status of particular VM
  
  Methods
  -------
  '''
  
  def __init__(self):
    '''
    Object constructor. Defines all needed metric objects
    '''
    self.backup_size = Gauge(
      "backup_size_bytes",
      "Backup size for VM",
      ["vmid", "name"]
    )

    self.backup_duration = Gauge(
      "backup_duration_seconds",
      "Backup duration for VM",
      ["vmid", "name"]
    )

    self.backup_timestamp = Gauge(
      "backup_timestamp",
      "Timestamp of backup completion",
      ["vmid", "name"]
    )

    self.backup_status = Gauge(
      "backup_status",
      "Status of backup execution",
      ["vmid", "name"]
    )
  
  def generate(self, input_data: dict) -> None:
    '''
    Method fills created metric objects with data from input_data dictionary
    
    :param input_data: Backup status information
    :type input_data: dict
    
    '''
    for row in input_data:
      vmid = str(row["vmid"])
      name = row["name"]
      status = 1 if row["status"] == "ok" else 0

      self.backup_size.labels(vmid, name).set(row["size"])
      self.backup_duration.labels(vmid, name).set(row["duration"])
      self.backup_timestamp.labels(vmid, name).set(row["timestamp"])
      self.backup_status.labels(vmid, name).set(status)
