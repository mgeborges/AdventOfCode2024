from pathlib import Path


def is_safe(sequence, drop_index=None):
    if drop_index is not None:
        sequence.pop(drop_index)
    for i in range(1, len(sequence) - 1):
        diff_prev = sequence[i] - sequence[i - 1]
        diff_next = sequence[i + 1] - sequence[i]
        if not (1 <= abs(diff_prev) <= 3) or not (1 <= abs(diff_next) <= 3):
            if drop_index is None:
                return (
                    is_safe(sequence.copy(), i - 1) or is_safe(sequence.copy(), i) or is_safe(sequence.copy(), i + 1)
                )
            else:
                return False
        elif (diff_prev < 0 and diff_next > 0) or (diff_prev > 0 and diff_next < 0):
            if drop_index is None:
                return (
                    is_safe(sequence.copy(), i - 1) or is_safe(sequence.copy(), i) or is_safe(sequence.copy(), i + 1)
                )
            else:
                return False
    return True


with open(Path(__file__).parent / "input.txt", "r") as f:
    safe_sequences = 0
    for line in f.readlines():
        sequence = list(map(int, line.split()))
        if is_safe(sequence):
            safe_sequences += 1


print(f"Safe sequences = {safe_sequences}")
