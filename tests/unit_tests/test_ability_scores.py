import lib.ability_scores as scores


def test_modifier_calculator():
    assert scores.score_modifier(10) == 0
    assert scores.score_modifier(1) == -5
    assert scores.score_modifier(18) == +4
    assert scores.score_modifier(11) == 0
    assert scores.score_modifier(15) == +2
