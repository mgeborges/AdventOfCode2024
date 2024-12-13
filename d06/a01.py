import time
from copy import deepcopy
from pathlib import Path
from typing import Tuple

GUARD_CHAR = "^"
BLOCK_CHAR = "#"
NOT_VISITED_CHAR = "."
VISITED_CHAR = "X"


class Map:
    def __init__(self):
        with open(Path(__file__).parent / "input.txt", "r") as f:
            self.map = [list(line.strip()) for line in f.readlines()]

    def reset_walked_path(self):
        for row in self.map:
            for col in row:
                if col == VISITED_CHAR:
                    col = NOT_VISITED_CHAR

    def get_map(self):
        return self.map


class Guard:
    def __init__(self, area_map):
        self.direction = (-1, 0)
        self.guard_icon = GUARD_CHAR
        self.set_map(area_map)
        self.pos: Tuple = self.find_starting_pos()
        self.visited_locations = 0
        self.mark_visited_location()
        self.steps = 0

    def set_map(self, area_map):
        self.area_map = deepcopy(area_map.get_map())

    def find_starting_pos(self):
        for i, row in enumerate(self.area_map):
            if GUARD_CHAR in row:
                pos = (i, row.index(GUARD_CHAR))
        return pos

    def change_direction(self):
        if self.direction == (-1, 0):
            self.direction = (0, 1)
        elif self.direction == (0, 1):
            self.direction = (1, 0)
        elif self.direction == (1, 0):
            self.direction = (0, -1)
        elif self.direction == (0, -1):
            self.direction = (-1, 0)

    def get_next_pos(self):
        return (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])

    def is_next_position_blocked(self):
        next_pos = self.get_next_pos()
        if self.area_map[next_pos[0]][next_pos[1]] == BLOCK_CHAR:
            return True
        return False

    def is_next_position_edge(self):
        next_pos = self.get_next_pos()
        if 0 <= next_pos[0] < len(self.area_map) and 0 <= next_pos[1] < len(self.area_map[0]):
            return False
        return True

    def mark_visited_location(self):
        if self.area_map[self.pos[0]][self.pos[1]] != VISITED_CHAR:
            self.area_map[self.pos[0]][self.pos[1]] = VISITED_CHAR
            self.visited_locations += 1

    def move_next(self):
        if self.is_next_position_edge():
            return None
        if self.is_next_position_blocked():
            self.change_direction()
        self.pos = self.get_next_pos()
        self.mark_visited_location()
        self.steps += 1
        return self.pos

    def patrol(self):
        while True:
            new_pos = self.move_next()
            if new_pos is None:
                break


def main():
    start_time = time.time()
    area_map = Map()
    guard = Guard(area_map)
    guard.patrol()
    print(f"Total steps taken = {guard.steps}")
    print(f"Total positions visited = {guard.visited_locations}")
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
