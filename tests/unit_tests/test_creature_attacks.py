import pytest

import lib.attacks as attacks
import lib.targets as targets


def get_creature_attack_valid_params():
    return ["name", 1, 5, targets.SingleTarget(), 2, 1.0, 1.0, 0.0]


def test_valid_melee_constructor():
    melee_attack = attacks.CreatureMeleeAttack(*get_creature_attack_valid_params())
    assert isinstance(melee_attack, attacks.CreatureMeleeAttack)
    assert melee_attack.is_melee is True
    assert melee_attack.name == "name"
    assert melee_attack.target == targets.SingleTarget()
    assert melee_attack.range == 5
    assert melee_attack.multiattack == 1
    assert melee_attack.to_hit_bonus == 2
    assert melee_attack.total_average_damage == 1.0
    assert melee_attack.dice_average_damage == 1.0
    assert melee_attack.fixed_damage == 0.0


def test_valid_ranged_constructor():
    ranged_attack = attacks.CreatureRangedAttack(*get_creature_attack_valid_params())
    assert isinstance(ranged_attack, attacks.CreatureRangedAttack)
    assert ranged_attack.is_melee is False
    assert ranged_attack.name == "name"
    assert ranged_attack.target == targets.SingleTarget()
    assert ranged_attack.range == 5
    assert ranged_attack.multiattack == 1
    assert ranged_attack.to_hit_bonus == 2
    assert ranged_attack.total_average_damage == 1.0
    assert ranged_attack.dice_average_damage == 1.0
    assert ranged_attack.fixed_damage == 0.0


def test_invalid_name_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[0] = ""
        attacks.CreatureMeleeAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[0] = 1
        attacks.CreatureMeleeAttack(*params)


def test_invalid_multiattack_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[1] = 0
        attacks.CreatureMeleeAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[1] = 1.5
        attacks.CreatureMeleeAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[1] = -10
        attacks.CreatureMeleeAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[1] = "other"
        attacks.CreatureMeleeAttack(*params)


def test_invalid_range_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[2] = "other"
        attacks.CreatureMeleeAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[2] = -1
        attacks.CreatureMeleeAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[2] = 1.1
        attacks.CreatureMeleeAttack(*params)


def test_invalid_target_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[3] = "other"
        attacks.CreatureMeleeAttack(*params)


def test_invalid_to_hit_bonus_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[4] = "other"
        attacks.CreatureMeleeAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[4] = 1.1
        attacks.CreatureMeleeAttack(*params)


def test_invalid_total_damage_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[5] = -1.0
        attacks.CreatureMeleeAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[5] = 3
        attacks.CreatureMeleeAttack(*params)


def test_invalid_dice_damage_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[6] = -1.0
        attacks.CreatureMeleeAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[6] = 3
        attacks.CreatureMeleeAttack(*params)


def test_invalid_fixed_damage_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[7] = 3
        attacks.CreatureMeleeAttack(*params)


def test_invalid_name_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[0] = ""
        attacks.CreatureRangedAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[0] = 1
        attacks.CreatureRangedAttack(*params)


def test_invalid_multiattack_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[1] = 0
        attacks.CreatureRangedAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[1] = 1.5
        attacks.CreatureRangedAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[1] = -10
        attacks.CreatureRangedAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[1] = "other"
        attacks.CreatureRangedAttack(*params)


def test_invalid_range_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[2] = "other"
        attacks.CreatureRangedAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[2] = -1
        attacks.CreatureRangedAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[2] = 1.1
        attacks.CreatureRangedAttack(*params)


def test_invalid_target_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[3] = "other"
        attacks.CreatureRangedAttack(*params)


def test_invalid_to_hit_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[4] = "other"
        attacks.CreatureRangedAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[4] = 1.1
        attacks.CreatureRangedAttack(*params)


def test_invalid_total_damage_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[5] = -1.0
        attacks.CreatureRangedAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[5] = 3
        attacks.CreatureRangedAttack(*params)


def test_invalid_dice_damage_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[6] = -1.0
        attacks.CreatureRangedAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[6] = 3
        attacks.CreatureRangedAttack(*params)


def test_invalid_fixed_damage_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_creature_attack_valid_params()
        params[7] = 3
        attacks.CreatureRangedAttack(*params)
