import numpy as np


def parse_input():
    with open('inputs/08.in', 'r') as f:
        return np.array([list(map(int, list(line))) for line in f.read().splitlines()])


trees_patch = parse_input()
N = trees_patch.shape[0]


def neighbours(row, col):
    left, right = trees_patch[row][:col], trees_patch[row][col + 1:]
    top, bottom = trees_patch[:, col][:row], trees_patch[:, col][row + 1:]

    return [list(reversed(left)), right, list(reversed(top)), bottom]


def is_tree_visible(row, col):
    left_max, right_max, top_max, bottom_max = list(
        map(max, neighbours(row, col)))

    tree_height = trees_patch[row][col]
    return tree_height > left_max or tree_height > right_max or tree_height > top_max or tree_height > bottom_max


def scenic_score(row, col):
    def view_distance(tree_row, tree_height):
        for distance, tree_height_in_view in enumerate(tree_row):
            if tree_height_in_view >= tree_height:
                return distance + 1

        return len(tree_row)

    return np.prod(list(map(lambda direction: view_distance(direction, trees_patch[row][col]), neighbours(row, col))))


def first_part():
    border_trees_count = 4 * N - 4
    interior_visible_count = np.sum(
        [[is_tree_visible(row, col) for col in range(1, N - 1)] for row in range(1, N - 1)])

    return border_trees_count + interior_visible_count


def second_part():
    return np.max([[scenic_score(row, col) for col in range(1, N - 1)] for row in range(1, N - 1)])


print(first_part())
print(second_part())
