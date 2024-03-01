import pathlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from matplotlib.axes import Axes
from matplotlib import font_manager
from typing import Tuple

from lib.interfaces import UnitStatBlock, StatBlock

mpl.use("QtAgg")
resource_folder = pathlib.Path(__file__).parent.parent.joinpath("resources")
VERTICAL_PAPER = np.asarray(Image.open(resource_folder.joinpath("paper.jpg")))
HORIZONTAL_PAPER = VERTICAL_PAPER.transpose([1, 0, 2])
font_files = font_manager.findSystemFonts(fontpaths=[resource_folder])
for font in font_files:
    filename = pathlib.Path(font).name
    if "ScalaSans" in filename:
        entry = font_manager.FontEntry(
            font,
            "Scala Sans",
            "italic" if "Italic" in filename else "normal",
            "normal",
            700 if "Bold" in filename else 400,
            "normal",
            "medium",
        )
        font_manager.fontManager.ttflist.append(entry)
    else:
        font_manager.fontManager.addfont(font)

LEFT_MARGIN = 100
RED = "#58170d"


def draw_separator_line(
    start: Tuple[float, float], length: float, width: float, ax: Axes
) -> None:
    points = [
        (start[0], start[1] + width / 2),
        (start[0], start[1] - width / 2),
        (start[0] + length, start[1]),
    ]
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    ax.fill(x, y, RED)


def explicit_sign_str(number: float) -> str:
    if number < 0:
        return str(number)
    return f"+{str(number)}"


def datasheet_from_unit_stat_block(stat_block: UnitStatBlock) -> plt.Figure:
    figure = plt.figure(figsize=(15, 10))
    ax = figure.add_subplot(111)
    ax.imshow(HORIZONTAL_PAPER)
    ax.set_axis_off()

    return figure


def datasheet_from_stat_block(stat_block: StatBlock) -> plt.Figure:
    # Init stat block background
    figure = plt.figure(figsize=(10, 15))
    ax = figure.add_subplot(111)
    ax.imshow(VERTICAL_PAPER)
    ax.set_axis_off()
    ax.set_xlim(0, 2000)
    ax.set_ylim(3000, 0)

    # Creature name
    name = " ".join([part.capitalize() for part in stat_block.name.split(" ")])
    ax.text(
        LEFT_MARGIN,
        200,
        name,
        color=RED,
        fontfamily="Spectral SC",
        fontweight="bold",
        fontsize=34,
        fontvariant="small-caps",
    )
    draw_separator_line((LEFT_MARGIN, 275), 1800, 20, ax)

    # AC, HP, Speed
    ac_text = ax.text(
        LEFT_MARGIN,
        375,
        "Armor Class ",
        fontfamily="Scala Sans",
        fontweight="bold",
        fontsize=17,
        color=RED,
    )
    ax.annotate(
        str(stat_block.armor_class),
        xycoords=ac_text,
        xy=(1, 0),
        verticalalignment="bottom",
        fontfamily="Scala Sans",
        fontweight="regular",
        fontsize=17,
    )

    hp_text = ax.annotate(
        "Hit Points ",
        xycoords=ac_text,
        xy=(0, -1),
        fontfamily="Scala Sans",
        fontweight="bold",
        fontsize=17,
        color=RED,
    )
    ax.annotate(
        str(stat_block.hit_points),
        xycoords=hp_text,
        xy=(1, 0),
        verticalalignment="bottom",
        fontfamily="Scala Sans",
        fontweight="regular",
        fontsize=17,
    )

    speed_text = ax.annotate(
        "Speed ",
        xycoords=hp_text,
        xy=(0, -1),
        fontfamily="Scala Sans",
        fontweight="bold",
        fontsize=17,
        color=RED,
    )
    ax.annotate(
        f"{stat_block.speed} ft.",
        xycoords=speed_text,
        xy=(1, 0),
        verticalalignment="bottom",
        fontfamily="Scala Sans",
        fontweight="regular",
        fontsize=17,
    )

    draw_separator_line((LEFT_MARGIN, 550), 1800, 20, ax)

    # Ability scores
    vertical_position = 630
    horizontal_positions = [i for i in np.linspace(0, 2000, 8, dtype=np.int64)]
    horizontal_positions = horizontal_positions[1:-1]

    str_text = ax.text(
        horizontal_positions[0],
        vertical_position,
        "STR",
        fontfamily="Scala Sans",
        fontweight="bold",
        fontsize=17,
        color=RED,
        ha="center",
    )
    dex_text = ax.text(
        horizontal_positions[1],
        vertical_position,
        "DEX",
        fontfamily="Scala Sans",
        fontweight="bold",
        fontsize=17,
        color=RED,
        ha="center",
    )
    con_text = ax.text(
        horizontal_positions[2],
        vertical_position,
        "CON",
        fontfamily="Scala Sans",
        fontweight="bold",
        fontsize=17,
        color=RED,
        ha="center",
    )
    int_text = ax.text(
        horizontal_positions[3],
        vertical_position,
        "INT",
        fontfamily="Scala Sans",
        fontweight="bold",
        fontsize=17,
        color=RED,
        ha="center",
    )
    wis_text = ax.text(
        horizontal_positions[4],
        vertical_position,
        "WIS",
        fontfamily="Scala Sans",
        fontweight="bold",
        fontsize=17,
        color=RED,
        ha="center",
    )
    cha_text = ax.text(
        horizontal_positions[5],
        vertical_position,
        "CHA",
        fontfamily="Scala Sans",
        fontweight="bold",
        fontsize=17,
        color=RED,
        ha="center",
    )

    ax.annotate(
        f"{stat_block.ability_scores.strength} ({explicit_sign_str(stat_block.ability_scores.strength_modifier)})",
        xycoords=str_text,
        xy=(0.5, -1),
        fontfamily="Scala Sans",
        fontweight="regular",
        fontsize=17,
        ha="center",
    )
    ax.annotate(
        f"{stat_block.ability_scores.dexterity} ({explicit_sign_str(stat_block.ability_scores.dexterity_modifier)})",
        xycoords=dex_text,
        xy=(0.5, -1),
        fontfamily="Scala Sans",
        fontweight="regular",
        fontsize=17,
        ha="center",
    )
    ax.annotate(
        f"{stat_block.ability_scores.constitution} ({explicit_sign_str(stat_block.ability_scores.constitution_modifier)})",
        xycoords=con_text,
        xy=(0.5, -1),
        fontfamily="Scala Sans",
        fontweight="regular",
        fontsize=17,
        ha="center",
    )
    ax.annotate(
        f"{stat_block.ability_scores.intelligence} ({explicit_sign_str(stat_block.ability_scores.intelligence_modifier)})",
        xycoords=int_text,
        xy=(0.5, -1),
        fontfamily="Scala Sans",
        fontweight="regular",
        fontsize=17,
        ha="center",
    )
    ax.annotate(
        f"{stat_block.ability_scores.wisdom} ({explicit_sign_str(stat_block.ability_scores.wisdom_modifier)})",
        xycoords=wis_text,
        xy=(0.5, -1),
        fontfamily="Scala Sans",
        fontweight="regular",
        fontsize=17,
        ha="center",
    )
    ax.annotate(
        f"{stat_block.ability_scores.charisma} ({explicit_sign_str(stat_block.ability_scores.charisma_modifier)})",
        xycoords=cha_text,
        xy=(0.5, -1),
        fontfamily="Scala Sans",
        fontweight="regular",
        fontsize=17,
        ha="center",
    )

    draw_separator_line((LEFT_MARGIN, 750), 1800, 20, ax)

    return figure


def export_datasheet_from_unit_stat_block(
    stat_block: UnitStatBlock, path: pathlib.Path
) -> None:
    fig = datasheet_from_unit_stat_block(stat_block)
    fig.tight_layout(pad=0)
    fig.canvas.draw()
    img = Image.frombytes(
        "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
    )
    img.save(path)


def export_datasheet_from_stat_block(stat_block: StatBlock, path: pathlib.Path) -> None:
    fig = datasheet_from_stat_block(stat_block)
    fig.tight_layout(pad=0)
    fig.canvas.draw()
    img = Image.frombytes(
        "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
    )
    img.save(path)
