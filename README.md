# cmake-format lint action

Formats CMake-specific files to the desired format using [`cmake-format`](https://github.com/cheshirekow/cmake_format). To control the style of formatting, make sure to add a configuration file to the root of your project. For details on how to do this, see [Configuration](https://cmake-format.readthedocs.io/en/latest/configuration.html#configuration).

**Note:** The current version of this action will format all `CMakeLists.txt` and `*.cmake` files in your project. If you require finer granularity, please request this feature (or any other features) by creating an Issue on the repository page.

## Usage

To use this action, pass arguments to the `args` element as you would to `cmake-format` - these arguments will be used to format each CMake file. For example

```yaml
  - name: Format CMake files
    id: cmake-format
    uses: PuneetMatharu/cmake-format-lint-action@v1.0.0
    with:
      # Arguments to be passed to cmake-format.
      #
      # Options:
      #   -h, --help            show this help message and exit
      #   -v, --version         show program's version number and exit
      #   -l {error,warning,info,debug}, --log-level {error,warning,info,debug}
      #   --dump-config [{yaml,json,python}]
      #                         If specified, print the default configuration to stdout and exit
      #   --dump {lex,parse,parsedb,layout,markup}
      #   --no-help             When used with --dump-config, will omit helptext comments in the output
      #   --no-default          When used with --dump-config, will omit any unmodified configuration value.
      #   -i, --in-place
      #   --check               Exit with status code 0 if formatting would not change file contents, or status code 1 if it would
      #   -o OUTFILE_PATH, --outfile-path OUTFILE_PATH
      #                         Where to write the formatted file. Default is stdout.
      #   -c CONFIG_FILES [CONFIG_FILES ...], --config-files CONFIG_FILES [CONFIG_FILES ...]
      #                         path to configuration file(s)
      args: --config-files .cmake-format.json --in-place
```

You will probably want to pair this with a GitHub Action (such as
[`stefanzweifel/git-auto-commit-action`](https://github.com/stefanzweifel/git-auto-commit-action))
to commit any modified files. For example:

```yaml
name: Run cmake-format linter

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Format CMake files
      id: cmake-format
      uses: PuneetMatharu/cmake-format-lint-action@v1.0.0
      with:
        args: --config-files .cmake-format.json --in-place

    - name: Commit changes
      uses: stefanzweifel/git-auto-commit-action@v4
      with:
        commit_user_name: cmake-format-bot
        commit_message: 'Automated commit of cmake-format changes.'
```

## Licence

The files distributed with this Action are provided under the blanket of an [MIT licence](LICENCE).
