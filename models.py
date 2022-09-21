# Placeholder classes

from typing import Iterable, Type

class NotImplementedClass:
    def __init__(self):
        raise NotImplementedError

class Doctor(NotImplementedClass):
    pass

class Dalek(NotImplementedClass):
    pass


class Turn:
    def __init__(self, turns: Iterable[Type]):
        self.turns = turns
        self.indx = -1
  
    def __iter__(self):
        return self

    def __next__(self):
        self.indx += 1
        self.indx = self.indx % len(self.turns)
        return self.turns[self.indx]

    def current(self):
        return self.turns[self.indx]