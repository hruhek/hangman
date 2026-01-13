# AGENTS.md

## Build & Run
- Package manager: `uv` (uses pyproject.toml and uv.lock)
- Python version: 3.13
- Install deps: `uv sync`
- Run script: `uv run python <script.py>`
- Run single test: `uv run pytest <path/to/test.py>::<test_name> -v`
- Run all tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`

## Architecture
- New/empty Python project - no source files yet
- Add source code to a `src/` or top-level package directory

## Code Style
- Follow PEP 8 conventions
- Use type hints for function signatures
- Prefer `pathlib.Path` over `os.path`
- Use `snake_case` for functions/variables, `PascalCase` for classes
- Handle errors with explicit exceptions, not silent failures
- Keep imports sorted: stdlib, third-party, local (use ruff/isort)
