from pathlib import Path


def read_input():
    rules = []
    books = []
    with open(Path(__file__).parent / "input.txt", "r") as f:
        for line in f.readlines():
            if line.find("|") != -1:
                pages = tuple(map(int, line.strip().split("|")))
                rules.append(pages)
            if line.find(",") != -1:
                books.append(tuple(map(int, line.strip().split(","))))
    return rules, books


def build_rule_book(rules):
    rule_book = {}
    for first_page, second_page in rules:
        if rule_book.get(second_page, None) is None:
            rule_book[second_page] = []
        rule_book[second_page].append(first_page)
    return rule_book


def are_pages_well_ordered(book, rule_book):
    for i in range(len(book) - 1):
        if book[i + 1] not in rule_book.keys():
            return False, f"Page {book[i + 1]} is not found in rule book for page {book[i]}"
        for j in book[i + 1 :]:
            if book[i] not in rule_book[j]:
                return False, f"Page {book[i]} does not precede page {j}"
    return True, ""


def main():
    rules, books = read_input()
    rule_book = build_rule_book(rules)
    sum_middle_pages = 0
    for book in books:
        ordered, reason = are_pages_well_ordered(book, rule_book)
        if not ordered:
            print(f"{book} is not well ordered: {reason}")
        else:
            sum_middle_pages += book[len(book) // 2]
    print(f"Sum of the middle pages = {sum_middle_pages}")


if __name__ == "__main__":
    main()
