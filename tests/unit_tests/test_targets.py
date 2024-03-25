import pytest

import lib.targets as targets


def test_target_eq():
    assert targets.SingleTarget() == targets.SingleTarget()
    assert targets.Cube(3) == targets.Cube(3)
    assert targets.Cube(3) != targets.Square(3)
    assert targets.SingleTarget() != "other"
    assert targets.Line(20, 30) != targets.Line(20, 20)
    assert targets.Line(20, 30) == targets.Line(20, 30)


def test_single_target_targets():
    t = targets.SingleTarget()

    assert t.number_of_targets == 1


def test_single_target_aoe():
    t = targets.SingleTarget()

    assert t.is_aoe is False


def test_single_target_description():
    t = targets.SingleTarget()

    assert t.description == "one target"


def test_cone_parameter_range():
    targets.Cone(3)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Cone(0)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Cone(-4)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Cone("other")  # noqa


def test_cone_targets():
    t15 = targets.Cone(15)
    t90 = targets.Cone(90)
    t30 = targets.Cone(30)

    assert t15.number_of_targets == 2
    assert t90.number_of_targets == 9
    assert t30.number_of_targets == 3


def test_cone_aoe():
    t = targets.Cone(15)

    assert t.is_aoe is True


def test_cone_description():
    t = targets.Cone(15)

    assert t.description == "15-foot cone"


def test_cube_parameter_range():
    targets.Cube(3)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Cube(0)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Cube(-4)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Cube("other")  # noqa


def test_cube_targets():
    t15 = targets.Cube(15)
    t90 = targets.Cube(90)
    t30 = targets.Cube(30)

    assert t15.number_of_targets == 3
    assert t90.number_of_targets == 18
    assert t30.number_of_targets == 6


def test_cube_aoe():
    t = targets.Cube(15)

    assert t.is_aoe is True


def test_cube_description():
    t = targets.Cube(15)

    assert t.description == "15-foot cube"


def test_square_parameter_range():
    targets.Square(3)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Square(0)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Square(-4)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Square("other")  # noqa


def test_square_targets():
    t15 = targets.Square(15)
    t90 = targets.Square(90)
    t30 = targets.Square(30)

    assert t15.number_of_targets == 3
    assert t90.number_of_targets == 18
    assert t30.number_of_targets == 6


def test_square_aoe():
    t = targets.Square(15)

    assert t.is_aoe is True


def test_square_description():
    t = targets.Square(15)

    assert t.description == "15-foot square"


def test_cylinder_parameter_range():
    targets.Cylinder(3, 3)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Cylinder(0, 3)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Cylinder(-4, 3)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Cylinder("other", 3)  # noqa
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Cylinder(3, 0)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Cylinder(3, -4)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Cylinder(3, "other")  # noqa


def test_cylinder_targets():
    t15 = targets.Cylinder(15, 20)
    t90 = targets.Cylinder(90, 20)
    t30 = targets.Cylinder(30, 20)

    assert t15.number_of_targets == 3
    assert t90.number_of_targets == 18
    assert t30.number_of_targets == 6


def test_cylinder_aoe():
    t = targets.Cylinder(15, 20)

    assert t.is_aoe is True


def test_cylinder_description():
    t = targets.Cylinder(15, 20)

    assert t.description == "15-foot-radius, 20-foot-high cylinder"


def test_sphere_parameter_range():
    targets.Sphere(3)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Sphere(0)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Sphere(-4)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Sphere("other")  # noqa


def test_sphere_targets():
    t15 = targets.Sphere(15)
    t90 = targets.Sphere(90)
    t30 = targets.Sphere(30)

    assert t15.number_of_targets == 3
    assert t90.number_of_targets == 18
    assert t30.number_of_targets == 6


def test_sphere_aoe():
    t = targets.Sphere(15)

    assert t.is_aoe is True


def test_sphere_description():
    t = targets.Sphere(15)

    assert t.description == "15-foot-radius sphere"


def test_circle_parameter_range():
    targets.Circle(3)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Circle(0)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Circle(-4)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Circle("other")  # noqa


def test_circle_targets():
    t15 = targets.Circle(15)
    t90 = targets.Circle(90)
    t30 = targets.Circle(30)

    assert t15.number_of_targets == 3
    assert t90.number_of_targets == 18
    assert t30.number_of_targets == 6


def test_circle_aoe():
    t = targets.Circle(15)

    assert t.is_aoe is True


def test_circle_description():
    t = targets.Circle(15)

    assert t.description == "15-foot-radius circle"


def test_line_parameter_range():
    targets.Line(3, 3)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Line(0, 3)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Line(-4, 3)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Line("other", 3)  # noqa
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Line(3, 0)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Line(3, -4)
    with pytest.raises(targets.InvalidTargetParamError):
        targets.Line(3, "other")  # noqa


def test_line_targets():
    t15 = targets.Line(15, 5)
    t90 = targets.Line(90, 5)
    t30 = targets.Line(30, 5)
    t30_wide = targets.Line(30, 10)

    assert t15.number_of_targets == 1
    assert t90.number_of_targets == 3
    assert t30.number_of_targets == 1
    assert t30_wide.number_of_targets == 2


def test_line_aoe():
    t = targets.Line(15, 20)

    assert t.is_aoe is True


def test_line_description():
    t = targets.Line(30, 10)

    assert t.description == "30-foot line that is 10 feet wide"
