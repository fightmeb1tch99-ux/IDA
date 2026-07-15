"""
Unit tests for the FastAPI proxy server (provider is mocked).
"""
import asyncio
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

import server
from server import ChatRequest, Message, chat_proxy, root


def test_root_reports_online():
    result = asyncio.run(root())
    assert result["status"] == "online"


def test_chat_proxy_returns_provider_content():
    provider = Mock()
    provider.is_available.return_value = True
    provider.chat.return_value = "hi from llm"
    request = ChatRequest(messages=[Message(role="user", content="hi")])

    with patch.object(server, "create_provider", return_value=provider):
        result = asyncio.run(chat_proxy(request))

    assert result == {"response": "hi from llm"}
    provider.chat.assert_called_once()


def test_chat_proxy_without_provider_raises_500():
    provider = Mock()
    provider.is_available.return_value = False
    request = ChatRequest(messages=[Message(role="user", content="hi")])

    with patch.object(server, "create_provider", return_value=provider):
        with pytest.raises(HTTPException) as exc:
            asyncio.run(chat_proxy(request))
    assert exc.value.status_code == 500


def test_chat_proxy_wraps_provider_error():
    provider = Mock()
    provider.is_available.return_value = True
    provider.chat.side_effect = RuntimeError("upstream boom")
    request = ChatRequest(messages=[Message(role="user", content="hi")])

    with patch.object(server, "create_provider", return_value=provider):
        with pytest.raises(HTTPException) as exc:
            asyncio.run(chat_proxy(request))
    assert exc.value.status_code == 500
    assert "boom" in str(exc.value.detail)
