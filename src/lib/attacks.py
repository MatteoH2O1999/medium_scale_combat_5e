from abc import ABC
from typing import Optional

from .ability_scores import Scores
from .dice import get_average_damage
from .interfaces import (
    Target,
    Attack,
    CreatureAttack as CreatureAttackInterface,
    StatBlock,
)


class InvalidAttackParamError(ValueError):
    pass


class CreatureAttack(CreatureAttackInterface, ABC):
    """
    Generic 5e creature attack
    """

    def __init__(
        self,
        name: str,
        multiattack: int,
        weapon_range: int,
        target: Target,
        to_hit: int,
        total_average_damage: float,
        dice_average_damage: float,
        fixed_damage: float,
    ):
        """
        A generic 5e creature attack
        :param name: the attack's name
        :param multiattack: the number of hits the creature makes with this attack
        :param weapon_range: the range of the weapon in feet (as in the original stat block)
        :param target: the target of the weapon as a Target instance
        :param to_hit: the *to hit* bonus of the weapon
        :param total_average_damage: the total average damage
        :param dice_average_damage: the dice average damage
        :param fixed_damage: the fixed damage
        """
        if not name or not isinstance(name, str):
            raise InvalidAttackParamError(
                f"name value should be a non-empty string. Got {name}."
            )
        if multiattack < 1 or not isinstance(multiattack, int):
            raise InvalidAttackParamError(
                f"multiattack value should be an integer > 0. Got {multiattack}."
            )
        if weapon_range < 0 or not isinstance(weapon_range, int):
            raise InvalidAttackParamError(
                f"weapon_range value should be a non-negative integer. Got {weapon_range}."
            )
        if not isinstance(target, Target):
            raise InvalidAttackParamError(
                f"target should be an instance of Target. Got instance of {type(target)}: {target}."
            )
        if not isinstance(to_hit, int):
            raise InvalidAttackParamError(f"to_hit should be an integer. Got {to_hit}.")
        if total_average_damage < 0 or not isinstance(total_average_damage, float):
            raise InvalidAttackParamError(
                f"total_average_damage should be a non-negative float. Got {total_average_damage}."
            )
        if (
            dice_average_damage < 0
            or not isinstance(dice_average_damage, float)
            and dice_average_damage > 0
        ):
            raise InvalidAttackParamError(
                f"dice_average_damage should be a non-negative float. Got {dice_average_damage}."
            )
        if fixed_damage != 0 and not isinstance(fixed_damage, float):
            raise InvalidAttackParamError(
                f"fixed_damage should be a float. Got {fixed_damage}."
            )
        self._name: str = name
        self._multiattack: int = multiattack
        self._weapon_range: int = weapon_range
        self._target: Target = target
        self._to_hit: int = to_hit
        self._total_average_damage: float = total_average_damage
        self._dice_average_damage: float = dice_average_damage
        self._fixed_damage: float = fixed_damage

    @property
    def name(self) -> str:
        return self._name

    @property
    def multiattack(self) -> int:
        return self._multiattack

    @property
    def range(self) -> int:
        return self._weapon_range

    @property
    def target(self) -> Target:
        return self._target

    @property
    def to_hit_bonus(self) -> int:
        return self._to_hit

    @property
    def total_average_damage(self) -> float:
        return self._total_average_damage

    @property
    def dice_average_damage(self) -> float:
        return self._dice_average_damage

    @property
    def fixed_damage(self) -> float:
        return self._fixed_damage


class CreatureMeleeAttack(CreatureAttack):
    """
    Generic 5e melee creature attack
    """

    @property
    def is_melee(self) -> bool:
        return True


class CreatureRangedAttack(CreatureAttack):
    """
    Generic 5e ranged creature attack
    """

    @property
    def is_melee(self) -> bool:
        return False


class AttackRollAttack(Attack):
    """
    Generic 5e creature attack template for attacks based on attack rolls
    """

    def __init__(
        self,
        name: str,
        weapon_range: int,
        multiattack: int,
        target: Target,
        base_damage: str,
        base_to_hit: int,
        ranged: bool,
        ability_score_scaling: Scores = None,
        to_hit_scaling: bool = True,
        to_hit_proficiency: bool = True,
        damage_scaling: bool = True,
        damage_proficiency: bool = False,
    ):
        """
        A generic 5e creature attack template for attacks based on attack rolls
        :param name: The attack's name
        :param weapon_range: The range of the attack in feet (as in the original stat block)
        :param multiattack: The number of hits the attack can make in one attack action
        :param target: The attack's target
        :param base_damage: The attack's base damage, without the creature modifiers (i.e. no strength or proficiency modifiers)
        :param base_to_hit: The attack's base *to hit* modifier, without the creatur modifiers (i.e. no strength or proficiency modifiers)
        :param ranged: Whether the attack is ranged
        :param ability_score_scaling: The ability score the attack scales on
        :param to_hit_scaling: Whether to add the ability_score_scaling modifier to the *to hit* value of the attack
        :param to_hit_proficiency: Whether to add the proficiency modifier to the *to hit* value of the attack
        :param damage_scaling: Whether to add the ability_score_scaling modifier to the attack's damage
        :param damage_proficiency: Whether to add the proficiency modifier to the attack's damage
        """
        if not name or not isinstance(name, str):
            raise InvalidAttackParamError(
                f"name value sould be a non-empty string. Got {name}."
            )
        if weapon_range < 0 or not isinstance(weapon_range, int):
            raise InvalidAttackParamError(
                f"weapon_range should be a non-negative integer. Got {weapon_range}."
            )
        if multiattack < 1 or not isinstance(multiattack, int):
            raise InvalidAttackParamError(
                f"multiattack should be a positive integer. Got {multiattack}."
            )
        if not isinstance(target, Target):
            raise InvalidAttackParamError(
                f"target should be an instance of Target. Got {type(target)}: {target}."
            )
        damage, _, _ = get_average_damage(base_damage)
        if damage <= 0:
            raise InvalidAttackParamError(
                f"base_damage should be an expression with and average damage > 0. Got {damage}"
            )
        if not isinstance(base_to_hit, int):
            raise InvalidAttackParamError(
                f"base_to_hit should be an integer. Got {base_to_hit}."
            )
        if (
            not to_hit_scaling
            and not damage_scaling
            and ability_score_scaling is not None
        ):
            raise InvalidAttackParamError(
                f"ability_score_scaling should be None. Got {ability_score_scaling}"
            )
        if (to_hit_scaling or damage_scaling) and not isinstance(
            ability_score_scaling, Scores
        ):
            raise InvalidAttackParamError(
                f"ability_score_scaling should be an instance of Scoring. Got instance of {type(ability_score_scaling)}: {ability_score_scaling}."
            )
        self._name: str = name
        self._range: int = weapon_range
        self._multiattack: int = multiattack
        self._target: Target = target
        self._base_damage: str = base_damage
        self._base_to_hit: int = base_to_hit
        self._ability_score_scaling: Optional[Scores] = ability_score_scaling
        self._to_hit_scaling: bool = bool(to_hit_scaling)
        self._damage_scaling: bool = bool(damage_scaling)
        self._to_hit_proficiency: bool = bool(to_hit_proficiency)
        self._damage_proficiency: bool = bool(damage_proficiency)
        self._ranged: bool = bool(ranged)

    @property
    def name(self) -> str:
        return self._name

    def combine(self, other: Attack) -> Attack:
        if not self.equals(other):
            raise InvalidAttackParamError(f"Expected {self.name}. Got {other.name}")
        assert isinstance(other, AttackRollAttack)
        return AttackRollAttack(
            self._name,
            self._range,
            self._multiattack + other._multiattack,
            self._target,
            self._base_damage,
            self._base_to_hit,
            self._ranged,
            self._ability_score_scaling,
            self._to_hit_scaling,
            self._to_hit_proficiency,
            self._damage_scaling,
            self._damage_proficiency,
        )

    def equals(self, other: object) -> bool:
        if not isinstance(other, AttackRollAttack):
            return False
        return (
            self._name == other._name
            and self._range == other._range
            and self._target == other._target
            and self._base_damage == other._base_damage
            and self._base_to_hit == other._base_to_hit
            and self._ability_score_scaling == other._ability_score_scaling
            and self._to_hit_scaling == other._to_hit_scaling
            and self._damage_scaling == other._damage_scaling
            and self._to_hit_proficiency == other._to_hit_proficiency
            and self._damage_proficiency == other._damage_proficiency
            and self._ranged == other._ranged
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, AttackRollAttack):
            return False
        return (
            self._name == other._name
            and self._range == other._range
            and self._multiattack == other._multiattack
            and self._target == other._target
            and self._base_damage == other._base_damage
            and self._base_to_hit == other._base_to_hit
            and self._ability_score_scaling == other._ability_score_scaling
            and self._to_hit_scaling == other._to_hit_scaling
            and self._damage_scaling == other._damage_scaling
            and self._to_hit_proficiency == other._to_hit_proficiency
            and self._damage_proficiency == other._damage_proficiency
            and self._ranged == other._ranged
        )

    def from_creature(self, stat_block: StatBlock) -> CreatureAttack:
        to_hit = self._base_to_hit
        if self._to_hit_scaling:
            to_hit += stat_block.ability_scores.get_ability_score_modifier(
                self._ability_score_scaling
            )
        if self._to_hit_proficiency:
            to_hit += stat_block.proficiency_modifier

        damage_string = self._base_damage
        if self._damage_scaling:
            damage_string += f"+{stat_block.ability_scores.get_ability_score_modifier(self._ability_score_scaling)}"
        if self._damage_proficiency:
            damage_string += f"+{stat_block.proficiency_modifier}"

        average_total, average_dice, fixed = get_average_damage(self._base_damage)

        if self._ranged:
            return CreatureRangedAttack(
                self._name,
                self._multiattack,
                self._range,
                self._target,
                to_hit,
                average_total,
                average_dice,
                fixed,
            )
        return CreatureMeleeAttack(
            self._name,
            self._multiattack,
            self._range,
            self._target,
            to_hit,
            average_total,
            average_dice,
            fixed,
        )


class SavingThrowAttack(Attack):
    """
    Generic 5e creature attack template for attacks based on saving throws
    """

    def __init__(
        self,
        name: str,
        weapon_range: int,
        multiattack: int,
        target: Target,
        base_damage: str,
        dc: int,
        ranged: bool,
        ability_score_scaling: Scores = None,
        damage_scaling: bool = True,
        damage_proficiency: bool = False,
    ):
        """
        A generic 5e creature attack template for attacks based on saving throws
        :param name: The attack's name
        :param weapon_range: The range of the attack in feet (as in the original stat block)
        :param multiattack: The number of hits the attack can make in one attack action
        :param target: The attack's target
        :param base_damage: The attack's base damage, without the creature modifiers (i.e. no strength or proficiency modifiers)
        :param dc: The difficulty class of the saving throw
        :param ranged: Whether the attack is ranged
        :param ability_score_scaling: The ability score the attack scales on
        :param damage_scaling: Whether to add the ability_score_scaling modifier to the attack's damage
        :param damage_proficiency: Whether to add the proficiency modifier to the attack's damage
        """
        if not name or not isinstance(name, str):
            raise InvalidAttackParamError(
                f"name value sould be a non-empty string. Got {name}."
            )
        if weapon_range < 0 or not isinstance(weapon_range, int):
            raise InvalidAttackParamError(
                f"weapon_range should be a non-negative integer. Got {weapon_range}."
            )
        if multiattack < 1 or not isinstance(multiattack, int):
            raise InvalidAttackParamError(
                f"multiattack should be a positive integer. Got {multiattack}."
            )
        if not isinstance(target, Target):
            raise InvalidAttackParamError(
                f"target should be an instance of Target. Got {type(target)}: {target}."
            )
        damage, _, _ = get_average_damage(base_damage)
        if damage <= 0:
            raise InvalidAttackParamError(
                f"base_damage should be an expression with and average damage > 0. Got {damage}"
            )
        if not isinstance(dc, int):
            raise InvalidAttackParamError(f"dc should be an integer. Got {dc}")
        self._name: str = name
        self._range: int = weapon_range
        self._multiattack: int = multiattack
        self._target: Target = target
        self._base_damage: str = base_damage
        self._dc: int = dc
        self._ranged: bool = bool(ranged)
        self._ability_score_scaling: Optional[Scores] = ability_score_scaling
        self._damage_scaling: bool = bool(damage_scaling)
        self._damage_proficiency: bool = bool(damage_proficiency)

    @property
    def name(self) -> str:
        return self._name

    def combine(self, other: Attack) -> Attack:
        if not self.equals(other):
            raise InvalidAttackParamError(f"Expected {self.name}. Got {other.name}")
        assert isinstance(other, SavingThrowAttack)
        return SavingThrowAttack(
            self._name,
            self._range,
            self._multiattack + other._multiattack,
            self._target,
            self._base_damage,
            self._dc,
            self._ranged,
            self._ability_score_scaling,
            self._damage_scaling,
            self._damage_proficiency,
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, SavingThrowAttack):
            return False
        return (
            self._name == other._name
            and self._range == other._range
            and self._multiattack == other._multiattack
            and self._target == other._target
            and self._base_damage == other._base_damage
            and self._dc == other._dc
            and self._ranged == other._ranged
            and self._ability_score_scaling == other._ability_score_scaling
            and self._damage_scaling == other._damage_scaling
            and self._damage_proficiency == other._damage_proficiency
        )

    def equals(self, other: object) -> bool:
        if not isinstance(other, SavingThrowAttack):
            return False
        return (
            self._name == other._name
            and self._range == other._range
            and self._target == other._target
            and self._base_damage == other._base_damage
            and self._dc == other._dc
            and self._ranged == other._ranged
            and self._ability_score_scaling == other._ability_score_scaling
            and self._damage_scaling == other._damage_scaling
            and self._damage_proficiency == other._damage_proficiency
        )

    def from_creature(self, stat_block: StatBlock) -> CreatureAttack:
        to_hit = self._dc - 8

        damage_string = self._base_damage
        if self._damage_scaling:
            ability_score_scaling = self._ability_score_scaling
            if ability_score_scaling is None:
                value = 0
                for stat in [Scores.INTELLIGENCE, Scores.WISDOM, Scores.CHARISMA]:
                    stat_value = stat_block.ability_scores.get_ability_score(stat)
                    if stat_value > value:
                        ability_score_scaling = stat
                        value = stat_value
            damage_string += f"+{stat_block.ability_scores.get_ability_score_modifier(ability_score_scaling)}"
        if self._damage_proficiency:
            damage_string += f"+{stat_block.proficiency_modifier}"

        average_total, average_dice, fixed = get_average_damage(self._base_damage)

        if self._ranged:
            return CreatureRangedAttack(
                self._name,
                self._multiattack,
                self._range,
                self._target,
                to_hit,
                average_total,
                average_dice,
                fixed,
            )
        return CreatureMeleeAttack(
            self._name,
            self._multiattack,
            self._range,
            self._target,
            to_hit,
            average_total,
            average_dice,
            fixed,
        )
