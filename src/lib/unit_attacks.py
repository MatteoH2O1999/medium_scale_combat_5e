import math

from abc import ABC
from typing import Optional

from .attacks import InvalidAttackParamError
from .dice import (
    get_average_damage,
    convert_to_d3_d6,
    convert_d6_d3_to_string,
    InvalidDamageExpressionError,
)
from .interfaces import UnitAttack as UnitAttackInterface, CreatureAttack


class UnitAttack(UnitAttackInterface, ABC):
    def __init__(
        self,
        name: str,
        weapon_range: int,
        attacks: str,
        skill: Optional[int],
        strength: int,
        ap: int,
        damage: str,
        aoe: bool,
    ):
        """
        A generic medium combat for 5e attack
        :param name: The attack's name
        :param weapon_range: The attack's range
        :param attacks: The number of attacks as a die expression
        :param skill: The attack's skill
        :param strength: The attack's strength
        :param ap: The attack's armor penetration
        :param damage: The attack's damage die expression
        :param aoe: Whether the attack is and Area of Effect attack.
        """
        if not name or not isinstance(name, str):
            raise InvalidAttackParamError(
                f"name value should be a non-empty string. Got {name}."
            )
        if not isinstance(weapon_range, int) or weapon_range < 0:
            raise InvalidAttackParamError(
                f"weapon_range value should be a non-negative integer. Got {weapon_range}."
            )
        if skill is not None and (not isinstance(skill, int) or skill < 2 or skill > 6):
            raise InvalidAttackParamError(
                f"skill should be an integer between 2 and 6 or None. Got {skill}."
            )
        if not isinstance(strength, int) or strength < 1:
            raise InvalidAttackParamError(
                f"strength should be a positive integer. Got {strength}."
            )
        if not isinstance(ap, int):
            raise InvalidAttackParamError(
                f"ap should be an integer. Got instance of {type(ap)}: {ap}."
            )
        try:
            d, _, _ = get_average_damage(damage)
        except InvalidDamageExpressionError:
            raise InvalidAttackParamError(
                f"damage should be a valid die expression. Got {damage}"
            )
        if d <= 0:
            raise InvalidAttackParamError(
                f"damage should be an expression with an average damage > 0. Got {d}"
            )
        try:
            d, _, _ = get_average_damage(attacks)
        except InvalidDamageExpressionError:
            raise InvalidAttackParamError(
                f"attacks should be a valid die expression. Gor {attacks}"
            )
        if d <= 0:
            raise InvalidAttackParamError(
                f"attacks should be an expression with and average value > 0. Got {d}"
            )
        self._name: str = name
        self._range: int = weapon_range
        self._attacks: str = attacks
        self._skill: Optional[int] = skill
        self._strength: int = strength
        self._ap: int = ap
        self._damage: str = damage
        self._aoe: bool = bool(aoe)

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
    def attack_skill(self) -> Optional[int]:
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

    @property
    def is_aoe(self) -> bool:
        return self._aoe

    def __eq__(self, other):
        if not isinstance(other, UnitAttackInterface):
            return False
        return (
            self.name == other.name
            and self.range == other.range
            and self.attack_skill == other.attack_skill
            and self.number_of_attacks == other.number_of_attacks
            and self.strength == other.strength
            and self.armor_penetration == other.armor_penetration
            and self.damage == other.damage
            and self.is_melee == other.is_melee
            and self.is_aoe == other.is_aoe
        )


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


def _range_from_attack(attack: CreatureAttack) -> int:  # pragma: no cover
    return attack.range


def _attack_skill_from_attack(
    attack: CreatureAttack,
) -> Optional[int]:  # pragma: no cover
    if attack.to_hit_bonus < 0:
        return 6
    elif attack.to_hit_bonus < 2:
        return 5
    elif attack.to_hit_bonus < 5:
        return 4
    elif attack.to_hit_bonus < 10:
        return 3
    return 2


def _strength_value_from_attack(attack: CreatureAttack) -> int:  # pragma: no cover
    return max(
        math.floor(math.sqrt(attack.total_average_damage + 1))
        + attack.to_hit_bonus
        - 1,
        1,
    )


def _armor_penetration_value_from_attack(
    attack: CreatureAttack,
) -> int:  # pragma: no cover
    damage_pen = math.floor(attack.total_average_damage / 20)
    to_hit_pen = (
        math.floor(max(attack.to_hit_bonus, 0) / 7) if not attack.target.is_aoe else 1
    )
    total_pen = damage_pen + to_hit_pen
    return -total_pen


def _damage_from_attack(attack: CreatureAttack) -> str:  # pragma: no cover
    scaled_dice = math.ceil(attack.dice_average_damage / 20)
    scale_fixed = math.ceil(attack.total_average_damage / 20) - scaled_dice
    d6, d3, fixed = convert_to_d3_d6(scaled_dice)
    fixed += scale_fixed
    return convert_d6_d3_to_string(d6, d3, fixed)


def _number_of_attacks_from_attack(attack: CreatureAttack) -> str:  # pragma: no cover
    attacks = attack.target.number_of_targets
    attacks *= attack.multiattack
    if attack.is_melee:
        attacks *= 2
    if attack.target.is_aoe:
        d6, d3, fixed = convert_to_d3_d6(attacks)
        return convert_d6_d3_to_string(d6, d3, fixed)
    return str(attacks)


def _is_aoe_from_attack(attack: CreatureAttack) -> bool:  # pragma: no cover
    return attack.target.is_aoe


def from_creature_attack(attack: CreatureAttack) -> UnitAttack:
    weapon_range = _range_from_attack(attack)
    damage = _damage_from_attack(attack)
    ap = _armor_penetration_value_from_attack(attack)
    attacks = _number_of_attacks_from_attack(attack)
    strength = _strength_value_from_attack(attack)
    skill = _attack_skill_from_attack(attack)
    aoe = _is_aoe_from_attack(attack)
    if attack.is_melee:
        return MeleeUnitAttack(
            attack.name, weapon_range, attacks, skill, strength, ap, damage, aoe
        )
    return RangedUnitAttack(
        attack.name, weapon_range, attacks, skill, strength, ap, damage, aoe
    )
