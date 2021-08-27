"""Test Phoenotype."""
import logging

import numpy as np
import pytest

from among_us.const import (
    DUPLICATE_ROOM_STRATEGY_EQUAL,
    DUPLICATE_ROOM_STRATEGY_LADDER,
    ORIGINAL_GENOME,
    VALID_GENOTYPE_LEN,
)
from among_us.genetics import Phenotype

VALID_GENOTYPE_MIN = np.zeros(VALID_GENOTYPE_LEN, int).tolist()
VALID_GENOTYPE_MAX = np.ones(VALID_GENOTYPE_LEN, int).tolist()

logging.basicConfig(filename="game.log", level=logging.ERROR)


def test_original_phonotype():
    """Test original gameplay."""
    phoenotype = Phenotype(1, ORIGINAL_GENOME)

    assert phoenotype.player_count == 4
    assert phoenotype.imposter_count == 1
    assert phoenotype.body_count == 1
    assert phoenotype.room_type_count == 7
    assert phoenotype.card_count_per_room == 5
    assert phoenotype.duplicate_room_count == 2
    assert phoenotype.duplicate_room_strategy == DUPLICATE_ROOM_STRATEGY_LADDER
    assert phoenotype.duplicate_room_intesity == 2
    assert phoenotype.imposter_chances == 5
    assert phoenotype.reward_imposter_to_crew == 10
    assert phoenotype.reward_crew_to_body == 1
    assert phoenotype.risk_crew_to_imposter == 10
    assert phoenotype.risk_crew_to_rival == 5

    assert round(phoenotype.score(), 3) == 5.452


def test_phonotype_strategy_equal():
    """Test original gameplay."""
    test_genome = np.array(ORIGINAL_GENOME)
    test_genome[20] = 0
    phoenotype = Phenotype(1, test_genome)

    assert phoenotype.player_count == 4
    assert phoenotype.imposter_count == 1
    assert phoenotype.body_count == 1
    assert phoenotype.room_type_count == 7
    assert phoenotype.card_count_per_room == 5
    assert phoenotype.duplicate_room_count == 2
    assert phoenotype.duplicate_room_strategy == DUPLICATE_ROOM_STRATEGY_EQUAL
    assert phoenotype.duplicate_room_intesity == 2
    assert phoenotype.imposter_chances == 5
    assert phoenotype.reward_imposter_to_crew == 10
    assert phoenotype.reward_crew_to_body == 1
    assert phoenotype.risk_crew_to_imposter == 10
    assert phoenotype.risk_crew_to_rival == 5

    assert round(phoenotype.score(), 3) == 5.452


def test_score():
    """Test score."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    score = phoenotype.score()

    assert round(score, 3) == 1.625


def test_score_2():
    """Test score."""
    phoenotype = Phenotype(2, VALID_GENOTYPE_MIN)
    score = phoenotype.score()

    assert round(score, 3) == 1.457


def test_player_count_min():
    """Test min player count."""

    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)

    assert phoenotype.player_count == 3
    assert phoenotype.imposter_count == 1
    assert phoenotype.body_count == 1
    assert phoenotype.room_type_count == 3
    assert phoenotype.card_count_per_room == 3
    assert phoenotype.duplicate_room_count == 0
    assert phoenotype.duplicate_room_strategy == DUPLICATE_ROOM_STRATEGY_EQUAL
    assert phoenotype.duplicate_room_intesity == 1
    assert phoenotype.imposter_chances == 3
    assert phoenotype.reward_imposter_to_crew == 0
    assert phoenotype.reward_crew_to_body == 0
    assert phoenotype.risk_crew_to_imposter == 0
    assert phoenotype.risk_crew_to_rival == 0


def test_duplicate_room_strategy_ladder():
    """Test duplicate room strategy."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.player_count == 18
    assert phoenotype.imposter_count == 8
    assert phoenotype.body_count == 8
    assert phoenotype.room_type_count == 10
    assert phoenotype.card_count_per_room == 18
    assert phoenotype.duplicate_room_count == 7
    assert phoenotype.duplicate_room_strategy == DUPLICATE_ROOM_STRATEGY_LADDER
    assert phoenotype.duplicate_room_intesity == 4
    assert phoenotype.imposter_chances == 18
    assert phoenotype.reward_imposter_to_crew == 15
    assert phoenotype.reward_crew_to_body == 15
    assert phoenotype.risk_crew_to_imposter == 15
    assert phoenotype.risk_crew_to_rival == 15


def test_invalid_genotype_imposter_player():
    """Test invalid genotype."""
    invalid_genotype = np.zeros(VALID_GENOTYPE_LEN, int)
    invalid_genotype[4:7] = 1  # Update Imposter Count

    with pytest.raises(ValueError):
        Phenotype(2, invalid_genotype.tolist())


def test_invalid_genotype_body_room():
    """Test invalid genotype."""
    invalid_genotype = np.zeros(VALID_GENOTYPE_LEN, int)
    invalid_genotype[7:11] = 1  # Update Body Count

    with pytest.raises(ValueError):
        Phenotype(2, invalid_genotype.tolist())


def test_invalid_genotype_duplicate_to_room():
    """Test invalid genotype."""
    invalid_genotype = np.zeros(VALID_GENOTYPE_LEN, int)
    invalid_genotype[17:21] = 1  # Update Body Count

    with pytest.raises(ValueError):
        Phenotype(2, invalid_genotype.tolist())
