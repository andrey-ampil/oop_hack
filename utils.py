from enum import Enum


class Moment(Enum):
    on_hit = 1
    end_round = 2


class Target(Enum):
    me = 1
    enemy = 2  # в конце раунда энеми нет: только на себя или в рандомного
    random = 3
