def parse_input():
    def parse_section_assignment(section_assignment):
        lower_bound, upper_bound = section_assignment.split('-')
        return set(range(int(lower_bound), int(upper_bound) + 1))

    def parse_pair(elf_pair):
        return [parse_section_assignment(elf) for elf in elf_pair.split(',')]

    with open('inputs/4.in', 'r') as f:
        return list(map(parse_pair, f.read().splitlines()))


def first_part(input):
    return sum([fst_elf <= snd_elf or snd_elf <= fst_elf for fst_elf, snd_elf in input])


def second_part(input):
    return sum([fst_elf & snd_elf != set() for fst_elf, snd_elf in input])


input = parse_input()
print(first_part(input))
print(second_part(input))
