from pathlib import Path


def load_stones():
    with open(Path(__file__).parent / "input.txt", "r") as file:
        return list(map(int, file.read().strip().split()))


def rule_one(stone):
    return (True, [1]) if stone == 0 else (False, [stone])


def rule_two(stone):
    if len(str(stone)) % 2 == 0:
        half_stone = len(str(stone)) // 2
        return (True, [int(str(stone)[:half_stone]), int(str(stone)[half_stone:])])
    return (False, [stone])


def blink(stones):
    new_arrangement = []
    for stone in stones:
        rule_one_applied, results = rule_one(stone)
        if rule_one_applied:
            new_arrangement += results
        else:
            rule_two_applied, results = rule_two(stone)
            if rule_two_applied:
                new_arrangement += results
            else:
                new_arrangement += [stone * 2024]
    return new_arrangement


def main():
    stones = load_stones()
    for _ in range(25):
        stones = blink(stones)
    print(stones)
    print(f"After blinking 25 times, the number of stones is {len(stones)}")


if __name__ == "__main__":
    main()
