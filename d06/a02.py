import time
from pathlib import Path
from typing import Tuple

GUARD_CHAR = "^"
BLOCK_CHAR = "#"


class Map:
    def __init__(self):
        self.blocks = []
        self.size = None
        self.map = self.load_map()
        self.blocks, self.starting_pos = self.find_landmarks()
        self.size = (len(self.map), len(self.map[0]))
        self.obstacle_pos = None

    def load_map(self):
        with open(Path(__file__).parent / "input.txt", "r") as f:
            return [line.strip() for line in f.readlines()]

    def find_landmarks(self):
        blocks = []
        starting_pos = None
        for line_number, line in enumerate(self.map):
            line_index = line.find(BLOCK_CHAR)
            while line_index != -1:
                blocks.append((line_number, line_index))
                line_index = line.find(BLOCK_CHAR, line_index + 1)
            line_index = line.find(GUARD_CHAR)
            if line_index != -1:
                starting_pos = (line_number, line_index)
        return blocks, starting_pos

    def get_barriers(self):
        return self.blocks + [self.obstacle_pos]

    def find_starting_pos(self):
        for i, row in enumerate(self.map):
            if GUARD_CHAR in row:
                pos = (i, row.index(GUARD_CHAR))
        return pos


class Guard:
    def __init__(self, area_map, start_pos=None, start_direction=None):
        self.area_map = area_map
        if start_pos:
            self.start_pos = start_pos
        else:
            self.start_pos: Tuple = self.area_map.find_starting_pos()
        self.direction = start_direction if start_direction else (-1, 0)
        self.reset()

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

    def is_position_blocked(self, pos):
        if pos in self.area_map.get_barriers():
            return True
        return False

    def is_position_edge(self, pos):
        if 0 <= pos[0] < self.area_map.size[0] and 0 <= pos[1] < self.area_map.size[1]:
            return False
        return True

    def is_loop_detected(self):
        # if the guard walks the same position and direction twice, he's in a loop
        return True if (self.pos, self.direction) in self.visited_locations else False

    def move_next(self):
        self.visited_locations.append((self.pos, self.direction))
        next_pos = self.get_next_pos()
        while self.is_position_blocked(next_pos):
            self.change_direction()
            self.visited_locations.append((self.pos, self.direction))
            next_pos = self.get_next_pos()
        # print(f"Guard at location {self.pos}. Moving to {next_pos}")
        self.pos = next_pos
        self.steps += 1
        return self.pos

    def patrol(self):
        pos = self.move_next()
        while not self.is_position_edge(pos) and not self.is_loop_detected():
            pos = self.move_next()

    def reset(self):
        self.visited_locations = []
        self.pos = self.start_pos
        self.steps = 0
        self.loop_detected = False
        self.direction = (-1, 0)

    def set_pos_and_direction(self, pos, direction):
        self.pos = pos
        self.direction = direction


def main():
    # start_time = time.time()
    area_map = Map()
    guard = Guard(area_map)
    # Complete a first run to discover the path the guard completed
    guard.patrol()
    successful_obstacles = 0

    # All locations except the starting position should be tested
    obstacle_locations = []
    for location in guard.visited_locations:
        if location[0] not in obstacle_locations and location[0] != guard.start_pos:
            obstacle_locations.append(location[0])
    start_time = time.time()
    for location in obstacle_locations:
        # print("######### Starting a new map ############")
        area_map.obstacle_pos = location
        guard.reset()
        guard.patrol()
        if guard.is_loop_detected():
            # print("Loop detected!!!")
            successful_obstacles += 1
    print(f"Successfully placed an obstacle at {successful_obstacles} different locations")
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
