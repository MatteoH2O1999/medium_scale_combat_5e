import math

from abc import ABC

from .attacks import InvalidAttackParamError
from .dice import get_average_damage, convert_to_d3_d6, convert_d6_d3_to_string
from .interfaces import UnitAttack as UnitAttackInterface, CreatureAttack


class UnitAttack(UnitAttackInterface, ABC):
    def __init__(
        self,
        name: str,
        weapon_range: int,
        attacks: str,
        skill: int,
        strength: int,
        ap: int,
        damage: str,
    ):
        """
        A generic medium combat for 5e attack
        :param name: The attack's name
        :param range: The attack's range
        :param attacks: The number of attacks as a die expression
        :param skill: The attack's skill
        :param strength: The attack's strength
        :param ap: The attack's armor penetration
        :param damage: The attack's damage die expression
        """
        if not name or not isinstance(name, str):
            raise InvalidAttackParamError(
                f"name value should be a non-empty string. Got {name}."
            )
        if weapon_range < 1 or not isinstance(weapon_range, int):
            raise InvalidAttackParamError(
                f"weapon_range value should be a positive integer. Got {weapon_range}."
            )
        if not isinstance(skill, int) or skill < 2 or skill > 6:
            raise InvalidAttackParamError(
                f"skill should be an integer between 2 and 6. Got {skill}."
            )
        if not isinstance(strength, int) and strength < 1:
            raise InvalidAttackParamError(
                f"strength should be a positive integer. Got {strength}."
            )
        if not isinstance(ap, int):
            raise InvalidAttackParamError(
                f"ap should be an integer. Got instance of {type(ap)}: {ap}."
            )
        d, _, _ = get_average_damage(damage)
        if d <= 0:
            raise InvalidAttackParamError(
                f"damage should be an expression with and average damage > 0. Got {d}"
            )
        d, _, _ = get_average_damage(attacks)
        if d <= 0:
            raise InvalidAttackParamError(
                f"attacks should be an expression with and average damage > 0. Got {d}"
            )
        self._name: str = name
        self._range: int = weapon_range
        self._attacks: str = attacks
        self._skill: int = skill
        self._strength: int = strength
        self._ap: int = ap
        self._damage: str = damage

    @property
    def name(self) -> str:
        return self._name

    @property
    def range(self) -> int:
        return self._range

    @property
    def number_of_attacks(self) -> str:
        return self._attacks

    @property
    def attack_skill(self) -> int:
        return self._skill

    @property
    def strength(self) -> int:
        return self._strength

    @property
    def armor_penetration(self) -> int:
        return self._ap

    @property
    def damage(self) -> str:
        return self._damage


class RangedUnitAttack(UnitAttack):
    """
    Generic medium combat for 5e ranged attack
    """

    @property
    def is_melee(self) -> bool:
        return False


class MeleeUnitAttack(UnitAttack):
    """
    Generic medium combat for 5e melee attack
    """

    @property
    def is_melee(self) -> bool:
        return True


def _range_from_attack(attack: CreatureAttack) -> int:
    return attack.range


def _attack_skill_from_attack(attack: CreatureAttack) -> int:
    if attack.to_hit_bonus < 0:
        return 6
    elif attack.to_hit_bonus < 2:
        return 5
    elif attack.to_hit_bonus < 5:
        return 4
    elif attack.to_hit_bonus < 12:
        return 3
    return 2


def _strength_value_from_attack(attack: CreatureAttack) -> int:
    return max(
        math.floor(math.sqrt(attack.total_average_damage + 1))
        + attack.to_hit_bonus
        - 1,
        1,
    )


def _armor_penetration_value_from_attack(attack: CreatureAttack) -> int:
    return -math.ceil(abs(attack.total_average_damage // 20))


def _damage_from_attack(attack: CreatureAttack) -> str:
    scaled_dice = math.ceil(attack.dice_average_damage / 20)
    scale_fixed = math.ceil(attack.total_average_damage / 20) - scaled_dice
    d6, d3, fixed = convert_to_d3_d6(scaled_dice)
    fixed += scale_fixed
    return convert_d6_d3_to_string(d6, d3, fixed)


def _number_of_attacks_from_attack(attack: CreatureAttack) -> str:
    attacks = attack.target.number_of_targets
    attacks *= attack.multiattack
    if attack.is_melee:
        attacks *= 2
    if attack.target.is_aoe:
        d6, d3, fixed = convert_to_d3_d6(attacks)
        return convert_d6_d3_to_string(d6, d3, fixed)
    return str(attacks)


def from_creature_attack(attack: CreatureAttack) -> UnitAttack:
    weapon_range = _range_from_attack(attack)
    damage = _damage_from_attack(attack)
    ap = _armor_penetration_value_from_attack(attack)
    attacks = _number_of_attacks_from_attack(attack)
    strength = _strength_value_from_attack(attack)
    skill = _attack_skill_from_attack(attack)
    if attack.is_melee:
        return MeleeUnitAttack(
            attack.name, weapon_range, attacks, skill, strength, ap, damage
        )
    return RangedUnitAttack(
        attack.name, weapon_range, attacks, skill, strength, ap, damage
    )
