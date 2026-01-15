# AGENTS.md

## Build & Run
- Package manager: `uv` (uses pyproject.toml and uv.lock)
- Python version: 3.13
- Install deps: `uv sync`
- Run game: `uv run hangman`
- Run single test: `uv run pytest <path/to/test.py>::<test_name> -v`
- Run all tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`

## Architecture
- Hangman game with terminal and web UI
- Source code in `src/hangman/` package (importable as `hangman`)
- Game logic: `src/hangman/game.py`
- Package exports: `src/hangman/__init__.py`
- Web UI: `src/hangman/ui.py` (Streamlit)
- Run web UI: `./start-ui.sh` or `uv run streamlit run src/hangman/ui.py`
- Tests in `tests/` directory

## Testing
- Framework: pytest
- Test files: `tests/test_hangman.py` (game logic), `tests/test_hangman_ui.py` (Streamlit UI)
- Run all tests: `uv run pytest`
- Run single test: `uv run pytest tests/test_hangman.py::TestClassName::test_name -v`
- Run tests with coverage: `uv run pytest --cov=src`

## Code Style
- Follow PEP 8 conventions
- Use type hints for function signatures
- Prefer `pathlib.Path` over `os.path`
- Use `snake_case` for functions/variables, `PascalCase` for classes
- Handle errors with explicit exceptions, not silent failures
- Keep imports sorted: stdlib, third-party, local (use ruff/isort)
