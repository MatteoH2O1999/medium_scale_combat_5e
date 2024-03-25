from typing import List, Dict

from .ability_scores import AbilityScores
from .interfaces import StatBlock as StatBlockInterface, Attack, CreatureAttack


class InvalidStatBlockParamError(ValueError):
    pass


class InvalidAttackNameError(ValueError):
    pass


class StatBlock(StatBlockInterface):
    """
    5e stat block
    """

    def __init__(
        self,
        name: str,
        scores: AbilityScores,
        prof: int,
        ac: int,
        hp: int,
        speed: int,
        attacks: List[Attack],
    ):
        """
        A 5e stat block
        :param name: The creature's name
        :param scores: The creature's ability scores
        :param prof: The creature's proficiency modifier
        :param ac: The creature's armor class
        :param hp: The creature's hit points
        :param speed: The creature's speed in feet
        :param attacks: The creature's attacks templates
        """
        if not name or not isinstance(name, str):
            raise InvalidStatBlockParamError(
                f"name value sould be a non-empty string. Got {name}."
            )
        if scores is None or not isinstance(scores, AbilityScores):
            raise InvalidStatBlockParamError(
                f"scores should be an instance of Scores. Got instance of {type(scores)}: {scores}."
            )
        if not isinstance(prof, int):
            raise InvalidStatBlockParamError(f"prof should be an integer. Got{prof}.")
        if not isinstance(ac, int) or ac < 1:
            raise InvalidStatBlockParamError(
                f"ac should be a positive integer. Got {ac}."
            )
        if not isinstance(hp, int) or hp < 1:
            raise InvalidStatBlockParamError(
                f"hp should be a positive integer. Got {hp}."
            )
        if not isinstance(speed, int) or speed < 0:
            raise InvalidStatBlockParamError(
                f"speed should be a non-negative integer. Got {speed}."
            )
        if not isinstance(attacks, list):
            raise InvalidStatBlockParamError(
                f"attacks should be a list. Got a {type(attacks)}"
            )
        names = []
        for a in attacks:
            if not isinstance(a, Attack):
                raise InvalidStatBlockParamError(
                    f"attacks should be a list of instances of Attack. Got {type(a)}: {a}"
                )
            if a.name in names:
                raise InvalidStatBlockParamError(
                    f"attacks should have unique names. Duplicate found: {a.name}"
                )
            names.append(a.name)
        self._name: str = name
        self._ability_scores: AbilityScores = scores
        self._proficiency: int = prof
        self._ac: int = ac
        self._hp: int = hp
        self._speed: int = speed
        self._attacks: Dict[str, Attack] = {}
        self._multiattacks: Dict[str, List[Attack]] = {}
        for a in attacks:
            self._attacks[a.name] = a

    @property
    def name(self) -> str:
        return self._name

    @property
    def ability_scores(self) -> AbilityScores:
        return self._ability_scores

    @property
    def proficiency_modifier(self) -> int:
        return self._proficiency

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
    def attacks(self) -> Dict[str, CreatureAttack]:
        ret = {}
        for attack_name, attack in self._attacks.items():
            ret[attack_name] = attack.from_creature(self)
        return ret

    @property
    def multiattacks(self) -> Dict[str, List[CreatureAttack]]:
        ret = {}
        for multiattack_name, multiattack in self._multiattacks.items():
            multi = []
            for attack in multiattack:
                multi.append(attack.from_creature(self))
            ret[multiattack_name] = multi
        return ret

    def create_multiattack(self, name: str, attack_names: List[str]) -> None:
        if name in self._multiattacks.keys():
            raise InvalidAttackNameError(f"multiattack {name} already present")
        for attack_name in attack_names:
            if attack_name not in self._attacks.keys():
                raise InvalidAttackNameError(f"{attack_name} not in creature's attacks")
        d = {}
        for attack_name in attack_names:
            if attack_name not in d.keys():
                d[attack_name] = 0
            d[attack_name] += 1
        multi = []
        for attack_name, number_of_attacks in d.items():
            attack = self._attacks[attack_name]
            for _ in range(number_of_attacks - 1):
                attack = attack.combine(self._attacks[attack_name])
            multi.append(attack)
        self._multiattacks[name] = multi
