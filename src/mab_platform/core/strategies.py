from abc import ABC, abstractmethod
import numpy as np
from typing import Dict
from ..models.experiment import ExperimentResult

class BanditStrategy(ABC):
    @abstractmethod
    def select_arm(self, results: Dict[str, ExperimentResult]) -> str:
        pass
    
    @abstractmethod
    def update(self, variant: str, reward: int, results: Dict[str, ExperimentResult]) -> None:
        pass

# https://en.wikipedia.org/wiki/Multi-armed_bandit#Semi-uniform_strategies
class EpsilonGreedy(BanditStrategy):
    def __init__(self, epsilon: float = 0.1):
        self.epsilon = epsilon
    
    def select_arm(self, results: Dict[str, ExperimentResult]) -> str:
        if np.random.random() < self.epsilon:
            return np.random.choice(list(results.keys()))
        return max(results.items(), key=lambda x: x[1].mean_reward)[0]
    
    def update(self, variant: str, reward: int, results: Dict[str, ExperimentResult]) -> None:
        results[variant].rewards += reward
        results[variant].trials += 1

# https://en.wikipedia.org/wiki/Multi-armed_bandit#Probability_matching_strategies
class ThompsonSampling(BanditStrategy):
    def select_arm(self, results: Dict[str, ExperimentResult]) -> str:
        samples = {
            variant: np.random.beta(
                result.rewards + 1,
                result.trials - result.rewards + 1
            )
            for variant, result in results.items()
        }
        return max(samples.items(), key=lambda x: x[1])[0]
    
    def update(self, variant: str, reward: int, results: Dict[str, ExperimentResult]) -> None:
        results[variant].rewards += reward
        results[variant].trials += 1
