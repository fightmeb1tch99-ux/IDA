"""
Unit tests for the vision / image-generation module (client is mocked).
"""
from types import SimpleNamespace
from unittest.mock import Mock, patch

import vision_art


def test_analyze_image_returns_vision_content(tmp_path):
    image = tmp_path / "img.jpg"
    image.write_bytes(b"fake-bytes")

    client = Mock()
    client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="a cat"))]
    )
    with patch.object(vision_art, "_get_client", return_value=client):
        result = vision_art.analyze_image(str(image), "what is this?")
    assert result == "a cat"


def test_analyze_image_handles_error(tmp_path):
    image = tmp_path / "img.jpg"
    image.write_bytes(b"fake-bytes")

    with patch.object(vision_art, "_get_client", side_effect=Exception("boom")):
        result = vision_art.analyze_image(str(image))
    assert "Ошибка зрения" in result


def test_generate_image_returns_url():
    client = Mock()
    client.images.generate.return_value = SimpleNamespace(
        data=[SimpleNamespace(url="https://example.com/img.png")]
    )
    with patch.object(vision_art, "_get_client", return_value=client):
        result = vision_art.generate_image("a sunset")
    assert result == "https://example.com/img.png"


def test_generate_image_handles_error():
    with patch.object(vision_art, "_get_client", side_effect=Exception("boom")):
        result = vision_art.generate_image("a sunset")
    assert "Ошибка генерации" in result
