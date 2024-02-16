import pathlib
import os
import sys
import subprocess
import shutil
import difflib

ROOT_DIR = pathlib.Path(__file__).parent.parent.parent
UI_SRC = ROOT_DIR.joinpath("ui")
COMPILED_UI = ROOT_DIR.joinpath("src").joinpath("ui")


def compile_ui():
    if COMPILED_UI.is_dir():
        shutil.rmtree(COMPILED_UI)
    os.mkdir(COMPILED_UI)
    with open(COMPILED_UI.joinpath("__init__.py"), "w") as f:
        f.writelines(["# Automatically generated module, DO NOT EDIT.\n"])
    for file in os.listdir(UI_SRC):
        input_file = UI_SRC.joinpath(file)
        output_file = COMPILED_UI.joinpath(file.replace(".ui", ".py"))
        subprocess.run(["pyuic6", input_file, "-o", output_file])
        with open(output_file) as f:
            lines = f.readlines()
        output_lines = []
        for line in lines:
            line = line.replace(str(UI_SRC), "ui")
            output_lines.append(line)
        with open(output_file, "w") as f:
            f.writelines(output_lines)
    subprocess.run(
        ["black", COMPILED_UI], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def check() -> None:
    starting_dict = {}
    for file in os.listdir(COMPILED_UI):
        file_path = COMPILED_UI.joinpath(file)
        with open(file_path) as f:
            starting_dict[str(file_path)] = f.readlines()
    compile_ui()
    compiled_dict = {}
    for file in os.listdir(COMPILED_UI):
        file_path = COMPILED_UI.joinpath(file)
        with open(file_path) as f:
            compiled_dict[str(file_path)] = f.readlines()
    starting_files = list(starting_dict.keys())
    compiled_files = list(compiled_dict.keys())
    assert (
        starting_files == compiled_files
    ), f"\n{os.linesep.join(difflib.ndiff(starting_files, compiled_files))}"
    for file, content in starting_dict.items():
        assert (
            content == compiled_dict[file]
        ), f"\n{os.linesep.join(difflib.ndiff(content, compiled_dict[file]))}"


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        check()
    else:
        compile_ui()
