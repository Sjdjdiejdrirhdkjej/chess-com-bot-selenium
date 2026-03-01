import sys
from unittest.mock import MagicMock, patch
import pytest

# Comprehensive mocking for selenium to prevent import errors and speed up tests
selenium_mock = MagicMock()
sys.modules['selenium'] = selenium_mock
sys.modules['selenium.common'] = MagicMock()
sys.modules['selenium.common.exceptions'] = MagicMock()
sys.modules['selenium.webdriver'] = MagicMock()
sys.modules['selenium.webdriver.chrome'] = MagicMock()
sys.modules['selenium.webdriver.chrome.options'] = MagicMock()
sys.modules['selenium.webdriver.chrome.service'] = MagicMock()
sys.modules['selenium.webdriver.common'] = MagicMock()
sys.modules['selenium.webdriver.common.by'] = MagicMock()
sys.modules['selenium.webdriver.support'] = MagicMock()
sys.modules['selenium.webdriver.support.ui'] = MagicMock()
sys.modules['selenium.webdriver.remote'] = MagicMock()
sys.modules['selenium.webdriver.remote.webdriver'] = MagicMock()
sys.modules['selenium.webdriver.support.expected_conditions'] = MagicMock()
sys.modules['selenium.webdriver.common.devtools'] = MagicMock()
sys.modules['selenium.webdriver.common.devtools.v119'] = MagicMock()

sys.modules['stockfish'] = MagicMock()
sys.modules['typer'] = MagicMock()

# Mock input() and os.path.exists so that main.py doesn't block or error on import
with patch('builtins.input', MagicMock()), patch('os.path.exists', MagicMock(return_value=True)):
    import main


@pytest.fixture(autouse=True)
def setup_main_state():
    """Reset main module state before each test."""
    main.previous_moves.clear()
    yield


def test_get_next_move_best_move_not_in_previous():
    """
    Test when the engine's best move hasn't been played recently.
    It should return the best move and add it to previous_moves.
    """
    engine_mock = MagicMock()
    engine_mock.get_best_move.return_value = "e2e4"

    move = main.get_next_move(engine_mock)

    assert move == "e2e4"
    assert "e2e4" in main.previous_moves
    engine_mock.get_top_moves.assert_not_called()


def test_get_next_move_draw_avoidance_fallback():
    """
    Test when the engine's best move was played recently (is in previous_moves).
    It should fall back to get_top_moves() and pick the first move that hasn't
    been played recently, or if all have, pick one that 'will not cause a draw yet'.
    """
    engine_mock = MagicMock()
    engine_mock.get_best_move.return_value = "e2e4"

    # Pre-populate previous_moves with "e2e4"
    main.previous_moves.append("e2e4")

    # get_top_moves returns a list of dictionaries
    engine_mock.get_top_moves.return_value = [
        {"Move": "e2e4"}, # First move is the one we want to avoid
        {"Move": "d2d4"}, # Second move is a new alternative
        {"Move": "g1f3"}
    ]

    move = main.get_next_move(engine_mock)

    # The current logic in get_next_move has:
    # for i, mv in enumerate(top_moves):
    #     if mv not in previous_moves: ...
    #     if i < 1: ...
    # So if i=0 and mv="e2e4" (which IS in previous_moves),
    # the first `if` is false, but the second `if i < 1` is true.
    # Therefore it actually breaks and returns "e2e4" in this specific edge case implementation.
    # We test the actual behavior here to ensure no regressions if refactored later.
    assert move == "e2e4"
    assert "e2e4" in main.previous_moves
    engine_mock.get_top_moves.assert_called_once_with(5)


def test_get_next_move_first_top_move_not_in_previous():
    """
    Test when the best move is in previous_moves, and the first top move
    is NOT in previous_moves. It should pick the first top move.
    """
    engine_mock = MagicMock()
    engine_mock.get_best_move.return_value = "e2e4"

    # Pre-populate previous_moves with "e2e4"
    main.previous_moves.append("e2e4")

    # get_top_moves returns "d2d4" first, which is not in previous_moves
    engine_mock.get_top_moves.return_value = [
        {"Move": "d2d4"},
        {"Move": "g1f3"}
    ]

    move = main.get_next_move(engine_mock)

    assert move == "d2d4"
    assert "d2d4" in main.previous_moves
    engine_mock.get_top_moves.assert_called_once_with(5)


def test_get_next_move_empty_top_moves():
    """
    Test when the engine's best move was played recently, but get_top_moves
    returns an empty list for some reason. The current code expects top_moves[0]
    to exist and raises an IndexError.
    """
    engine_mock = MagicMock()
    engine_mock.get_best_move.return_value = "e2e4"

    # Pre-populate previous_moves with "e2e4"
    main.previous_moves.append("e2e4")

    # get_top_moves returns an empty list
    engine_mock.get_top_moves.return_value = []

    with pytest.raises(IndexError):
        main.get_next_move(engine_mock)

    engine_mock.get_top_moves.assert_called_once_with(5)
