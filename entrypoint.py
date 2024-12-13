#!/usr/bin/env python3

import argparse
import os
import re
import subprocess
from pathlib import Path
from multiprocessing import Pool
from typing import List, Tuple, Optional


def format_cmake_file(file_and_args: Tuple[Path, str]) -> Optional[str]:
    (file_path, cmake_format_args) = file_and_args
    cmake_command = f"cmake-format {cmake_format_args} {file_path}"
    cmake_format_result = subprocess.run(cmake_command, shell=True, capture_output=True, text=True)
    if cmake_format_result.returncode != 0:
        return f"Error formatting {file_path}: {cmake_format_result.stderr}"
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Format CMake files using cmake-format.")
    parser.add_argument('--file-regex', required=True, help="Regex pattern to match filenames.")
    parser.add_argument('--cmake-format-args', required=True, help="Additional arguments for cmake-format.")
    args = parser.parse_args()
    if len(args.file_regex) == 0:
        parser.error("The --file-regex argument cannot be empty.")
    return args


if __name__ == "__main__":
    args = parse_args()

    file_regex = re.compile(args.file_regex)
    workspace_path = Path(os.environ['GITHUB_WORKSPACE'])

    matched_files = [
        (file_path, args.cmake_format_args)
        for file_path in workspace_path.rglob('*')
        if file_path.is_file() and file_regex.match(file_path.name)
    ]

    if len(matched_files) > 0:
        with Pool() as pool:
            format_results = pool.map(format_cmake_file, matched_files)
        for result in format_results:
            if result:
                print(result)
    else:
        print("No files matched the given regex.")
