import pytest
import uvicorn
import multiprocessing
import time
import os
from pathlib import Path
from pact import Verifier
import sys

# Add parent dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from init_db import init_db


@pytest.fixture(scope="session")
def server():
    # Initialize DB with test data (from schema_postgres.sql)
    if os.path.exists("database.db"):
        os.remove("database.db")
    init_db()

    # Start Server
    proc = multiprocessing.Process(target=run_server, daemon=True)
    proc.start()
    time.sleep(2)
    yield
    proc.terminate()


def run_server():
    os.environ["DATABASE_URL"] = ""
    uvicorn.run(app, host="localhost", port=8001)


def test_pact_verification(server):
    pact_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../pacts"))

    verifier = (
        Verifier("BackendProvider")
        .add_source(pact_dir)
        .add_transport(url="http://localhost:8001")
    )

    success = verifier.verify()
    assert success
