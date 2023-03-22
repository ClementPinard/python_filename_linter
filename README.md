# python_filename_linter
Checks that your python file follow PEP8 and are all in snake_case

See reference : https://peps.python.org/pep-0008/#package-and-module-names

## Features

Check all the python filenames of your codebase and check they are in snake_case.

If not, will propose renaming recommendations that follow snake_case by trying to parse
camelCase or PascalCase

It can also optionally lint the folder names, and do the renaming for you (see options below)

renaming is not done by default, because it would then break the imports. Some IDEs like
VScode or pycharm do have a renaming tool that fix all the imports at the same time, so
you might prefer using that.

If anyone has a solution to this smart renaming from CLI, please let me know so that I
can add it as a feature in this repo.

## How to use it

### CLI

Install it with pip

```bash
pip install -e .
```

Run it at the root of your code base

```bash
lint_python_filenames **/*
```

### Pre-commit

Use the following hook in your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/ClementPinard/python_filename_linter
  rev: v0.1.0
  hooks:
  - id: python-filename-linter
    args:
    - --lint-folders
    - --root <root>
    - --rename
```

Note that you can use `exclude` and `files` entries to control what to include or
exclude.

```yaml
- repo: https://github.com/ClementPinard/python_filename_linter
  rev: v0.1.0
  hooks:
  - id: python-filename-linter
    args:
    - --lint-folders
    - --root <root>
    - --rename
    exclude: "test_"
```

### Arguments

- `--lint-folders`: If selected, will also lint folder names
- `--rename`: If selected, will rename paths according to snake_case recommendations.
  Be aware that this will break your imports
- `--root <folder>`: In the case not all your folders are storing python code,
  the tool will only lint names of files and folders included in given root folder.
  By default is the current working directory (given by `os.getcwd()`)
