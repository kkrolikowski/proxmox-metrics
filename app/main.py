import os
import logging
from aiohttp import web
from aiohttp.web_runner import GracefulExit

async def on_startup(app: object) -> None:
  '''
  Health check function. It's executed on app startup
  and checks if database connection is alive
  
  :param app: aiohttp app object
  :type app: object
  '''

  dbstatus = app["db"].ping()
  if not dbstatus:
    logging.error("Database connection error. Shutting down")
    raise GracefulExit()
  
  logging.info(f"Database status: {dbstatus}")
  logging.info("Server started...")

if __name__ == "__main__":
  from aiohttp import web

  from handlers.handlers import Handler
  from db.mongo import DB

  mongo_url = os.environ.get("MONGO_URL")
  mongo_timeout = int(os.environ.get("MONGO_TIMEOUT", "5"))
  collecttion = os.environ.get("MONGO_COLLECTION")
  mongo_hisory_days = int(os.environ.get("MONGO_HISTORY_DAYS", "7"))
  loglevel = os.environ.get("LOG_LEVEL", "INFO").upper()

  logging.basicConfig(
    level = loglevel,
    format="%(asctime)s - %(levelname)s - %(message)s"
  )

  conf = {
    "url": mongo_url,
    "timeout": mongo_timeout * 1000,
    "collection": collecttion,
    "mongo_history_days": mongo_hisory_days
  }


  # Initiate database connection
  db = DB(conf)

  try:
    app = web.Application()
    app['db'] = db
    app.on_startup.append(on_startup) # hook on_startup function to on_startup phase

    handler = Handler()

    # Routing configuration
    app.add_routes([
      web.get("/", handler.healthcheck),
      web.post("/backups", handler.read_report_content),
      web.get("/metrics", handler.generate_prometheus_metrics)
    ])
    web.run_app(app, access_log=None)
  except Exception as e:
    logging.error(str(e)) 