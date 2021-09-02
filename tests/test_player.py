"""Test Player functionality."""
from among_us import Player, get_players


def test_player_name():
    """Test Player name."""

    player = Player("Player 1", "Crew")
    assert player.name == "Player 1"


def test_player_position():
    """Test getting player's position."""
    player = Player("Player 1", "Crew", "Room 1")
    assert player.position == "Room 1"


def test_player_set_position():
    """Test getting player's position."""
    player = Player("Player 1", "Crew", "Room 1")
    assert player.position == "Room 1"

    player.position = "Room 2"
    assert player.position == "Room 2"


def test_player_assignment():
    """Test getting player's assignment."""
    players = get_players(["Crew"])
    assert players[0].assignment == "Crew"


def test_get_players():
    """Test getting players."""

    players = get_players(["Crew", "Crew", "Crew", "Crew", "Imposter"])
    assert len(players) == 5

    assert players[0].name == "Player 1"
    assert players[1].name == "Player 2"
    assert players[2].name == "Player 3"
    assert players[3].name == "Player 4"
    assert players[4].name == "Player 5"


def test_player_print():
    """Test player print value."""
    player = Player("Player 1", "Crew")

    assert player.__repr__()
