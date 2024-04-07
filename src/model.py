import pickle
from PyQt6 import QtCore
from typing import List, Union, Dict, Optional, Tuple

import lib.targets as targets
from lib.ability_scores import Scores, AbilityScores
from lib.attacks import AttackRollAttack, SavingThrowAttack
from lib.stat_block import StatBlock


class TargetModel:
    def __init__(self):
        self.name: str = "single target"
        self.first_param: int = 1
        self.second_param: int = 1

    def copy_from(self, other: "TargetModel"):
        self.name = other.name
        self.first_param = other.first_param
        self.second_param = other.second_param

    def to_target(self) -> targets.Target:
        if self.name == "single target":
            return targets.SingleTarget()
        if self.name == "cone":
            return targets.Cone(self.first_param)
        if self.name == "cube":
            return targets.Cube(self.first_param)
        if self.name == "square":
            return targets.Square(self.first_param)
        if self.name == "cylinder":
            return targets.Cylinder(self.first_param, self.second_param)
        if self.name == "sphere":
            return targets.Sphere(self.first_param)
        if self.name == "circle":
            return targets.Circle(self.first_param)
        if self.name == "line":
            return targets.Line(self.first_param, self.second_param)
        raise ValueError(f"Invalid target name: {self.name}")

    def parameters(self) -> Tuple[Optional[str], Optional[str]]:
        if self.name == "single target":
            return None, None
        if self.name in ["cone", "cube", "square"]:
            return "Size", None
        if self.name in ["sphere", "circle"]:
            return "Radius", None
        if self.name == "line":
            return "Length", "Width"
        if self.name == "cylinder":
            return "Radius", "Height"
        raise ValueError(f"Invalid target name: {self.name}")


class AttackRollModel:
    def __init__(self):
        self.name: str = ""
        self.weapon_range: int = 5
        self.multiattack: int = 1
        self.target: TargetModel = TargetModel()
        self.base_damage: str = ""
        self.base_to_hit: int = 0
        self.ranged: bool = False
        self.ability_score_scaling: Optional[Scores] = None
        self.to_hit_scaling: bool = False
        self.to_hit_proficiency: bool = True
        self.damage_scaling: bool = False
        self.damage_proficiency: bool = False

    def copy_from(self, other: "AttackRollModel"):
        self.name = other.name
        self.weapon_range = other.weapon_range
        self.multiattack = other.multiattack
        self.target = TargetModel()
        self.target.copy_from(other.target)
        self.base_damage = other.base_damage
        self.base_to_hit = other.base_to_hit
        self.ranged = other.ranged
        self.ability_score_scaling = other.ability_score_scaling
        self.to_hit_scaling = other.to_hit_scaling
        self.to_hit_proficiency = other.to_hit_proficiency
        self.damage_scaling = other.damage_scaling
        self.damage_proficiency = other.damage_proficiency


class SavingThrowModel:
    def __init__(self):
        self.name: str = ""
        self.weapon_range: int = 5
        self.multiattack: int = 1
        self.target: TargetModel = TargetModel()
        self.base_damage: str = ""
        self.dc: int = 10
        self.ranged: bool = False
        self.ability_score_scaling: Optional[Scores] = None
        self.damage_scaling: bool = True
        self.damage_proficiency: bool = False

    def copy_from(self, other: "SavingThrowModel"):
        self.name = other.name
        self.weapon_range = other.weapon_range
        self.multiattack = other.multiattack
        self.target = TargetModel()
        self.target.copy_from(other.target)
        self.base_damage = other.base_damage
        self.dc = other.dc
        self.ranged = other.ranged
        self.ability_score_scaling = other.ability_score_scaling
        self.damage_scaling = other.damage_scaling
        self.damage_proficiency = other.damage_proficiency


class StatBlockModel:
    def __init__(self):
        self.str: int = 10
        self.dex: int = 10
        self.con: int = 10
        self.int: int = 10
        self.wis: int = 10
        self.cha: int = 10
        self.hp: int = 1
        self.ac: int = 10
        self.speed: int = 30
        self.name: str = "creature name"
        self.proficiency: int = 2
        self.attacks: List[Union[AttackRollModel, SavingThrowModel]] = []
        self.multiattacks: Dict[str, List[str]] = {}

    def reset(self) -> None:
        self.str = 10
        self.dex = 10
        self.con = 10
        self.int = 10
        self.wis = 10
        self.cha = 10
        self.hp = 1
        self.ac = 10
        self.speed = 30
        self.name = "creature name"
        self.proficiency = 2
        self.attacks = []
        self.multiattacks = {}

    def copy_from(self, other: "StatBlockModel"):
        self.str = other.str
        self.dex = other.dex
        self.con = other.con
        self.int = other.int
        self.wis = other.wis
        self.cha = other.cha
        self.hp = other.hp
        self.ac = other.ac
        self.speed = other.speed
        self.name = other.name
        self.proficiency = other.proficiency
        self.attacks = []
        for a in other.attacks:
            if isinstance(a, AttackRollModel):
                attack = AttackRollModel()
            else:
                attack = SavingThrowModel()
            attack.copy_from(a)
            self.attacks.append(attack)
        self.multiattacks = {}
        for name, multi in other.multiattacks.items():
            attacks = []
            for attack_name in multi:
                attacks.append(attack_name)
            self.multiattacks[name] = attacks

    @staticmethod
    def load(path: str) -> "StatBlockModel":
        with open(path, "rb") as file:
            block = pickle.load(file)
        if not isinstance(block, StatBlockModel):
            raise RuntimeError(
                f"Expected a StatBlockModel instance. Got a {type(block)} instance."
            )
        return block

    def save(self, path: str):
        with open(path, "wb") as file:
            pickle.dump(self, file)


def from_model(stat_block: StatBlockModel) -> StatBlock:
    ability_scores = AbilityScores(
        stat_block.str,
        stat_block.dex,
        stat_block.con,
        stat_block.int,
        stat_block.wis,
        stat_block.cha,
    )
    attacks = []
    for attack in stat_block.attacks:
        target = attack.target.to_target()
        if isinstance(attack, AttackRollModel):
            attacks.append(
                AttackRollAttack(
                    attack.name,
                    attack.weapon_range,
                    attack.multiattack,
                    target,
                    attack.base_damage,
                    attack.base_to_hit,
                    attack.ranged,
                    attack.ability_score_scaling,
                    attack.to_hit_scaling,
                    attack.to_hit_proficiency,
                    attack.damage_scaling,
                    attack.damage_proficiency,
                )
            )
        elif isinstance(attack, SavingThrowModel):
            attacks.append(
                SavingThrowAttack(
                    attack.name,
                    attack.weapon_range,
                    attack.multiattack,
                    target,
                    attack.base_damage,
                    attack.dc,
                    attack.ranged,
                    attack.ability_score_scaling,
                    attack.damage_scaling,
                    attack.damage_proficiency,
                )
            )
        else:
            raise RuntimeError("Unexpected error in attack creation")
    ret = StatBlock(
        stat_block.name,
        ability_scores,
        stat_block.proficiency,
        stat_block.ac,
        stat_block.hp,
        stat_block.speed,
        attacks,
    )
    for multiattack_name, multiattack in stat_block.multiattacks.items():
        ret.create_multiattack(multiattack_name, multiattack)
    return ret


class AttackListModel(QtCore.QAbstractListModel):
    def __init__(self, model: StatBlockModel, *args, **kwargs):
        super(AttackListModel, self).__init__(*args, **kwargs)
        self.model = model

    def data(self, index, role=None):
        attacks = self.model.attacks
        attacks.sort(key=lambda x: x.name)
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return attacks[index.row()].name

    def rowCount(self, parent=None):
        return len(self.model.attacks)


class MultiattackListModel(QtCore.QAbstractListModel):
    def __init__(self, model: StatBlockModel, *args, **kwargs):
        super(MultiattackListModel, self).__init__(*args, **kwargs)
        self.model = model

    @property
    def multiattack_names(self) -> List[str]:
        ret = []
        for multiattack_name, _ in self.model.multiattacks.items():
            ret.append(multiattack_name)
        ret.sort()
        return ret

    def data(self, index, role=None):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.multiattack_names[index.row()]

    def rowCount(self, parent=None):
        return len(self.multiattack_names)


class MultiattackDetailedListModel(QtCore.QAbstractListModel):
    def __init__(self, attacks: List[str], *args, **kwargs):
        super(MultiattackDetailedListModel, self).__init__(*args, **kwargs)
        self.model: List[str] = attacks

    @property
    def attack_names(self) -> List[str]:
        ret = []
        for attack in self.model:
            if attack not in ret:
                ret.append(attack)
        ret.sort()
        return ret

    def data(self, index, role=None):
        count = 0
        name = self.attack_names[index.row()]
        for attack in self.model:
            if attack == name:
                count += 1
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            ret = name
            if count > 1:
                ret += f" (x{count})"
            return ret

    def rowCount(self, parent=None):
        return len(self.attack_names)

    def add(self, attack: str):
        self.model.append(attack)

    def remove(self, attack: str):
        self.model.remove(attack)
