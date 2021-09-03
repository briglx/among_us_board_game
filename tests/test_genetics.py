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
    create_offspring,
    crossover,
    is_valid_genotype,
    mutate_genotype,
    parse_genotype,
    record_top_variants,
    select_parents,
    simple_genetic_algorithm,
    small_print_genotype,
)

from . import POOR_VARIANTS, VALID_GENOTYPE_MIN


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
    assert len(population_fitness) == 13
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


def test_create_offspring():
    """Test Create Offspring."""
    test_genome = np.array(ORIGINAL_GENOME)
    test_genome[:2] = [0, 1]
    population = np.array([ORIGINAL_GENOME, test_genome])
    seed = 100

    test_fitness = np.array([[0.3, 0.7]])
    # test_fitness.reshape(1, len(test_fitness))
    population_fitness = np.append(population, test_fitness.T, axis=1)

    offspring, _ = create_offspring(population_fitness, 10, POOR_VARIANTS, seed)

    assert offspring[0].tolist() not in POOR_VARIANTS.tolist()
    assert offspring[1].tolist() not in POOR_VARIANTS.tolist()
    assert offspring[2].tolist() not in POOR_VARIANTS.tolist()
    assert offspring[3].tolist() not in POOR_VARIANTS.tolist()
    assert offspring[4].tolist() not in POOR_VARIANTS.tolist()
    assert offspring[5].tolist() not in POOR_VARIANTS.tolist()
    assert offspring[6].tolist() not in POOR_VARIANTS.tolist()
    assert offspring[7].tolist() not in POOR_VARIANTS.tolist()
    assert offspring[8].tolist() not in POOR_VARIANTS.tolist()
    assert offspring[9].tolist() not in POOR_VARIANTS.tolist()


def test_record_top_variants_when_all_zero():
    """Test recording top variants."""
    generation = 1

    test_genome = np.array(ORIGINAL_GENOME)
    test_genome[:2] = [0, 1]
    population = np.array([ORIGINAL_GENOME, test_genome])

    test_fitness = np.array([[0.0, 0.0]])
    # test_fitness.reshape(1, len(test_fitness))
    population_fitness = np.append(population, test_fitness.T, axis=1)

    # Test no error
    record_top_variants(generation, population_fitness)

def test_small_print_genotype():
    """Test small print genotype."""

    test_genome = np.array(ORIGINAL_GENOME)
    str_genotype = small_print_genotype(test_genome)
                           
    assert str_genotype == '1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,1,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,1,0,1,0'