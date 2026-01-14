# AGENTS.md

## Build & Run
- Package manager: `uv` (uses pyproject.toml and uv.lock)
- Python version: 3.13
- Install deps: `uv sync`
- Run game: `uv run python src/hangman.py`
- Run single test: `uv run pytest <path/to/test.py>::<test_name> -v`
- Run all tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`

## Architecture
- Terminal-based Hangman game
- Source code in `src/` directory
- Main entry point: `src/hangman.py`
- Tests in `tests/` directory

## Testing
- Framework: pytest
- Test file: `tests/test_hangman.py`
- Test classes cover: `GameState`, `GuessResult`, `get_display_word`, `get_random_word`, `process_guess`, `validate_guess`
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
