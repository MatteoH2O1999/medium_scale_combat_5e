import pytest

import lib.dice as dice


def test_die_creation():
    d1 = dice.Die(1)
    assert d1.average_value == 1
    assert d1.roll() == 1
    with pytest.raises(dice.InvalidDieParamError):
        dice.Die(0)
    with pytest.raises(dice.InvalidDieParamError):
        dice.Die(-10)
    with pytest.raises(dice.InvalidDieParamError):
        dice.Die("other")  # noqa


def test_default_dice_average_values():
    assert dice.D2.average_value == 1.5
    assert dice.D3.average_value == 2.0
    assert dice.D4.average_value == 2.5
    assert dice.D6.average_value == 3.5
    assert dice.D8.average_value == 4.5
    assert dice.D10.average_value == 5.5
    assert dice.D12.average_value == 6.5
    assert dice.D20.average_value == 10.5
    assert dice.D100.average_value == 50.5


def test_get_dice_average_value():
    assert dice.get_dice_average_value(20) == 10.5
    assert dice.get_dice_average_value(1) == 1
    with pytest.raises(dice.InvalidDieParamError):
        dice.get_dice_average_value(0)
    with pytest.raises(dice.InvalidDieParamError):
        dice.get_dice_average_value(-1)
    with pytest.raises(dice.InvalidDieParamError):
        dice.get_dice_average_value("other")  # noqa


def test_get_average_damage_invalid_strings():
    with pytest.raises(dice.InvalidDamageExpressionError):
        dice.get_average_damage("no")
    with pytest.raises(dice.InvalidDamageExpressionError):
        dice.get_average_damage("1 / 2")
    with pytest.raises(dice.InvalidDamageExpressionError):
        dice.get_average_damage(1)  # noqa


def test_get_average_damage():
    assert dice.get_average_damage("1") == (1.0, 0.0, 1.0)
    assert dice.get_average_damage("1d3") == (2.0, 2.0, 0.0)
    assert dice.get_average_damage("2 - 1") == (1.0, 0.0, 1.0)
    assert dice.get_average_damage("4d6 + 2d8 + 4 - 1 - 1d3") == (24.0, 21.0, 3.0)
    assert dice.get_average_damage("-4d6 + 1") == (-13.0, -14.0, 1.0)
    assert dice.get_average_damage("d3 + 1") == (3.0, 2.0, 1.0)


def test_convert_to_d3_d6_invalid():
    with pytest.raises(dice.InvalidDamageExpressionError):
        dice.convert_to_d3_d6(-1)
    with pytest.raises(dice.InvalidDamageExpressionError):
        dice.convert_to_d3_d6("other")  # noqa


def test_convert_to_d3_d6():
    assert dice.convert_to_d3_d6(0) == (0, 0, 0)
    assert dice.convert_to_d3_d6(1) == (0, 0, 1)
    assert dice.convert_to_d3_d6(2) == (0, 1, 0)
    assert dice.convert_to_d3_d6(3) == (0, 1, 1)
    assert dice.convert_to_d3_d6(4) == (1, 0, 0)
    assert dice.convert_to_d3_d6(5) == (1, 0, 1)
    assert dice.convert_to_d3_d6(6) == (1, 0, 2)
    assert dice.convert_to_d3_d6(10) == (2, 0, 3)


def test_convert_to_d6_d3_str_invalid():
    with pytest.raises(dice.InvalidDamageExpressionError):
        dice.convert_d6_d3_to_string(-1, 1, 1)
    with pytest.raises(dice.InvalidDamageExpressionError):
        dice.convert_d6_d3_to_string(1, -1, 1)
    with pytest.raises(dice.InvalidDamageExpressionError):
        dice.convert_d6_d3_to_string("other", 1, 1)  # noqa
    with pytest.raises(dice.InvalidDamageExpressionError):
        dice.convert_d6_d3_to_string(1, "other", 1)  # noqa
    with pytest.raises(dice.InvalidDamageExpressionError):
        dice.convert_d6_d3_to_string(1, 1, "other")  # noqa


def test_convert_to_d6_d3_str():
    assert dice.convert_d6_d3_to_string(0, 0, 0) == "0"
    assert dice.convert_d6_d3_to_string(1, 0, -1) == "D6-1"
    assert dice.convert_d6_d3_to_string(0, 1, 1) == "D3+1"
    assert dice.convert_d6_d3_to_string(1, 1, 1) == "D6+D3+1"
    assert dice.convert_d6_d3_to_string(2, 2, 2) == "2D6+2D3+2"
