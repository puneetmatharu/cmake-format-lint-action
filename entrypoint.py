#!/bin/python3

import os
import argparse
import re
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-regex')
    parser.add_argument('--cmake-format-args')
    args = parser.parse_args()

    regex = re.compile(rf"{args.file_regex}")

    for root, dirs, files in os.walk(os.environ['GITHUB_WORKSPACE']):
      for file in files:
        if re.match(regex,file):
           cmake_format_return = subprocess.run(["cmake-format", f"{args.cmake_format_args}",f"{os.path.join(root,file)}"],capture_output=True, text=True)
           if cmake_format_return.returncode != 0:
               print(cmake_format_return.stderr)
