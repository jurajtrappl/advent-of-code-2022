import numpy as np


def parse_input():
    with open('inputs/03.in', 'r') as f:
        return f.read().splitlines()


def assign_prio(items):
    def eval_lowercase(item): return ord(item) - 96
    def eval_uppercase(item): return ord(item) - 38

    return sum([eval_lowercase(item) if str.islower(item) else eval_uppercase(item) for item in items])


def first_part(input):
    return sum([assign_prio(set(a) & set(b)) for a, b in map(lambda rucksack: np.array_split(list(rucksack), 2), input)])


def second_part(input):
    return sum([assign_prio(set(a) & set(b) & set(c)) for a, b, c in np.array_split(input, len(input) // 3)])


input = parse_input()
print(first_part(input))
print(second_part(input))
