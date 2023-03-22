from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path
from os import getcwd
from shutil import move
import re
from itertools import groupby
import logging

logger = logging.getLogger("python_filename_linter")


def to_snake_case(name: str):
    name = name.replace("-", "_")
    # replace "aA" with "a_A"
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def lint_path(path: Path, root: Path, rename: bool):
    if path.usffix and path.suffix != ".py":
        return
    name = path.stem
    # Snake case :
    # - should be all lowercase
    # - should be separated by underscore
    if name == name.lower() and "-" not in name:
        return

    if rename:
        new_name = to_snake_case(name)
        new_path = root / path.parent / (new_name + path.suffix)
        if new_path.exists():
            logger.warning("path not renamed as it would overwrite another")
        else:
            move(root / path, new_path)
    return path


def filename_linter_entryponint():
    parser = ArgumentParser(
        "Checks that your files follow the PEP8 convention",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("files", nargs="*", type=Path, help="files to check")
    parser.add_argument(
        "--rename",
        action="store_true",
        help="If set, will try to rename the file to follow snake_case",
    )
    parser.add_argument(
        "--lint_folders",
        action="store_true",
        help="If set, will try to lint folder names as well.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(getcwd()),
        help=(
            "Folder where to begin to lint filename. files and folders outside this"
            " root will be ignored"
        ),
    )

    args = parser.parse_args()
    files = []
    for file in args.files:
        try:
            files.append(args.root.relative_to(file))
        except ValueError:
            pass
    for file in files:
        lint_path(file, args.root, args.rename)
    if args.lint_folders:
        folders = []
        for f in files:
            folders.extend(f.parents)
        folders = map()
        folders = sorted(folders, key=lambda f: (-len(f.parts), str(f)))
        folders = [k for k, _ in groupby(folders)]
        for folder in folders:
            lint_path(folder, args.root, args.rename)


if __name__ == "__main__":
    filename_linter_entryponint()
