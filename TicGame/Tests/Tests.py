import pytest
from SourceCode.Source import Tic2Player

@pytest.fixture
def game():
    return Tic2Player()

def test_board_initialization(game):
    assert game.board == ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
    assert game.current_player == "X"
    assert game.winner is None
    assert game.game_running is True

def test_player_input(game):
    game.Sysinput(1)
    assert game.board[0] == "X"
    assert game.current_player == "X"

    game.Sysinput(5)
    assert game.board[4] == "X"
    assert game.current_player == "X"

    game.Sysinput(1)  # Invalid move
    assert game.board[0] == "X"  # Board should remain unchanged

def test_ai_move(game):
    game.switch_player()  # Switch to AI's turn
    game.ai_opp()
    assert game.board.count("O") == 1  # AI should have placed one "O"

def test_check_winner(game):
    game.board = ["X", "X", "X", "-", "-", "-", "-", "-", "-"]
    assert game.check_winner() is True
    assert game.winner == "X"
    assert game.game_running is False

    game.board = ["O", "-", "-", "O", "-", "-", "O", "-", "-"]
    assert game.check_winner() is True
    assert game.winner == "O"
    assert game.game_running is False

def test_check_tie(game):
    game.board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
    game.check_tie()
    assert game.game_running is False

def test_switch_player(game):
    initial_player = game.current_player
    game.switch_player()
    assert game.current_player != initial_player
    game.switch_player()
    assert game.current_player == initial_player
