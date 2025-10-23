# HB_Tools

A simple AI agent project using Microsoft Agent Framework and GitHub models.

## Setup

1. Clone the repository.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
4. Install dependencies: `pip install agent-framework-azure-ai --pre`
5. Set the `GITHUB_TOKEN` environment variable with your GitHub Personal Access Token (see [GitHub PAT documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)).
6. Run the agent: `python main.py`

## Features

- AI agent powered by GitHub models
- Built-in weather tool for location-based queries
- Extensible framework for adding more tools

## Requirements

- Python 3.8 or higher
- GitHub Personal Access Token with model access permissions