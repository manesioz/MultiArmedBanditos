from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ExperimentCreate(BaseModel):
    name: str
    variants: List[str]
    end_date: Optional[datetime] = None

class RewardRecord(BaseModel):
    variant: str
    reward: int