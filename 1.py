import heapq

from input_parser import InputParser

input = InputParser.parse_input('1.in', int)

calories_blocks = []
for block in input:
    heapq.heappush(calories_blocks, (-sum(block), block))

def n_largest_sum(n):
    largest_calories_blocks = heapq.nsmallest(n, calories_blocks)
    return sum([-block_sum for block_sum, _ in largest_calories_blocks])

def first_part():
    return n_largest_sum(1)

def second_part():
    return n_largest_sum(3)

print(first_part())
print(second_part())