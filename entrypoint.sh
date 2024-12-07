#!/bin/sh

cd "$GITHUB_WORKSPACE" || exit

find . \( -name '*.cmake' -o -name '*.cmake.in' -o -name 'CMakeLists.txt' \) -exec cmake-format $* {} +

exit $?
