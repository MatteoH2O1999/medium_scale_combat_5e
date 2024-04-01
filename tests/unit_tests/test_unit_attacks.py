import pytest

import lib.interfaces as interfaces
import lib.targets as targets
import lib.unit_attacks as attacks


def get_unit_attack_valid_params():
    return ["attack name", 5, "D3+1", 3, 6, -1, "2"]


def test_valid_melee_constructor():
    melee_attack = attacks.MeleeUnitAttack(*get_unit_attack_valid_params())
    assert isinstance(melee_attack, attacks.MeleeUnitAttack)
    assert melee_attack.name == "attack name"
    assert melee_attack.range == 5
    assert melee_attack.number_of_attacks == "D3+1"
    assert melee_attack.attack_skill == 3
    assert melee_attack.strength == 6
    assert melee_attack.armor_penetration == -1
    assert melee_attack.damage == "2"
    assert melee_attack.is_melee is True


def test_valid_ranged_constructor():
    ranged_attack = attacks.RangedUnitAttack(*get_unit_attack_valid_params())
    assert isinstance(ranged_attack, attacks.RangedUnitAttack)
    assert ranged_attack.name == "attack name"
    assert ranged_attack.range == 5
    assert ranged_attack.number_of_attacks == "D3+1"
    assert ranged_attack.attack_skill == 3
    assert ranged_attack.strength == 6
    assert ranged_attack.armor_penetration == -1
    assert ranged_attack.damage == "2"
    assert ranged_attack.is_melee is False


def test_invalid_name_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[0] = ""
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[0] = 1
        attacks.MeleeUnitAttack(*params)


def test_invalid_range_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[1] = -1
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[1] = 1.5
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[1] = "other"
        attacks.MeleeUnitAttack(*params)


def test_invalid_number_of_attacks_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[2] = "0"
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[2] = "-1"
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[2] = "other"
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[2] = -1
        attacks.MeleeUnitAttack(*params)


def test_invalid_skill_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[3] = -1
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[3] = 0
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[3] = 10
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[3] = 4.5
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[3] = "other"
        attacks.MeleeUnitAttack(*params)


def test_invalid_strength_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[4] = -1
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[4] = 0
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[4] = 3.5
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[4] = "other"
        attacks.MeleeUnitAttack(*params)


def test_invalid_ap_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[5] = 0.5
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[5] = "other"
        attacks.MeleeUnitAttack(*params)


def test_invalid_damage_melee_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[6] = ""
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[6] = "-1"
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[6] = "-D3"
        attacks.MeleeUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[6] = "other"
        attacks.MeleeUnitAttack(*params)


def test_invalid_name_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[0] = ""
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[0] = 1
        attacks.RangedUnitAttack(*params)


def test_invalid_range_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[1] = -1
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[1] = 1.5
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[1] = "other"
        attacks.RangedUnitAttack(*params)


def test_invalid_number_of_attacks_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[2] = "0"
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[2] = "-1"
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[2] = "other"
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[2] = -1
        attacks.RangedUnitAttack(*params)


def test_invalid_skill_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[3] = -1
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[3] = 0
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[3] = 10
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[3] = 4.5
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[3] = "other"
        attacks.RangedUnitAttack(*params)


def test_invalid_strength_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[4] = -1
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[4] = 0
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[4] = 3.5
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[4] = "other"
        attacks.RangedUnitAttack(*params)


def test_invalid_ap_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[5] = 0.5
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[5] = "other"
        attacks.RangedUnitAttack(*params)


def test_invalid_damage_ranged_constructor():
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[6] = ""
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[6] = "-1"
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[6] = "-D3"
        attacks.RangedUnitAttack(*params)
    with pytest.raises(attacks.InvalidAttackParamError):
        params = get_unit_attack_valid_params()
        params[6] = "other"
        attacks.RangedUnitAttack(*params)


class MockCreatureAttack(interfaces.CreatureAttack):
    def __init__(
        self,
        *,
        name,
        is_melee,
        multiattack,
        weapon_range,
        target,
        to_hit_bonus,
        tot_avg_dmg,
        dice_avg_dmg,
        fixed_dmg
    ):
        self._name = name
        self._melee = is_melee
        self._multiattack = multiattack
        self._range = weapon_range
        self._target = target
        self._to_hit_bonus = to_hit_bonus
        self._tot_avg_dmg = tot_avg_dmg
        self._dice_avg_dmg = dice_avg_dmg
        self._fixed_dmg = fixed_dmg

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_melee(self) -> bool:
        return self._melee

    @property
    def multiattack(self) -> int:
        return self._multiattack

    @property
    def range(self) -> int:
        return self._range

    @property
    def target(self) -> interfaces.Target:
        return self._target

    @property
    def to_hit_bonus(self) -> int:
        return self._to_hit_bonus

    @property
    def total_average_damage(self) -> float:
        return self._tot_avg_dmg

    @property
    def dice_average_damage(self) -> float:
        return self._dice_avg_dmg

    @property
    def fixed_damage(self) -> float:
        return self._fixed_dmg


def test_from_creature_attack_melee():
    creature_attack = MockCreatureAttack(
        name="attack name",
        is_melee=True,
        target=targets.SingleTarget(),
        multiattack=1,
        weapon_range=5,
        tot_avg_dmg=8.0,
        dice_avg_dmg=5.0,
        fixed_dmg=3.0,
        to_hit_bonus=5,
    )

    unit_attack = attacks.from_creature_attack(creature_attack)

    assert isinstance(unit_attack, attacks.MeleeUnitAttack)
    assert unit_attack.is_melee is True
    assert unit_attack.number_of_attacks == attacks._number_of_attacks_from_attack(
        creature_attack
    )
    assert unit_attack.attack_skill == attacks._attack_skill_from_attack(
        creature_attack
    )
    assert unit_attack.name == "attack name"
    assert unit_attack.range == attacks._range_from_attack(creature_attack)
    assert unit_attack.damage == attacks._damage_from_attack(creature_attack)
    assert (
        unit_attack.armor_penetration
        == attacks._armor_penetration_value_from_attack(creature_attack)
    )
    assert unit_attack.strength == attacks._strength_value_from_attack(creature_attack)


def test_from_creature_attack_ranged():
    creature_attack = MockCreatureAttack(
        name="spell name",
        is_melee=False,
        target=targets.Sphere(20),
        weapon_range=150,
        multiattack=1,
        to_hit_bonus=7,
        tot_avg_dmg=28.0,
        dice_avg_dmg=28.0,
        fixed_dmg=0.0,
    )

    unit_attack = attacks.from_creature_attack(creature_attack)

    assert isinstance(unit_attack, attacks.RangedUnitAttack)
    assert unit_attack.is_melee is False
    assert unit_attack.number_of_attacks == attacks._number_of_attacks_from_attack(
        creature_attack
    )
    assert unit_attack.attack_skill == attacks._attack_skill_from_attack(
        creature_attack
    )
    assert unit_attack.name == "spell name"
    assert unit_attack.range == attacks._range_from_attack(creature_attack)
    assert unit_attack.damage == attacks._damage_from_attack(creature_attack)
    assert (
        unit_attack.armor_penetration
        == attacks._armor_penetration_value_from_attack(creature_attack)
    )
    assert unit_attack.strength == attacks._strength_value_from_attack(creature_attack)
