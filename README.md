# Hangman

A Hangman game with ASCII art, available as both a terminal game and a web UI.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

## Installation

```bash
uv sync
```

## Running the Game

```bash
uv run hangman
```

### Web UI

Run the Streamlit web interface:

```bash
./start-ui.sh
```

Or manually:

```bash
uv run streamlit run src/hangman/ui.py
```

This opens an interactive web page in your browser.

## How to Play

1. A random word is selected
2. Guess one letter at a time
3. You have 6 wrong guesses before the hangman is complete
4. Win by guessing all letters in the word

## Credits

Created by [Amp](https://ampcode.com)
