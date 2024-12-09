#!/bin/sh

cd "$GITHUB_WORKSPACE" || exit

FILE_REGEX="${PROCESS_FILES:-'*.cmake|CMakeLists.txt'}"

find . -regex $FILE_REGEX -exec cmake-format $* {} +

exit $?
