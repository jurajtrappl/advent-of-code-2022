import os

class InputParser():
    @staticmethod
    def parse_input(filename, map_f=str):
        with open(f'inputs/{filename}', 'r') as f:
            content = f.read()
            splitted_by_empty_lines = content.split(os.linesep + os.linesep)
            raw_calories_blocks = list(map(lambda block: block.split(os.linesep), splitted_by_empty_lines))
            return list(map(lambda block: list(map(map_f, block)), raw_calories_blocks))