import pytest
import numpy as np
from mab_platform.core.strategies import EpsilonGreedy, ThompsonSampling
from mab_platform.models.experiment import ExperimentResult

@pytest.fixture
def results():
    return {
        "A": ExperimentResult(variant="A", rewards=10, trials=100),
        "B": ExperimentResult(variant="B", rewards=20, trials=100)
    }

def test_epsilon_greedy(results):
    strategy = EpsilonGreedy(epsilon=0.1)
    np.random.seed(42)
    
    # Test multiple selections to ensure both exploration and exploitation
    selections = [strategy.select_arm(results) for _ in range(100)]
    
    # Should mostly select B (higher reward) but sometimes A
    assert "B" in selections
    assert "A" in selections
    assert selections.count("B") > selections.count("A")

def test_thompson_sampling(results):
    strategy = ThompsonSampling()
    np.random.seed(42)
    
    # Test multiple selections
    selections = [strategy.select_arm(results) for _ in range(100)]
    
    # Should mostly select B (higher reward) but sometimes A
    assert "B" in selections
    assert "A" in selections
    assert selections.count("B") > selections.count("A")
