import sys
from PyQt6 import QtWidgets, QtCore
from typing import List, Union, Dict

import lib.targets as targets
from custom_ui.datasheet import (
    datasheet_from_unit_stat_block,
    datasheet_from_stat_block,
)
from lib.ability_scores import Scores, AbilityScores
from lib.attacks import AttackRollAttack, SavingThrowAttack
from lib.stat_block import StatBlock
from lib.unit_stat_block import from_stat_block
from ui.edit_multiattack import Ui_Dialog as Ui_MultiattackDialog
from ui.edit_roll_attack import Ui_Dialog as Ui_AttackRollDialog
from ui.edit_save_attack import Ui_Dialog as Ui_SavingThrowDialog
from ui.mainwindow import Ui_MainWindow


class TargetModel:
    def __init__(self):
        self.name: str = "single"
        self.first_param: int = 1
        self.second_param: int = 1

    def copy_from(self, other: "TargetModel"):
        self.name = other.name
        self.first_param = other.first_param
        self.second_param = other.second_param


class AttackRollModel:
    def __init__(self):
        self.name: str = "attack name"
        self.weapon_range: int = 5
        self.multiattack: int = 1
        self.target: TargetModel = TargetModel()
        self.base_damage: str = "1"
        self.base_to_hit: int = 0
        self.ranged: bool = False
        self.ability_score_scaling: Scores = Scores.STRENGTH
        self.to_hit_scaling: bool = True
        self.to_hit_proficiency: bool = True
        self.damage_scaling: bool = True
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
        self.name: str = "attack name"
        self.weapon_range: int = 5
        self.multiattack: int = 1
        self.target: TargetModel = TargetModel()
        self.base_damage: str = "1"
        self.dc: int = 10
        self.ranged: bool = False
        self.ability_score_scaling: Scores = Scores.STRENGTH
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
        if attack.target.name == "single":
            target = targets.SingleTarget()
        else:
            raise ValueError(f"Invalid target name: {attack.target.name}")
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
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.model.attacks[index.row()].name

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
        return ret

    def data(self, index, role=None):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.multiattack_names[index.row()]

    def rowCount(self, parent=None):
        return len(self.multiattack_names)


class AttackRollDialog(QtWidgets.QDialog, Ui_AttackRollDialog):
    def __init__(
        self, model: StatBlockModel, attack: AttackRollModel = None, parent=None
    ):
        super().__init__(parent)
        self.setupUi(self)
        self.attack = AttackRollModel()
        if attack:
            self.attack.copy_from(attack)
        self.model = model
        self.dialogButtons.rejected.connect(self.discard)
        self.dialogButtons.accepted.connect(self.save)

    def save(self):
        self.accept()

    def discard(self):
        self.reject()


class SavingThrowDialog(QtWidgets.QDialog, Ui_SavingThrowDialog):
    def __init__(
        self, model: StatBlockModel, attack: SavingThrowModel = None, parent=None
    ):
        super().__init__(parent)
        self.setupUi(self)
        self.attack = SavingThrowModel()
        if attack:
            self.attack.copy_from(attack)
        self.model = model
        self.dialogButtons.rejected.connect(self.discard)
        self.dialogButtons.accepted.connect(self.save)

    def save(self):
        self.accept()

    def discard(self):
        self.reject()


class MultiattackDialog(QtWidgets.QDialog, Ui_MultiattackDialog):
    def __init__(self, model: StatBlockModel, name: str = None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.old_name = None
        if name:
            self.old_name = name
        self.attacks = model.multiattacks.get(name, [])
        self.name = self.old_name or "multiattack name"
        self.dialogButtons.rejected.connect(self.discard)
        self.dialogButtons.accepted.connect(self.save)

    def save(self):
        self.accept()

    def discard(self):
        self.reject()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.model = StatBlockModel()
        self.attacks_model = AttackListModel(self.model)
        self.multiattacks_model = MultiattackListModel(self.model)
        self.attacksListView.setModel(self.attacks_model)
        self.multiattackListView.setModel(self.multiattacks_model)
        self.stat_block = from_model(self.model)
        self.medium_combat_stat_block = from_stat_block(self.stat_block)
        self.update_gui()

        self.strBox.valueChanged.connect(lambda x: self.update_model("str", x))
        self.dexBox.valueChanged.connect(lambda x: self.update_model("dex", x))
        self.conBox.valueChanged.connect(lambda x: self.update_model("con", x))
        self.intBox.valueChanged.connect(lambda x: self.update_model("int", x))
        self.wisBox.valueChanged.connect(lambda x: self.update_model("wis", x))
        self.chaBox.valueChanged.connect(lambda x: self.update_model("cha", x))
        self.nameInput.textChanged.connect(
            lambda x: self.update_model("name", x or "creature name")
        )
        self.hpBox.valueChanged.connect(lambda x: self.update_model("hp", x))
        self.acBox.valueChanged.connect(lambda x: self.update_model("ac", x))
        self.speedBox.valueChanged.connect(lambda x: self.update_model("speed", x))
        self.profBox.valueChanged.connect(lambda x: self.update_model("proficiency", x))
        self.addRollAttackButton.clicked.connect(self.edit_attack_roll_attack)
        self.addSaveAttackButton.clicked.connect(self.edit_saving_throw_attack)
        self.editAttackButton.clicked.connect(self.edit_attack)
        self.attacksListView.activated.connect(self.edit_attack)
        self.addMultiattackButton.clicked.connect(self.edit_multiattack)
        self.editMultiattackButton.clicked.connect(self.edit_multiattack)
        self.multiattackListView.activated.connect(self.edit_multiattack)
        self.deleteAttackButton.clicked.connect(self.delete_attack)
        self.deleteMultiattackButton.clicked.connect(self.delete_multiattack)
        self.attacksListView.selectionModel().selectionChanged.connect(self.update_gui)
        self.multiattackListView.selectionModel().selectionChanged.connect(
            self.update_gui
        )

        self.actionNew.triggered.connect(self.reset)

    def delete_multiattack(self):
        indexes = self.multiattackListView.selectedIndexes()
        multiattacks_to_delete = [
            self.multiattacks_model.multiattack_names[index.row()] for index in indexes
        ]
        for multiattack_to_delete in multiattacks_to_delete:
            self.model.multiattacks.pop(multiattack_to_delete)
        self.multiattacks_model.layoutChanged.emit()
        self.multiattackListView.clearSelection()
        self.update_gui()

    def delete_attack(self):
        indexes = self.attacksListView.selectedIndexes()
        attacks_to_delete = [self.model.attacks[index.row()] for index in indexes]
        for attack in attacks_to_delete:
            self.model.attacks.remove(attack)
        self.attacks_model.layoutChanged.emit()
        self.attacksListView.clearSelection()
        self.update_gui()

    def edit_attack(self):
        name_to_edit = self.model.attacks[
            self.attacksListView.selectedIndexes()[0].row()
        ].name
        for attack in self.model.attacks:
            if attack.name == name_to_edit:
                if isinstance(attack, AttackRollModel):
                    return self.edit_attack_roll_attack(attack)
                if isinstance(attack, SavingThrowModel):
                    return self.edit_saving_throw_attack(attack)
                raise RuntimeError(f"Invalid model")
        raise RuntimeError(f"Invalid attack name")

    def edit_attack_roll_attack(self, attack: AttackRollModel = None):
        dialog = AttackRollDialog(self.model, attack, self)
        if dialog.exec():
            if attack:
                attack.copy_from(dialog.attack)
            else:
                for a in self.model.attacks:
                    if a.name == dialog.attack.name:
                        raise RuntimeError(f"Dupliacate name: {a.name}")
                self.model.attacks.append(dialog.attack)
        self.attacks_model.layoutChanged.emit()
        self.update_gui()

    def edit_saving_throw_attack(self, attack: SavingThrowModel = None):
        dialog = SavingThrowDialog(self.model, attack, self)
        if dialog.exec():
            if attack:
                attack.copy_from(dialog.attack)
            else:
                for a in self.model.attacks:
                    if a.name == dialog.attack.name:
                        raise RuntimeError(f"Dupliacate name: {a.name}")
                self.model.attacks.append(dialog.attack)
        self.attacks_model.layoutChanged.emit()
        self.update_gui()

    def edit_multiattack(self, name: str = None):
        dialog = MultiattackDialog(self.model, name, self)
        if not name and self.multiattackListView.selectedIndexes():
            name = self.multiattacks_model.multiattack_names[
                self.multiattackListView.selectedIndexes()[0].row()
            ]
        if dialog.exec():
            if name:
                if name != dialog.name:
                    self.model.multiattacks.pop(name)
                    self.model.multiattacks[dialog.name] = dialog.attacks
            else:
                if dialog.name in self.model.multiattacks.keys():
                    raise RuntimeError(f"Duplicate name: {dialog.name}")
                self.model.multiattacks[dialog.name] = dialog.attacks
        self.multiattacks_model.layoutChanged.emit()
        self.update_gui()

    def update_stat_block(self):
        self.srdPreviewPlot.axes.clear()
        self.mediumScalePreviewPlot.axes.clear()
        self.stat_block = from_model(self.model)
        self.medium_combat_stat_block = from_stat_block(self.stat_block)
        datasheet_from_unit_stat_block(
            self.medium_combat_stat_block, self.mediumScalePreviewPlot.axes
        )
        datasheet_from_stat_block(self.stat_block, self.srdPreviewPlot.axes)
        self.mediumScalePreviewPlot.draw()
        self.srdPreviewPlot.draw()

    def update_gui(self):
        self.editAttackButton.setEnabled(False)
        self.deleteAttackButton.setEnabled(False)
        self.editMultiattackButton.setEnabled(False)
        self.deleteMultiattackButton.setEnabled(False)
        if self.attacksListView.selectedIndexes():
            self.editAttackButton.setEnabled(True)
            self.deleteAttackButton.setEnabled(True)
        if self.multiattackListView.selectedIndexes():
            self.editMultiattackButton.setEnabled(True)
            self.deleteMultiattackButton.setEnabled(True)
        self.update_stat_block()

    def update_model(self, name, value):
        self.model.__setattr__(name, value)
        self.update_stat_block()
        self.update_gui()

    def reset(self):
        self.model.reset()
        self.strBox.setValue(self.model.str)
        self.dexBox.setValue(self.model.dex)
        self.conBox.setValue(self.model.con)
        self.intBox.setValue(self.model.int)
        self.wisBox.setValue(self.model.wis)
        self.chaBox.setValue(self.model.cha)
        self.nameInput.clear()
        self.hpBox.setValue(self.model.hp)
        self.acBox.setValue(self.model.ac)
        self.speedBox.setValue(self.model.speed)
        self.profBox.setValue(self.model.proficiency)
        self.update_stat_block()
        self.update_gui()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.actionExit.triggered.connect(lambda: sys.exit(0))
    app.exec()
