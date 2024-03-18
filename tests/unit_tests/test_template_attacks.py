import pytest

import lib.attacks as attacks
import lib.targets as targets
from lib.ability_scores import Scores


def get_attack_roll_valid_params():
    return [
        "attack name",
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
    ]


def test_valid_attack_roll_constructor():
    params = get_attack_roll_valid_params()
    attack = attacks.AttackRollAttack(*params)
    assert attack._name == "attack name"
    assert attack._range == 5
    assert attack._multiattack == 1
    assert attack._target == targets.SingleTarget()
    assert attack._base_damage == "1d8"
    assert attack._base_to_hit == 0
    assert attack._ranged is False
    assert attack._ability_score_scaling == Scores.STRENGTH
    assert attack._damage_scaling is True
    assert attack._damage_proficiency is False
    assert attack._to_hit_proficiency is True
    assert attack._to_hit_scaling is True
    assert attack.name == "attack name"


def test_invalid_name_attack_roll_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[0] = ""
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[0] = 1
        attacks.AttackRollAttack(*params)


def test_invalid_range_attack_roll_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[1] = "other"
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[1] = 1.5
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[1] = -1
        attacks.AttackRollAttack(*params)


def test_invalid_multiattack_attack_roll_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[2] = -1
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[2] = 1.5
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[2] = "other"
        attacks.AttackRollAttack(*params)


def test_invalid_target_attack_roll_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[3] = "other"
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[3] = None
        attacks.AttackRollAttack(*params)


def test_invalid_base_damage_attack_roll_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[4] = 1.5
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[4] = "invalid"
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[4] = "-4d6"
        attacks.AttackRollAttack(*params)


def test_invalid_base_to_hit_attack_roll_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[5] = "other"
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[5] = -0.5
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[5] = 0.5
        attacks.AttackRollAttack(*params)


def test_invalid_scaling_attacks_roll_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[7] = "invalid"
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[8] = True
        params[10] = True
        params[7] = None
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[8] = False
        params[10] = True
        params[7] = None
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[8] = True
        params[10] = False
        params[7] = None
        attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_attack_roll_valid_params()
        params[8] = False
        params[10] = False
        attacks.AttackRollAttack(*params)
    params = get_attack_roll_valid_params()
    params[8] = False
    params[10] = False
    params[7] = None
    attacks.AttackRollAttack(*params)


def test_combine_success_attack_roll():
    params = get_attack_roll_valid_params()
    attack = attacks.AttackRollAttack(*params)
    combined = attack.combine(attack)
    assert isinstance(combined, attacks.AttackRollAttack)
    assert attack._multiattack == 1
    assert combined._multiattack == 2


def test_combine_failure_attack_roll():
    params = get_attack_roll_valid_params()
    attack = attacks.AttackRollAttack(*params)
    params[0] = "attack2"
    attack_2 = attacks.AttackRollAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        attack.combine(attack_2)
    with pytest.raises(attacks.InvalidAttackParamError):
        attack.combine("other")  # noqa


def test_eq_attack_roll():
    params = get_attack_roll_valid_params()
    attack = attacks.AttackRollAttack(*params)
    params[0] = "attack2"
    attack_2 = attacks.AttackRollAttack(*params)
    combined = attack.combine(attack)
    assert attack == attack
    assert attack != combined
    assert attack_2 != combined
    assert attack != attack_2
    assert attack_2 == attacks.AttackRollAttack(*params)
    assert attack != "other"


def get_saving_throw_valid_params():
    return [
        "attack name",
        5,
        1,
        targets.SingleTarget(),
        "4d6",
        15,
        True,
        Scores.WISDOM,
        True,
        False,
    ]


def test_valid_saving_throw_constructor():
    params = get_saving_throw_valid_params()
    attack = attacks.SavingThrowAttack(*params)
    assert attack._name == "attack name"
    assert attack._range == 5
    assert attack._multiattack == 1
    assert attack._target == targets.SingleTarget()
    assert attack._base_damage == "4d6"
    assert attack._dc == 15
    assert attack._ranged is True
    assert attack._ability_score_scaling == Scores.WISDOM
    assert attack._damage_scaling is True
    assert attack._damage_proficiency is False
    assert attack.name == "attack name"


def test_invalid_name_saving_throw_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[0] = ""
        attacks.SavingThrowAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[0] = 1
        attacks.SavingThrowAttack(*params)


def test_invalid_range_saving_throw_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[1] = "other"
        attacks.SavingThrowAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[1] = 1.5
        attacks.SavingThrowAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[1] = -1
        attacks.SavingThrowAttack(*params)


def test_invalid_multiattack_saving_throw_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[2] = -1
        attacks.SavingThrowAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[2] = 1.5
        attacks.SavingThrowAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[2] = "other"
        attacks.SavingThrowAttack(*params)


def test_invalid_target_saving_throw_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[3] = "other"
        attacks.SavingThrowAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[3] = None
        attacks.SavingThrowAttack(*params)


def test_invalid_base_damage_saving_throw_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[4] = 1.5
        attacks.SavingThrowAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[4] = "invalid"
        attacks.SavingThrowAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[4] = "-4d6"
        attacks.SavingThrowAttack(*params)


def test_invalid_dc_saving_throw_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[5] = "other"
        attacks.SavingThrowAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[5] = -0.5
        attacks.SavingThrowAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_saving_throw_valid_params()
        params[5] = 0.5
        attacks.SavingThrowAttack(*params)


def test_combine_success_saving_throw():
    params = get_saving_throw_valid_params()
    attack = attacks.SavingThrowAttack(*params)
    combined = attack.combine(attack)
    assert isinstance(combined, attacks.SavingThrowAttack)
    assert attack._multiattack == 1
    assert combined._multiattack == 2


def test_combine_failure_saving_throw():
    params = get_saving_throw_valid_params()
    attack = attacks.SavingThrowAttack(*params)
    params[0] = "attack2"
    attack_2 = attacks.SavingThrowAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        attack.combine(attack_2)
    with pytest.raises(attacks.InvalidAttackParamError):
        attack.combine("other")  # noqa


def test_eq_saving_throw():
    params = get_saving_throw_valid_params()
    attack = attacks.SavingThrowAttack(*params)
    params[0] = "attack2"
    attack_2 = attacks.SavingThrowAttack(*params)
    combined = attack.combine(attack)
    assert attack == attack
    assert attack != combined
    assert attack_2 != combined
    assert attack != attack_2
    assert attack_2 == attacks.SavingThrowAttack(*params)
    assert attack != "other"
