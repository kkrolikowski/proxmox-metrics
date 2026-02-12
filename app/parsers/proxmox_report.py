import re

class ProxmoxReport:
  '''
  ProxmmoxReport is responsible for parsing data recieved from proxmox notification system.
  It does such things like time and datasize units conversions. It produces list of json objects
  with data used for crafting prometheus metrics.

  Attributes
  ----------
  content : dict
    Raw content recieved from Proxmox notifications system

  Methods
  -------
  '''

  def __init__(self, content: dict) -> None:
    '''
    Object constructor initialized with raw data form proxmox notifications system
    
    :param content: Raw data from proxmox notifications system
    :type content: dict
    '''

    self.content = content

  def __convert_size(self, size: str) -> float:
    '''
    Converts time string value from Gigabytes or Megabytes to a bytes.
    
    :param size: string representig size in Megabytes or Gigabytes
    :type size: str
    :return: float value rounded to 3 digits after the comma
    :rtype: float
    '''

    m = re.search(r'(\d+.*\d+)\ \w+', size)
    
    # convert Gigabytes to bytes
    if 'GiB' in size:
      return round(float(m.group(1)) * 1000000000, 3)
    
    # convert Megabytes to bytes
    if 'MiB' in size:
      return round(float(m.group(1)) * 1000000, 3)
    
    # last resort return statement if value isn't a Gigabytes or Megabytes
    return round(float(m.group(1)), 3)

  def __convert_time(self, time: str) -> int:
    '''
    Convert time string in format: "hms" to a number of seconds. 
    
    :param time: time string in format: hours, minutes, seconds
    :type time: str
    :return: number of seconds
    :rtype: int
    '''

    # make a list from a string to use a proper regular expression
    elements = time.split()

    # input string example: 1h 23m 45s
    if len(elements) == 3:
      m = re.search(r'(\d+)h\ +(\d+)m\ +(\d+)s', time)
      seconds = int(m.group(1)) * 60 * 60 # convert hours to seconds
      seconds += int(m.group(2)) * 60     # convert minutes to seconds
      seconds += int(m.group(3))

    # input string example: 23m 45s
    elif len(elements) == 2:
      m = re.search(r'(\d+)m\ +(\d+)s', time)
      seconds = int(m.group(1)) * 60      # convert minutes to seconds
      seconds += int(m.group(2))
    
    # input string example: 45s
    else:
      m = re.search(r'(\d+)s', time)
      seconds = int(m.group(1))

    return seconds

  def report_parser(self) -> list:
    '''
    Generate list of JSON data containing required key value paris.
    Those data will be used to produce prometheus metrics in following steps.
    
    :return: List of JSON data containing backup job statistics
    :rtype: list
    '''
    
    pattern = re.compile(r'\s+\\n(\d+)\s+(.*?)\s+(\w+)\s+([\d+h\ ]*[\d+m\ ]*[\d+s]+)\s+(\d+\.\d+\ \w+)\s+')
    
    values = []
    for m in re.finditer(pattern, self.content):
      values.append({
        "vmid": m.group(1),                          # Virtual Machine ID
        "name": m.group(2),                          # Virtual Machine name
        "status": m.group(3),                        # Backup status (ok or error)
        "duration": self.__convert_time(m.group(4)), # convert time to seconds
        "size": self.__convert_size(m.group(5))      # convert size value to bytes
      })
    return values