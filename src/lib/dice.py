import math
import random


class InvalidDieParamError(ValueError):
    pass


class InvalidDamageExpressionError(ValueError):
    pass


class Die:
    """
    Simple die utilities for specific dice
    """

    def __init__(self, sides: int):
        """
        Die of specified sides
        :param sides: The number of sides of the die
        """
        if not isinstance(sides, int) or sides < 1:
            raise InvalidDieParamError(
                f"sides should be a positive integer. Got {sides}."
            )
        self._sides: int = sides

    @property
    def average_value(self) -> float:
        """
        The average value of the die
        :return: The average value of the die
        """
        return get_dice_average_value(self._sides)

    def roll(self) -> int:
        """
        Roll the die
        :return: The roll result
        """
        return random.randint(1, self._sides)


D2 = Die(2)
D3 = Die(3)
D4 = Die(4)
D6 = Die(6)
D8 = Die(8)
D10 = Die(10)
D12 = Die(12)
D20 = Die(20)
D100 = Die(100)


def get_dice_average_value(sides: int) -> float:
    """
    Returns the average value of a die with *sides* sides
    :param sides: The number of sides the die has
    :return: The die average value
    """
    if not isinstance(sides, int) or sides < 1:
        raise InvalidDieParamError(f"sides should be a positive integer. Got {sides}.")
    return (1 + sides) / 2


def get_average_damage(dice_damage_string: str) -> tuple[float, float, float]:
    """
    Returns the average of a die expression
    :param dice_damage_string: The die expression
    :return: The average value
    """
    if not dice_damage_string or not isinstance(dice_damage_string, str):
        raise InvalidDamageExpressionError(
            f"Expected a non empty die expression string"
        )
    dice_damage_string = "".join(
        dice_damage_string.lower().replace("-", "+-").replace("++", "+").split(" ")
    )
    if dice_damage_string.startswith("+"):
        dice_damage_string = dice_damage_string[1:]
    if "*" in dice_damage_string or "/" in dice_damage_string:
        raise InvalidDamageExpressionError(
            f"Expected only + and - signs in expression '{dice_damage_string}'"
        )
    dice_damage = 0
    fixed_damage = 0
    total_damage = 0
    for part in dice_damage_string.split("+"):
        part = part.strip()
        for p in part.split("d"):
            if p == "":
                p = "1"
            try:
                p = int(p)
            except ValueError:
                raise InvalidDamageExpressionError(
                    f"Expected either a die expression or a number. Got {part}"
                )
        if "d" in part:
            number_of_dice, sides_of_dice = part.split("d")
            number_of_dice = int(number_of_dice or "1")
            sides_of_dice = int(sides_of_dice)
            damage = number_of_dice * get_dice_average_value(sides_of_dice)
            dice_damage += damage
            total_damage += damage
        else:
            fixed_damage += float(part or "0")
            total_damage += float(part or "0")
    return total_damage, dice_damage, fixed_damage


def convert_to_d3_d6(damage: int) -> tuple[int, int, int]:
    """
    Converts an average value to a tuple (d6, d3, fixed)
    :param damage: The average value to convert
    :return: The number of d6, the number of d3, the modifier
    """
    if not isinstance(damage, int) or damage < 0:
        raise InvalidDamageExpressionError(
            f"damage should be a non-negative integer. Got {damage}."
        )
    if damage < 2:
        return 0, 0, damage
    if damage == 2:
        return 0, 1, 0
    if damage == 3:
        return 0, 1, 1
    d6 = math.floor(damage / D6.average_value)
    fixed = math.floor(damage - (d6 * D6.average_value))
    return d6, 0, fixed


def convert_d6_d3_to_string(d6: int, d3: int, fixed: int) -> str:
    """
    Converts a number of d6, d3 and modifier to a die expression
    :param d6: The number of d6
    :param d3: The number of d3
    :param fixed: The fixed modifier
    :return: The die expression
    """
    if not isinstance(d6, int) or d6 < 0:
        raise InvalidDamageExpressionError(
            f"d6 should be a non-negative integer. Got {d6}."
        )
    if not isinstance(d3, int) or d3 < 0:
        raise InvalidDamageExpressionError(
            f"d3 should be a non-negative integer. Got {d3}."
        )
    if not isinstance(fixed, int):
        raise InvalidDamageExpressionError(f"fixed should be an integer. Got {fixed}.")
    ret = ""
    if d6:
        if d6 > 1:
            ret += str(d6)
        ret += "D6"
    if d3:
        if ret and d3 > 0:
            ret += "+"
        if d3 > 1:
            ret += str(d3)
        ret += "D3"
    if fixed:
        if ret and fixed > 0:
            ret += "+"
        ret += str(fixed)
    if not ret:
        return "0"
    return ret
