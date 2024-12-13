import re
from pathlib import Path

PATTERN = r"mul\((\d{1,3}),(\d{1,3})\)|don?\'?t?\(\)"
compiled_pattern = re.compile(PATTERN)

with open(Path(__file__).parent / "input.txt", "r") as f:
    sum = 0
    for line in f.readlines():
        for match in compiled_pattern.finditer(line):
            sum += int(match.group(1)) * int(match.group(2))

print(sum)

PATTERN = r"mul\((\d{1,3}),(\d{1,3})\)"
compiled_pattern = re.compile(PATTERN)

with open(Path(__file__).parent / "input.txt", "r") as f:
    sum = 0
    enabled = True
    for line in f.readlines():
        for match in compiled_pattern.finditer(line):
            if match.group(0) == "do()":
                enabled = True
            elif match.group(0) == r"don't()":
                enabled = False
            else:
                if enabled:
                    sum += int(match.group(1)) * int(match.group(2))

print(sum)
