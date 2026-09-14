# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python 3.11 application built with LangGraph. Early-stage — currently a scaffold.

## Build & Run

This project uses **uv** as the package manager and build backend.

```bash
# Install dependencies
uv sync

# Run the app
uv run ai-app

# Run a Python script or module
uv run python <script>.py

# Add a dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>
```

## Architecture

- **src/ai_app/** — application package; business logic in `main.py`, imported via `__init__.py`
- **pyproject.toml** — project config; CLI entry point registered as `ai-app` → `ai_app:main`
- **uv.lock** — locked dependency graph (committed to repo)

LangGraph is the core dependency for building AI agent workflows.

## Environment Variables

- `MIMO_API_KEY` — API key for MiMo Token Plan (see `.env.example`)