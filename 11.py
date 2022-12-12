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
    total_inspected: int = 0

    def catch(self, item: int) -> None:
        self.items.append(item)

    def throw(self, inspected_worries_levels: deque[int], monkeys: list['Monkey']) -> None:
        while inspected_worries_levels:
            worry_level = inspected_worries_levels.popleft()
            monkey_recipient_i = self.where_to_throw[self.__division_test(
                worry_level)]

            monkeys[monkey_recipient_i].catch(worry_level)

    def __division_test(self, item_worry_level: int) -> bool:
        return item_worry_level % self.test_condition == 0

    # def inspect_and_throw(self, monkeys, modulo):
    #     for worry_level in self.worry_levels:
    #         new_worry_level = self.operation(worry_level) % modulo
    #         monkeys[self.where_to_throw[(new_worry_level % self.test_value) == 0]].catch(new_worry_level)

    #     self.total_inspected += len(self.worry_levels)
    #     self.worry_levels = []


def inspect_monkey_items(monkey: Monkey, lcm_modulo: int, relief_factor: int) -> int:
    worry_levels = []
    while monkey.items:
        item = monkey.items.popleft()
        worry_levels.append(
            (monkey.operation(item) // relief_factor) % lcm_modulo)

    return worry_levels


@dataclass
class KeepAway:
    monkeys: list[Monkey]
    inspected: list[int]

    def play_round(self, lcm_modulo: int, relief_factor: int = 3):
        for m in self.monkeys:
            worries_levels = inspect_monkey_items(m, lcm_modulo, relief_factor)
            m.throw(worries_levels, monkeys)

    def play_game(self, n_rounds, relief_factor: int = 3):
        lcm_modulo = math.prod([m.test_condition for m in self.monkeys])

        for _ in range(1, n_rounds + 1):
            self.play_round(lcm_modulo, relief_factor)


def parse_input():
    def get_numbers(value: str) -> list[int]:
        return list(map(int, re.findall('\d+', value)))

    def parse_monkey(block: str) -> Monkey:
        raw_worry_levels, raw_op, raw_divided_by, raw_true_path, raw_false_path = block.split(os.linesep)[
            1:]

        worry_levels = get_numbers(raw_worry_levels)
        def op(old): return eval(raw_op.split('=')[1], {'old': old})
        test_condition = get_numbers(raw_divided_by)[0]
        if_true_monkey_i, if_false_monkey_i = get_numbers(
            raw_true_path)[0], get_numbers(raw_false_path)[0]

        return Monkey(worry_levels, op, test_condition, {True: if_true_monkey_i, False: if_false_monkey_i})

    with open('inputs/11.in', 'r') as f:
        return list(map(parse_monkey, f.read().split(os.linesep + os.linesep)))


monkeys = parse_input()


def simulate_monkeys(n_rounds: int, modulo) -> int:
    for round in range(1, n_rounds + 1):
        for i, m in enumerate(monkeys):
            m.inspect_and_throw(monkeys, modulo)

    return operator.mul(*sorted([m.total_inspected for m in monkeys], reverse=True)[:2])

# def first_part():
#     return simulate_monkeys(20)


def second_part():
    # for m in monkeys:
    #     m.modify_relief(1)
    modulo = math.prod([m.test_value for m in monkeys])
    return simulate_monkeys(10000, modulo)


# print(first_part())
print(second_part())
