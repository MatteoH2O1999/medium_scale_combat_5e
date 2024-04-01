import pytest
from typing import Optional, List, Dict

import lib.interfaces as interfaces
import lib.targets as targets
import lib.unit_stat_block as stat_block
from lib.ability_scores import AbilityScores


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


class MockStatBlock(interfaces.StatBlock):
    def __init__(self, *, name, scores, prof, ac, hp, speed, attacks, multiattacks):
        self._name = name
        self._scores = scores
        self._prof = prof
        self._ac = ac
        self._hp = hp
        self._speed = speed
        self._attacks = attacks
        self._multiattacks = multiattacks

    @property
    def name(self) -> str:
        return self._name

    @property
    def ability_scores(self) -> AbilityScores:
        return self._scores

    @property
    def proficiency_modifier(self) -> int:
        return self._prof

    @property
    def armor_class(self) -> int:
        return self._ac

    @property
    def hit_points(self) -> int:
        return self._hp

    @property
    def speed(self) -> int:
        return self._speed

    @property
    def attacks(self) -> Dict[str, interfaces.CreatureAttack]:
        return self._attacks

    @property
    def multiattacks(self) -> Dict[str, List[interfaces.CreatureAttack]]:
        return self._multiattacks

    def create_multiattack(self, name: str, attack_names: List[str]) -> None:
        raise NotImplementedError


class MockAttack(interfaces.UnitAttack):
    def __init__(
        self, *, name, weapon_range, number_of_attacks, skill, strength, ap, dmg, melee
    ):
        self._name = name
        self._range = weapon_range
        self._attacks = number_of_attacks
        self._skill = skill
        self._strength = strength
        self._ap = ap
        self._dmg = dmg
        self._melee = melee

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
        return self._dmg

    @property
    def is_melee(self) -> bool:
        return self._melee

    def __eq__(self, other):
        if not isinstance(other, MockAttack):
            return False
        return (
            self._name == other._name
            and self._range == other._range
            and self._attacks == other._attacks
            and self._skill == other._skill
            and self._strength == other._strength
            and self._ap == other._ap
            and self._dmg == other._dmg
            and self._melee == other._melee
        )


def get_mock_attacks():
    return [
        MockAttack(
            name="attack 1",
            weapon_range=5,
            number_of_attacks="2",
            strength=5,
            dmg="1",
            ap=0,
            melee=True,
            skill=4,
        ),
        MockAttack(
            name="attack 2",
            weapon_range=60,
            number_of_attacks="1",
            strength=6,
            dmg="1",
            ap=-1,
            melee=False,
            skill=4,
        ),
        MockAttack(
            name="spell name",
            number_of_attacks="D3+1",
            skill=None,
            weapon_range=150,
            strength=7,
            melee=False,
            ap=-2,
            dmg="D3",
        ),
    ]


def get_mock_multiattack():
    return {
        "multiattack name 1": [
            MockAttack(
                name="attack 1",
                weapon_range=5,
                number_of_attacks="4",
                strength=5,
                dmg="1",
                ap=0,
                melee=True,
                skill=4,
            ),
            MockAttack(
                name="attack 2",
                weapon_range=60,
                number_of_attacks="1",
                strength=6,
                dmg="1",
                ap=-1,
                melee=False,
                skill=4,
            ),
        ]
    }


def get_unit_stat_block_valid_parameters():
    return [
        "creature name",
        30,
        6,
        4,
        None,
        3,
        get_mock_attacks(),
        get_mock_multiattack(),
    ]


def test_valid_constructor():
    block = stat_block.UnitStatBlock(*get_unit_stat_block_valid_parameters())

    assert isinstance(block, stat_block.UnitStatBlock)
    assert block.name == "creature name"
    assert block.speed == 30
    assert block.hit_points == 3
    assert block.resistance == 6
    assert block.saving_throw == 4
    assert block.invulnerable_saving_throw is None
    assert block.attacks == get_mock_attacks()
    assert block.multiattacks == get_mock_multiattack()


def test_invalid_name_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[0] = ""
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[0] = 1
        stat_block.UnitStatBlock(*params)


def test_invalid_speed_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[1] = "other"
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[1] = -5
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[1] = 5.5
        stat_block.UnitStatBlock(*params)


def test_invalid_resistance_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[2] = 0
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[2] = -5
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[2] = "other"
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[2] = 5.5
        stat_block.UnitStatBlock(*params)


def test_invalid_saving_throw_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[3] = 0
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[3] = 1
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[3] = 7
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[3] = -5
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[3] = 4.5
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[3] = "other"
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[3] = None
        stat_block.UnitStatBlock(*params)


def test_invalid_invulnerable_saving_throw_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[4] = 0
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[4] = 1
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[4] = "other"
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[4] = 7
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[4] = 4.5
        stat_block.UnitStatBlock(*params)
    params = get_unit_stat_block_valid_parameters()
    params[4] = None
    stat_block.UnitStatBlock(*params)


def test_invalid_hp_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[5] = None
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[5] = "other"
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[5] = 0
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[5] = -5
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[5] = 5.5
        stat_block.UnitStatBlock(*params)


def test_invalid_attacks_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[6] = None
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[6] = "other"
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[6] = [None]
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[6] = ["other"]
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[6] = [*get_mock_attacks(), "other"]
        stat_block.UnitStatBlock(*params)


def test_invalid_multiattacks_constructor():
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[7] = None
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[7] = "other"
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        atks = params[7].pop("multiattack name 1")
        params[7][2] = atks
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[7]["multiattack name 1"] = None
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[7]["multiattack name 1"] = ["other"]
        stat_block.UnitStatBlock(*params)
    with pytest.raises(stat_block.InvalidStatBlockParamError):
        params = get_unit_stat_block_valid_parameters()
        params[7]["multiattack name 1"] = [None]
        stat_block.UnitStatBlock(*params)


def test_from_stat_block():
    mock_attacks = {
        "attack 1": MockCreatureAttack(
            name="attack 1",
            is_melee=True,
            multiattack=1,
            weapon_range=5,
            target=targets.SingleTarget(),
            to_hit_bonus=5,
            tot_avg_dmg=5.5,
            dice_avg_dmg=3.5,
            fixed_dmg=2.0,
        ),
        "attack 2": MockCreatureAttack(
            name="attack 2",
            is_melee=False,
            multiattack=1,
            target=targets.SingleTarget(),
            weapon_range=60,
            to_hit_bonus=5,
            tot_avg_dmg=6.5,
            dice_avg_dmg=4.5,
            fixed_dmg=2.0,
        ),
        "spell": MockCreatureAttack(
            name="spell",
            is_melee=False,
            multiattack=1,
            weapon_range=150,
            target=targets.Sphere(20),
            to_hit_bonus=7,
            tot_avg_dmg=28.0,
            dice_avg_dmg=28.0,
            fixed_dmg=0.0,
        ),
    }
    mock_multiattacks = {
        "multiattack name 1": [
            MockCreatureAttack(
                name="attack 1",
                is_melee=True,
                multiattack=2,
                weapon_range=5,
                target=targets.SingleTarget(),
                to_hit_bonus=5,
                tot_avg_dmg=5.5,
                dice_avg_dmg=3.5,
                fixed_dmg=2.0,
            ),
            MockCreatureAttack(
                name="attack 2",
                is_melee=False,
                multiattack=1,
                target=targets.SingleTarget(),
                weapon_range=60,
                to_hit_bonus=5,
                tot_avg_dmg=6.5,
                dice_avg_dmg=4.5,
                fixed_dmg=2.0,
            ),
        ]
    }
    mock_stat_block = MockStatBlock(
        name="creature name",
        scores=AbilityScores(12, 14, 8, 12, 14, 8),
        ac=14,
        hp=18,
        prof=2,
        speed=30,
        attacks=mock_attacks,
        multiattacks=mock_multiattacks,
    )

    block = stat_block.from_stat_block(mock_stat_block)

    assert isinstance(block, stat_block.UnitStatBlock)
    assert block.name == "creature name"
    assert block.speed == stat_block._speed_from_stat_block(mock_stat_block)
    assert block.hit_points == stat_block._hit_points_per_creature_from_stat_block(
        mock_stat_block
    )
    assert block.resistance == stat_block._resistance_value_from_stat_block(
        mock_stat_block
    )
    assert block.saving_throw == stat_block._saving_throw_value_from_stat_block(
        mock_stat_block
    )
    assert (
        block.invulnerable_saving_throw
        == stat_block._invulnerable_saving_throw_value_from_stat_block(mock_stat_block)
    )
    assert block.attacks == [
        stat_block.from_creature_attack(attack) for _, attack in mock_attacks.items()
    ]
    assert block.multiattacks == {
        "multiattack name 1": [
            stat_block.from_creature_attack(attack)
            for attack in mock_multiattacks["multiattack name 1"]
        ]
    }
