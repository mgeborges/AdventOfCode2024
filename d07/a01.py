import math
import threading
from pathlib import Path
from typing import List


def read_input():
    equations = []
    with open(Path(__file__).parent / "input.txt", "r") as f:
        for line in f.readlines():
            result, values = line.split(":")
            values = tuple(map(int, values.strip().split()))
            equations.append((int(result), values))
    return equations


def run_calculations(operands):
    if len(operands) == 2:
        result_1 = operands[0] + operands[1]
        result_2 = operands[0] * operands[1]
        return [result_1] + [result_2]
    results = run_calculations(operands[:-1])
    result_1 = [operands[-1] + res for res in results]
    result_2 = [operands[-1] * res for res in results]
    return result_1 + result_2


def worker(equations, results, idx):
    sum = 0
    for equation in equations:
        results_list = run_calculations(equation[1])
        if equation[0] in (results_list):
            sum += equation[0]
    results[idx] = sum
    return None


def main():
    equations = read_input()
    threads: List[threading.Thread] = []
    num_threads = 16
    num_equations_per_thread = int(math.ceil(len(equations) // num_threads)) + 1
    results = [0] * num_threads
    for i in range(num_threads):
        work_set = equations[i * num_equations_per_thread : (i + 1) * num_equations_per_thread]
        thread = threading.Thread(target=worker, args=(work_set, results, i), name=str(i + 1))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    sum = 0
    for result in results:
        sum += result

    print(sum)


if __name__ == "__main__":
    main()
