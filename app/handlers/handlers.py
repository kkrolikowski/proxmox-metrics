import sys
import time
import logging
from aiohttp import web
from prometheus_client import generate_latest

from parsers.proxmox_report import ProxmoxReport
from metrics.prometheus import Prometheus
from db.mongo import DB

logging.getLogger(__name__)

class Handler:
  '''
  Handlers for managing client requests.

  Methods
  -------
  '''

  def __init__(self):
    self.prometheus = Prometheus()

  async def read_report_content(self, request) -> object:
    '''
    This method is waitting for POST requests from Proxmox server.
    It revieves backup job data in JSON format, runs a perser and 
    than stores data in database. It also initiates old data cleanup.
    
    :param request: aiohttp request object
    :type request: object
    :return: web json_response object with status
    :rtype: object
    '''
    try:
      # Retrieve data from proxmox
      payload = await request.json()
      logging.info("Recieved data from proxmox")
      
      # Escaping newlines to produce long single line string
      content = payload['content'].replace("\n", "\\n")

      # Parsing whole proxmox content to extract actual report.
      # This data will be stored in a list of JSON object
      # Every single row contains report data regarding single vm
      pr = ProxmoxReport(content)
      backup_info = pr.report_parser()
      
      # Iterate through array of vm-related informations and save it
      # in a separate database records
      timestamp = int(time.time())
      for item in backup_info:
        item.update({ "timestamp": timestamp })
        request.app["db"].insert(item)
      
      logging.info("Data stored in database")
      
      # Removing old data from database
      deleted = request.app["db"].cleanup()
      if deleted:
        logging.info(f"Removed {deleted} records from database...")

      return web.json_response({ "status": "ok" })
    
    except Exception as e:
      logging.error(str(e))
      return web.json_response({ "error": str(e) })

  async def healthcheck(self, request):
    '''
    Simple dummy response hooked to root url, only for kubernetes healthcheck
    
    :param request: mandatory aiohttp request object
    :return: Simple text response
    :rtype: object
    '''
    return web.Response(text="Proxmox Metrics started...")
  
  async def generate_prometheus_metrics(self, request):
    '''
    Method generates prometheus metrics based on database information
    and shares them on the http url
    
    :param request: mandatory aiohttp request object
    :return: prometheus metrics
    :rtype: object
    '''
    try:
      # Get metrics data from database
      metrics_input_data = request.app["db"].collect()
      
      # Create metric basend on collected data
      self.prometheus.generate(metrics_input_data)
      output = generate_latest()

      # returns prometheus metric to the http endpoint
      logging.info(f"{request.remote} - {request.method} {request.url}")
      return web.Response(text=output.decode('ascii'))

    except Exception as e:
      logging.error(str(e))
      return None