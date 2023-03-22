import logging
import re
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from itertools import groupby
from os import getcwd
from pathlib import Path
from shutil import move

logger = logging.getLogger("python_filename_linter")


def to_snake_case(name: str):
    name = name.replace("-", "_")
    # replace "aA" with "a_A"
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def lint_path(path: Path, root: Path, rename: bool):
    name = path.stem
    # Snake case :
    # - should be all lowercase
    # - should be separated by underscore
    if name == name.lower() and "-" not in name:
        return

    recommended_name = to_snake_case(name) + path.suffix
    if rename:
        new_path = root / path.parent / recommended_name
        if new_path.exists():
            logger.warning("path not renamed as it would overwrite another")
        else:
            move(root / path, new_path)
    return path, recommended_name


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
        "--lint-folders",
        "-f",
        action="store_true",
        help="If set, will try to lint folder names as well.",
    )
    parser.add_argument(
        "--root",
        "-r",
        type=Path,
        default=Path(getcwd()),
        help=(
            "Folder where to begin to lint filename. files and folders outside this"
            " root will be ignored"
        ),
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Log debug messages to the CLI"
    )

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    args.files = [
        file for file in args.files if file.is_file() and file.suffix == ".py"
    ]
    files = []
    for file in args.files:
        if file.is_dir():
            continue
        try:
            files.append(file.absolute().relative_to(args.root))
        except ValueError:
            logger.debug(f"Ignored: {file} (because it is outside root {args.root})")

    bad_file_paths = []
    for file in files:
        bad_file_paths.append(lint_path(file, args.root, args.rename))
    bad_file_paths = list(filter(bool, bad_file_paths))

    bad_folder_paths = []
    if args.lint_folders:
        folders = []
        for f in files:
            folders.extend(f.parents)
        folders = sorted(folders, key=lambda f: (-len(f.parts), str(f)))
        folders = [k for k, _ in groupby(folders) if str(k) != "."]
        for folder in folders:
            bad_folder_paths.append(lint_path(folder, args.root, args.rename))
        bad_folder_paths = list(filter(bool, bad_folder_paths))

    if bad_file_paths or bad_folder_paths:
        recommendations = list(
            map(lambda x: f"(🐍 module) {x[0]} -> {x[1]}", bad_file_paths)
        )
        recommendations += list(
            map(lambda x: f"(📁 folder) {x[0]} -> {x[1]}", bad_folder_paths)
        )

        logger.warning("\n Paths not in snake cases -> recommended name :")
        logger.warning("\n - " + "\n - ".join(recommendations))

    exit(bool(bad_file_paths or bad_folder_paths))


if __name__ == "__main__":
    filename_linter_entryponint()
