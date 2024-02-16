import math

from enum import Enum, auto, unique


def score_modifier(score: int) -> int:
    return math.floor((score - 10) / 2)


@unique
class Scores(Enum):
    STRENGTH = auto()
    DEXTERITY = auto()
    CONSTITUTION = auto()
    INTELLIGENCE = auto()
    WISDOM = auto()
    CHARISMA = auto()


class AbilityScoreOutOfRangeError(ValueError):
    pass


class InvalidAbilityScoreError(ValueError):
    pass


class AbilityScores:
    def __init__(
        self,
        str_score: int,
        dex_score: int,
        con_score: int,
        int_score: int,
        wis_score: int,
        cha_score: int,
    ):
        """
        A 5e compatible ability scores
        :param str_score: The strength ability score
        :param dex_score: The dexterity ability score
        :param con_score: The constitution ability score
        :param int_score: The intelligence ability score
        :param wis_score: The wisdom ability score
        :param cha_score: The charisma ability score
        """
        if str_score > 30 or str_score < 1:
            raise AbilityScoreOutOfRangeError(
                f"Strength score should be between 1 and 30. Got {str_score}."
            )
        if dex_score > 30 or dex_score < 1:
            raise AbilityScoreOutOfRangeError(
                f"Dexterity score should be between 1 and 30. Got {dex_score}."
            )
        if con_score > 30 or con_score < 1:
            raise AbilityScoreOutOfRangeError(
                f"Constitution score should be between 1 and 30. Got {con_score}."
            )
        if int_score > 30 or int_score < 1:
            raise AbilityScoreOutOfRangeError(
                f"Intelligence score should be between 1 and 30. Got {int_score}."
            )
        if wis_score > 30 or wis_score < 1:
            raise AbilityScoreOutOfRangeError(
                f"Wisdom score should be between 1 and 30. Got {wis_score}."
            )
        if cha_score > 30 or cha_score < 1:
            raise AbilityScoreOutOfRangeError(
                f"Charisma score should be between 1 and 30. Got {cha_score}."
            )
        self._str: int = str_score
        self._dex: int = dex_score
        self._con: int = con_score
        self._int: int = int_score
        self._wis: int = wis_score
        self._cha: int = cha_score

    @property
    def strength(self) -> int:
        """
        The strength ability score
        :return: The strength ability score as an integer between 1 and 30
        """
        return self._str

    @property
    def dexterity(self) -> int:
        """
        The dexterity ability score
        :return: The dexterity ability score as an integer between 1 and 30
        """
        return self._dex

    @property
    def constitution(self) -> int:
        """
        The constitution ability score
        :return: The constitution ability score as an integer between 1 and 30
        """
        return self._con

    @property
    def intelligence(self) -> int:
        """
        The intelligence ability score
        :return: The intelligence ability score as an integer between 1 and 30
        """
        return self._int

    @property
    def wisdom(self) -> int:
        """
        The wisdom ability score
        :return: The wisdom ability score as an integer between 1 and 30
        """
        return self._wis

    @property
    def charisma(self) -> int:
        """
        The charisma ability score
        :return: The charisma ability score as an integer between 1 and 30
        """
        return self._cha

    @property
    def strength_modifier(self) -> int:
        """
        The strength modifier
        :return: The strength modifier as an integer between -5 and 10
        """
        return score_modifier(self._str)

    @property
    def dexterity_modifier(self) -> int:
        """
        The dexterity modifier
        :return: The dexterity modifier as an integer between -5 and 10
        """
        return score_modifier(self._dex)

    @property
    def constitution_modifier(self) -> int:
        """
        The constitution modifier
        :return: The constitution modifier as an integer between -5 and 10
        """
        return score_modifier(self._con)

    @property
    def intelligence_modifier(self) -> int:
        """
        The intelligence modifier
        :return: The intelligence modifier as an integer between -5 and 10
        """
        return score_modifier(self._int)

    @property
    def wisdom_modifier(self) -> int:
        """
        The wisdom modifier
        :return: The wisdom modifier as an integer between -5 and 10
        """
        return score_modifier(self._wis)

    @property
    def charisma_modifier(self) -> int:
        """
        The charisma modifier
        :return: The charisma modifier as an integer between -5 and 10
        """
        return score_modifier(self._cha)

    def get_ability_score(self, score: Scores) -> int:
        """
        Gets the specified ability score
        :param score: The ability score to find as a Scores enumerator.
        :return: The requested ability score as an integer between 1 and 30
        """
        if score is Scores.STRENGTH:
            return self._str
        if score is Scores.DEXTERITY:
            return self._dex
        if score is Scores.CONSTITUTION:
            return self._con
        if score is Scores.INTELLIGENCE:
            return self._int
        if score is Scores.WISDOM:
            return self._wis
        if score is Scores.CHARISMA:
            return self._cha
        raise InvalidAbilityScoreError(f"Expected the enum Scores. Got {score}.")

    def get_ability_score_modifier(self, score: Scores) -> int:
        """
        Gets the specified ability score modifier
        :param score: The ability score modifier to find as a Scores enumerator
        :return: The requested ability score modifier as an integer between -5 and 10
        """
        return score_modifier(self.get_ability_score(score))

    def __eq__(self, other) -> bool:
        if not isinstance(other, AbilityScores):
            return False
        return (
            self._str == other._str
            and self._dex == other._dex
            and self._con == other._con
            and self._int == other._int
            and self._wis == other._wis
            and self._cha == other._cha
        )
