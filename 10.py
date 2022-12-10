from dataclasses import dataclass
from typing import ClassVar, Optional

class Memory:
    """
    Base CPU memory class tracking one register and tact count.
    """
    def __init__(self):
        self.tact, self.register = 0, 1

    def add_to_register(self, value: int) -> None:
        self.register += value

    def increment_tact(self) -> None:
        self.tact += 1

class FirstPartMemory(Memory):
    """
    Memory class extension for the first part. Calculates interesting signals.
    """
    def __init__(self):
        super().__init__()

        self.thresholds = list(range(20, 220 + 1, 40))
        self.interesting_signal_strengths = []

    def try_mark_interesting_signal(self):
        if self.tact in self.thresholds:
            self.interesting_signal_strengths.append(self.register * self.tact)

    def increment_tact(self) -> None:
        super().increment_tact()
        self.try_mark_interesting_signal()

class SecondPartMemory(Memory):
    """
    Memory class extension for the second part. Draws sprite positions.
    """
    def __init__(self):
        super().__init__()

        self.crt = []
    
    def draw_sprite(self):
        self.crt.append('#' if abs((self.register + 1) - (self.tact % 40)) <= 1 else '.')

    def increment_tact(self) -> None:
        super().increment_tact()
        self.draw_sprite()

@dataclass
class Instruction:
    """
    Base CPU instruction class.
    """
    n_cycles: ClassVar[int]
    value: Optional[int] = None

    def execute(self, mem: Memory):
        for _ in range(self.n_cycles):
            mem.increment_tact()

@dataclass
class Addx(Instruction):
    """
    CPU instruction that adds to memory register X.
    """
    n_cycles = 2

    def execute(self, mem: Memory):
        Instruction.execute(self, mem)
        mem.add_to_register(int(self.value))

@dataclass
class Noop(Instruction):
    """
    CPU instruction that does nothing.
    """
    n_cycles = 1

def CPUInstruction(name, value=None):
    """CPU instructions factory."""
    for cls in Instruction.__subclasses__():
        if cls.__name__.lower() == name:
            return cls(value)

def parse_input() -> list[Instruction]:
    with open('inputs/10.in') as f:
        return list(map(lambda line: CPUInstruction(*line.split()), f.read().splitlines()))

def first_part():
    mem = FirstPartMemory()
    for instruction in instructions:
        instruction.execute(mem)

    return sum(mem.interesting_signal_strengths)

def second_part():
    mem = SecondPartMemory()
    for instruction in instructions:
        instruction.execute(mem)

    return '\n'.join([''.join(mem.crt[i:i + 40]) for i in range(0, 241, 40)])

instructions = parse_input()
print(first_part())
print(second_part())
