from pathlib import Path


def load_input():
    with open(Path(__file__).parent / "input.txt", "r") as file:
        return file.read().strip()


def process_input(input):
    return input[::2], input[1::2]


def expand_input(input):
    filesystem = []
    file_indices = []
    free_space_indices = []
    file_id = 0
    index = 0
    for i in range(len(input)):
        if i % 2 == 0:
            file_length = int(input[i])
            if file_length > 0:
                file_indices += list(range(index, index + file_length))
            filesystem += [file_id] * file_length
            file_id += 1
            index += file_length
        else:
            free_space_size = int(input[i])
            if free_space_size > 0:
                free_space_indices += list(range(index, index + free_space_size))
            filesystem += [None] * free_space_size
            index += free_space_size
    return filesystem, file_indices, free_space_indices


def fragment(filesystem, file_indices, free_space_indices):
    for i in range(len(free_space_indices)):
        free_space_index = free_space_indices[i]
        file_index = file_indices[-i - 1]
        if free_space_index > file_index:
            break
        # print(f"Swapping file block at {file_index} with free space at {free_space_index}")
        filesystem[free_space_index], filesystem[file_index] = (
            filesystem[file_index],
            filesystem[free_space_index],
        )
    return filesystem


def calc_checksum(filesystem):
    checksum = 0
    for i, f in enumerate(filesystem):
        if f:
            checksum += f * i
    return checksum


def main():
    input = load_input()
    filesystem, file_indices, free_space_indices = expand_input(input)
    defragged_filesystem = fragment(filesystem, file_indices, free_space_indices)
    checksum = calc_checksum(defragged_filesystem)
    print(checksum)


if __name__ == "__main__":
    main()
