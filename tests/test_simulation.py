"""Test Simulation functionality."""
from among_us import Simulation
from among_us.const import CONF_BODY_LOCATIONS, CONF_DECK, CONF_SEED


def test_all_ghosts_in_grave_when_imposter_wins():
    """Teste all ghosts are in graves when imposter wins."""

    config = {}
    config[CONF_SEED] = 31316319423
    simulation = Simulation(config)
    simulation.run()

    players_in_grave = [
        player for player in simulation.players if player.position == "Grave"
    ]
    assert len(players_in_grave) == len(simulation.ghosts)


def test_simulation_results():
    """Test restuls of simulation."""

    config = {}
    config[CONF_SEED] = 1
    simulation = Simulation(config)
    _, winner = simulation.run()

    assert winner == "Crew"


def test_imposter_wins():
    """Test imposter win."""

    config = {}
    config[CONF_SEED] = 3208357999
    config[CONF_DECK] = ["Room1", "Room1", "Room1", "Room1"]
    config[CONF_BODY_LOCATIONS] = ["Bedroom"]
    simulation = Simulation(config)
    _, winner = simulation.run()

    assert winner == "Imposter"
