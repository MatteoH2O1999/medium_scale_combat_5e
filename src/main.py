import sys
from PyQt6 import QtWidgets

from custom_ui.datasheet import (
    datasheet_from_unit_stat_block,
    datasheet_from_stat_block,
)
from lib.ability_scores import Scores
from lib.unit_stat_block import from_stat_block
from ui.edit_multiattack import Ui_Dialog as Ui_MultiattackDialog
from ui.edit_roll_attack import Ui_Dialog as Ui_AttackRollDialog
from ui.edit_save_attack import Ui_Dialog as Ui_SavingThrowDialog
from ui.mainwindow import Ui_MainWindow
from model import (
    StatBlockModel,
    AttackRollModel,
    AttackListModel,
    MultiattackListModel,
    MultiattackDetailedListModel,
    SavingThrowModel,
    from_model,
)


class AttackRollDialog(QtWidgets.QDialog, Ui_AttackRollDialog):
    def __init__(
        self, model: StatBlockModel, attack: AttackRollModel = None, parent=None
    ):
        super().__init__(parent)
        self.setupUi(self)
        self.model = StatBlockModel()
        self.model.copy_from(model)
        self.saveButton = self.dialogButtons.button(
            QtWidgets.QDialogButtonBox.StandardButton.Save
        )
        self.attack = AttackRollModel()
        if attack:
            self.attack.copy_from(attack)
            for a in self.model.attacks:
                if a.name == attack.name:
                    self.model.attacks.remove(a)
                    break
            self.load_attack()
        self.dialogButtons.rejected.connect(self.discard)
        self.dialogButtons.accepted.connect(self.save)
        self.attackNameInput.textChanged.connect(self.update_model)
        self.attackTypeInput.currentIndexChanged.connect(self.update_model)
        self.attackRangeInput.valueChanged.connect(self.update_model)
        self.multihitInput.valueChanged.connect(self.update_model)
        self.abilityScoreScalingInput.currentIndexChanged.connect(self.update_model)
        self.targetTypeInput.currentIndexChanged.connect(self.update_model)
        self.firstParameterInput.valueChanged.connect(self.update_model)
        self.secondParameterInput.valueChanged.connect(self.update_model)
        self.baseToHitInput.valueChanged.connect(self.update_model)
        self.toHitScalingCheck.stateChanged.connect(self.update_model)
        self.toHitProficiencyCheck.stateChanged.connect(self.update_model)
        self.baseDamageInput.textChanged.connect(self.update_model)
        self.damageScalingCheck.stateChanged.connect(self.update_model)
        self.damageProficiencyCheck.stateChanged.connect(self.update_model)
        self.update_gui()

    def load_attack(self):
        self.attackNameInput.setText(self.attack.name)
        ranged_text = "Ranged" if self.attack.ranged else "Melee"
        self.attackTypeInput.setCurrentIndex(self.attackTypeInput.findText(ranged_text))
        self.attackRangeInput.setValue(self.attack.weapon_range)
        self.multihitInput.setValue(self.attack.multiattack)
        score = self.attack.ability_score_scaling
        if score is None:
            score = "None"
        else:
            score = score.name.lower().capitalize()
        self.abilityScoreScalingInput.setCurrentIndex(
            self.abilityScoreScalingInput.findText(score)
        )
        self.targetTypeInput.setCurrentIndex(
            self.targetTypeInput.findText(
                " ".join([s.capitalize() for s in self.attack.target.name.split(" ")])
            )
        )
        self.firstParameterInput.setValue(self.attack.target.first_param)
        self.secondParameterInput.setValue(self.attack.target.second_param)
        self.baseToHitInput.setValue(self.attack.base_to_hit)
        self.toHitScalingCheck.setChecked(self.attack.to_hit_scaling)
        self.toHitProficiencyCheck.setChecked(self.attack.to_hit_proficiency)
        self.baseDamageInput.setText(self.attack.base_damage)
        self.damageScalingCheck.setChecked(self.attack.damage_scaling)
        self.damageProficiencyCheck.setChecked(self.attack.damage_proficiency)

    def update_model(self):
        self.attack.name = self.attackNameInput.text().strip()
        self.attack.ranged = self.attackTypeInput.currentText() == "Ranged"
        self.attack.weapon_range = self.attackRangeInput.value()
        self.attack.multiattack = self.multihitInput.value()
        self.attack.ability_score_scaling = Scores.from_string(
            self.abilityScoreScalingInput.currentText()
        )
        self.attack.target.name = self.targetTypeInput.currentText().lower().strip()
        self.attack.target.first_param = self.firstParameterInput.value()
        self.attack.target.second_param = self.secondParameterInput.value()
        self.attack.base_to_hit = self.baseToHitInput.value()
        self.attack.to_hit_scaling = self.toHitScalingCheck.isChecked()
        self.attack.to_hit_proficiency = self.toHitProficiencyCheck.isChecked()
        self.attack.base_damage = self.baseDamageInput.text().lower().strip()
        self.attack.damage_scaling = self.damageScalingCheck.isChecked()
        self.attack.damage_proficiency = self.damageProficiencyCheck.isChecked()
        self.update_gui()

    def update_gui(self):
        if not self.attack.to_hit_scaling and not self.attack.damage_scaling:
            if self.abilityScoreScalingInput.currentIndex() != 0:
                self.abilityScoreScalingInput.setCurrentIndex(0)
            self.abilityScoreScalingInput.setEnabled(False)
        else:
            self.abilityScoreScalingInput.setEnabled(True)

        label_1, label_2 = self.attack.target.parameters()
        if label_1 is None:
            self.firstParameterLabel.setText("")
            self.firstParameterInput.setEnabled(False)
        else:
            self.firstParameterLabel.setText(label_1)
            self.firstParameterInput.setEnabled(True)
        if label_2 is None:
            self.secondParameterLabel.setText("")
            self.secondParameterInput.setEnabled(False)
        else:
            self.secondParameterLabel.setText(label_2)
            self.secondParameterInput.setEnabled(True)

        try:
            model = StatBlockModel()
            model.copy_from(self.model)
            model.attacks.append(self.attack)
            from_model(model)
        except ValueError as e:
            self.saveButton.setEnabled(False)
            self.update_status(str(e), False)
            return
        self.saveButton.setEnabled(True)
        self.update_status("Valid \u2714", True)

    def update_status(self, status: str, green):
        self.statusText.setText(status)
        if green:
            self.statusText.setStyleSheet("QLabel {color: green}")
        else:
            self.statusText.setStyleSheet("QLabel {color: red}")

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
        self.model = StatBlockModel()
        self.model.copy_from(model)
        self.saveButton = self.dialogButtons.button(
            QtWidgets.QDialogButtonBox.StandardButton.Save
        )
        self.attack = SavingThrowModel()
        if attack:
            self.attack.copy_from(attack)
            for a in self.model.attacks:
                if a.name == attack.name:
                    self.model.attacks.remove(a)
                    break
            self.load_attack()
        self.dialogButtons.rejected.connect(self.discard)
        self.dialogButtons.accepted.connect(self.save)
        self.attackNameInput.textChanged.connect(self.update_model)
        self.attackTypeInput.currentIndexChanged.connect(self.update_model)
        self.attackRangeInput.valueChanged.connect(self.update_model)
        self.multihitInput.valueChanged.connect(self.update_model)
        self.abilityScoreScalingInput.currentIndexChanged.connect(self.update_model)
        self.targetTypeInput.currentIndexChanged.connect(self.update_model)
        self.firstParameterInput.valueChanged.connect(self.update_model)
        self.secondParameterInput.valueChanged.connect(self.update_model)
        self.dcInput.valueChanged.connect(self.update_model)
        self.baseDamageInput.textChanged.connect(self.update_model)
        self.damageScalingCheck.stateChanged.connect(self.update_model)
        self.damageProficiencyCheck.stateChanged.connect(self.update_model)
        self.update_gui()

    def load_attack(self):
        self.attackNameInput.setText(self.attack.name)
        ranged_text = "Ranged" if self.attack.ranged else "Melee"
        self.attackTypeInput.setCurrentIndex(self.attackTypeInput.findText(ranged_text))
        self.attackRangeInput.setValue(self.attack.weapon_range)
        self.multihitInput.setValue(self.attack.multiattack)
        score = self.attack.ability_score_scaling
        if score is None:
            score = "None"
        else:
            score = score.name.lower().capitalize()
        self.abilityScoreScalingInput.setCurrentIndex(
            self.abilityScoreScalingInput.findText(score)
        )
        self.targetTypeInput.setCurrentIndex(
            self.targetTypeInput.findText(
                " ".join([s.capitalize() for s in self.attack.target.name.split(" ")])
            )
        )
        self.firstParameterInput.setValue(self.attack.target.first_param)
        self.secondParameterInput.setValue(self.attack.target.second_param)
        self.dcInput.setValue(self.attack.dc)
        self.baseDamageInput.setText(self.attack.base_damage)
        self.damageScalingCheck.setChecked(self.attack.damage_scaling)
        self.damageProficiencyCheck.setChecked(self.attack.damage_proficiency)

    def update_model(self):
        self.attack.name = self.attackNameInput.text().strip()
        self.attack.ranged = self.attackTypeInput.currentText() == "Ranged"
        self.attack.weapon_range = self.attackRangeInput.value()
        self.attack.multiattack = self.multihitInput.value()
        self.attack.ability_score_scaling = Scores.from_string(
            self.abilityScoreScalingInput.currentText()
        )
        self.attack.target.name = self.targetTypeInput.currentText().lower().strip()
        self.attack.target.first_param = self.firstParameterInput.value()
        self.attack.target.second_param = self.secondParameterInput.value()
        self.attack.dc = self.dcInput.value()
        self.attack.base_damage = self.baseDamageInput.text().lower().strip()
        self.attack.damage_scaling = self.damageScalingCheck.isChecked()
        self.attack.damage_proficiency = self.damageProficiencyCheck.isChecked()
        self.update_gui()

    def update_gui(self):
        if not self.attack.damage_scaling:
            if self.abilityScoreScalingInput.currentIndex() != 0:
                self.abilityScoreScalingInput.setCurrentIndex(0)
            self.abilityScoreScalingInput.setEnabled(False)
        else:
            self.abilityScoreScalingInput.setEnabled(True)

        label_1, label_2 = self.attack.target.parameters()
        if label_1 is None:
            self.firstParameterLabel.setText("")
            self.firstParameterInput.setEnabled(False)
        else:
            self.firstParameterLabel.setText(label_1)
            self.firstParameterInput.setEnabled(True)
        if label_2 is None:
            self.secondParameterLabel.setText("")
            self.secondParameterInput.setEnabled(False)
        else:
            self.secondParameterLabel.setText(label_2)
            self.secondParameterInput.setEnabled(True)

        try:
            model = StatBlockModel()
            model.copy_from(self.model)
            model.attacks.append(self.attack)
            from_model(model)
        except ValueError as e:
            self.saveButton.setEnabled(False)
            self.update_status(str(e), False)
            return
        self.saveButton.setEnabled(True)
        self.update_status("Valid \u2714", True)

    def update_status(self, status: str, green):
        self.statusText.setText(status)
        if green:
            self.statusText.setStyleSheet("QLabel {color: green}")
        else:
            self.statusText.setStyleSheet("QLabel {color: red}")

    def save(self):
        self.accept()

    def discard(self):
        self.reject()


class MultiattackDialog(QtWidgets.QDialog, Ui_MultiattackDialog):
    def __init__(self, model: StatBlockModel, name: str = None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.old_name = name
        self.name = name or ""
        self.model = StatBlockModel()
        self.model.copy_from(model)
        self.attacks = self.model.multiattacks.get(name, [])
        self.attacks_model = AttackListModel(self.model)
        self.multiattack_model = MultiattackDetailedListModel(self.attacks)
        self.saveButton = self.dialogButtons.button(
            QtWidgets.QDialogButtonBox.StandardButton.Save
        )
        self.availableAttacksList.setModel(self.attacks_model)
        self.multiattackList.setModel(self.multiattack_model)
        self.nameInput.textChanged.connect(self.update_model)
        self.dialogButtons.rejected.connect(self.discard)
        self.dialogButtons.accepted.connect(self.save)
        self.availableAttacksList.selectionModel().selectionChanged.connect(
            self.update_model
        )
        self.availableAttacksList.activated.connect(self.add)
        self.multiattackList.selectionModel().selectionChanged.connect(
            self.update_model
        )
        self.multiattackList.activated.connect(self.remove)
        self.addAttackButton.clicked.connect(self.add)
        self.removeAttackButton.clicked.connect(self.remove)
        self.nameInput.setText(self.name)
        self.update_model()

    def add(self):
        selected_attack_name = self.model.attacks[
            self.availableAttacksList.currentIndex().row()
        ].name
        self.multiattack_model.add(selected_attack_name)
        self.update_model()

    def remove(self):
        self.multiattack_model.remove(
            self.multiattack_model.attack_names[
                self.multiattackList.currentIndex().row()
            ]
        )
        self.update_model()

    def update_model(self):
        self.name = self.nameInput.text()
        self.update_gui()

    def update_status(self, status: str, green):
        self.statusText.setText(status)
        if green:
            self.statusText.setStyleSheet("QLabel {color: green}")
        else:
            self.statusText.setStyleSheet("QLabel {color: red}")

    def update_gui(self):
        self.multiattack_model.layoutChanged.emit()
        self.addAttackButton.setEnabled(False)
        self.removeAttackButton.setEnabled(False)
        if self.availableAttacksList.selectedIndexes():
            self.addAttackButton.setEnabled(True)
        if self.attacks and self.multiattackList.selectedIndexes():
            self.removeAttackButton.setEnabled(True)

        if not self.name:
            self.saveButton.setEnabled(False)
            self.update_status("Invalid multiattack name", False)
            return
        if (
            self.old_name
            and self.old_name != self.name
            and self.name in self.model.multiattacks.keys()
        ):
            self.saveButton.setEnabled(False)
            self.update_status(f"Duplicate multiattack name: {self.name}", False)
            return
        if not self.old_name and self.name in self.model.multiattacks.keys():
            self.saveButton.setEnabled(False)
            self.update_status(f"Duplicate multiattack name: {self.name}", False)
            return
        if len(self.attacks) < 2:
            self.saveButton.setEnabled(False)
            self.update_status(
                f"At least 2 attacks must be selected. Got {len(self.attacks)}", False
            )
            return
        try:
            model = StatBlockModel()
            model.copy_from(self.model)
            model.multiattacks[self.name] = self.attacks
            from_model(model)
        except ValueError as e:
            self.saveButton.setEnabled(False)
            self.update_status(str(e), False)
            if "Claw" in str(e):
                model = StatBlockModel()
                model.copy_from(self.model)
                model.multiattacks[self.name] = self.attacks
                from_model(model)
            return
        self.saveButton.setEnabled(True)
        self.update_status("Valid \u2714", True)

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
        self.addMultiattackButton.clicked.connect(lambda: self.edit_multiattack(""))
        self.editMultiattackButton.clicked.connect(lambda: self.edit_multiattack())
        self.multiattackListView.activated.connect(lambda: self.edit_multiattack())
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
        if name is None and self.multiattackListView.selectedIndexes():
            name = self.multiattacks_model.multiattack_names[
                self.multiattackListView.selectedIndexes()[0].row()
            ]
        if not name:
            name = ""
        if name and name not in self.model.multiattacks.keys():
            raise RuntimeError(f"Invalid multiattack name: {name}")
        dialog = MultiattackDialog(self.model, name, self)
        if dialog.exec():
            if name:
                if name != dialog.name:
                    if dialog.name in self.model.multiattacks.keys():
                        raise RuntimeError(f"Duplicate name: {dialog.name}")
                    self.model.multiattacks.pop(name)
                self.model.multiattacks[dialog.name] = dialog.attacks
            else:
                if dialog.name in self.model.multiattacks.keys():
                    raise RuntimeError(f"Duplicate name: {dialog.name}")
                self.model.multiattacks[dialog.name] = dialog.attacks
        self.multiattacks_model.layoutChanged.emit()
        self.update_gui()

    def update_stat_block(self):
        self.stat_block = from_model(self.model)
        self.medium_combat_stat_block = from_stat_block(self.stat_block)
        self.mediumScalePreviewPlot.update_preview(
            datasheet_from_unit_stat_block(self.medium_combat_stat_block)
        )
        self.srdPreviewPlot.update_preview(datasheet_from_stat_block(self.stat_block))

    def update_gui(self):
        self.editAttackButton.setEnabled(False)
        self.deleteAttackButton.setEnabled(False)
        self.editMultiattackButton.setEnabled(False)
        self.deleteMultiattackButton.setEnabled(False)
        self.addMultiattackButton.setEnabled(False)
        if self.attacksListView.selectedIndexes():
            self.editAttackButton.setEnabled(True)
            self.deleteAttackButton.setEnabled(True)
        if self.attacks_model.rowCount() > 0:
            self.addMultiattackButton.setEnabled(True)
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
