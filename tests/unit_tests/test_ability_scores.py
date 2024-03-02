import pytest

import lib.ability_scores as scores


def test_modifier_calculator():
    assert scores.score_modifier(10) == 0
    assert scores.score_modifier(1) == -5
    assert scores.score_modifier(18) == +4
    assert scores.score_modifier(11) == 0
    assert scores.score_modifier(15) == +2


def test_score_from_string():
    assert scores.Scores.from_string("strength") == scores.Scores.STRENGTH
    assert scores.Scores.from_string("dexterity") == scores.Scores.DEXTERITY
    assert scores.Scores.from_string("constitution") == scores.Scores.CONSTITUTION
    assert scores.Scores.from_string("intelligence") == scores.Scores.INTELLIGENCE
    assert scores.Scores.from_string("wisdom") == scores.Scores.WISDOM
    assert scores.Scores.from_string("charisma") == scores.Scores.CHARISMA
    assert scores.Scores.from_string("Strength") == scores.Scores.STRENGTH
    assert scores.Scores.from_string("other") is None


def test_ability_score_ranges():
    for i in range(6):
        valid_values = [10 for _ in range(6)]
        score = scores.AbilityScores(*valid_values)
        valid_values[i] = 0
        with pytest.raises(scores.AbilityScoreOutOfRangeError):
            score = scores.AbilityScores(*valid_values)
        valid_values[i] = -1
        with pytest.raises(scores.AbilityScoreOutOfRangeError):
            score = scores.AbilityScores(*valid_values)
        valid_values[i] = 31
        with pytest.raises(scores.AbilityScoreOutOfRangeError):
            score = scores.AbilityScores(*valid_values)


def test_ability_score_getters():
    score = scores.AbilityScores(1, 2, 3, 4, 5, 6)
    assert score.strength == 1
    assert score.dexterity == 2
    assert score.constitution == 3
    assert score.intelligence == 4
    assert score.wisdom == 5
    assert score.charisma == 6


def test_ability_score_modifier_getters():
    score = scores.AbilityScores(10, 8, 12, 13, 30, 1)
    assert score.strength_modifier == 0
    assert score.dexterity_modifier == -1
    assert score.constitution_modifier == 1
    assert score.intelligence_modifier == 1
    assert score.wisdom_modifier == 10
    assert score.charisma_modifier == -5


def test_ability_score_enum_getter():
    score = scores.AbilityScores(10, 8, 12, 13, 30, 1)
    assert score.get_ability_score(scores.Scores.STRENGTH) == 10
    assert score.get_ability_score(scores.Scores.DEXTERITY) == 8
    assert score.get_ability_score(scores.Scores.CONSTITUTION) == 12
    assert score.get_ability_score(scores.Scores.INTELLIGENCE) == 13
    assert score.get_ability_score(scores.Scores.WISDOM) == 30
    assert score.get_ability_score(scores.Scores.CHARISMA) == 1
    with pytest.raises(scores.InvalidAbilityScoreError):
        score.get_ability_score("other")  # noqa


def test_ability_score_modifier_enum_getter():
    score = scores.AbilityScores(10, 8, 12, 13, 30, 1)
    assert score.get_ability_score_modifier(scores.Scores.STRENGTH) == 0
    assert score.get_ability_score_modifier(scores.Scores.DEXTERITY) == -1
    assert score.get_ability_score_modifier(scores.Scores.CONSTITUTION) == 1
    assert score.get_ability_score_modifier(scores.Scores.INTELLIGENCE) == 1
    assert score.get_ability_score_modifier(scores.Scores.WISDOM) == 10
    assert score.get_ability_score_modifier(scores.Scores.CHARISMA) == -5
    with pytest.raises(scores.InvalidAbilityScoreError):
        score.get_ability_score_modifier("other")  # noqa


def test_equality():
    score1 = scores.AbilityScores(10, 8, 12, 13, 30, 1)
    score2 = scores.AbilityScores(10, 8, 12, 13, 30, 1)

    assert score1 == score2


def test_not_equal():
    score1 = scores.AbilityScores(10, 8, 12, 13, 28, 1)
    assert score1 != "other"
    for i in range(6):
        values = [10, 8, 12, 13, 28, 1]
        score_equal = scores.AbilityScores(*values)
        values[i] += 1
        score2 = scores.AbilityScores(*values)

        assert score1 == score_equal
        assert score1 != score2
