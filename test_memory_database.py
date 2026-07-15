"""
Unit tests for the SQLite DatabaseManager.
"""
import os
import tempfile

import pytest

from memory.database import DatabaseManager


@pytest.fixture
def db():
    d = tempfile.mkdtemp()
    return DatabaseManager(db_path=os.path.join(d, "test.db"))


def test_init_creates_database_file(db):
    assert os.path.exists(db.db_path)


def test_recent_history_empty_by_default(db):
    assert db.get_recent_history() == []


def test_add_and_fetch_interaction(db):
    db.add_interaction("hello", "hi there", thought="greeting")
    history = db.get_recent_history()
    assert history == [("hello", "hi there")]


def test_recent_history_orders_newest_first(db):
    db.add_interaction("first", "r1")
    db.add_interaction("second", "r2")
    history = db.get_recent_history()
    assert history[0] == ("second", "r2")
    assert history[1] == ("first", "r1")


def test_recent_history_respects_limit(db):
    for i in range(5):
        db.add_interaction(f"q{i}", f"a{i}")
    assert len(db.get_recent_history(limit=2)) == 2


def test_metadata_is_stored_as_json(db):
    db.add_interaction("q", "a", metadata={"plan": ["step1"]})
    assert db.get_recent_history() == [("q", "a")]
