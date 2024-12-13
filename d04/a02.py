from pathlib import Path

MAS = "MAS"

with open(Path(__file__).parent / "input.txt", "r") as f:
    board = []
    for line in f.readlines():
        board.append(list(line.strip()))

hits = 0
for i in range(1, len(board) - 1):
    for j in range(1, len(board[i]) - 1):
        if board[i][j] != "A":
            continue

        forward_cross = "".join([board[i - 1][j - 1], board[i][j], board[i + 1][j + 1]])
        reverse_cross = "".join([board[i - 1][j + 1], board[i][j], board[i + 1][j - 1]])
        if forward_cross in (MAS, MAS[::-1]) and reverse_cross in (MAS, MAS[::-1]):
            hits += 1

print(hits)
