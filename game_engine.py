from enum import Enum

class Direction(Enum):
    UP = 0
    UPRIGHT = 1
    RIGHT = 2
    DOWNRIGHT = 3
    DOWN = 4
    DOWNLEFT = 5
    LEFT = 6
    UPLEFT = 7
    
class Ability(Enum):
    TELEPORT = 0
    ZAP = 1