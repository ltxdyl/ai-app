# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python 3.11+ AI agent application built with **LangGraph** and **LangChain Anthropic**. Uses MiMo Token Plan (Xiaomi's Anthropic-compatible API proxy) as the model provider. Early-stage — currently a single-node streaming chatbot.

## Build & Run

This project uses **uv** as the package manager and build backend.

```bash
uv sync                   # Install dependencies
uv run ai-app             # Run the CLI entry point
uv run python <script>.py # Run any script in the venv
uv add <package>          # Add a runtime dependency
uv add --dev <package>    # Add a dev dependency
```

No test framework, linter, or CI is configured yet.

## Architecture

- **src/ai_app/main.py** — all application logic: LLM init, LangGraph graph definition, and CLI entry point
- **src/ai_app/__init__.py** — re-exports `main` from `main.py` (entry point for the `ai-app` console script)
- **pyproject.toml** — project config; entry point `ai-app` → `ai_app:main`

### LangGraph Pattern

The app builds a `StateGraph` with a single `chat` node:
1. `State` is a `TypedDict` with `messages` annotated using `add_messages` (LangGraph's message-reducer)
2. `chat_node` invokes the LLM with the full message history and returns the response
3. The graph flows: `START → chat → END`
4. `main()` streams output via `app.stream()` with `stream_mode="messages"`, handling both string and structured (thinking/text block) content from `AIMessageChunk`

### Model Provider

Uses `ChatAnthropic` pointed at MiMo's Anthropic-compatible endpoint (`https://token-plan-cn.xiaomimimo.com/anthropic`). The model name is `mimo-v2.5-pro`. Code comments and the README are in Chinese.

## Environment Variables

- `MIMO_API_KEY` — API key for MiMo Token Plan (see `.env.example`; set via `$env:MIMO_API_KEY` on Windows PowerShell or `export` on Linux/macOS)