"""Test Genetics."""
import numpy as np

from among_us.const import (
    BODY_COUNT,
    CARD_COUNT_BY_ROOM,
    DUPLICATE_ROOM_INTESITY,
    DUPLICATE_ROOM_STRATEGY,
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
)
from among_us.genetics import (
    calc_fitness,
    crossover,
    is_valid_genotype,
    mutate_genotype,
    parse_genotype,
    select_parents,
    simple_genetic_algorithm,
)

VALID_GENOTYPE_MIN = np.zeros(VALID_GENOTYPE_LEN, int).tolist()


def test_calc_fitness():
    """Calculate the fitness for the original genome."""
    fitness = calc_fitness(ORIGINAL_GENOME, 1)
    assert round(fitness, 3) == 0.00


def test_calc_min_genome_fitness():
    """Calculate the fitness for the min genome."""
    fitness = calc_fitness(VALID_GENOTYPE_MIN, 1)
    assert round(fitness, 3) == 0.095


def test_simple_genetic_algorithm():
    """Test genetic algorithm."""
    population_fitness = simple_genetic_algorithm(100, generations=2)

    # print(parents)
    assert len(population_fitness) == 12
    assert population_fitness.max() == 1.0
    # assert fitnesses[4][0] == 0.72987


def test_parse_genotype():
    """Test Parse Genotype."""
    parsed_genotype = parse_genotype(ORIGINAL_GENOME)

    assert parsed_genotype[PLAYER_COUNT] == 4
    assert parsed_genotype[IMPOSTER_COUNT] == 1
    assert parsed_genotype[BODY_COUNT] == 1
    assert parsed_genotype[ROOM_TYPE_COUNT] == 7
    assert parsed_genotype[CARD_COUNT_BY_ROOM] == 5
    assert parsed_genotype[DUPLICATE_ROOMS] == 2
    assert parsed_genotype[DUPLICATE_ROOM_STRATEGY] == DUPLICATE_ROOM_STRATEGY_LADDER
    assert parsed_genotype[DUPLICATE_ROOM_INTESITY] == 2
    assert parsed_genotype[IMPOSTER_CHANCES] == 5
    assert parsed_genotype[REWARD_IMPOSTER_TO_CREW] == 10
    assert parsed_genotype[REWARD_CREW_TO_BODY] == 1
    assert parsed_genotype[RISK_CREW_TO_IMPOSTER] == 10
    assert parsed_genotype[RISK_CREW_TO_RIVAL] == 5


def test_mutate_genotype_head():
    """Test Mutate_genotype."""
    point = 4
    is_head = True
    seed = 1
    mutated = mutate_genotype(ORIGINAL_GENOME, point, is_head, seed)

    assert np.all(mutated[point:] == ORIGINAL_GENOME[point:])
    assert np.all(mutated[:point] == [1, 1, 0, 0])


def test_mutate_genotype_tail():
    """Test Mutate_genotype."""
    point = len(ORIGINAL_GENOME) - 4
    is_head = False
    seed = 1
    mutated = mutate_genotype(ORIGINAL_GENOME, point, is_head, seed)

    assert np.all(mutated[:point] == ORIGINAL_GENOME[:point])
    assert np.all(mutated[point:] == [1, 1, 0, 0])


def test_select_parents_few_population():
    """Test selecting parents."""
    population_fitness = np.array([[0, 1, 0, 0.5]])
    parents = select_parents(population_fitness)

    assert parents is None


def test_select_parents():
    """Test selecting parents."""
    population_fitness = np.array([[1, 0, 0, 0.5], [0, 1, 0, 0.5]])
    parents = select_parents(population_fitness)

    assert len(parents) == 2


def test_select_parents_default_prob():
    """Test selecting parents."""
    population_fitness = np.array([[1, 0, 0], [0, 1, 0]])
    parents = select_parents(population_fitness)

    assert len(parents) == 2


def test_select_parents_few_non_zero():
    """Test when Fewer non-zero entries in p than size."""

    population_fitness = np.array([[1, 0, 0, 0.0], [0, 1, 0, 1.0]])
    parents = select_parents(population_fitness)

    assert len(parents) == 2


def test_select_best_parents():
    """Test selecting the best parents"""
    population_fitness = np.array(
        [[0, 0, 0, 0.0], [0, 0, 1, 0.0], [0, 1, 0, 0.5], [0, 1, 1, 0.5]]
    )
    parents = select_parents(population_fitness)

    assert len(parents) == 2
    assert parents[0][1] == 1
    assert parents[1][1] == 1


def test_is_valid_genotype():
    """Test valid genotype."""

    assert is_valid_genotype(ORIGINAL_GENOME)


def test_is_invalid_genotype():
    """Test invalid genotype."""
    invalid_genotype = np.zeros(VALID_GENOTYPE_LEN, int)
    invalid_genotype[4:7] = 1  # Update Imposter Count
    assert not is_valid_genotype(invalid_genotype)


def test_crossover():
    """Test genotype crossover."""
    # test_fitness = np.array([[0.3, 0.7]])
    # test_fitness.reshape(1, len(test_fitness))
    test_genome = np.array(ORIGINAL_GENOME)
    test_genome[:2] = [0, 1]
    population = np.array([ORIGINAL_GENOME, test_genome])
    # population_fitness = np.append(population, test_fitness.T, axis=1)

    offspring, _ = crossover(population)

    assert len(offspring) == 2
