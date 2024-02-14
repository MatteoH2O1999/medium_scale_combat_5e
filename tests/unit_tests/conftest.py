import sys
import pathlib

current_folder = pathlib.Path(__file__)
root_dir = current_folder.parent.parent.parent.absolute()
src_dir = root_dir.joinpath("src")

sys.path.append(str(src_dir))
