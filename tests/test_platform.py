import pytest
from datetime import datetime
import numpy as np
from mab_platform.core.platform import ExperimentPlatform
from mab_platform.core.strategies import ThompsonSampling

def test_create_experiment(platform, example_experiment_data):
    exp_id = platform.create_experiment(
        name=example_experiment_data["name"],
        variants=example_experiment_data["variants"],
        start_date=datetime.now()
    )
    assert exp_id in platform.experiments
    assert len(platform.results[exp_id]) == len(example_experiment_data["variants"])

def test_get_variant(platform, example_experiment_data):
    exp_id = platform.create_experiment(
        name=example_experiment_data["name"],
        variants=example_experiment_data["variants"],
        start_date=datetime.now()
    )
    variant = platform.get_variant(exp_id)
    assert variant in example_experiment_data["variants"]

def test_record_reward(platform, example_experiment_data):
    exp_id = platform.create_experiment(
        name=example_experiment_data["name"],
        variants=example_experiment_data["variants"],
        start_date=datetime.now()
    )
    variant = example_experiment_data["variants"][0]
    platform.record_reward(exp_id, variant, 1)
    assert platform.results[exp_id][variant].rewards == 1
    assert platform.results[exp_id][variant].trials == 1

def test_experiment_not_found(platform):
    with pytest.raises(ValueError, match="Experiment .* not found"):
        platform.get_variant("nonexistent_id")

def test_invalid_variant(platform, example_experiment_data):
    exp_id = platform.create_experiment(
        name=example_experiment_data["name"],
        variants=example_experiment_data["variants"],
        start_date=datetime.now()
    )
    with pytest.raises(ValueError, match="Variant .* not found"):
        platform.record_reward(exp_id, "invalid_variant", 1)
