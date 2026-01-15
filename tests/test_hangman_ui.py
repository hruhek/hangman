import pytest
from streamlit.testing.v1 import AppTest

from hangman import GameState


@pytest.fixture
def app() -> AppTest:
    """Create a fresh AppTest instance with a fixed word."""
    at = AppTest.from_file("src/hangman/ui.py")
    at.session_state["game"] = GameState(word="python")
    at.run()
    return at


def submit_guess(app: AppTest, letter: str) -> AppTest:
    """Helper to input a letter and submit the form."""
    app.text_input[0].input(letter)
    # Find the form submit button
    for btn in app.button:
        if "Guess" in btn.label:
            btn.click()
            break
    return app.run()


class TestInitialState:
    def test_page_title_displayed(self, app: AppTest):
        assert "Hangman" in app.title[0].value

    def test_initial_hangman_display(self, app: AppTest):
        assert len(app.code) == 1

    def test_initial_word_hidden(self, app: AppTest):
        assert "_ _ _ _ _ _" in app.markdown[1].value

    def test_initial_remaining_attempts(self, app: AppTest):
        assert "6" in app.markdown[2].value

    def test_initial_guessed_letters_empty(self, app: AppTest):
        assert "None" in app.markdown[3].value

    def test_guess_form_present(self, app: AppTest):
        assert len(app.text_input) == 1

    def test_guess_button_present(self, app: AppTest):
        assert any("Guess" in btn.label for btn in app.button)


class TestCorrectGuess:
    def test_correct_letter_reveals_in_word(self, app: AppTest):
        submit_guess(app, "p")
        assert "p" in app.markdown[1].value.lower()

    def test_correct_guess_shows_success_message(self, app: AppTest):
        submit_guess(app, "p")
        assert len(app.success) >= 1

    def test_correct_guess_no_attempt_lost(self, app: AppTest):
        submit_guess(app, "p")
        assert "6" in app.markdown[2].value

    def test_guessed_letter_added_to_list(self, app: AppTest):
        submit_guess(app, "p")
        assert "p" in app.markdown[3].value


class TestIncorrectGuess:
    def test_incorrect_guess_shows_error_message(self, app: AppTest):
        submit_guess(app, "z")
        assert len(app.error) >= 1

    def test_incorrect_guess_decrements_attempts(self, app: AppTest):
        submit_guess(app, "z")
        assert "5" in app.markdown[2].value

    def test_incorrect_guess_updates_hangman(self, app: AppTest):
        initial_hangman = app.code[0].value
        submit_guess(app, "z")
        updated_hangman = app.code[0].value
        assert initial_hangman != updated_hangman


class TestAlreadyGuessed:
    def test_already_guessed_shows_warning(self, app: AppTest):
        submit_guess(app, "p")
        submit_guess(app, "p")
        assert len(app.warning) >= 1


class TestGameWin:
    def test_win_shows_congratulations(self, app: AppTest):
        for letter in "python":
            submit_guess(app, letter)
        success_messages = [s.value for s in app.success]
        assert any("Congratulations" in msg for msg in success_messages)

    def test_win_reveals_word(self, app: AppTest):
        for letter in "python":
            submit_guess(app, letter)
        success_messages = [s.value for s in app.success]
        assert any("python" in msg for msg in success_messages)

    def test_win_shows_play_again_button(self, app: AppTest):
        for letter in "python":
            submit_guess(app, letter)
        assert any("Play Again" in btn.label for btn in app.button)


class TestGameLoss:
    def test_loss_shows_game_over(self, app: AppTest):
        for letter in "abcdfg":  # 6 wrong guesses
            submit_guess(app, letter)
        error_messages = [e.value for e in app.error]
        assert any("Game Over" in msg for msg in error_messages)

    def test_loss_reveals_word(self, app: AppTest):
        for letter in "abcdfg":
            submit_guess(app, letter)
        error_messages = [e.value for e in app.error]
        assert any("python" in msg for msg in error_messages)

    def test_loss_shows_play_again_button(self, app: AppTest):
        for letter in "abcdfg":
            submit_guess(app, letter)
        assert any("Play Again" in btn.label for btn in app.button)


class TestPlayAgain:
    def test_play_again_resets_attempts_after_loss(self, app: AppTest):
        for letter in "abcdfg":
            submit_guess(app, letter)

        play_again_btn = next(btn for btn in app.button if "Play Again" in btn.label)
        play_again_btn.click()
        app.run()

        # After clicking play again, remaining attempts should be reset to 6
        assert "6" in app.markdown[2].value
