import pytest
import logging
from unittest.mock import Mock

from app.main import on_startup, GracefulExit

@pytest.mark.asyncio
async def test_on_startup_db_ok():
  db = Mock()
  db.ping.return_value = True

  app = {"db": db}
  await on_startup(app)

  db.ping.assert_called_once()

@pytest.mark.asyncio
async def test_on_startup_db_fail():
  db = Mock()
  db.ping.return_value = False

  app = {"db": db}

  with pytest.raises(GracefulExit):
    await on_startup(app)

  db.ping.assert_called_once()

