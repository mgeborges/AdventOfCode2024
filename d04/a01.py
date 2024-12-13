from pathlib import Path

XMAS = "XMAS"


def check_horizontal(line):
    count_hits = 0
    for index in range(len(line) - len(XMAS) + 1):
        snippet = line[index : index + len(XMAS)]
        if "".join(snippet) in (XMAS, XMAS[::-1]):
            count_hits += 1
    return count_hits


def check_vertical_diagonals(crosswords):
    count_hits = 0
    for i in range(len(crosswords) - len(XMAS) + 1):
        for j in range(len(crosswords[0])):
            # Check verticals
            vertical_snippet = "".join([crosswords[idx][j] for idx in range(i, i + (len(XMAS)))])
            if "".join(vertical_snippet) in (XMAS, XMAS[::-1]):
                count_hits += 1

            # Check diagonals
            if j <= len(crosswords[i]) - len(XMAS):
                forward_diagonal_snippet = "".join([crosswords[i + idx][j + idx] for idx in range(len(XMAS))])
                if "".join(forward_diagonal_snippet) in (XMAS, XMAS[::-1]):
                    count_hits += 1
            if j >= len(XMAS) - 1:
                reverse_diagonal_snippet = "".join([crosswords[i + idx][j - idx] for idx in range(len(XMAS))])
                if "".join(reverse_diagonal_snippet) in (XMAS, XMAS[::-1]):
                    count_hits += 1
    return count_hits


with open(Path(__file__).parent / "input.txt", "r") as f:
    board = []
    for line in f.readlines():
        board.append(list(line.strip()))

hits = 0
for line in board:
    hits += check_horizontal(line)
hits += check_vertical_diagonals(board)

print(hits)
