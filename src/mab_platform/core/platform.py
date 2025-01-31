from typing import Dict, List, Optional
from datetime import datetime
import logging
import json
from ..models.experiment import Experiment, ExperimentResult
from .strategies import BanditStrategy

class ExperimentPlatform:
    def __init__(self, strategy: BanditStrategy):
        self.experiments: Dict[str, Experiment] = {}
        self.results: Dict[str, Dict[str, ExperimentResult]] = {}
        self.strategy = strategy
        self.logger = logging.getLogger(__name__)
    
    def create_experiment(
        self,
        name: str,
        variants: List[str],
        start_date: datetime,
        end_date: Optional[datetime] = None
    ) -> str:
        exp_id = f"exp_{len(self.experiments) + 1}"
        experiment = Experiment(
            id=exp_id,
            name=name,
            variants=variants,
            start_date=start_date,
            end_date=end_date
        )
        self.experiments[exp_id] = experiment
        self.results[exp_id] = {
            variant: ExperimentResult(variant=variant, rewards=0, trials=0)
            for variant in variants
        }
        self.logger.info(f"Created experiment: {exp_id} - {name}")
        return exp_id
    
    def get_variant(self, experiment_id: str) -> str:
        if experiment_id not in self.experiments:
            raise ValueError(f"Experiment {experiment_id} not found")
            
        experiment = self.experiments[experiment_id]
        experiment.total_samples += 1
        
        variant = self.strategy.select_arm(self.results[experiment_id])
        self.logger.debug(f"Selected variant {variant} for experiment {experiment_id}")
        return variant
    
    def record_reward(self, experiment_id: str, variant: str, reward: int) -> None:
        if experiment_id not in self.results:
            raise ValueError(f"Experiment {experiment_id} not found")
            
        if variant not in self.results[experiment_id]:
            raise ValueError(f"Variant {variant} not found in experiment {experiment_id}")
            
        self.strategy.update(variant, reward, self.results[experiment_id])
        self.logger.debug(f"Recorded reward {reward} for variant {variant} in experiment {experiment_id}")
    
    def get_experiment_results(self, experiment_id: str) -> Dict[str, Dict[str, float]]:
        if experiment_id not in self.results:
            raise ValueError(f"Experiment {experiment_id} not found")
            
        return {
            variant: {
                "mean_reward": result.mean_reward,
                "total_trials": result.trials,
                "total_rewards": result.rewards
            }
            for variant, result in self.results[experiment_id].items()
        }
    
    def export_results(self, experiment_id: str, filepath: str) -> None:
        results = self.get_experiment_results(experiment_id)
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        self.logger.info(f"Exported results for experiment {experiment_id} to {filepath}")
