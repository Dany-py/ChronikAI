# ChronikAI

A powerful AI-driven project building agentic workflows with LangChain, LangGraph, and Ollama.

## Overview

ChronikAI is designed to leverage Large Language Models (LLMs) to automate and manage complex tasks through structured agentic workflows. It integrates with Ollama for local LLM execution and uses LangGraph for stateful multi-agent orchestration.

## Features

- **Agentic Workflows**: Controlled task execution using LangGraph.
- **Local LLM Support**: Seamless integration with Ollama.
- **Database Integration**: SQLAlchemy and Alembic for robust data management.
- **Watcher System**: Real-time monitoring and event-driven actions.
- **Studio Tools**: Interactive components for managing AI interactions.

## Project Structure

- `src/apps`: Main application components (Studio, Watcher).
- `src/core`: Core logic and agent definitions.
- `src/infrastructure`: Database, API clients, and external integrations.
- `src/shared`: Generic utilities and shared models.

## Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai/) (for local LLM support)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd chronikAI
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Copy the example environment file and fill in your details:
   ```bash
   cp src/.env.example src/.env
   ```

## Usage

Describe how to run the main applications here. For example:
```bash
python -m src.apps.watcher.main
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify License, e.g., MIT]
