from setuptools import setup, find_packages

setup(
    name="mab-platform",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "numpy>=1.21.0",
        "pydantic>=1.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.12.0",
            "pytest-asyncio>=0.15.0",
            "httpx>=0.18.0",
            "black>=21.0",
            "isort>=5.0",
            "mypy>=0.910",
        ]
    },
)