"""
Unit tests for the vector storage (cosine-similarity semantic search).
"""
import json
import os
import tempfile

import pytest

from memory.vector_storage import VectorStorage


@pytest.fixture
def storage_path():
    d = tempfile.mkdtemp()
    yield os.path.join(d, "embeddings.json")


def test_empty_search_returns_empty(storage_path):
    store = VectorStorage(storage_path)
    assert store.search([1.0, 0.0]) == []


def test_add_text_persists_to_disk(storage_path):
    store = VectorStorage(storage_path)
    store.add_text("hello", [1.0, 0.0], {"type": "note"})
    assert os.path.exists(storage_path)

    with open(storage_path, encoding="utf-8") as f:
        data = json.load(f)
    assert data[0]["text"] == "hello"
    assert data[0]["metadata"] == {"type": "note"}


def test_search_orders_by_cosine_similarity(storage_path):
    store = VectorStorage(storage_path)
    store.add_text("x-axis", [1.0, 0.0])
    store.add_text("y-axis", [0.0, 1.0])
    store.add_text("diagonal", [0.9, 0.1])

    results = store.search([1.0, 0.0], top_k=2)
    assert [r["text"] for r in results] == ["x-axis", "diagonal"]


def test_search_respects_top_k(storage_path):
    store = VectorStorage(storage_path)
    for i in range(5):
        store.add_text(f"t{i}", [float(i), 1.0])
    assert len(store.search([1.0, 1.0], top_k=3)) == 3


def test_reloads_existing_storage(storage_path):
    VectorStorage(storage_path).add_text("persisted", [0.5, 0.5])
    reloaded = VectorStorage(storage_path)
    assert len(reloaded.embeddings_data) == 1
    assert reloaded.embeddings_data[0]["text"] == "persisted"
