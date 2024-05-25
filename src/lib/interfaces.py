from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from .ability_scores import AbilityScores


class Target(ABC):
    """
    Generic interface for an attack's target
    """

    @property
    @abstractmethod
    def number_of_targets(self) -> int:
        """
        The average number of targets the area covers rounded up.
        """

    @property
    @abstractmethod
    def is_aoe(self) -> bool:
        """
        Whether the target is an Area of Effect.
        If it is, number_of_targets is average rounded up.
        """

    @property
    @abstractmethod
    def description(self) -> str:
        """
        The textual description of the target
        """


class CreatureAttack(ABC):
    """
    Generic 5e creature attack interface
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The attack's name
        """

    @property
    @abstractmethod
    def is_melee(self) -> bool:
        """
        Whether the attack is melee
        """

    @property
    @abstractmethod
    def multiattack(self) -> int:
        """
        The number of hits this attack can make
        """

    @property
    @abstractmethod
    def range(self) -> int:
        """
        The range of the attack in feet
        """

    @property
    @abstractmethod
    def target(self) -> Target:
        """
        The target of the attack
        """

    @property
    @abstractmethod
    def to_hit_bonus(self) -> int:
        """
        The *to hit* bonus of the attack
        """

    @property
    @abstractmethod
    def total_average_damage(self) -> float:
        """
        The attack's total average damage
        """

    @property
    @abstractmethod
    def dice_average_damage(self) -> float:
        """
        The attack's dice average damage
        """

    @property
    @abstractmethod
    def fixed_damage(self) -> float:
        """
        The attack's fixed damage
        """


class StatBlock:
    """
    5e stat block interface
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The creature's name
        """

    @property
    @abstractmethod
    def ability_scores(self) -> AbilityScores:
        """
        The creature's ability scores
        """

    @property
    @abstractmethod
    def proficiency_modifier(self) -> int:
        """
        The creature's proficiency modifier
        """

    @property
    @abstractmethod
    def armor_class(self) -> int:
        """
        The creature's armor class
        """

    @property
    @abstractmethod
    def hit_points(self) -> int:
        """
        The creature's average hit points
        """

    @property
    @abstractmethod
    def speed(self) -> int:
        """
        The creature's speed in feet
        """

    @property
    @abstractmethod
    def attacks(self) -> Dict[str, CreatureAttack]:
        """
        The creature's attacks
        """

    @property
    @abstractmethod
    def multiattacks(self) -> Dict[str, List[CreatureAttack]]:
        """
        The creature's multiattacks
        """

    @abstractmethod
    def create_multiattack(self, name: str, attack_names: List[str]) -> None:
        """
        Create a multiattack
        :param name: Name of the multiattack
        :param attack_names: The names of the attacks to combine
        """


class Attack(ABC):
    """
    Generic 5e creature attack template interface
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The name of the attack
        """

    @abstractmethod
    def from_creature(self, stat_block: StatBlock) -> CreatureAttack:
        """
        Returns the creature attack from the attack template
        :param stat_block: The creature's stat block
        :return: The creature's attack
        """

    @abstractmethod
    def combine(self, other: "Attack") -> "Attack":
        """
        If *other* is the same attack, condenses both attacks in one and returns the result.
        :param other: The attack to combine
        :return: The combined attack
        """


class UnitAttack(ABC):
    """
    Generic medium combat for 5e attack interface
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The name of the attack
        """

    @property
    @abstractmethod
    def range(self) -> int:
        """
        The range of the attack in feet
        """

    @property
    @abstractmethod
    def number_of_attacks(self) -> str:
        """
        The number of attacks as a die expression
        """

    @property
    @abstractmethod
    def attack_skill(self) -> Optional[int]:
        """
        The attack's skill. If `None`, the attack always hits (`N/A`)
        """

    @property
    @abstractmethod
    def strength(self) -> int:
        """
        The attack's strength
        """

    @property
    @abstractmethod
    def armor_penetration(self) -> int:
        """
        The attack's armor penetration
        """

    @property
    @abstractmethod
    def damage(self) -> str:
        """
        The damage die expression
        """

    @property
    @abstractmethod
    def is_melee(self) -> bool:
        """
        Whether the attack is melee
        """

    @property
    @abstractmethod
    def is_aoe(self) -> bool:
        """
        Whether the attack is an Area of Effect attack
        """


class UnitStatBlock(ABC):
    """
    Stat block interface for a unit in medium combat 5e
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The unit's name
        """

    @property
    @abstractmethod
    def speed(self) -> int:
        """
        The unit's movement speed in feet
        """

    @property
    @abstractmethod
    def resistance(self) -> int:
        """
        The unit's resistance value used for wound rolls
        """

    @property
    @abstractmethod
    def saving_throw(self) -> int:
        """
        The unit's armor saving throw.
        """

    @property
    @abstractmethod
    def invulnerable_saving_throw(self) -> Optional[int]:
        """
        The unit's invulnerable saving throw, if any.
        """

    @property
    @abstractmethod
    def hit_points(self) -> int:
        """
        The unit's HP/creature value
        """

    @property
    @abstractmethod
    def attacks(self) -> List[UnitAttack]:
        """
        The attacks the unit may perform
        """

    @property
    @abstractmethod
    def multiattacks(self) -> Dict[str, List[UnitAttack]]:
        """
        The multiattacks the unit may perform
        """
