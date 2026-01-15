import streamlit as st

from hangman import (
    HANGMAN_STAGES,
    WORDS,
    GameState,
    get_display_word,
    get_random_word,
    process_guess,
)


def init_game() -> None:
    st.session_state.game = GameState(word=get_random_word(WORDS))


def main() -> None:
    st.set_page_config(page_title="Hangman", page_icon="🎮", layout="centered")
    st.title("🎮 Hangman")

    if "game" not in st.session_state:
        init_game()

    game: GameState = st.session_state.game

    col1, col2 = st.columns([1, 1])

    with col1:
        st.code(HANGMAN_STAGES[game.wrong_guesses], language=None)

    with col2:
        st.markdown("### Word")
        st.markdown(
            f"<h2 style='letter-spacing: 0.3em; font-family: monospace;'>"
            f"{get_display_word(game.word, game.guessed_letters)}</h2>",
            unsafe_allow_html=True,
        )

        st.markdown(f"**Remaining attempts:** {game.remaining_attempts}")
        st.markdown(
            f"**Guessed letters:** {', '.join(sorted(game.guessed_letters)) or 'None'}"
        )

    if game.message:
        if "✓" in game.message:
            st.success(game.message)
        elif "✗" in game.message:
            st.error(game.message)
        else:
            st.warning(game.message)

    if game.is_word_guessed():
        st.balloons()
        st.success(f"🎉 Congratulations! You won! The word was: **{game.word}**")
        if st.button("Play Again", type="primary"):
            init_game()
            st.rerun()
    elif game.is_game_over():
        st.error(f"💀 Game Over! The word was: **{game.word}**")
        if st.button("Play Again", type="primary"):
            init_game()
            st.rerun()
    else:
        with st.form("guess_form", clear_on_submit=True):
            guess = st.text_input(
                "Enter a letter:",
                max_chars=1,
                key="guess_input",
            )
            submitted = st.form_submit_button("Guess", type="primary")

            if submitted and guess:
                process_guess(game, guess)
                st.rerun()


if __name__ == "__main__":
    main()
