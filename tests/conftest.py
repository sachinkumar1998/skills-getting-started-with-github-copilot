import copy
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Ensure the src directory is on sys.path so we can import app.py as a module
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))
import app as app_module


@pytest.fixture(scope="session")
def original_activities():
    return copy.deepcopy(app_module.activities)


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def restore_activities(original_activities):
    # Reset the in-memory activities before each test
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_activities))
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_activities))
