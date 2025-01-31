from fastapi import FastAPI
from ..core.platform import ExperimentPlatform
from ..core.strategies import ThompsonSampling
from .routes import experiments

app = FastAPI(title="Multi-Armed Bandit API")

# Initialize platform globally
platform = ExperimentPlatform(strategy=ThompsonSampling())
experiments.platform = platform  # Share platform with routes

app.include_router(experiments.router, prefix="/experiments", tags=["experiments"])