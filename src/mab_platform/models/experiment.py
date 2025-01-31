from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Experiment:
    id: str
    name: str
    variants: List[str]
    start_date: datetime
    end_date: Optional[datetime] = None
    total_samples: int = 0

@dataclass
class ExperimentResult:
    variant: str
    rewards: int
    trials: int
    
    @property
    def mean_reward(self) -> float:
        return self.rewards / self.trials if self.trials > 0 else 0
