# Multi-Armed Bandit Experimentation Platform

A production-ready platform for running advanced A/B tests and multi-armed bandit experiments. This platform implements both Thompson Sampling and Epsilon-Greedy strategies for efficient experimentation.

## Features
- Multiple bandit strategies (Thompson Sampling, Epsilon-Greedy)
- REST API with automatic documentation
- Real-time variant selection
- Results tracking and export
- Comprehensive test suite

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mab-platform.git
cd mab-platform
```

2. Install the package with development dependencies:
```bash
python3 -m pip install -e ".[dev]"
```

## Running the Server

1. Start the API server:
```bash
uvicorn mab_platform.api.main:app --reload
```

2. The server will start at `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Alternative Documentation: `http://localhost:8000/redoc`

## Using the API via Swagger UI

1. Open `http://localhost:8000/docs` in your browser

2. Create an Experiment:
   - Click on `POST /experiments/`
   - Click "Try it out"
   - Enter experiment details in the JSON body:
   ```json
   {
     "name": "Button Color Test",
     "variants": ["blue", "green", "red"],
     "end_date": null
   }
   ```
   - Click "Execute"
   - Save the returned `experiment_id` (e.g., "exp_1")

3. Get a Variant:
   - Click on `GET /experiments/{experiment_id}/variant`
   - Click "Try it out"
   - Enter your experiment_id
   - Click "Execute"
   - The API will return a variant to test

4. Record a Reward:
   - Click on `POST /experiments/{experiment_id}/reward`
   - Click "Try it out"
   - Enter your experiment_id
   - Enter reward details:
   ```json
   {
     "variant": "blue",
     "reward": 1
   }
   ```
   - Click "Execute"

5. View Results:
   - Click on `GET /experiments/{experiment_id}/results`
   - Click "Try it out"
   - Enter your experiment_id
   - Click "Execute"
   - View the performance of each variant

## Using the API Programmatically

```python
import requests

# Create experiment
response = requests.post(
    "http://localhost:8000/experiments/",
    json={
        "name": "Button Test",
        "variants": ["blue", "green", "red"]
    }
)
exp_id = response.json()["experiment_id"]

# Get variant
variant = requests.get(
    f"http://localhost:8000/experiments/{exp_id}/variant"
).json()["variant"]

# Record reward
requests.post(
    f"http://localhost:8000/experiments/{exp_id}/reward",
    json={"variant": variant, "reward": 1}
)

# Get results
results = requests.get(
    f"http://localhost:8000/experiments/{exp_id}/results"
).json()
print(results)
```

## Running Tests

Run the full test suite with coverage:
```bash
pytest --cov=mab_platform --cov-report=term-missing
```

Run specific test files:
```bash
pytest tests/test_api.py
pytest tests/test_platform.py
pytest tests/test_strategies.py
```

## Project Structure
```
mab-platform/
├── src/mab_platform/      # Main package
│   ├── api/              # FastAPI application
│   ├── core/             # Core MAB implementation
│   └── models/           # Data models
├── tests/                # Test suite
└── examples/             # Usage examples
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

## License

MIT License