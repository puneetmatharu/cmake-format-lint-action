#!/usr/bin/env python3

import argparse
import difflib
import os
import re
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence


@dataclass
class FileResult:
    success: bool
    message: str


def should_write_files(cmake_format_args: Sequence[str]) -> bool:
    write_flags = {'-i', '--in-place', '-o', '--outfile-path'}
    return any(
        flag in write_flags or flag.startswith('--outfile-path=')
        for flag in cmake_format_args
    )


def strip_check_and_write_args(cmake_format_args: Sequence[str]) -> list[str]:
    filtered_args: list[str] = []
    skip_next = False
    for arg in cmake_format_args:
        if skip_next:
            skip_next = False
            continue
        if arg in {'--check', '-i', '--in-place'}:
            continue
        # Drop outfile flags so check mode always compares stdout against the file on disk.
        if arg in {'-o', '--outfile-path'}:
            skip_next = True
            continue
        if arg.startswith('--outfile-path='):
            continue
        filtered_args.append(arg)
    return filtered_args


def run_cmake_format(file_path: Path, cmake_format_args: Sequence[str]) -> subprocess.CompletedProcess[str]:
    command = ['cmake-format', *cmake_format_args, str(file_path)]
    return subprocess.run(command, capture_output=True, text=True)


def render_command_error(file_path: Path, result: subprocess.CompletedProcess[str]) -> str:
    output = result.stderr.strip() or result.stdout.strip() or "cmake-format exited with no output."
    return f"Error processing {file_path}:\n{output}"


def render_diff(file_path: Path, original_contents: str, formatted_contents: str) -> str:
    diff = ''.join(
        difflib.unified_diff(
            original_contents.splitlines(keepends=True),
            formatted_contents.splitlines(keepends=True),
            fromfile=f"{file_path} (current)",
            tofile=f"{file_path} (formatted)",
        )
    ).strip()
    if len(diff) == 0:
        diff = "Formatting differs, but no diff could be generated."
    return f"Formatting issues found in {file_path}:\n{diff}"


def process_cmake_file(file_path: Path, cmake_format_args: Sequence[str], write_files: bool) -> FileResult:
    # Check mode needs formatted stdout; write mode should preserve the caller's flags.
    args_for_run = cmake_format_args if write_files else strip_check_and_write_args(cmake_format_args)
    result = run_cmake_format(file_path, args_for_run)
    if result.returncode != 0:
        return FileResult(False, render_command_error(file_path, result))
    if write_files:
        return FileResult(True, f"Successfully formatted {file_path}.")

    # Return a failure if there is a difference between the current file and cmake-format output
    original_contents = file_path.read_text()
    formatted_contents = result.stdout
    if original_contents != formatted_contents:
        return FileResult(False, render_diff(file_path, original_contents, formatted_contents))
    return FileResult(True, f"{file_path} is correctly formatted.")


def find_matching_files(path: Path, pattern: re.Pattern[str]) -> list[Path]:
    return sorted(f for f in path.rglob('*') if f.is_file() and pattern.match(f.name))


def split_cmake_format_args(cmake_format_args: str) -> list[str]:
    return shlex.split(cmake_format_args)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Format CMake files using cmake-format.")
    parser.add_argument('--file-regex', required=True, help="Regex pattern to match filenames.")
    parser.add_argument('--cmake-format-args', default="", help="Additional arguments for cmake-format.")
    args = parser.parse_args(argv)
    if not args.file_regex:
        parser.error("The --file-regex argument cannot be empty.")
    return args


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)

    cmake_format_args = split_cmake_format_args(args.cmake_format_args)
    workspace_path = Path(os.environ['GITHUB_WORKSPACE'])
    files = find_matching_files(workspace_path, re.compile(args.file_regex))

    if len(files) == 0:
        print("No files matched the given regex.")
        return 0

    # Any "write" flag switches the action from linting/checking mode to rewriting mode
    write_files = should_write_files(cmake_format_args)
    results = [process_cmake_file(fp, cmake_format_args, write_files) for fp in files]

    for result in results:
        print(result.message)

    return int(any(not result.success for result in results))


if __name__ == "__main__":
    raise SystemExit(main())
