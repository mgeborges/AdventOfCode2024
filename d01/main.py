i1, i2 = [], []
d = 0
with open("input.txt", "r") as f:
    for line in f.readlines():
        numbers = line.split()
        i1.append(int(numbers[0]))
        i2.append(int(numbers[1]))
i1.sort()
i2.sort()
for i in range(len(i1)):
    d += abs(i2[i] - i1[i])
print(f"Distance={d}")

similarity_score = 0
for i in i1:
    similarity_score += i * i2.count(i)
print(f"Similarity score={similarity_score}")
