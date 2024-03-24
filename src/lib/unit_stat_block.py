import math
from typing import List, Dict, Optional

from .interfaces import (
    UnitStatBlock as UnitStatBlockInterface,
    StatBlock,
    UnitAttack,
)
from .stat_block import InvalidStatBlockParamError
from .unit_attacks import from_creature_attack


class UnitStatBlock(UnitStatBlockInterface):
    """
    Stat block for a unit in medium combat 5e
    """

    def __init__(
        self,
        name: str,
        speed: int,
        resistance: int,
        saving_throw: int,
        invulnerable_saving_throw: Optional[int],
        hp: int,
        attacks: List[UnitAttack],
        multiattacks: Dict[str, List[UnitAttack]],
    ):
        """
        A stat block for a unit in medium combat 5e
        :param name: The unit's name
        :param speed: The unit's speed
        :param resistance: The unit's resistance value
        :param saving_throw: The unit's armor saving throw
        :param invulnerable_saving_throw: The unit's invulnerable armor saving throw
        :param hp: The hit point of each creature in the unit
        :param attacks: The attacks this unit may perform
        :param multiattacks: The multiattacks this unit may perform
        """
        if not name or not isinstance(name, str):
            raise InvalidStatBlockParamError(
                f"name value should be a non-empty string. Got {name}."
            )
        if not isinstance(speed, int) or speed < 0:
            raise InvalidStatBlockParamError(
                f"speed value should be a non-negative integer. Got {speed}."
            )
        if not isinstance(resistance, int) or resistance < 1:
            raise InvalidStatBlockParamError(
                f"resistance value should be a positive integer. Got {resistance}."
            )
        if not isinstance(saving_throw, int) or saving_throw < 2 or saving_throw > 6:
            raise InvalidStatBlockParamError(
                f"saving_throw value should be an integer between 2 and 6. Got {saving_throw}."
            )
        if invulnerable_saving_throw is not None and (
            not isinstance(invulnerable_saving_throw, int)
            or invulnerable_saving_throw < 2
            or invulnerable_saving_throw > 6
        ):
            raise InvalidStatBlockParamError(
                f"invulnerable_saving_throw should be an integer between 2 and 6 or None. Got {invulnerable_saving_throw}"
            )
        if not isinstance(hp, int) or hp < 1:
            raise InvalidStatBlockParamError(
                f"hp value should be a positive integer. Got {hp}."
            )
        if not isinstance(attacks, list):
            raise InvalidStatBlockParamError(f"attacks should be a list.")
        for attack in attacks:
            if not isinstance(attack, UnitAttack):
                raise InvalidStatBlockParamError(
                    f"attacks should be a list of UnitAttack. Got instance of {type(attack)}: {attack}."
                )
        if not isinstance(multiattacks, dict):
            raise InvalidStatBlockParamError(f"multiattacks should be a dictionary")
        for multiattack_name, multiattack in multiattacks.items():
            if not multiattack_name or not isinstance(multiattack_name, str):
                raise InvalidStatBlockParamError(
                    f"multiattacks keys should be strings. Got instance of {type(multiattack_name)}: {multiattack_name}."
                )
            if not isinstance(multiattack, list):
                raise InvalidStatBlockParamError(
                    f"multiattacks values should be lists. Got instance of {type(multiattack)}: {multiattack}."
                )
            for attack in multiattack:
                if not isinstance(attack, UnitAttack):
                    raise InvalidStatBlockParamError(
                        f"multiattacks values should be a list of UnitAttack. Got instance of {type(attack)}: {attack}."
                    )
        self._name: str = name
        self._speed: int = speed
        self._resistance: int = resistance
        self._saving_throw: int = saving_throw
        self._invulnerable_saving_throw: Optional[int] = invulnerable_saving_throw
        self._hp: int = hp
        self._attacks: List[UnitAttack] = attacks
        self._multiattacks: Dict[str, List[UnitAttack]] = multiattacks

    @property
    def speed(self) -> int:
        return self._speed

    @property
    def resistance(self) -> int:
        return self._resistance

    @property
    def saving_throw(self) -> int:
        return self._saving_throw

    @property
    def invulnerable_saving_throw(self) -> Optional[int]:
        return self._invulnerable_saving_throw

    @property
    def hit_points(self) -> int:
        return self._hp

    @property
    def name(self) -> str:
        return self._name

    @property
    def attacks(self) -> List[UnitAttack]:
        return self._attacks

    @property
    def multiattacks(self) -> Dict[str, List[UnitAttack]]:
        return self._multiattacks


def _speed_from_stat_block(stat_block: StatBlock) -> int:
    return stat_block.speed


def _resistance_value_from_stat_block(stat_block: StatBlock) -> int:
    constitution_modifier = stat_block.ability_scores.constitution_modifier
    prof_modifier = stat_block.proficiency_modifier
    return max(2 + constitution_modifier + prof_modifier // 2, 1)


def _saving_throw_value_from_stat_block(stat_block: StatBlock) -> int:
    ac = stat_block.armor_class
    if ac < 11:
        return 5
    elif ac < 14:
        return 4
    elif ac < 18:
        return 3
    return 2


def _invulnerable_saving_throw_value_from_stat_block(
    stat_block: StatBlock,
) -> Optional[int]:  # pragma: no cover
    ac = stat_block.armor_class
    if ac < 18:
        return None
    elif ac < 20:
        return 6
    elif ac < 22:
        return 5
    elif ac < 25:
        return 4
    elif ac < 30:
        return 3
    return 2


def _hit_points_per_creature_from_stat_block(
    stat_block: StatBlock,
) -> int:  # pragma: no cover
    return math.ceil(stat_block.hit_points / 20)


def from_stat_block(stat_block: StatBlock) -> UnitStatBlock:
    speed = _speed_from_stat_block(stat_block)
    resistance = _resistance_value_from_stat_block(stat_block)
    saving_throw = _saving_throw_value_from_stat_block(stat_block)
    invulnerable_saving_throw = _invulnerable_saving_throw_value_from_stat_block(
        stat_block
    )
    hp = _hit_points_per_creature_from_stat_block(stat_block)
    attacks = []
    for attack in stat_block.attacks.values():
        attacks.append(from_creature_attack(attack))
    multiattacks = {}
    for multiattack_name, multiattack in stat_block.multiattacks.items():
        multi = []
        for attack in multiattack:
            multi.append(from_creature_attack(attack))
        multiattacks[multiattack_name] = multi
    return UnitStatBlock(
        stat_block.name,
        speed,
        resistance,
        saving_throw,
        invulnerable_saving_throw,
        hp,
        attacks,
        multiattacks,
    )
