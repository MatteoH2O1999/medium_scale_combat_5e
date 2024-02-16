import pathlib
import matplotlib as mpl
import matplotlib.pyplot as plt

from matplotlib.axes import Axes

from lib.interfaces import UnitStatBlock, StatBlock

mpl.use("QtAgg")


def datasheet_from_unit_stat_block(stat_block: UnitStatBlock, axes: Axes) -> None:
    axes.plot([0, 1], [10, 1])


def datasheet_from_stat_block(stat_block: StatBlock, axes: Axes) -> None:
    axes.plot([0, 1], [1, 10])


def export_datasheet_from_unit_stat_block(
    stat_block: UnitStatBlock, path: pathlib.Path
) -> None:
    fig = plt.figure(figsize=(15, 10), dpi=300)
    ax = fig.add_subplot(111)
    datasheet_from_unit_stat_block(stat_block, ax)
    fig.savefig(fname=str(path))


def export_datasheet_from_stat_block(stat_block: StatBlock, path: pathlib.Path) -> None:
    fig = plt.figure(figsize=(15, 10), dpi=300)
    ax = fig.add_subplot(111)
    datasheet_from_stat_block(stat_block, ax)
    fig.savefig(fname=str(path))
