import time
from copy import deepcopy
from pathlib import Path
from typing import Tuple

GUARD_CHAR = "^"
BLOCK_CHAR = "#"
NOT_VISITED_CHAR = "."
VISITED_CHAR = "X"
OBSTACLE_CHAR = "O"


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
        return deepcopy(self.map)

    def add_obstacle(self, pos):
        self.map[pos[0]][pos[1]] = OBSTACLE_CHAR

    def find_starting_pos(self):
        for i, row in enumerate(self.map):
            if GUARD_CHAR in row:
                pos = (i, row.index(GUARD_CHAR))
        return pos


class Guard:
    def __init__(self, area_map, start_pos=None):
        self.direction = (-1, 0)
        self.guard_icon = GUARD_CHAR
        self.area_map = area_map
        self.area_map_matrix = area_map.get_map()
        if start_pos:
            self.start_pos = start_pos
        else:
            self.start_pos: Tuple = self.area_map.find_starting_pos()
        self.pos = self.start_pos
        self.visited_locations = []
        self.mark_visited_location()
        self.steps = 0
        self.loop_detected = False
        self.invalid_obstacle_detected = False

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
        if self.area_map_matrix[next_pos[0]][next_pos[1]] in (BLOCK_CHAR, OBSTACLE_CHAR):
            return True
        return False

    def is_next_position_edge(self):
        next_pos = self.get_next_pos()
        if 0 <= next_pos[0] < len(self.area_map_matrix) and 0 <= next_pos[1] < len(self.area_map_matrix[0]):
            return False
        return True

    def mark_visited_location(self):
        for location in self.visited_locations:
            if self.pos == location[0]:
                # if the guard walks the same position and direction twice, he's in a loop
                if self.direction == location[1]:
                    self.loop_detected = True
                    break
                # if the guard hits an obstacle that makes him walk the opposite direction, the obstacle is invalid
                elif (-self.direction[0], -self.direction[1]) == location[1]:
                    self.invalid_obstacle_detected = True
                    break
        else:
            self.visited_locations.append((self.pos, self.direction))
            return

    def move_next(self):
        self.pos = self.get_next_pos()
        self.mark_visited_location()
        self.steps += 1
        return self.pos

    def patrol(self):
        while True:
            while self.is_next_position_blocked():
                self.change_direction()
            _ = self.move_next()
            if self.is_next_position_edge() or self.loop_detected or self.invalid_obstacle_detected:
                return None


def main():
    start_time = time.time()
    area_map = Map()
    guard = Guard(area_map)

    # Complete a first run to discover the path the guard completed
    guard.patrol()

    successful_obstacles = 0
    obstacle_locations = {location[0] for location in guard.visited_locations}
    print(len(obstacle_locations))
    for location in obstacle_locations:
        area_map.reset_walked_path()
        area_map.add_obstacle(location)
        new_guard = Guard(area_map, guard.start_pos)
        new_guard.patrol()
        if new_guard.loop_detected:
            successful_obstacles += 1

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
