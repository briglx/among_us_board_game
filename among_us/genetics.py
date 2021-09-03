"""Genetic Algorithm to optimize game parameters."""
import logging
import math
import random

import numpy as np

from among_us import Simulation

from .const import (
    BODY_COUNT,
    CARD_COUNT_BY_ROOM,
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
    DUPLICATE_ROOM_INTESITY,
    DUPLICATE_ROOM_STRATEGY,
    DUPLICATE_ROOM_STRATEGY_EQUAL,
    DUPLICATE_ROOM_STRATEGY_LADDER,
    DUPLICATE_ROOMS,
    IMPOSTER_CHANCES,
    IMPOSTER_COUNT,
    ORIGINAL_GENOME,
    PLAYER_COUNT,
    REWARD_CREW_TO_BODY,
    REWARD_IMPOSTER_TO_CREW,
    RISK_CREW_TO_IMPOSTER,
    RISK_CREW_TO_RIVAL,
    ROOM_TYPE_COUNT,
    VALID_GENOTYPE_LEN,
    WINNER_CREW,
    WINNER_CREW_TURNS,
    WINNER_IMPOSTER,
)

POOR_VARIANT_FILE_NAME = "poor_variants.out"

variant_logger = logging.getLogger("algo_run_history")
fmt = logging.Formatter("%(asctime)s %(message)s", datefmt="%Y-%m-%d-%H:%M:%S")
handler = logging.FileHandler("among_us_variants.log")
handler.setFormatter(fmt)
variant_logger.addHandler(handler)
variant_logger.setLevel(logging.INFO)


def create_random_population(size, seed=None):
    """Create random population from size."""
    np.random.seed(seed)
    population = []

    count = 0
    while count < size:
        try:
            genotype = np.random.randint(0, 2, VALID_GENOTYPE_LEN).tolist()
            Phenotype(seed, genotype)
            population.append(genotype)
            count = count + 1
        except ValueError:
            pass

    return np.array(population).astype(int)


def calc_fitness(genotype, seed=None):
    """Calculate the fitness of the genotype. Return a number between 0-1.

    Gaussian curve around 1 with a long tail. 1/2 and 2 give similar results
    1/3 and 3 also give similar results.
    y=e^(-10(log(x^2))) long tail
    y=e^(-h(x-1)^2) original with hyper parameter
    """
    hyper_parameter_standard_dev = -1

    phenotype = Phenotype(seed, genotype)
    score = phenotype.score()

    # fitness = math.exp(hyper_parameter_standard_dev * (score-1)**2)

    # Long tail
    fitness = math.exp(10 * hyper_parameter_standard_dev * (math.log(score)) ** 2)

    return round(fitness, 5)


def select_parents(pop_fit, seed=None):
    """Select the best genotypes based on fitness."""
    rng = np.random
    rng.seed(seed)

    if len(pop_fit) < 2:
        return None

    # Add small value in case of zeros and normalize
    pop_fit = pop_fit.astype(float)
    pop_fit[:, -1] += 0.0001
    pop_fit[:, -1] = pop_fit[:, -1] / pop_fit[:, -1].sum()

    # Select parents based on probabilities
    parents = pop_fit[
        rng.choice(len(pop_fit), 2, replace=False, p=pop_fit[:, -1]), :-1
    ].astype(int)
    return parents


def is_valid_genotype(genotype):
    """Check is genotype is valid."""
    try:
        Phenotype(seed=None, genotype=genotype)
        return True
    except ValueError:
        return False


def crossover(parents, seed=None):
    """Cross over the pair at a randomly chosen point.

    parents are only the genotype.

    """
    count = 0
    offspring = []

    random.seed(seed)

    while count < 2:

        point = random.randrange(1, len(parents[0][:-1]))

        offspring1 = np.concatenate((parents[0][:point], parents[1][point:]))
        offspring2 = np.concatenate((parents[1][:point], parents[0][point:]))

        if is_valid_genotype(offspring1) and is_valid_genotype(offspring2):

            offspring.append(offspring1)
            offspring.append(offspring2)
            count = count + 2

    return (offspring, point)


def mutate_genotype(genotype, point, is_head, seed=None):
    """Mutate genotype at locus."""
    np.random.seed(seed)
    while True:

        if is_head:
            mutant_alleles = np.random.randint(0, 2, point).tolist()
            mutated_genotype = np.concatenate((mutant_alleles, genotype[point:]))
        else:

            mutant_alleles = np.random.randint(
                0, 2, VALID_GENOTYPE_LEN - point
            ).tolist()
            mutated_genotype = np.concatenate((genotype[:point], mutant_alleles))

        if is_valid_genotype(mutated_genotype):
            return mutated_genotype


def create_offspring(population_fitness, size, poor_variants, seed=None):
    """Create offspring from parents."""
    mutation_threshold = 0.1
    rng = np.random
    rng.seed(seed)

    # Select Parents
    parents = select_parents(population_fitness)
    # parents = np.array(parents).astype(int)

    # Select Children from different crossover points
    children = set()
    while len(children) < size:
        # Cross over
        offspring, point = crossover(parents)

        potential_child1 = None
        potential_child2 = None
        # Check first Offspring
        if rng.rand() < mutation_threshold:
            potential_child1 = mutate_genotype(offspring[0], point, True, seed)
            # children.add(tuple(child1))
        else:
            potential_child1 = offspring[0]
            # children.add(tuple(offspring[0]))

        if potential_child1.tolist() not in poor_variants.tolist():
            children.add(tuple(potential_child1))

        # Check second offspring
        if rng.rand() < mutation_threshold:
            potential_child2 = mutate_genotype(offspring[1], point, False, seed)
        else:
            potential_child2 = offspring[1]

        if potential_child2.tolist() not in poor_variants.tolist():
            children.add(tuple(potential_child2))

    # convert set back to arrays
    items = []
    for child in children:
        items.append(list(child))
    children = np.array(items)

    return children, parents


def get_poor_variants():
    """Load poor variants."""
    poor_variants = np.empty((0, 43))
    try:
        poor_variants = np.loadtxt(POOR_VARIANT_FILE_NAME, dtype="int64", delimiter=",")
    except OSError:
        pass

    return poor_variants


def add_poor_variants(poor_variants, pop_fit):
    """Add poor variants to list."""
    new_variants = pop_fit[np.where(pop_fit[:, -1] == 0)][:, :-1].astype(int)

    # Append variants to save_file
    variant_file = open(POOR_VARIANT_FILE_NAME, "a")
    np.savetxt(variant_file, new_variants, fmt="%.0f", delimiter=",")
    variant_file.close()

    # Append to in-memory list
    if len(poor_variants) == 0:
        poor_variants = new_variants
    else:
        poor_variants = np.concatenate((poor_variants, new_variants))

    return poor_variants


def record_top_variants(generation, pop_fit):
    """Record the top performs."""
    top_idx = np.argmax(pop_fit[:, -1])

    top_variant = pop_fit[top_idx, :-1].astype(int)
    score = pop_fit[top_idx, -1]

    # top_variant = pop_fit[top_idx][:,:-1].astype(int)
    # score = pop_fit[top_idx][-1]
    variant_logger.info("Gen-%s, %.5f, %s ", generation, score, top_variant)


def simple_genetic_algorithm(seed=None, generations=100):
    """Implement a simple genetic algorithm."""
    population_size = 10

    variant_logger.info(
        "Simple genetic algorithm run. Seed:%s, Generations:%s", seed, generations
    )

    poor_variants = get_poor_variants()
    variant_logger.info("Loading %s poor variants.", len(poor_variants))

    # Select randomly generated population
    random.seed(seed)
    population = create_random_population(population_size, seed)
    population = np.vstack([population, np.array(ORIGINAL_GENOME)])

    for generation in range(generations):
        fitnesses = []
        # Calculate Fitness for Population
        for genotype in population:
            fitness = calc_fitness(genotype, random.randint(1, 100000000000))
            fitnesses.append(fitness)

        fitnesses = np.array(fitnesses)
        if fitnesses.sum() > 0:
            fitnesses = fitnesses / fitnesses.sum()
        fitness_score = fitnesses.reshape(1, len(fitnesses))
        population_fitness = np.append(population, fitness_score.T, axis=1)

        # Track top/poor variants
        poor_variants = add_poor_variants(poor_variants, population_fitness)
        record_top_variants(generation, population_fitness)

        # Select Offspring
        offspring, parents = create_offspring(
            population_fitness, 10, poor_variants, seed
        )
        population = np.concatenate((offspring, parents))

    # Calc last population
    fitnesses = []
    for genotype in population:
        fitness = calc_fitness(genotype, random.randint(1, 100000000000))
        fitnesses.append(fitness)

    fitnesses = np.array(fitnesses)
    if fitnesses.sum() > 0:
        fitnesses = fitnesses / fitnesses.sum()
    fitnesses = fitnesses.reshape(1, len(fitnesses))
    population_fitness = np.append(population, fitnesses.T, axis=1)

    # Track top/poor variants
    poor_variants = add_poor_variants(poor_variants, population_fitness)
    record_top_variants(generation + 1, population_fitness)

    return population_fitness


def parse_genotype(genotype):
    """Parse genotype to readable dictionary."""
    # Parse genotype
    parsed_genotype = {}

    parsed_genotype[PLAYER_COUNT] = (
        3 + np.packbits(genotype[:4], bitorder="little").tolist()[0]
    )
    parsed_genotype[IMPOSTER_COUNT] = (
        1 + np.packbits(genotype[4:6], bitorder="little").tolist()[0]
    )
    parsed_genotype[BODY_COUNT] = (
        1 + np.packbits(genotype[7:10], bitorder="little").tolist()[0]
    )
    parsed_genotype[ROOM_TYPE_COUNT] = (
        3 + np.packbits(genotype[10:13], bitorder="little").tolist()[0]
    )
    parsed_genotype[CARD_COUNT_BY_ROOM] = (
        3 + np.packbits(genotype[13:17], bitorder="little").tolist()[0]
    )
    parsed_genotype[DUPLICATE_ROOMS] = np.packbits(
        genotype[17:20], bitorder="little"
    ).tolist()[0]
    if np.packbits(genotype[20:21], bitorder="little").tolist()[0]:
        parsed_genotype[DUPLICATE_ROOM_STRATEGY] = DUPLICATE_ROOM_STRATEGY_LADDER
    else:
        parsed_genotype[DUPLICATE_ROOM_STRATEGY] = DUPLICATE_ROOM_STRATEGY_EQUAL
    parsed_genotype[DUPLICATE_ROOM_INTESITY] = (
        1 + np.packbits(genotype[21:23], bitorder="little").tolist()[0]
    )
    parsed_genotype[IMPOSTER_CHANCES] = (
        3 + np.packbits(genotype[23:27], bitorder="little").tolist()[0]
    )
    parsed_genotype[REWARD_IMPOSTER_TO_CREW] = np.packbits(
        genotype[27:31], bitorder="little"
    ).tolist()[0]
    parsed_genotype[REWARD_CREW_TO_BODY] = np.packbits(
        genotype[31:35], bitorder="little"
    ).tolist()[0]
    parsed_genotype[RISK_CREW_TO_IMPOSTER] = np.packbits(
        genotype[35:39], bitorder="little"
    ).tolist()[0]
    parsed_genotype[RISK_CREW_TO_RIVAL] = np.packbits(
        genotype[39:43], bitorder="little"
    ).tolist()[0]
    return parsed_genotype


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
            1 + np.packbits(genotype[4:6], bitorder="little").tolist()[0]
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

        crew_wins = 0
        if score.get(WINNER_CREW):
            crew_wins = crew_wins + score.get(WINNER_CREW)
        if score.get(WINNER_CREW_TURNS):
            crew_wins = crew_wins + score.get(WINNER_CREW_TURNS)

        imposter_wins = 0.0000001  # avoid divide by zero
        if score.get(WINNER_IMPOSTER):
            imposter_wins = score.get(WINNER_IMPOSTER)

        return (crew_wins + 0.0001) / imposter_wins
