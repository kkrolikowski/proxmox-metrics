import pytest
from unittest.mock import Mock, AsyncMock, patch
from aiohttp import web
from app.handlers.handlers import Handler

@pytest.mark.asyncio
async def test_read_report_content_ok():
  
  payload = {
    "content": "firstline\nsecondline"
  }

  mock_request = Mock()
  mock_request.json = AsyncMock(return_value=payload)
 
  mock_db = Mock()
  mock_db.insert.return_value = {"id": "111122333"}
  mock_db.cleanup.return_value = 2

  mock_request.app = {
    "db": mock_db
  }

  mock_pr = Mock()
  mock_pr.report_parser.return_value = [{
    "vmid": "111",
    "vm_name": "testvm"
  }]

  with patch("app.handlers.handlers.ProxmoxReport", return_value=mock_pr):
    with patch("time.time", return_value=123456789):
      handler = Handler()
      response = await handler.read_report_content(mock_request)
  
  assert response.status == 200

  from json import loads
  assert loads(response.text) == {"status": "ok"}

  mock_db.insert.assert_called_once_with({
    "vmid": "111",
     "vm_name": "testvm",
     "timestamp": 123456789
  })
  mock_db.cleanup.assert_called_once()