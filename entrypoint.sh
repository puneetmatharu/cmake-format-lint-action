#!/bin/sh

cd "$GITHUB_WORKSPACE" || exit

files=$(find . \( -name '*.cmake' -o -name 'CMakeLists.txt' \))

for file in ${files}; do
    echo "Processing file: ${file}"
    cmake-format $* "${file}"
    exit_code="$?"
    if [ ${exit_code} -ne 0 ]; then
        echo "cmake-format failed. Exiting with exit code ${exit_code}."
        exit ${exit_code}
    fi
done
