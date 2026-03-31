import pytest
from db import Database


@pytest.fixture
def db():
    """Provides a fresh instance of the Database class and cleans up after the test."""
    database = Database()
    yield database  # Provide the fixture instance
    database.data.clear()  # Cleanup step (not needed for in-memory, but useful for real DBs)


def test_add_user(db):
    db.add_user(1, "Alice")
    assert db.get_user(1) == "Alice"


def test_add_duplicate_user(db):
    db.add_user(1, "Alice")
    with pytest.raises(ValueError) as excinfo:
        db.add_user(1, "Bob")
    assert str(excinfo.value) == "User already exists"


def test_delete_user(db):
    db.add_user(2, "Bob")
    db.delete_user(2)
    assert db.get_user(2) is None
