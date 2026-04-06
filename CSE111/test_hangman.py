import pytest
import tkinter as tk
from Hangman import HangmanApp, CATEGORIES

@pytest.fixture(scope="module")
def app():
    """Initialize one hidden Tkinter instance for all tests in this module."""
    root = tk.Tk()
    root.withdraw()  # Hide the window
    application = HangmanApp(root)
    
    yield application
    
    try:
        root.destroy()
    except:
        pass

def test_initial_word_selection(app):
    """Test 1: Verify word selection."""
    # Reset game state for a fresh test
    app._new_game()
    current_cat = app.category_var.get()
    word_pool = CATEGORIES[current_cat]
    
    assert app.word in word_pool
    assert len(app.wrong) == 0

def test_correct_guess_logic(app):
    """Test 2: Verify correct letter logic."""
    app.word = "python"
    app.guessed = set()
    app.wrong = set()
    
    app._on_guess("p")
    
    assert "p" in app.guessed
    display_text = app.word_label.cget("text").replace(" ", "").lower()
    assert "p" in display_text

def test_wrong_guess_limit(app):
    """Test 3: Verify wrong letter logic."""
    app.word = "apple"
    app.wrong = set()
    
    app._on_guess("z")
    
    assert "z" in app.wrong
    assert "Z" in app.wrong_label.cget("text")
if __name__ == "__main__":
    import pytest
    import sys
    # This calls pytest on the current file
    sys.exit(pytest.main([__file__]))