"""Placeholder classes to develop components that require them."""

from __future__ import annotations
from collections.abc import Sequence
from enum import Enum

class NotImplementedClass:
    def __init__(self):
        raise NotImplementedError

class Doctor(NotImplementedClass):
    pass

class Dalek(NotImplementedClass):
    pass


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