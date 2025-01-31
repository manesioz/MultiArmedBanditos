from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..schemas.experiment import ExperimentCreate, RewardRecord
from ...core.platform import ExperimentPlatform

router = APIRouter()
platform = None  # Set by main.py

@router.post("/", status_code=201)
async def create_experiment(experiment: ExperimentCreate):
    try:
        exp_id = platform.create_experiment(
            name=experiment.name,
            variants=experiment.variants,
            start_date=datetime.now(),
            end_date=experiment.end_date
        )
        return {"experiment_id": exp_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{experiment_id}/variant")
async def get_variant(experiment_id: str):
    try:
        variant = platform.get_variant(experiment_id)
        return {"variant": variant}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{experiment_id}/reward")
async def record_reward(experiment_id: str, reward: RewardRecord):
    try:
        platform.record_reward(
            experiment_id=experiment_id,
            variant=reward.variant,
            reward=reward.reward
        )
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{experiment_id}/results")
async def get_results(experiment_id: str):
    try:
        results = platform.get_experiment_results(experiment_id)
        return results
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
