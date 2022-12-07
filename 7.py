from collections import deque
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from typing import Optional

ROOT_DIR, PARENT_DIR = '/', '..'
CMD_START, DIR_START = '$', 'dir'
FIRST_PART_AT_MOST_SPACE, TOTAL_SPACE, UPDATE_SPACE = 10e4, 70e6, 30e6

class CommandName(Enum):
    CHANGE_DIR = 'cd'
    LIST = 'ls'

@dataclass
class Node:
    name: str
    content: list['Node'] = field(default_factory=list)
    parent: 'Node' = None

@dataclass
class Directory(Node):
    """
    Class for keeping track of a directory.
    """

@dataclass
class File(Node):
    """
    Class for keeping track of a file.
    """
    size: int = 0

@dataclass(init=False)
class Command:
    """
    Class for keeping track of a command and its output together.
    """
    name: str
    arg: Optional[str]
    output: list[Directory | File] = field(default_factory=list)

    def __init__(self, cmd_line: str):
        self.output, self.arg = [], None

        parts = cmd_line.split()[1:]
        self.name = parts[0]
        
        if len(parts) == 2:
            self.arg = parts[1]

    def add(self, output_line: str) -> None:
        parts = output_line.split()
        self.output.append(Directory(parts[1]) if parts[0] == DIR_START else File(name=parts[1], size=int(parts[0])))

FileSystem = list[Node]
Program = list[Command]

def parse_input() -> Program:
    def parse_program(content) -> Program:
        """
        Returns a collection of commands with their output together.
        """
        commands = []
        for line in content:
            if line.startswith(CMD_START):
                commands.append(Command(line))
            else:
                commands[-1].add(line)
        
        return commands

    with open('inputs/7.in', 'r') as f:
        return parse_program(f.read().splitlines())

def assemble_filesystem(program: Program) -> FileSystem:
    """
    Returns an adjacency list of a graph representing ownership of directories and files.
    """
    root_dir = Directory(name=ROOT_DIR)
    dirs, current_dir = [root_dir], root_dir
    for command in program[1:]:
        if command.name == CommandName.LIST.value:
            for o in command.output:
                current_dir.content.append(o)
                o.parent = current_dir

                if isinstance(o, Directory):
                    dirs.append(o)
        
        if command.name == CommandName.CHANGE_DIR.value:
            if command.arg == PARENT_DIR:
                current_dir = current_dir.parent
            else:
                new_dir = [child_dir for child_dir in current_dir.content if child_dir.name == command.arg][0]
                current_dir = new_dir

    return dirs

def calculate_dir_size(dir): 
    """
    Performs BFS without checking for already seen nodes because it is a tree-like structure.
    """
    q, size = deque([dir]), 0
    while q:
        current_dir = q.pop()

        child_files = filter(lambda item: isinstance(item, File), current_dir.content)
        size += sum([f.size for f in child_files])
        
        child_dirs = list(filter(lambda item: isinstance(item, Directory), current_dir.content))
        q.extend(child_dirs)

    return size

def first_part(sizes):
    return sum(sizes[sizes <= FIRST_PART_AT_MOST_SPACE])

def second_part(sizes):
    unused_space = TOTAL_SPACE - sizes[-1]  # the last one is root dir
    space_to_delete = UPDATE_SPACE - unused_space

    return sizes[np.argmax(sizes >= space_to_delete)]

program = parse_input()
fs = assemble_filesystem(program)
sizes = np.sort(np.array([calculate_dir_size(dir) for dir in fs]))

print(first_part(sizes))
print(second_part(sizes))