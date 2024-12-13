from pathlib import Path
from typing import Tuple

GUARD_CHAR = "^"
BLOCK_CHAR = "#"
NORTH_DIRECTION = "^"
SOUTH_DIRECTION = "v"
EAST_DIRECTION = ">"
WEST_DIRECTION = "<"
NORTH_TO_EAST = "E"
EAST_TO_SOUTH = "C"
SOUTH_TO_WEST = "Z"
WEST_TO_NORTH = "Q"


def is_heading_north(guard_direction):
    return True if guard_direction in (GUARD_CHAR, NORTH_DIRECTION) else False


def is_heading_south(guard_direction):
    return True if guard_direction == SOUTH_DIRECTION else False


def is_heading_east(guard_direction):
    return True if guard_direction == EAST_DIRECTION else False


def is_heading_west(guard_direction):
    return True if guard_direction == WEST_DIRECTION else False


def read_input():
    with open(Path(__file__).parent / "input.txt", "r") as f:
        map = [list(line.strip()) for line in f.readlines()]
    return map


def find_starting_pos(mapped_area) -> Tuple[int, int]:
    for i in range(len(mapped_area)):
        row = mapped_area[i]
        if GUARD_CHAR in row:
            pos = (i, row.index(GUARD_CHAR))
    return pos


def move_north(guard_pos, mapped_area):
    new_guard_pos = None
    for i in range(guard_pos[0], 0, -1):
        if mapped_area[i - 1][guard_pos[1]] != BLOCK_CHAR:
            mapped_area[i][guard_pos[1]] = NORTH_DIRECTION
        else:
            new_guard_pos = i, guard_pos[1]
            mapped_area[new_guard_pos[0]][new_guard_pos[1]] = EAST_DIRECTION
            break
    else:
        mapped_area[0][guard_pos[1]] = NORTH_DIRECTION
    return new_guard_pos


def move_south(guard_pos, mapped_area):
    new_guard_pos = None
    for i in range(guard_pos[0], len(mapped_area) - 1):
        if mapped_area[i + 1][guard_pos[1]] != BLOCK_CHAR:
            mapped_area[i][guard_pos[1]] = SOUTH_DIRECTION
        else:
            new_guard_pos = i, guard_pos[1]
            mapped_area[new_guard_pos[0]][new_guard_pos[1]] = WEST_DIRECTION
            break
    else:
        mapped_area[len(mapped_area) - 1][guard_pos[1]] = SOUTH_DIRECTION
    return new_guard_pos


def move_east(guard_pos, mapped_area):
    new_guard_pos = None
    for i in range(guard_pos[1], len(mapped_area[0]) - 1):
        if mapped_area[guard_pos[0]][i + 1] != BLOCK_CHAR:
            mapped_area[guard_pos[0]][i] = EAST_DIRECTION
        else:
            new_guard_pos = guard_pos[0], i
            mapped_area[new_guard_pos[0]][new_guard_pos[1]] = SOUTH_DIRECTION
            break
    else:
        mapped_area[guard_pos[0]][len(mapped_area) - 1] = EAST_DIRECTION
    return new_guard_pos


def move_west(guard_pos, mapped_area):
    new_guard_pos = None
    for i in range(guard_pos[1], 0, -1):
        if mapped_area[guard_pos[0]][i - 1] != BLOCK_CHAR:
            mapped_area[guard_pos[0]][i] = WEST_DIRECTION
        else:
            new_guard_pos = guard_pos[0], i
            mapped_area[new_guard_pos[0]][new_guard_pos[1]] = NORTH_DIRECTION
            break
    else:
        mapped_area[guard_pos[0]][0] = WEST_DIRECTION
    return new_guard_pos


def move_to_next_block(guard_pos, mapped_area):
    guard_direction = mapped_area[guard_pos[0]][guard_pos[1]]
    new_guard_pos = None
    if is_heading_north(guard_direction):
        new_guard_pos = move_north(guard_pos, mapped_area)
    elif is_heading_south(guard_direction):
        new_guard_pos = move_south(guard_pos, mapped_area)
    elif is_heading_east(guard_direction):
        new_guard_pos = move_east(guard_pos, mapped_area)
    elif is_heading_west(guard_direction):
        new_guard_pos = move_west(guard_pos, mapped_area)
    return new_guard_pos


def walk_the_route(mapped_area):
    guard_pos = find_starting_pos(mapped_area)
    while guard_pos is not None:
        guard_pos = move_to_next_block(guard_pos, mapped_area)


def main():
    mapped_area = read_input()
    walk_the_route(mapped_area)
    with open(Path(__file__).parent / "final_mapped_area_2.txt", "w") as f:
        for row in mapped_area:
            f.write("".join(row) + "\n")


if __name__ == "__main__":
    main()
