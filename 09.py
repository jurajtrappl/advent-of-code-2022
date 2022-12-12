from dataclasses import dataclass
from enum import Enum
from functools import reduce
import math


class Direction(Enum):
    R = (1, 0)
    D = (0, -1)
    L = (-1, 0)
    U = (0, 1)


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, other: 'Position') -> 'Position':
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __hash__(self) -> int:
        return hash(self.x) + hash(self.y)


def parse_input():
    def get_head_movement(command_line: str) -> list[Position]:
        direction, n_steps = command_line.split()
        return [Position(*Direction[direction].value)] * int(n_steps)

    with open('inputs/09.in', 'r') as f:
        return reduce(list.__add__, list(map(get_head_movement, f.read().splitlines())))


def is_head_far(head: Position, tail: Position) -> bool:
    dx, dy = abs(tail.x - head.x), abs(tail.y - head.y)
    return not (0 <= dx <= 1 and 0 <= dy <= 1)


def move(direction: Position) -> Position:
    new_x, new_y = direction.x / 2, direction.y / 2
    new_x = math.ceil(new_x) if new_x > 0 else math.floor(new_x)
    new_y = math.ceil(new_y) if new_y > 0 else math.floor(new_y)
    return Position(new_x, new_y)


def model_head_positions():
    head_moves, head_pos = parse_input(), Position(0, 0)
    return [head_pos := head_pos + move for move in head_moves]


def model_knots_positions(tail_length: int) -> int:
    rope_parts_positions = [Position(0, 0)] * (tail_length + 1)
    tail_visited_positions = set()
    for head_position in model_head_positions():
        rope_parts_positions[0] = head_position

        for i in range(1, tail_length + 1):
            if is_head_far(head := rope_parts_positions[i - 1], tail := rope_parts_positions[i]):
                rope_parts_positions[i] += move(direction=head - tail)

        tail_visited_positions.add(rope_parts_positions[-1])

    tail_visited_positions.add(rope_parts_positions[-1])
    return len(tail_visited_positions)


print(model_knots_positions(tail_length=1))
print(model_knots_positions(tail_length=9))
