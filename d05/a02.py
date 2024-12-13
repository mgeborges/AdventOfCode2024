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


def count_dependency_frequency(book, rule_book):
    frequency = {page: 0 for page in book}
    for page in book:
        all_other_pages = list(book).copy()
        all_other_pages.remove(page)
        for other_page in all_other_pages:
            if page in rule_book[other_page]:
                frequency[page] += 1
    return frequency


def are_pages_well_ordered(book, rule_book):
    for i in range(len(book) - 1):
        if book[i + 1] not in rule_book.keys():
            return False, f"Page {book[i + 1]} has no dependent pages in the rule book"
        for j in book[i + 1 :]:
            if book[i] not in rule_book[j]:
                return False, f"Page {book[i]} cannot precede page {j}"
    return True, ""


def fix_ordering(book, rule_book):
    frequencies = count_dependency_frequency(book, rule_book)
    ordered_frequencies = dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True))
    return tuple(ordered_frequencies.keys())


def main():
    rules, books = read_input()
    rule_book = build_rule_book(rules)
    sum_middle_pages = 0
    for book in books:
        ordered, _ = are_pages_well_ordered(book, rule_book)
        if not ordered:
            fixed_book = fix_ordering(book, rule_book)
            ordered, reason = are_pages_well_ordered(fixed_book, rule_book)
            if not ordered:
                print(f"{fixed_book} still has ordering issues: {reason}")
            sum_middle_pages += fixed_book[len(fixed_book) // 2]
    print(f"Sum of the middle pages = {sum_middle_pages}")


if __name__ == "__main__":
    main()
