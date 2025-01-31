import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from mab_platform.api.main import app
from mab_platform.core.platform import ExperimentPlatform
from mab_platform.core.strategies import ThompsonSampling

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def platform():
    return ExperimentPlatform(strategy=ThompsonSampling())

@pytest.fixture
def example_experiment_data():
    return {
        "name": "Test Experiment",
        "variants": ["A", "B", "C"],
        "end_date": None
    }