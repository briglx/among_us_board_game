"""Genetic Algorithm to optimize game parameters."""
import random

import numpy as np

from among_us import Simulation

from .const import (
    CONF_ASSIGNMENTS,
    CONF_BODY_LOCATIONS,
    CONF_DECK,
    CONF_IMPOSTER_CHANCES,
    CONF_POTENTIAL_ROOMS,
    CONF_REWARD_CREW_TO_BODY,
    CONF_REWARD_IMPOSTER_TO_CREW,
    CONF_RISK_CREW_TO_IMPOSTER,
    CONF_RISK_CREW_TO_RIVAL,
    CONF_SEED,
    DUPLICATE_ROOM_STRATEGY_EQUAL,
    DUPLICATE_ROOM_STRATEGY_LADDER,
    VALID_GENOTYPE_LEN,
)


def create_random_population(size):
    """Create random population from size."""
    population = [
        np.random.randint(0, 2, VALID_GENOTYPE_LEN).tolist() for _ in range(size)
    ]
    return population


def calc_fitness(genotype, seed=None):
    """Calculate the fitness of the genotype."""
    phenotype = Phenotype(seed, genotype)

    return phenotype.score()


# pylint: disable-msg=R0902
class Phenotype:
    """Genetic class to simulate multiple game."""

    def __init__(self, seed, genotype, iterations=None):
        """Initialize the phenotype."""
        self._seed = seed
        if iterations is None:
            iterations = 1000
        self._genotype = genotype
        self._iterations = iterations

        # Parse genotype
        self._player_count = (
            3 + np.packbits(genotype[:4], bitorder="little").tolist()[0]
        )
        self._imposter_count = (
            1 + np.packbits(genotype[4:7], bitorder="little").tolist()[0]
        )
        self._body_count = (
            1 + np.packbits(genotype[7:10], bitorder="little").tolist()[0]
        )
        self._room_type_count = (
            3 + np.packbits(genotype[10:13], bitorder="little").tolist()[0]
        )
        self._card_count_per_room = (
            3 + np.packbits(genotype[13:17], bitorder="little").tolist()[0]
        )
        self._duplicate_room_count = np.packbits(
            genotype[17:20], bitorder="little"
        ).tolist()[0]
        if np.packbits(genotype[20:21], bitorder="little").tolist()[0]:
            self._duplicate_room_strategy = DUPLICATE_ROOM_STRATEGY_LADDER
        else:
            self._duplicate_room_strategy = DUPLICATE_ROOM_STRATEGY_EQUAL
        self._duplicate_room_intesity = (
            1 + np.packbits(genotype[21:23], bitorder="little").tolist()[0]
        )
        self._imposter_chances = (
            3 + np.packbits(genotype[23:27], bitorder="little").tolist()[0]
        )
        self._reward_imposter_to_crew = np.packbits(
            genotype[27:31], bitorder="little"
        ).tolist()[0]
        self._reward_crew_to_body = np.packbits(
            genotype[31:35], bitorder="little"
        ).tolist()[0]
        self._risk_crew_to_imposter = np.packbits(
            genotype[35:39], bitorder="little"
        ).tolist()[0]
        self._risk_crew_to_rival = np.packbits(
            genotype[39:43], bitorder="little"
        ).tolist()[0]

        # Init Class
        random.seed(seed)

        if not self.is_valid_genotype():
            raise ValueError("Invalid Genotype.")

    @property
    def player_count(self):
        """Player count."""
        return self._player_count

    @property
    def imposter_count(self):
        """Imposter Count."""
        return self._imposter_count

    @property
    def body_count(self):
        """Body Count."""
        return self._body_count

    @property
    def room_type_count(self):
        """Room type describes the number of different types of rooms."""
        return self._room_type_count

    @property
    def card_count_per_room(self):
        """Card count by Room Type is the number of each room type in the deck."""
        return self._card_count_per_room

    @property
    def duplicate_room_count(self):
        """Duplicate Room count."""
        return self._duplicate_room_count

    @property
    def duplicate_room_strategy(self):
        """Strategy used to build duplicate rooms. Default is DUPLICATE_ROOM_STRATEGY_EQUAL."""
        return self._duplicate_room_strategy

    @property
    def duplicate_room_intesity(self):
        """Duplicate room intensity."""
        return self._duplicate_room_intesity

    @property
    def imposter_chances(self):
        """Imposter chance count after killing the first time."""
        return self._imposter_chances

    @property
    def reward_imposter_to_crew(self):
        """Reward metric used when imposter is seeking a crew."""
        return self._reward_imposter_to_crew

    @property
    def reward_crew_to_body(self):
        """Reward metric used when crew is seeking the body."""
        return self._reward_crew_to_body

    @property
    def risk_crew_to_imposter(self):
        """Risk metric used when crew is moving to the imposter."""
        return self._risk_crew_to_imposter

    @property
    def risk_crew_to_rival(self):
        """Risk metric used when crew is moving to a rival."""
        return self._risk_crew_to_rival

    def is_valid_genotype(self):
        """Validate the genotype."""
        # Imposter Count less than or equal Players
        # Body less than or equal to rooms
        # Duplicate rooms must be less than or equal to room count

        is_valid = True
        is_valid = is_valid and (self._imposter_count < self._player_count)
        is_valid = is_valid and (self._body_count <= self.room_type_count)
        is_valid = is_valid and (self.duplicate_room_count <= self.room_type_count)

        return is_valid

    def get_assignments(self):
        """Get player assignments."""
        assignments = []

        for _ in range(self._imposter_count):
            assignments.append("Imposter")

        remaining_players = self._player_count - self._imposter_count

        for _ in range(remaining_players):
            assignments.append("Crew")
        random.shuffle(assignments)

        return assignments

    def get_deck(self):
        """Get deck for simulation."""
        deck = []
        for i in range(self.room_type_count):
            for _ in range(self.card_count_per_room):
                deck.append(f"Room{i}")
        random.shuffle(deck)
        return deck

    def get_body_locations(self, deck):
        """Get body locations for simulation."""
        body_locations = []
        for _ in range(self.body_count):
            # Don't place bodies in same room
            body_locations.append(
                random.choice([card for card in deck if card not in body_locations])
            )
        return body_locations

    def get_duplicate_rooms(self, deck):
        """Get the duplicate rooms."""
        potential_room_types = []
        for _ in range(self.duplicate_room_count):
            # Don't choose the same room type
            potential_room_types.append(
                random.choice(
                    [card for card in deck if card not in potential_room_types]
                )
            )

        potential_rooms = {}
        if self.duplicate_room_strategy == DUPLICATE_ROOM_STRATEGY_LADDER:
            ladder_count = 0
            for room_type in potential_room_types:
                potential_rooms[room_type] = self.duplicate_room_intesity + ladder_count
                ladder_count = ladder_count + 1
        else:
            for room_type in potential_room_types:
                potential_rooms[room_type] = self.duplicate_room_intesity

        return potential_rooms

    def score(self):
        """Return winning ratio score from simulation."""
        score = {}
        for _ in range(self._iterations):

            assignments = self.get_assignments()
            deck = self.get_deck()
            body_locations = self.get_body_locations(deck)
            potential_rooms = self.get_duplicate_rooms(deck)

            config = {}
            config[CONF_SEED] = random.randint(1, 100000000000)
            config[CONF_ASSIGNMENTS] = assignments
            config[CONF_BODY_LOCATIONS] = body_locations
            config[CONF_DECK] = deck
            config[CONF_POTENTIAL_ROOMS] = potential_rooms
            config[CONF_IMPOSTER_CHANCES] = self.imposter_chances
            config[CONF_REWARD_IMPOSTER_TO_CREW] = self.reward_imposter_to_crew
            config[CONF_REWARD_CREW_TO_BODY] = self.reward_crew_to_body
            config[CONF_RISK_CREW_TO_IMPOSTER] = self.risk_crew_to_imposter
            config[CONF_RISK_CREW_TO_RIVAL] = self.risk_crew_to_rival

            _, winner = Simulation(config).run()

            if winner not in score:
                score[winner] = 1
            else:
                score[winner] = score[winner] + 1

        crew_wins = score["Crew"] + score["Crew (Imposter ran out of turns)"]
        imposter_wins = score["Imposter"]

        return crew_wins / imposter_wins
