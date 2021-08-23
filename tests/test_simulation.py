"""Test Simulation functionality."""
from among_us import Simulation


def test_all_ghosts_in_grave_when_imposter_wins():
    """Teste all ghosts are in graves when imposter wins."""

    simulation = Simulation(seed=31316319423)
    simulation.run()

    players_in_grave = [
        player for player in simulation.players if player.position == "Grave"
    ]
    assert len(players_in_grave) == len(simulation.ghosts)


test_all_ghosts_in_grave_when_imposter_wins()
