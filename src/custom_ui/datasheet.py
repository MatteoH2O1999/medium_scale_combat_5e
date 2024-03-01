import pathlib
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from matplotlib.axes import Axes
from matplotlib import font_manager
from typing import Tuple, List

from lib.interfaces import UnitStatBlock, StatBlock, CreatureAttack

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
SPACE_BETWEEN_ATTACKS = 100


def draw_separator_line(
    start: Tuple[float, float],
    length: float,
    width: float,
    ax: Axes,
    color=RED,
    line=False,
) -> None:
    if line:
        points = [
            (start[0], start[1] + width / 2),
            (start[0], start[1] - width / 2),
            (start[0] + length, start[1] - width / 2),
            (start[0] + length, start[1] + width / 2),
        ]
    else:
        points = [
            (start[0], start[1] + width / 2),
            (start[0], start[1] - width / 2),
            (start[0] + length, start[1]),
        ]
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    ax.fill(x, y, color)


def explicit_sign_str(number: float) -> str:
    if number < 0:
        return str(number)
    return f"+{str(number)}"


def multiattack_string(creature_name: str, attack_list: List[CreatureAttack]) -> str:
    ret = f"The {creature_name} makes "
    for index, attack in list(enumerate(attack_list, start=0)):
        remaining_items = len(attack_list) - 1 - index
        if index > 0:
            if remaining_items > 0:
                ret += ", "
            else:
                ret += " and "
        ret += f"{attack.multiattack} {attack.name} attack"
        if attack.multiattack > 1:
            ret += "s"
    return f"{ret}."


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

    # Attack title
    vertical_position = 875

    attacks_text = ax.text(
        LEFT_MARGIN,
        vertical_position,
        "A",
        fontfamily="Scala Sans",
        fontweight="regular",
        fontsize=28,
    )
    ax.annotate(
        "CTIONS",
        xycoords=attacks_text,
        xy=(1, 0),
        verticalalignment="bottom",
        fontfamily="Scala Sans",
        fontweight="regular",
        fontsize=24,
    )

    draw_separator_line((LEFT_MARGIN, 900), 1800, 2, ax, "black", True)

    # Multiattacks
    vertical_position = 975

    multiattack_names = list(stat_block.multiattacks.keys())
    multiattack_names.sort()
    for multiattack_name in multiattack_names:
        multiattack = stat_block.multiattacks[multiattack_name]
        name_text = ax.text(
            LEFT_MARGIN,
            vertical_position,
            f"{multiattack_name.capitalize()}.",
            fontfamily="Scala Sans",
            fontweight="bold",
            fontstyle="italic",
            fontsize=17,
        )
        ax.annotate(
            multiattack_string(
                " ".join(
                    [part.capitalize() for part in stat_block.name.lower().split(" ")]
                ),
                multiattack,
            ),
            xycoords=name_text,
            xy=(1, 0),
            verticalalignment="bottom",
            fontfamily="Scala Sans",
            fontweight="regular",
            fontsize=17,
        )
        vertical_position += SPACE_BETWEEN_ATTACKS

    # Attacks
    attack_names = list(stat_block.attacks.keys())
    attack_names.sort()
    for attack_name in attack_names:
        attack = stat_block.attacks[attack_name]
        name_text = ax.text(
            LEFT_MARGIN,
            vertical_position,
            f"{attack.name.capitalize()}. ",
            fontfamily="Scala Sans",
            fontweight="bold",
            fontstyle="italic",
            fontsize=17,
        )
        weapon_text = ax.annotate(
            f"{'Melee' if attack.is_melee else 'Ranged'} Weapon Attack: ",
            xycoords=name_text,
            xy=(1, 0),
            verticalalignment="bottom",
            fontfamily="Scala Sans",
            fontweight="regular",
            fontstyle="italic",
            fontsize=17,
        )
        to_hit_text = ax.annotate(
            f"{explicit_sign_str(attack.to_hit_bonus)} to hit, ",
            xycoords=weapon_text,
            xy=(1, 0),
            verticalalignment="bottom",
            fontfamily="Scala Sans",
            fontweight="regular",
            fontsize=17,
        )
        range_text = ax.annotate(
            f"{'reach' if attack.is_melee else 'range'} {attack.range} ft., ",
            xycoords=to_hit_text,
            xy=(1, 0),
            verticalalignment="bottom",
            fontfamily="Scala Sans",
            fontweight="regular",
            fontsize=17,
        )
        target_text = ax.annotate(
            f"{attack.target.description}. ",
            xycoords=range_text,
            xy=(1, 0),
            verticalalignment="bottom",
            fontfamily="Scala Sans",
            fontweight="regular",
            fontsize=17,
        )
        hit_italic_text = ax.annotate(
            "Hit: ",
            xycoords=target_text,
            xy=(1, 0),
            verticalalignment="bottom",
            fontfamily="Scala Sans",
            fontweight="regular",
            fontstyle="italic",
            fontsize=17,
        )
        ax.annotate(
            f"{math.floor(attack.total_average_damage)} damage.",
            xycoords=hit_italic_text,
            xy=(1, 0),
            verticalalignment="bottom",
            fontfamily="Scala Sans",
            fontweight="regular",
            fontsize=17,
        )

        vertical_position += SPACE_BETWEEN_ATTACKS

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
