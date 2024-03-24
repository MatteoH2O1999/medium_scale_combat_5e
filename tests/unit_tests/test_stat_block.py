import pytest

import lib.attacks as attacks
import lib.targets as targets
import lib.stat_block as stat_block
from lib.ability_scores import AbilityScores, Scores


def get_stat_block_valid_params():
    return [
        "creature name",
        AbilityScores(12, 14, 8, 12, 14, 8),
        2,
        15,
        16,
        30,
        [
            attacks.AttackRollAttack(
                "melee attack name 1",
                5,
                1,
                targets.SingleTarget(),
                "1d8",
                0,
                False,
                Scores.STRENGTH,
                True,
                True,
                True,
                False,
            ),
            attacks.AttackRollAttack(
                "ranged attack name 1",
                80,
                1,
                targets.SingleTarget(),
                "1d10",
                1,
                True,
                Scores.DEXTERITY,
                True,
                True,
                True,
                False,
            ),
            attacks.SavingThrowAttack(
                "ranged spell attack name",
                120,
                1,
                targets.Sphere(30),
                "4d6",
                14,
                True,
                None,
                False,
                False,
            ),
        ],
    ]


def test_valid_constructor():
    block = stat_block.StatBlock(*get_stat_block_valid_params())
    assert block.name == "creature name"
    assert block.speed == 30
    assert block.proficiency_modifier == 2
    assert block.hit_points == 16
    assert block.armor_class == 15
    assert block.ability_scores == AbilityScores(12, 14, 8, 12, 14, 8)


def test_invalid_name_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[0] = ""
        stat_block.StatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[0] = 1
        stat_block.StatBlock(*params)


def test_invalid_scores_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[1] = "other"
        stat_block.StatBlock(*params)


def test_invalid_proficiency_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[2] = "other"
        stat_block.StatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[2] = 1.5
        stat_block.StatBlock(*params)


def test_invalid_ac_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[3] = "other"
        stat_block.StatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[3] = 0
        stat_block.StatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[3] = -1
        stat_block.StatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[3] = 1.5
        stat_block.StatBlock(*params)


def test_invalid_hp_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[4] = "other"
        stat_block.StatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[4] = 0
        stat_block.StatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[4] = -2
        stat_block.StatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[4] = 10.2
        stat_block.StatBlock(*params)


def test_invalid_speed_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[5] = "other"
        stat_block.StatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[5] = -2
        stat_block.StatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[5] = 10.2
        stat_block.StatBlock(*params)


def test_invalid_attacks_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[6] = "other"
        stat_block.StatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[6] = ["other"]
        stat_block.StatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_stat_block_valid_params()
        params[6][0] = params[6][1]
        stat_block.StatBlock(*params)


def test_attacks():
    block = stat_block.StatBlock(*get_stat_block_valid_params())
    assert block.attacks == {
        "melee attack name 1": attacks.CreatureMeleeAttack(
            "melee attack name 1", 1, 5, targets.SingleTarget(), 3, 5.5, 4.5, 1.0
        ),
        "ranged attack name 1": attacks.CreatureRangedAttack(
            "ranged attack name 1", 1, 80, targets.SingleTarget(), 5, 7.5, 5.5, 2.0
        ),
        "ranged spell attack name": attacks.CreatureRangedAttack(
            "ranged spell attack name", 1, 120, targets.Sphere(30), 6, 14.0, 14.0, 0.0
        ),
    }


def test_multiattacks():
    block = stat_block.StatBlock(*get_stat_block_valid_params())
    block.create_multiattack(
        "multiattack 1", ["melee attack name 1", "ranged attack name 1"]
    )
    block.create_multiattack(
        "multiattack 2",
        ["melee attack name 1", "melee attack name 1", "ranged attack name 1"],
    )

    assert block.multiattacks == {
        "multiattack 1": [
            attacks.CreatureMeleeAttack(
                "melee attack name 1", 1, 5, targets.SingleTarget(), 3, 5.5, 4.5, 1.0
            ),
            attacks.CreatureRangedAttack(
                "ranged attack name 1", 1, 80, targets.SingleTarget(), 5, 7.5, 5.5, 2.0
            ),
        ],
        "multiattack 2": [
            attacks.CreatureMeleeAttack(
                "melee attack name 1", 2, 5, targets.SingleTarget(), 3, 5.5, 4.5, 1.0
            ),
            attacks.CreatureRangedAttack(
                "ranged attack name 1", 1, 80, targets.SingleTarget(), 5, 7.5, 5.5, 2.0
            ),
        ],
    }


def test_multiattacks_duplicate_name():
    block = stat_block.StatBlock(*get_stat_block_valid_params())
    block.create_multiattack(
        "multiattack 1", ["melee attack name 1", "ranged attack name 1"]
    )
    with pytest.raises(stat_block.InvalidAttackNameError):
        block.create_multiattack(
            "multiattack 1", ["melee attack name 1", "ranged spell attack name"]
        )


def test_multiattacks_invalid_attack():
    block = stat_block.StatBlock(*get_stat_block_valid_params())
    with pytest.raises(stat_block.InvalidAttackNameError):
        block.create_multiattack("multiattack 1", ["melee attack name 1", "no attack"])
    with pytest.raises(stat_block.InvalidAttackNameError):
        block.create_multiattack("multiattack 1", ["melee attack name 1", None])
