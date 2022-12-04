from enum import Enum

class HandShape(Enum):
    ROCK = 'A'
    PAPER = 'B'
    SCISSORS = 'C'

class DuelResult(Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6

handshape_scores = { HandShape.ROCK.value: 1, HandShape.PAPER.value: 2, HandShape.SCISSORS.value: 3 }

loss_handshapes = {
    HandShape.ROCK.value: HandShape.SCISSORS.value,
    HandShape.PAPER.value: HandShape.ROCK.value,
    HandShape.SCISSORS.value: HandShape.PAPER.value
}

win_handshapes = dict([(v, k) for k, v in loss_handshapes.items()])

def parse_input():
    with open('inputs/2.in', 'r') as f:
        content = f.read().splitlines()
        splitted = list(map(str.split, content))
        return splitted

def first_part_guide(opponent_handshape: str, my_handshape: str) -> int:
    guide = { 'X': HandShape.ROCK.value, 'Y': HandShape.PAPER.value, 'Z': HandShape.SCISSORS.value }
    handshape_score = handshape_scores[guide[my_handshape]]

    if opponent_handshape == guide[my_handshape]:
        return DuelResult.DRAW.value + handshape_score

    rock_loss = opponent_handshape == HandShape.PAPER.value and guide[my_handshape] == HandShape.ROCK.value
    scissors_loss = opponent_handshape == HandShape.ROCK.value and guide[my_handshape] == HandShape.SCISSORS.value
    paper_loss = opponent_handshape == HandShape.SCISSORS.value and guide[my_handshape] == HandShape.PAPER.value
    if rock_loss or scissors_loss or paper_loss:
        return DuelResult.LOSS.value + handshape_score

    return DuelResult.WIN.value + handshape_score

def second_part_guide(opponent_handshape: str, desired_outcome: str) -> int:
    guide = { 'X': DuelResult.LOSS, 'Y': DuelResult.DRAW, 'Z': DuelResult.WIN }

    score = guide[desired_outcome].value
    if guide[desired_outcome] == DuelResult.LOSS:
        score += handshape_scores[loss_handshapes[opponent_handshape]]
    
    if guide[desired_outcome] == DuelResult.DRAW:
        score += handshape_scores[opponent_handshape]

    if guide[desired_outcome] == DuelResult.WIN:
        score += handshape_scores[win_handshapes[opponent_handshape]]

    return score

def first_part(tournament):
    return sum([first_part_guide(opponent_handshape, my_handshape) for opponent_handshape, my_handshape in tournament])

def second_part(tournament):
    return sum([second_part_guide(opponent_handshape, desired_outcome) for opponent_handshape, desired_outcome in tournament])

input = parse_input()
print(first_part(input))
print(second_part(input))