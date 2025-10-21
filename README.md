# Medical Dialogues Scoring

This project provides a FastAPI-based service for evaluating medical dialogues against a set of predefined quality standards using a Large Language Model (LLM). It also includes a script to run bulk evaluations on a dataset of dialogues.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the FastAPI Server](#running-the-fastapi-server)
  - [Running the Evaluation Script](#running-the-evaluation-script)
- [API Documentation](#api-documentation)
  - [POST /api/score](#post-apiscore)
- [Docker](#docker)
  - [Building the Image](#building-the-image)
  - [Running with Docker](#running-with-docker)

## Features

- **LLM-Powered Evaluation**: Uses OpenAI's GPT models via LangChain to score dialogues.
- **Structured Output**: Leverages LangChain's `with_structured_output` for reliable JSON parsing.
- **Async API**: Built with FastAPI for high-performance, asynchronous request handling.
- **Bulk Evaluation**: Includes a script to process large datasets and handle API rate limits gracefully.
- **Containerized**: Comes with a `Dockerfile` for easy deployment.

## Project Structure

```
├── Dockerfile
├── env.example
├── pyproject.toml
├── src
│   └── medical_dialogues_scoring
│       ├── __main__.py         # FastAPI app entry point
│       ├── config.py           # Pydantic settings management
│       ├── models
│       │   └── scoring_endpoint.py # Pydantic models for the API
│       ├── routers
│       │   └── api.py          # API router and endpoint definitions
│       └── services
│           └── scoring.py      # Core logic for LLM interaction
└── tests
    ├── evaluation_script.py  # Script to run bulk evaluations
    └── evaluation_set.csv    # Sample dataset for evaluation
```

## Getting Started

### Prerequisites

- Python 3.13+
- UV package manager [(see installation guide)](https://docs.astral.sh/uv/#installation)
- An OpenAI API key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd medical_dialogues_scoring
    ```

2.  **Set up environment variables:**
    Copy the `env.example` file to `.env` and add your OpenAI API key.
    ```bash
    cp env.example .env
    # Now, edit .env and add your key
    # OPENAI_API_KEY=sk-xxxxxxxxxx
    ```

## Usage

### Running the FastAPI Server

To start the API server, run the following command from the root of the project:

1.  **Create and activate virtual environment:**
    ```bash
    # This creates .venv and uv.lock
    uv sync
    
    # Windows Powershell
    ./venv/Scripts/activate.ps1

    # Linux, MacOS
    source ./venv/bin/activate
    ```

2. **Launch FastAPI application:**
    ```bash
    uvicorn medical_dialogues_scoring.__main__:app 
    --host 0.0.0.0 --port 8000 --reload
    ```

The API will be available at `http://localhost:8000`, and interactive documentation can be found at `http://localhost:8000/docs`.

### Running the Evaluation Script

The evaluation script reads `tests/evaluation_set.csv`, calls the API for each dialogue, and saves the results to `tests/evaluation_set_results.csv`.

**Prerequisites:**
- The FastAPI server must be running.
- Test folder should contain `evaluation_set.csv` file

To run the script:
```bash
python tests/evaluation_script.py
```
The script includes logic to handle API rate limits by controlling concurrency and adding delays between requests. You can configure these settings at the top of the `tests/evaluation_script.py` file.

## Docker

### Building the Image

To build and run Docker container containing the application:
```bash
# Simple run
docker compose -f .\docker-compose.yml up

# In case you need to re-build the image:
docker compose -f .\docker-compose.yml up --build
```

