#!/usr/bin/python
"""Main script for Game Simulator."""
import argparse
import logging
import random

from among_us import Simulation
from among_us.const import CONF_SEED

logging.basicConfig(filename="game.log", level=logging.WARNING)


# def fitness(simulation):
#     pass

# def test_parameters():


#     seed = random.randint(1, 100000000000)

#     sim = Simulation(seed=seed)
#     sim.run()
#     sim.results()


if __name__ == "__main__":
    logging.debug("Starting script")

    parser = argparse.ArgumentParser(
        description="Among Us Board Game Simulator.",
        add_help=True,
    )
    parser.add_argument(
        "--players",
        "-p",
        help="Players",
    )
    parser.add_argument(
        "--assignments",
        "-a",
        help="Player assignments",
    )
    parser.add_argument(
        "--body_location",
        "-b",
        help="Room location of.",
    )
    parser.add_argument(
        "--deck",
        "-d",
        help="Shuffled Deck",
    )

    args = parser.parse_args()

    assignments = ["Imposter", "Crew", "Crew", "Crew"]
    BODY_LOCATION = "Back Patio"
    deck = ["Kitchen", "Kitchen", "Kitchen", "Kitchen", "Office", "Office"]

    # for _ in range(1000):

    #     import random

    #     seed = random.randint(1, 100000000000)

    #     simulation = Simulation(seed=seed)
    #     simulation.run()

    # simulation = Simulation(seed=31316319423)
    # simulation.run()

    random.seed(1)
    config = {}
    for _ in range(1000):
        seed = random.randint(1, 100000000000)
        config[CONF_SEED] = seed
        sim = Simulation(config)
        _, winner = sim.run()

    # game = Game(seed=100,assignments=assignments,body_location=body_location,deck=deck )
    # game.game_loop()
