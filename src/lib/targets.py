import math

from abc import ABC

from .interfaces import Target as TargetInterface


class InvalidTargetParamError(ValueError):
    pass


class Target(TargetInterface, ABC):
    def __eq__(self, other) -> bool:
        if not isinstance(other, Target):
            return False
        return (
            self.number_of_targets == other.number_of_targets
            and self.is_aoe == other.is_aoe
            and self.description == other.description
        )


class SingleTarget(Target):
    def __init__(self):
        """
        Single target.
        """

    @property
    def number_of_targets(self) -> int:
        return 1

    @property
    def is_aoe(self) -> bool:
        return False

    @property
    def description(self) -> str:
        return "one target"


class AreaOfEffectTarget(Target, ABC):
    @property
    def is_aoe(self) -> bool:
        return True


class Cone(AreaOfEffectTarget):
    """
    Cone area of effect
    """

    def __init__(self, size: int):
        """
        Cone area of effect of *size* ft.
        :param size: The size of the cone in feet as written in the 5e description
        """
        if not isinstance(size, int) or size < 1:
            raise InvalidTargetParamError(
                f"size should be a positive integer. Got {size}."
            )
        self._size: int = size

    @property
    def number_of_targets(self) -> int:
        return math.ceil(self._size / 10)

    @property
    def description(self) -> str:
        return f"{self._size}-foot cone"


class Cube(AreaOfEffectTarget):
    """
    Cube area of effect
    """

    def __init__(self, size: int):
        """
        Cube area of effect of *size* ft.
        :param size: The size of the cube in feet as written in the 5e description
        """
        if not isinstance(size, int) or size < 1:
            raise InvalidTargetParamError(
                f"size should be a positive integer. Got {size}."
            )
        self._size: int = size

    @property
    def number_of_targets(self) -> int:
        return math.ceil(self._size / 5)

    @property
    def description(self) -> str:
        return f"{self._size}-foot cube"


class Square(AreaOfEffectTarget):
    """
    Square area of effect
    """

    def __init__(self, size: int):
        """
        Square area of effect of *size* ft.
        :param size: The size of the square in feet as written in the 5e description
        """
        if not isinstance(size, int) or size < 1:
            raise InvalidTargetParamError(
                f"size should be a positive integer. Got {size}."
            )
        self._size: int = size

    @property
    def number_of_targets(self) -> int:
        return math.ceil(self._size / 5)

    @property
    def description(self) -> str:
        return f"{self._size}-foot square"


class Cylinder(AreaOfEffectTarget):
    """
    Cylindrical area of effect
    """

    def __init__(self, radius: int, height: int):
        """
        Cylindrical area of effect of *radius*-foot radius
        :param radius: The radius of the cylinder of the area of effect in feet as written in the 5e description
        :param height The height of the cylinder of the area of effect in feet as written in the 5e description
        """
        if not isinstance(radius, int) or radius < 1:
            raise InvalidTargetParamError(
                f"radius should be a positive integer. Got {radius}."
            )
        if not isinstance(height, int) or height < 1:
            raise InvalidTargetParamError(
                f"height should be a positive integer. Gor {height}."
            )
        self._radius: int = radius
        self._height: int = height

    @property
    def number_of_targets(self) -> int:
        return math.ceil(self._radius / 5)

    @property
    def description(self) -> str:
        return f"{self._radius}-foot-radius, {self._height}-foot-high cylinder"


class Sphere(AreaOfEffectTarget):
    """
    Spherical area of effect
    """

    def __init__(self, radius: int):
        """
        Spherical area of effect of *radius*-foot radius
        :param radius: The radius of the sphere in feet as written in the 5e description
        """
        if not isinstance(radius, int) or radius < 1:
            raise InvalidTargetParamError(
                f"radius should be a positive integer. Got {radius}."
            )
        self._radius: int = radius

    @property
    def number_of_targets(self) -> int:
        return math.ceil(self._radius / 5)

    @property
    def description(self) -> str:
        return f"{self._radius}-foot-radius sphere"


class Circle(AreaOfEffectTarget):
    """
    Circular area of effect
    """

    def __init__(self, radius: int):
        """
        Circular area of effect of *radius*foot radius
        :param radius: The radius of the sphere in feet as written in the 5e description
        """
        if not isinstance(radius, int) or radius < 1:
            raise InvalidTargetParamError(
                f"radius should be a positive integer. Got {radius}."
            )
        self._radius: int = radius

    @property
    def number_of_targets(self) -> int:
        return math.ceil(self._radius / 5)

    @property
    def description(self) -> str:
        return f"{self._radius}-foot-radius circle"


class Line(AreaOfEffectTarget):
    """
    Line area of effect
    """

    def __init__(self, length: int, width: int = 5):
        """
        Line area of effect *length*-foot long and *width*-foot wide.
        :param length: The length of the line area of effect in feet as written in the 5e description
        :param width: The width of the line area of effect in feet as written in the 5e description. By default it is 5 feet.
        """
        if not isinstance(length, int) or length < 1:
            raise InvalidTargetParamError(
                f"length should be a positive integer. Got {length}."
            )
        if not isinstance(width, int) or width < 1:
            raise InvalidTargetParamError(
                f"width should be a positive integer. Got {width}."
            )
        self._length: int = length
        self._width: int = width

    @property
    def _area(self) -> int:
        return self._length * self._width

    @property
    def number_of_targets(self) -> int:
        return math.ceil(self._area / 150)

    @property
    def description(self) -> str:
        return f"{self._length}-foot line that is {self._width} feet wide"
