import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from mab_platform.api.main import app, platform
from mab_platform.core.strategies import ThompsonSampling

@pytest.fixture(autouse=True)
def reset_platform():
    """Reset platform state before each test"""
    platform.experiments = {}
    platform.results = {}
    yield platform

def test_create_experiment(client, example_experiment_data):
    response = client.post(
        "/experiments/",
        json=example_experiment_data
    )
    assert response.status_code == 201
    data = response.json()
    assert "experiment_id" in data
    assert data["experiment_id"].startswith("exp_")

def test_get_variant(client, example_experiment_data):
    # First create an experiment
    create_response = client.post(
        "/experiments/",
        json=example_experiment_data
    )
    assert create_response.status_code == 201
    exp_id = create_response.json()["experiment_id"]
    
    # Then get a variant
    response = client.get(f"/experiments/{exp_id}/variant")
    assert response.status_code == 200
    assert "variant" in response.json()
    assert response.json()["variant"] in example_experiment_data["variants"]

def test_record_reward(client, example_experiment_data):
    # Create experiment
    create_response = client.post(
        "/experiments/",
        json=example_experiment_data
    )
    assert create_response.status_code == 201
    exp_id = create_response.json()["experiment_id"]
    
    # Get a variant
    variant_response = client.get(f"/experiments/{exp_id}/variant")
    variant = variant_response.json()["variant"]
    
    # Record reward
    reward_data = {
        "variant": variant,
        "reward": 1
    }
    response = client.post(
        f"/experiments/{exp_id}/reward",
        json=reward_data
    )
    assert response.status_code == 200
    
    # Check results
    response = client.get(f"/experiments/{exp_id}/results")
    results = response.json()
    assert results[variant]["total_rewards"] == 1

def test_nonexistent_experiment(client):
    response = client.get("/experiments/nonexistent/variant")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()