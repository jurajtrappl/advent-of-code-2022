from collections import deque
from dataclasses import dataclass
import math
import os
import re
from typing import Callable


@dataclass
class Monkey:
    items: deque[int]
    operation: Callable[[int], int]
    test_condition: int
    where_to_throw: dict[bool, int]

    def catch(self, item: int) -> None:
        self.items.append(item)

    def throw(self, inspected_worries_levels: deque[int], monkeys: list['Monkey']) -> None:
        while inspected_worries_levels:
            worry_level = inspected_worries_levels.popleft()
            division_test_result = self.__division_test(worry_level)
            monkey_recipient_i = self.where_to_throw[division_test_result]

            monkeys[monkey_recipient_i].catch(worry_level)

    def __division_test(self, item_worry_level: int) -> bool:
        return item_worry_level % self.test_condition == 0


def inspect_monkey_items(monkey: Monkey, lcm_modulo: int, relief_factor: int) -> int:
    worry_levels = deque()
    while monkey.items:
        item = monkey.items.popleft()
        worry_levels.append(
            (monkey.operation(item) // relief_factor) % lcm_modulo)

    return worry_levels


class KeepAway:
    def __init__(self, monkeys: list[Monkey]):
        self.monkeys = monkeys
        self.inspected = [0] * len(monkeys)

    def play_round(self, lcm_modulo: int, relief_factor: int):
        for i, m in enumerate(self.monkeys):
            worries_levels = inspect_monkey_items(m, lcm_modulo, relief_factor)
            self.inspected[i] += len(worries_levels)

            m.throw(worries_levels, self.monkeys)

    def play_game(self, n_rounds: int, relief_factor: int):
        lcm_modulo = math.prod([m.test_condition for m in self.monkeys])

        for _ in range(1, n_rounds + 1):
            self.play_round(lcm_modulo, relief_factor)


def parse_input():
    def get_numbers(value: str) -> list[int]:
        return list(map(int, re.findall('\d+', value)))

    def parse_monkey(block: str) -> Monkey:
        raw_worry_lvls, raw_op, raw_div_by, raw_true, raw_false = block.split(os.linesep)[1:]

        worry_levels = deque(get_numbers(raw_worry_lvls))
        def op(old): return eval(raw_op.split('=')[1], {'old': old})
        test_condition = get_numbers(raw_div_by)[0]
        if_true_monkey_i, if_false_monkey_i = get_numbers(
            raw_true)[0], get_numbers(raw_false)[0]

        return Monkey(worry_levels, op, test_condition, {True: if_true_monkey_i, False: if_false_monkey_i})

    with open('inputs/11.in', 'r') as f:
        return list(map(parse_monkey, f.read().split(os.linesep + os.linesep)))


def simulate(monkeys: list[Monkey], n_rounds: int, relief_factor: int) -> int:
    game = KeepAway(monkeys)
    game.play_game(n_rounds, relief_factor)

    inspected_items = sorted(game.inspected)
    return inspected_items[-2] * inspected_items[-1]


print(simulate(parse_input(), n_rounds=20, relief_factor=3))
print(simulate(parse_input(), n_rounds=10000, relief_factor=1))
