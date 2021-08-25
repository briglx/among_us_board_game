"""Test Phoenotype."""
import numpy as np

from among_us.genetics import (
    DUPLICATE_ROOM_STRATEGY_EQUAL,
    DUPLICATE_ROOM_STRATEGY_LADDER,
    Phenotype,
)

VALID_GENOTYPE_LEN = 45
VALID_GENOTYPE_MIN = np.zeros(VALID_GENOTYPE_LEN, int).tolist()
VALID_GENOTYPE_MAX = np.ones(VALID_GENOTYPE_LEN, int).tolist()


def test_score():
    """Test score."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    score = phoenotype.score()

    assert round(score, 3) == 2.571


test_score()


def test_score_2():
    """Test score."""
    phoenotype = Phenotype(2, VALID_GENOTYPE_MIN)
    score = phoenotype.score()

    assert round(score, 3) == 2.846


def test_player_count_min():
    """Test min player count."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    assert phoenotype.player_count == 3


def test_player_count_max():
    """Test max player count."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.player_count == 18


def test_imposter_count_min():
    """Test min imposter count."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    assert phoenotype.imposter_count == 1


def test_imposter_count_max():
    """Test max imposter count."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.imposter_count == 8


def test_valid_body_count_min():
    """Test min body count."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    assert phoenotype.body_count == 1


def test_valid_body_count_max():
    """Test invalid body count."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.body_count == 8


def test_valid_room_type_count_min():
    """Test min room type count."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    assert phoenotype.room_type_count == 3


def test_valid_room_type_count_max():
    """Test max room type count."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.room_type_count == 10


def test_card_count_per_room_min():
    """Test min card count by type."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    assert phoenotype.card_count_per_room == 3


def test_card_count_per_room_max():
    """Test max card count by type."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.card_count_per_room == 18


def test_duplicate_room_count_min():
    """Test min card count by type."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    assert phoenotype.duplicate_room_count == 0


def test_duplicate_room_count_max():
    """Test max card count by type."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.duplicate_room_count == 15


def test_duplicate_room_strategy_ladder():
    """Test duplicate room strategy."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.duplicate_room_strategy == DUPLICATE_ROOM_STRATEGY_LADDER


def test_duplicate_room_strategy_default():
    """Test duplicate room strategy."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    assert phoenotype.duplicate_room_strategy == DUPLICATE_ROOM_STRATEGY_EQUAL


def test_duplicate_room_intensity_min():
    """Test min card count by type."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    assert phoenotype.duplicate_room_intesity == 1


def test_duplicate_room_cinstensity_max():
    """Test max card count by type."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.duplicate_room_intesity == 4


def test_imposter_chances_min():
    """Test min imposter chance."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    assert phoenotype.imposter_chances == 3


def test_imposter_chances_max():
    """Test max imposter chance."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.imposter_chances == 18


def test_reward_imposter_to_crew_min():
    """Test min reward imposter to crew."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    assert phoenotype.reward_imposter_to_crew == 0


def test_reward_imposter_to_crew_max():
    """Test max reward imposter to crew."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.reward_imposter_to_crew == 15


def test_reward_crew_to_body_min():
    """Test min reward crew to body."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    assert phoenotype.reward_crew_to_body == 0


def test_reward_crew_to_body_max():
    """Test max reward crew to body."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.reward_crew_to_body == 15


def test_risk_crew_to_imposter_min():
    """Test min risk crew to imposter."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    assert phoenotype.risk_crew_to_imposter == 0


def test_risk_crew_to_imposter_max():
    """Test max risk crew to imposter."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.risk_crew_to_imposter == 15


def test_risk_crew_to_rival_min():
    """Test min risk crew to rival."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MIN)
    assert phoenotype.risk_crew_to_rival == 0


def test_risk_crew_to_rival_max():
    """Test max risk crew to rival."""
    phoenotype = Phenotype(1, VALID_GENOTYPE_MAX)
    assert phoenotype.risk_crew_to_rival == 15
