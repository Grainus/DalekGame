"""Placeholder classes to develop components that require them."""

from __future__ import annotations
from collections.abc import Sequence
from enum import Enum
from settings import DEFAULT_ZAP

# Characters

class Doctor:
    def __init__(self, zap_count: int = DEFAULT_ZAP):
        self.zap_count = zap_count

    def can_zap(self) -> bool:
        return self.zap_count > 0

class Dalek:
    def __init__(self):
        self.move_count=0

class Junk:
    pass



# Enums

class Direction(Enum):
    UP = 0
    UPRIGHT = 1
    RIGHT = 2
    DOWNRIGHT = 3
    DOWN = 4
    DOWNLEFT = 5
    LEFT = 6
    UPLEFT = 7
    NONE = -1


class Ability(Enum):
    TELEPORT = 0
    ZAP = 1


class Difficulty(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


class PlayMode(Enum):
    NORMAL = 0
    DEBUG = 1


class State(Enum):
    MENU = 0
    PLAY = 1
    TEXTINPUT = 2
    GAMEOVER = 3
    HIGHSCORE = 4



# Custom models

class Turn:
    def __init__(self, turns: Sequence[type]):
        self.turns = turns
        self.indx = 0
  
    def __iter__(self) -> Turn:
        return self

    def __next__(self) -> type:
        turn = self.turns[self.indx]
        self.indx += 1
        self.indx = self.indx % len(self.turns)
        return turn

    def current(self) -> type:
        return self.turns[self.indx]
