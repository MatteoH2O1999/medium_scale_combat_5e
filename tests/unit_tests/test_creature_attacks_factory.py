from typing import List, Dict

import lib.attacks as attacks
import lib.targets as targets
from lib.interfaces import StatBlock as StatBlockInterface, CreatureAttack
from lib.ability_scores import AbilityScores, Scores


class MockStatBlock(StatBlockInterface):
    def __init__(
        self, str_score, dex_score, con_score, int_score, wis_score, cha_score, prof
    ):
        self.scores = AbilityScores(
            str_score, dex_score, con_score, int_score, wis_score, cha_score
        )
        self.prof = prof

    @property
    def name(self) -> str:
        return "creature name"

    @property
    def ability_scores(self) -> AbilityScores:
        return self.scores

    @property
    def proficiency_modifier(self) -> int:
        return self.prof

    @property
    def armor_class(self) -> int:
        return 10

    @property
    def hit_points(self) -> int:
        return 15

    @property
    def speed(self) -> int:
        return 30

    @property
    def attacks(self) -> Dict[str, CreatureAttack]:
        return {}

    @property
    def multiattacks(self) -> Dict[str, List[CreatureAttack]]:
        return {}

    def create_multiattack(self, name: str, attack_names: List[str]) -> None:
        pass


def test_base_melee_attack_roll():
    stat_block = MockStatBlock(12, 8, 16, 12, 8, 14, 3)
    attack = attacks.AttackRollAttack(
        "base melee attack roll",
        5,
        2,
        targets.SingleTarget(),
        "2d8",
        0,
        False,
        Scores.STRENGTH,
        True,
        True,
        True,
        False,
    )

    creature_attack = attack.from_creature(stat_block)

    assert isinstance(creature_attack, attacks.CreatureMeleeAttack)
    assert creature_attack.name == "base melee attack roll"
    assert creature_attack.is_melee is True
    assert creature_attack.target == targets.SingleTarget()
    assert creature_attack.range == 5
    assert creature_attack.to_hit_bonus == 4
    assert creature_attack.multiattack == 2
    assert creature_attack.total_average_damage == 10
    assert creature_attack.dice_average_damage == 9
    assert creature_attack.fixed_damage == 1


def test_base_ranged_attack_roll():
    stat_block = MockStatBlock(12, 8, 16, 12, 8, 14, 3)
    attack = attacks.AttackRollAttack(
        "base ranged attack roll",
        50,
        1,
        targets.SingleTarget(),
        "2d8",
        0,
        True,
        Scores.STRENGTH,
        True,
        True,
        True,
        False,
    )

    creature_attack = attack.from_creature(stat_block)

    assert isinstance(creature_attack, attacks.CreatureRangedAttack)
    assert creature_attack.name == "base ranged attack roll"
    assert creature_attack.is_melee is False
    assert creature_attack.target == targets.SingleTarget()
    assert creature_attack.range == 50
    assert creature_attack.to_hit_bonus == 4
    assert creature_attack.multiattack == 1
    assert creature_attack.total_average_damage == 10
    assert creature_attack.dice_average_damage == 9
    assert creature_attack.fixed_damage == 1


def test_ranged_no_scaling_attack_roll():
    stat_block = MockStatBlock(12, 8, 16, 12, 8, 14, 3)
    attack = attacks.AttackRollAttack(
        "no scaling ranged attack roll",
        50,
        1,
        targets.SingleTarget(),
        "1d6",
        0,
        True,
        None,
        False,
        False,
        False,
        False,
    )

    creature_attack = attack.from_creature(stat_block)

    assert isinstance(creature_attack, attacks.CreatureRangedAttack)
    assert creature_attack.name == "no scaling ranged attack roll"
    assert creature_attack.is_melee is False
    assert creature_attack.target == targets.SingleTarget()
    assert creature_attack.range == 50
    assert creature_attack.to_hit_bonus == 0
    assert creature_attack.multiattack == 1
    assert creature_attack.total_average_damage == 3.5
    assert creature_attack.dice_average_damage == 3.5
    assert creature_attack.fixed_damage == 0


def test_melee_all_scaling_attack_roll():
    stat_block = MockStatBlock(12, 8, 16, 12, 8, 14, 3)
    attack = attacks.AttackRollAttack(
        "all scaling ranged attack roll",
        5,
        1,
        targets.SingleTarget(),
        "1d12",
        1,
        False,
        Scores.DEXTERITY,
        True,
        True,
        True,
        True,
    )

    creature_attack = attack.from_creature(stat_block)

    assert isinstance(creature_attack, attacks.CreatureMeleeAttack)
    assert creature_attack.name == "all scaling ranged attack roll"
    assert creature_attack.is_melee is True
    assert creature_attack.target == targets.SingleTarget()
    assert creature_attack.range == 5
    assert creature_attack.to_hit_bonus == 3
    assert creature_attack.multiattack == 1
    assert creature_attack.total_average_damage == 8.5
    assert creature_attack.dice_average_damage == 6.5
    assert creature_attack.fixed_damage == 2


def test_base_melee_saving_throw():
    stat_block = MockStatBlock(12, 8, 16, 12, 8, 14, 3)
    attack = attacks.SavingThrowAttack(
        "base melee saving throw",
        5,
        1,
        targets.SingleTarget(),
        "3d10",
        15,
        False,
        Scores.INTELLIGENCE,
        True,
        False,
    )

    creature_attack = attack.from_creature(stat_block)

    assert isinstance(creature_attack, attacks.CreatureMeleeAttack)
    assert creature_attack.name == "base melee saving throw"
    assert creature_attack.is_melee is True
    assert creature_attack.target == targets.SingleTarget()
    assert creature_attack.range == 5
    assert creature_attack.to_hit_bonus == 7
    assert creature_attack.multiattack == 1
    assert creature_attack.total_average_damage == 17.5
    assert creature_attack.dice_average_damage == 16.5
    assert creature_attack.fixed_damage == 1


def test_base_ranged_saving_throw():
    stat_block = MockStatBlock(12, 8, 16, 12, 8, 14, 3)
    attack = attacks.SavingThrowAttack(
        "base ranged saving throw",
        50,
        1,
        targets.Sphere(20),
        "2d6",
        14,
        True,
        Scores.CHARISMA,
        False,
        False,
    )

    creature_attack = attack.from_creature(stat_block)

    assert isinstance(creature_attack, attacks.CreatureRangedAttack)
    assert creature_attack.name == "base ranged saving throw"
    assert creature_attack.is_melee is False
    assert creature_attack.target == targets.Sphere(20)
    assert creature_attack.range == 50
    assert creature_attack.to_hit_bonus == 6
    assert creature_attack.multiattack == 1
    assert creature_attack.total_average_damage == 7
    assert creature_attack.dice_average_damage == 7
    assert creature_attack.fixed_damage == 0


def test_ranged_none_scaling_saving_throw():
    stat_block = MockStatBlock(12, 8, 16, 12, 8, 14, 3)
    attack = attacks.SavingThrowAttack(
        "none scaling ranged saving throw",
        50,
        1,
        targets.SingleTarget(),
        "3d10",
        13,
        True,
        None,
        True,
        False,
    )

    creature_attack = attack.from_creature(stat_block)

    assert isinstance(creature_attack, attacks.CreatureRangedAttack)
    assert creature_attack.name == "none scaling ranged saving throw"
    assert creature_attack.is_melee is False
    assert creature_attack.target == targets.SingleTarget()
    assert creature_attack.range == 50
    assert creature_attack.to_hit_bonus == 5
    assert creature_attack.multiattack == 1
    assert creature_attack.total_average_damage == 18.5
    assert creature_attack.dice_average_damage == 16.5
    assert creature_attack.fixed_damage == 2


def test_melee_all_scaling_saving_throw():
    stat_block = MockStatBlock(12, 8, 16, 12, 8, 14, 3)
    attack = attacks.SavingThrowAttack(
        "all scaling ranged saving throw",
        5,
        1,
        targets.SingleTarget(),
        "10d12",
        19,
        False,
        Scores.WISDOM,
        True,
        True,
    )

    creature_attack = attack.from_creature(stat_block)

    assert isinstance(creature_attack, attacks.CreatureMeleeAttack)
    assert creature_attack.name == "all scaling ranged saving throw"
    assert creature_attack.is_melee is True
    assert creature_attack.target == targets.SingleTarget()
    assert creature_attack.range == 5
    assert creature_attack.to_hit_bonus == 11
    assert creature_attack.multiattack == 1
    assert creature_attack.total_average_damage == 67
    assert creature_attack.dice_average_damage == 65
    assert creature_attack.fixed_damage == 2
