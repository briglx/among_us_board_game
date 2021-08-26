"""Genetic Algorithm to optimize game parameters."""
import random

import numpy as np

from among_us import Simulation

# Genome is made up of an array of features.
# [0, 0, 1, ... , 0, 1, 1]
# The index of the feature is define by the constants below

# Player Count is bitwise added from 0-15
# Base is 3 so values are 3-18
# index[0:4]
PLAYER_COUNT_0 = 0
PLAYER_COUNT_2 = 1
PLAYER_COUNT_4 = 2
PLAYER_COUNT_8 = 3

# Imposter is bitwise added from 0 to 7
# Base is 1 so values are 1-8
# index[4:7]
IMPOSTER_COUNT_0 = 4
IMPOSTER_COUNT_2 = 5
IMPOSTER_COUNT_4 = 6

# Body count is bitwise added from 0 to 7
# Base is 1 so values are 1-8
# index[7:10]
BODY_COUNT_0 = 7
BODY_COUNT_2 = 8
BODY_COUNT_4 = 9

# Room type count is bitwise from 0-7
# Describes the number of different types of rooms
# Base is 3 so values are 3-10
# index[10:13]
ROOM_TYPE_COUNT_0 = 10
ROOM_TYPE_COUNT_2 = 11
ROOM_TYPE_COUNT_4 = 12

# Card count by Room Type is the number of each room type in the deck
# is bitwise added from 0 to 15
# Base is 3 so values are 3-18
# index[13:17]
CARD_COUNT_BY_ROOM_0 = 13
CARD_COUNT_BY_ROOM_2 = 14
CARD_COUNT_BY_ROOM_4 = 15
CARD_COUNT_BY_ROOM_8 = 16

# Duplicate Rooms is Bitwise added from 0-7
# index[17:20]
DUPLICATE_ROOMS_0 = 17
DUPLICATE_ROOMS_2 = 18
DUPLICATE_ROOMS_4 = 19

# Duplicate Rooms Strategy is how the rooms are built and is Categorical.
# Default behavior is to build DUPLICATE_ROOM_STRATEGY_EQUAL  is Bitwise added from 0-15
# index[20:21]
DUPLICATE_ROOM_STRATEGY_EQUAL = (
    101  # All duplicate rooms will have the same number of rooms
)
DUPLICATE_ROOM_STRATEGY_LADDER = 20  # Duplicate Rooms will have growing number of room

# Duplicate room instensity determines the number of duplicate room is Bitwise added from 0-3
# Base is 1 so values are 1-4
# index[21:23]
DUPLICATE_ROOM_INTESITY_0 = 21
DUPLICATE_ROOM_INTESITY_2 = 22

# Imposter chances are bitwise added from 0-15.
# Base is 3 so values are 3-18
# index[23:27]
IMPOSTER_CHANCES_0 = 23
IMPOSTER_CHANCES_2 = 24
IMPOSTER_CHANCES_4 = 25
IMPOSTER_CHANCES_8 = 26

# Reward Imposter to Crew is bitwise added from 0 to 15
# index[27:31]
REWARD_IMPOSTER_TO_CREW_0 = 27
REWARD_IMPOSTER_TO_CREW_2 = 28
REWARD_IMPOSTER_TO_CREW_4 = 29
REWARD_IMPOSTER_TO_CREW_8 = 30

# Reward Crew to Body is bitwise added from 0 to 15
# index[31:34]
REWARD_CREW_TO_BODY_0 = 31
REWARD_CREW_TO_BODY_2 = 32
REWARD_CREW_TO_BODY_4 = 33
REWARD_CREW_TO_BODY_8 = 34

# Reward Crew to Imposter is bitwise added from 0 to 15
# index[35:39]
RISK_CREW_TO_IMPOSTER_0 = 35
RISK_CREW_TO_IMPOSTER_2 = 36
RISK_CREW_TO_IMPOSTER_4 = 37
RISK_CREW_TO_IMPOSTER_8 = 38

# Reward Crew to Rival is bitwise added from 0 to 15
# index[39:43]
RISK_CREW_TO_RIVAL_0 = 39
RISK_CREW_TO_RIVAL_2 = 40
RISK_CREW_TO_RIVAL_4 = 41
RISK_CREW_TO_RIVAL_8 = 42

# Other Invalid combinations
# Imposter Count Greater than or equal Players
# Body count greater than or equal to rooms
# Duplicate rooms can't be greater than room count


def create_random_population(size):
    """Create random population from size."""
    population = [np.random.randint(0, 2, 45).tolist() for _ in range(size)]
    return population


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

    def score(self):
        """Return winning ratio score from simulation."""
        score = {}
        for _ in range(self._iterations):
            seed = random.randint(1, 100000000000)
            sim = Simulation(seed=seed)
            _, winner = sim.run()

            if winner not in score:
                score[winner] = 1
            else:
                score[winner] = score[winner] + 1

        crew_wins = score["Crew"] + score["Crew (Imposter ran out of turns)"]
        imposter_wins = score["Imposter"]

        return crew_wins / imposter_wins
