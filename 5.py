from collections import deque, namedtuple
import numpy as np
import os

NUM_OF_STACKS = 9
CRATES_INDICES = [i for i in range(1, 35, 4)]
CraneCommand = namedtuple('CraneCommand', ['count', 'start', 'end'])


def parse_input():
    def parse_stacks_of_crates(raw_stacks):
        horizontal_stacks = np.array([np.array(
            list(line))[CRATES_INDICES] for line in raw_stacks.split(os.linesep)[:-1]])
        stacks = [deque([crate for crate in horizontal_stacks[:, col]])
                  for col in range(NUM_OF_STACKS)]

        for s in stacks:
            while s[0] == ' ':
                s.popleft()

        return stacks

    def parse_commands(raw_crane_commands):
        commands = raw_crane_commands.split(os.linesep)
        splitted = list(map(str.split, commands))
        return [CraneCommand(int(count), int(start), int(end)) for _, count, _, start, _, end in splitted]

    with open('inputs/5.in', 'r') as f:
        content = f.read()
        raw_crates, raw_crane_commands = content.split(os.linesep + os.linesep)
        return parse_stacks_of_crates(raw_crates), parse_commands(raw_crane_commands)


def first_part(stack_from, stack_to, count):
    stack_to.extendleft([stack_from.popleft() for _ in range(count)])


def second_part(stack_from, stack_to, count):
    stack_to.extendleft(reversed([stack_from.popleft() for _ in range(count)]))


def rearrangement_procedure(input, move_crates_func):
    crates_stacks, commands = input

    for cmd in commands:
        stack_from, stack_to = crates_stacks[cmd.start -
                                             1], crates_stacks[cmd.end - 1]
        move_crates_func(stack_from, stack_to, cmd.count)

    return [stack[0] for stack in crates_stacks]


print(rearrangement_procedure(parse_input(), first_part))
print(rearrangement_procedure(parse_input(), second_part))
