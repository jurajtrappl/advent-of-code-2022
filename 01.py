import heapq
import os

def parse_input():
    with open(f'inputs/01.in', 'r') as f:
        content = f.read()
        splitted_by_empty_lines = content.split(os.linesep + os.linesep)
        raw_calories_chunks = list(map(lambda chunk: chunk.split(os.linesep), splitted_by_empty_lines))
        return list(map(lambda block: list(map(int, block)), raw_calories_chunks))


def first_part():
    return -sum(heapq.nsmallest(1, calories_blocks))


def second_part():
    return -sum(heapq.nsmallest(3, calories_blocks))


calories_blocks = []
for block in parse_input():
    heapq.heappush(calories_blocks, -sum(block))

print(first_part())
print(second_part())
