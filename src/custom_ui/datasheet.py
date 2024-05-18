import pathlib
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import re

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
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.default"] = "regular"
plt.rcParams["mathtext.bfit"] = font_manager.FontProperties(
    "Scala Sans", "italic", "normal", 700
).get_fontconfig_pattern()
plt.rcParams["mathtext.bf"] = font_manager.FontProperties(
    "Scala Sans", "normal", "normal", 700
).get_fontconfig_pattern()
plt.rcParams["mathtext.it"] = font_manager.FontProperties(
    "Scala Sans", "italic", "normal", 400
).get_fontconfig_pattern()
plt.rcParams["mathtext.rm"] = font_manager.FontProperties(
    "Scala Sans", "normal", "normal", 400
).get_fontconfig_pattern()

LEFT_MARGIN = 100
RED = "#58170d"
DARKER_CELL = f"{RED}1A"
PAPER_COLOR = "#eee7d7"
SPACE_BETWEEN_ATTACKS = 77


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


def capitalize_name(name: str) -> str:
    ret = name.capitalize()
    ret = capitalize_after_symbol(ret, " ")
    ret = capitalize_after_symbol(ret, "(")
    return ret


def capitalize_after_symbol(string: str, symbol: str) -> str:
    ret = list(string)
    for match in re.finditer(re.escape(symbol), string):
        index_to_change = match.end()
        if index_to_change < len(string):
            ret[index_to_change] = string[index_to_change].upper()
    return "".join(ret)


def square(x: int, y: int, half_size: int) -> List[Tuple[int, int]]:
    round_size = 20
    return [
        (x - half_size + round_size, y - half_size),
        (x - half_size, y - half_size + round_size),
        (x - half_size, y + half_size),
        (x + half_size - round_size, y + half_size),
        (x + half_size, y + half_size - round_size),
        (x + half_size, y - half_size),
    ]


def dotted_line(x: float, y: float, length: int, ax: Axes):
    points = [(x, y), (x + length, y)]
    x = [p[0] for p in points]
    y = [p[1] for p in points]

    ax.plot(x, y, linestyle=(0, (1, 4)), linewidth=1, color=RED)


def datasheet_from_unit_stat_block(stat_block: UnitStatBlock) -> plt.Figure:
    figure = plt.figure(figsize=(15, 10))
    ax = figure.add_subplot(111)
    figure.subplots_adjust(0.0, 0.0, 1.0, 1.0)
    ax.imshow(HORIZONTAL_PAPER)
    ax.set_axis_off()
    ax.set_xlim(0, 3000)
    ax.set_ylim(2000, 0)

    # Title background
    title_box_height = 550

    points = [(0, 0), (3000, 0), (3000, title_box_height), (0, title_box_height)]
    x = [p[0] for p in points]
    y = [p[1] for p in points]

    ax.fill(x, y, RED)

    # Creature name
    name = " ".join([part.capitalize() for part in stat_block.name.split(" ")])
    ax.text(
        LEFT_MARGIN,
        150,
        name,
        color="w",
        fontfamily="Spectral SC",
        fontweight="bold",
        fontsize=36,
        fontvariant="small-caps",
    )

    # Stats labels and boxes
    interval = 175
    height = 225
    box_half_size = 60
    box_offset = 80
    start = LEFT_MARGIN + 20 + box_half_size
    font_size = 25
    stats = [
        ("Spd", str(stat_block.speed)),
        ("Def", str(stat_block.resistance)),
        ("Save", f"{stat_block.saving_throw}+"),
        ("HP", str(stat_block.hit_points)),
    ]

    x = start
    y = height
    box_y = y + box_offset
    for stat, value in stats:
        points = square(x, box_y, box_half_size)
        x_points = [p[0] for p in points]
        y_points = [p[1] for p in points]

        ax.text(
            x,
            y,
            stat,
            color="w",
            fontfamily="Scala Sans",
            fontweight="bold",
            fontsize=17,
            horizontalalignment="center",
        )
        ax.fill(x_points, y_points, PAPER_COLOR)
        ax.text(
            x,
            box_y,
            value,
            color=RED,
            fontfamily="Scala Sans",
            fontweight="bold",
            fontsize=font_size,
            horizontalalignment="center",
            verticalalignment="center",
        )

        if stat == "Save" and stat_block.invulnerable_saving_throw is not None:
            invul_y = box_y + 2 * box_half_size + 30
            points = square(x, invul_y, box_half_size)
            x_points = [p[0] for p in points]
            y_points = [p[1] for p in points]
            ax.fill(x_points, y_points, PAPER_COLOR)
            ax.text(
                x,
                invul_y,
                f"{stat_block.invulnerable_saving_throw}+",
                color=RED,
                fontfamily="Scala Sans",
                fontweight="bold",
                fontsize=font_size,
                horizontalalignment="center",
                verticalalignment="center",
            )
            ax.text(
                x + box_half_size + 20,
                invul_y,
                "Invulnerable Save",
                color="w",
                fontfamily="Scala Sans",
                fontweight="bold",
                fontsize=17,
                verticalalignment="center",
            )

        x += interval

    ranged = any([not a.is_melee for a in stat_block.attacks])

    if ranged:
        # Ranged weapon title
        vertical_position = 650
        interval = 300
        font_size = 20

        range_position = 1200
        attacks_position = range_position + interval
        skill_position = attacks_position + interval
        strength_position = skill_position + interval
        ap_position = strength_position + interval
        damage_position = ap_position + interval

        attacks_text = ax.text(
            LEFT_MARGIN,
            vertical_position,
            "R",
            fontfamily="Spectral SC",
            fontweight="bold",
            fontsize=28,
        )
        ax.annotate(
            "ANGED WEAPONS",
            xycoords=attacks_text,
            xy=(1, 0),
            verticalalignment="bottom",
            fontfamily="Spectral SC",
            fontweight="bold",
            fontsize=24,
        )

        ax.text(
            range_position,
            vertical_position,
            "Range",
            fontfamily="Spectral SC",
            fontweight="regular",
            fontsize=font_size,
            horizontalalignment="center",
        )
        ax.text(
            attacks_position,
            vertical_position,
            "Attacks",
            fontfamily="Spectral SC",
            fontweight="regular",
            fontsize=font_size,
            horizontalalignment="center",
        )
        ax.text(
            skill_position,
            vertical_position,
            "Skill",
            fontfamily="Spectral SC",
            fontweight="regular",
            fontsize=font_size,
            horizontalalignment="center",
        )
        ax.text(
            strength_position,
            vertical_position,
            "Strength",
            fontfamily="Spectral SC",
            fontweight="regular",
            fontsize=font_size,
            horizontalalignment="center",
        )
        ax.text(
            ap_position,
            vertical_position,
            "AP",
            fontfamily="Spectral SC",
            fontweight="regular",
            fontsize=font_size,
            horizontalalignment="center",
        )
        ax.text(
            damage_position,
            vertical_position,
            "Damage",
            fontfamily="Spectral SC",
            fontweight="regular",
            fontsize=font_size,
            horizontalalignment="center",
        )

        draw_separator_line((LEFT_MARGIN, 675), 2800, 2, ax, RED, True)

        # Ranged weapons

        y = 715
        name_x = LEFT_MARGIN + 20
        cell_height = 75
        half_cell_height = cell_height / 2
        data_font_size = 17
        darken = False

        for ranged_attack in stat_block.attacks:
            if ranged_attack.is_melee:
                continue
            if darken:
                points = [
                    (LEFT_MARGIN, y - half_cell_height),
                    (LEFT_MARGIN + 2800, y - half_cell_height),
                    (LEFT_MARGIN + 2800, y + half_cell_height),
                    (LEFT_MARGIN, y + half_cell_height),
                ]

                x_points = [p[0] for p in points]
                y_points = [p[1] for p in points]
                ax.fill(x_points, y_points, DARKER_CELL)

            ax.text(
                name_x,
                y,
                ranged_attack.name,
                fontfamily="Scala Sans",
                fontweight="regular",
                fontsize=data_font_size,
                verticalalignment="center",
            )

            ax.text(
                range_position,
                y,
                f"{ranged_attack.range} ft.",
                fontfamily="Spectral SC",
                fontweight="regular",
                fontsize=data_font_size,
                verticalalignment="center",
                horizontalalignment="center",
            )
            ax.text(
                attacks_position,
                y,
                ranged_attack.number_of_attacks,
                fontfamily="Spectral SC",
                fontweight="regular",
                fontsize=data_font_size,
                verticalalignment="center",
                horizontalalignment="center",
            )
            ax.text(
                skill_position,
                y,
                (
                    f"{ranged_attack.attack_skill}+"
                    if ranged_attack.attack_skill is not None
                    else "N/A"
                ),
                fontfamily="Spectral SC",
                fontweight="regular",
                fontsize=data_font_size,
                verticalalignment="center",
                horizontalalignment="center",
            )
            ax.text(
                strength_position,
                y,
                str(ranged_attack.strength),
                fontfamily="Spectral SC",
                fontweight="regular",
                fontsize=data_font_size,
                verticalalignment="center",
                horizontalalignment="center",
            )
            ax.text(
                ap_position,
                y,
                str(ranged_attack.armor_penetration),
                fontfamily="Spectral SC",
                fontweight="regular",
                fontsize=data_font_size,
                verticalalignment="center",
                horizontalalignment="center",
            )
            ax.text(
                damage_position,
                y,
                ranged_attack.damage,
                fontfamily="Spectral SC",
                fontweight="regular",
                fontsize=data_font_size,
                verticalalignment="center",
                horizontalalignment="center",
            )

            dotted_line(LEFT_MARGIN, y + half_cell_height, 2800, ax)

            y += cell_height
            darken = not darken

        # Ranged multiattacks

        for multiattack_name, attack_list in stat_block.multiattacks.items():
            if attack_list[0].is_melee:
                continue

            # Ranged mumultiattack single attack
            for attack in attack_list:
                if darken:
                    points = [
                        (LEFT_MARGIN, y - half_cell_height),
                        (LEFT_MARGIN + 2800, y - half_cell_height),
                        (LEFT_MARGIN + 2800, y + half_cell_height),
                        (LEFT_MARGIN, y + half_cell_height),
                    ]

                    x_points = [p[0] for p in points]
                    y_points = [p[1] for p in points]
                    ax.fill(x_points, y_points, DARKER_CELL)

                ax.text(
                    name_x,
                    y,
                    f"{multiattack_name} - {attack.name}",
                    fontfamily="Scala Sans",
                    fontweight="regular",
                    fontsize=data_font_size,
                    verticalalignment="center",
                )

                ax.text(
                    range_position,
                    y,
                    f"{attack.range} ft.",
                    fontfamily="Spectral SC",
                    fontweight="regular",
                    fontsize=data_font_size,
                    verticalalignment="center",
                    horizontalalignment="center",
                )
                ax.text(
                    attacks_position,
                    y,
                    attack.number_of_attacks,
                    fontfamily="Spectral SC",
                    fontweight="regular",
                    fontsize=data_font_size,
                    verticalalignment="center",
                    horizontalalignment="center",
                )
                ax.text(
                    skill_position,
                    y,
                    (
                        f"{attack.attack_skill}+"
                        if attack.attack_skill is not None
                        else "N/A"
                    ),
                    fontfamily="Spectral SC",
                    fontweight="regular",
                    fontsize=data_font_size,
                    verticalalignment="center",
                    horizontalalignment="center",
                )
                ax.text(
                    strength_position,
                    y,
                    str(attack.strength),
                    fontfamily="Spectral SC",
                    fontweight="regular",
                    fontsize=data_font_size,
                    verticalalignment="center",
                    horizontalalignment="center",
                )
                ax.text(
                    ap_position,
                    y,
                    str(attack.armor_penetration),
                    fontfamily="Spectral SC",
                    fontweight="regular",
                    fontsize=data_font_size,
                    verticalalignment="center",
                    horizontalalignment="center",
                )
                ax.text(
                    damage_position,
                    y,
                    attack.damage,
                    fontfamily="Spectral SC",
                    fontweight="regular",
                    fontsize=data_font_size,
                    verticalalignment="center",
                    horizontalalignment="center",
                )

                if attack == attack_list[-1]:
                    dotted_line(LEFT_MARGIN, y + half_cell_height, 2800, ax)
                y += cell_height

            darken = not darken

    return figure


def datasheet_from_stat_block(stat_block: StatBlock) -> plt.Figure:
    # Init stat block background
    figure = plt.figure(figsize=(10, 15))
    ax = figure.add_subplot(111)
    figure.subplots_adjust(0.0, 0.0, 1.0, 1.0)
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

    figure.draw_without_rendering()
    avg_line_height = speed_text.get_window_extent().height

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
    vertical_position = 950

    multiattack_names = list(stat_block.multiattacks.keys())
    multiattack_names.sort()
    for multiattack_name in multiattack_names:
        multiattack = stat_block.multiattacks[multiattack_name]
        multiattack_description = multiattack_string(
            capitalize_name(stat_block.name.lower()),
            multiattack,
        )
        multiattack_text = "\\ ".join(
            f"$\\mathbfit{{{capitalize_name(multiattack_name)}.}}$".split(" ")
        )
        multiattack_text += multiattack_description
        text = ax.text(
            LEFT_MARGIN,
            vertical_position,
            multiattack_text,
            fontfamily="Scala Sans",
            fontweight="regular",
            fontsize=17,
            wrap=True,
            verticalalignment="top",
        )
        figure.draw_without_rendering()
        vertical_position += SPACE_BETWEEN_ATTACKS * max(
            1, math.floor(text.get_window_extent().height / avg_line_height)
        )

    # Attacks
    attack_names = list(stat_block.attacks.keys())
    attack_names.sort()
    for attack_name in attack_names:
        attack = stat_block.attacks[attack_name]
        text_string = ""
        text_string += "\\ ".join(
            f"$\\mathbfit{{{capitalize_name(attack.name)}.}}$".split(" ")
        )
        text_string += f"$\\mathit{{{'Melee' if attack.is_melee else 'Ranged'} Weapon Attack:}}$".replace(
            " ", "\\ "
        )
        text_string += f"{explicit_sign_str(attack.to_hit_bonus)} to hit, "
        text_string += f"{'reach' if attack.is_melee else 'range'} {attack.range} ft., "
        text_string += f"{attack.target.description}. "
        text_string += (
            f"$\\mathit{{Hit:}}${math.floor(attack.total_average_damage)} damage."
        )
        text = ax.text(
            LEFT_MARGIN,
            vertical_position,
            text_string,
            fontfamily="Scala Sans",
            fontweight="regular",
            fontsize=17,
            wrap=True,
            verticalalignment="top",
        )
        figure.draw_without_rendering()
        vertical_position += SPACE_BETWEEN_ATTACKS * max(
            1, math.floor(text.get_window_extent().height / avg_line_height)
        )

    return figure


def export_datasheet_from_unit_stat_block(
    stat_block: UnitStatBlock, path: pathlib.Path
) -> None:
    fig = datasheet_from_unit_stat_block(stat_block)
    fig.subplots_adjust(0.0, 0.0, 1.0, 1.0)
    fig.canvas.draw()
    img = Image.frombytes(
        "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
    )
    img.save(path)


def export_datasheet_from_stat_block(stat_block: StatBlock, path: pathlib.Path) -> None:
    fig = datasheet_from_stat_block(stat_block)
    fig.subplots_adjust(0.0, 0.0, 1.0, 1.0)
    fig.canvas.draw()
    img = Image.frombytes(
        "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
    )
    img.save(path)
