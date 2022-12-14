# ---------------------------------------------------------------------#
# Written by : Christopher Perreault
# Updated by : Grainus
# Date : 2022-09-25
# Updated: 2022-10-01
# Description : This is the main file for the game's grid logic. 
#               It creates the grid, do the unit's movements, etc.
# Version : 0.5.0
# Contains :
#   - The grid class
#   - The grid's methods
#   - The grid's functions
#   - Logic for the movement of the units
# ---------------------------------------------------------------------#

from random import randint, choice
from math import dist
from models import Difficulty, Doctor, Dalek, Junk, Direction, Ability
from typing import Type, Generator
import settings

Pos = tuple[int, int]
CellType = Doctor | Dalek | Junk | None

class GameGrid:
    def __init__(self, width: int = settings.DEFAULT_WIDTH, 
            height: int = settings.DEFAULT_HEIGHT):
        self.width = width
        self.height = height
        self.cells: list[list[CellType]] = []
        self.turn = 0
        self.create_grid()

    def create_grid(self) -> None:
        self.cells = [
            [None for _ in range(self.width)]
                for _ in range(self.height)
        ]

    def flatten(self) -> Generator[CellType, None, None]:
        for lst in self.cells:
            for cell in lst:
                yield cell

    def cell_at(self, pos: Pos) -> CellType:
        return self.cells[pos[0]][pos[1]]

    def summon_daleks(self, dalek_count: int) -> None:
        """Summon the daleks on the grid, \
            depending on how many were asked.

            If there are not enough empty spaces, fill the grid instead.
        """
        if (max_ := sum(1 for c in self.flatten() if not c)) < dalek_count:
            dalek_count = max_

        simplerand = lambda val: randint(0, val - 1)
        for _ in range(dalek_count):
            while True: # do ... while
                x, y = simplerand(self.height), simplerand(self.width)
                if self.cells[x][y] is None:
                    break
            self.cells[x][y] = Dalek()

    def summon_doctor(self, zap_count: int = settings.DEFAULT_ZAP) -> Doctor:
        """Summon the doctor on the grid"""
        x, y = randint(0, self.height - 1), randint(0, self.width - 1)
        doc = Doctor(zap_count)
        self.cells[x][y] = doc
        return doc

    def find_pos(self, 
                obj_type: Type[Doctor] | Type[Dalek] | Type[Junk]
        ) -> Pos | None:
        """Find the position of the object given"""
        for i in range(self.height):
            for k in range(self.width):
                if isinstance(self.cells[i][k],obj_type):
                    return (i, k)
        return None
    
    def is_inside(self, pos: Pos) -> bool:
        return 0 <= pos[0] < self.height and 0 <= pos[1] < self.width

    def find_doctor(self) -> Pos | None:
        """Find the doctor on the grid using find_pos, shortcut."""
        return self.find_pos(Doctor)
    
    def can_die_next(self) -> bool:
        """Return if a dalek is in position to kill the doctor next turn
        if he doesn't move.
        """
        docpos = self.find_doctor()
        return dist(
            docpos, # type: ignore
            self.find_closest_dalek(docpos) # type: ignore
        ) <= 1.5

    def junk_at(self, pos: Pos) -> None:
        """Converts the selected cell to junk, no matter what is on it.
        """
        self.cells[pos[0]][pos[1]] = Junk()

    def kill_at(self, pos: Pos) -> None:
        """Removes any object from the grid at the given position."""
        self.cells[pos[0]][pos[1]] = None

    def make_move(self, _from: Pos, to: Pos) -> None:
        """Move the object from the move_from position to the move_to position"""
        self.cells[to[0]][to[1]] = self.cell_at(_from)
        self.cells[_from[0]][_from[1]] = None

    def request_move(self, move: Direction | Ability) -> bool:
        """Get the move from the user, validates it and then makes \
            the move if and only if it was validated.
        Then return if the move was valid or not.
        """
        if isinstance(move, Ability):
            return True
        pos = self.find_doctor()
        if pos is not None and self.validate_move(pos, move):
            newPos = self.new_pos(pos, move)
            if self.cell_at(newPos) is None:
                self.make_move(pos, newPos)
            return True
        return False

    def validate_move(self, pos: Pos, request: Direction) -> bool:
        """Validate a move requested by the user."""
        return self.is_inside(self.new_pos(pos, request))

    def dalek_direction_to_doctor(self, distance: Pos) -> Direction:
        """Get the direction to the doctor from the distance between \
            the dalek and the doctor"""
        if distance[0] > 0:
            direction = 'DOWN'
            if distance[1] > 0:
                direction += 'RIGHT'
            elif distance[1] < 0:
                direction += 'LEFT'
        elif distance[0] < 0:
            direction = 'UP'
            if distance[1] > 0:
                direction += 'RIGHT'
            elif distance[1] < 0:
                direction += 'LEFT'

        else:
            if distance[1] > 0:
                direction = 'RIGHT'
            elif distance[1] < 0:
                direction = 'LEFT'
            else:
                direction = 'NONE'
        return Direction[direction]

    def new_pos(self, pos: Pos, direction: Direction) -> Pos:
        if direction == Direction.UP:
            return (pos[0] - 1, pos[1])
        elif direction == Direction.UPRIGHT:
            return (pos[0] - 1, pos[1] + 1)
        elif direction == Direction.UPLEFT:
            return (pos[0] - 1, pos[1] - 1)
        elif direction == Direction.DOWN:
            return (pos[0] + 1, pos[1])
        elif direction == Direction.DOWNRIGHT:
            return (pos[0] + 1, pos[1] + 1)
        elif direction == Direction.DOWNLEFT:
            return (pos[0] + 1, pos[1] - 1)
        elif direction == Direction.LEFT:
            return (pos[0], pos[1] - 1)
        elif direction == Direction.RIGHT:
            return (pos[0], pos[1] + 1)
        else:
            return pos
    
    def find_closest_dalek(self, pos: Pos) -> Pos | None:
        daleks = self.get_all_daleks()
        if daleks:
            return min(
                daleks,
                key=lambda p: dist(p, pos)
            )
        return None
    
    def teleport_doctor(self, difficulty: Difficulty) -> None:
        valid_pos = []
        for x, lst in enumerate(self.cells):
            for y, cell in enumerate(lst):
                if isinstance(cell, Junk):
                    continue
                elif (isinstance(cell, Dalek) 
                        and difficulty != Difficulty.HARD):
                    continue
                else:
                    pos: Pos = (x, y)
                    if difficulty == Difficulty.EASY:
                        closest = self.find_closest_dalek(pos)
                        if not closest or dist(pos, closest) > 2:
                            valid_pos.append(pos)
                    else:
                        valid_pos.append(pos)

        if valid_pos:
            pos = choice(valid_pos)
            self.make_move(self.find_doctor(), pos) # type: ignore

    def get_all_daleks(self) -> list[Pos]:
        """Get all the daleks in the grid"""
        daleks = []
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if isinstance(cell, Dalek):
                    daleks.append((i, j))
        return daleks

    def move_all_daleks(self) -> None:
        """Move all the daleks on the grid"""
        posdoctor = self.find_doctor()
        daleks = self.get_all_daleks()
        if daleks and posdoctor:
            daleks.sort(
                key=lambda p: dist(p, posdoctor) # type: ignore
            )
            self.turn += 1
            for dalek in daleks:
                cell = self.cell_at(dalek)
                if isinstance(cell, Dalek) \
                        and cell.move_count < self.turn:
                    self.move_dalek(posdoctor, dalek)

    def move_dalek(self, pos_doctor: Pos, pos_dalek: Pos) -> None:
        # move the dalek on the grid
        distance = (
            pos_doctor[0] - pos_dalek[0],
            pos_doctor[1] - pos_dalek[1]
        )
        direction = self.dalek_direction_to_doctor(distance)
        if self.validate_move(pos_dalek, direction):
            new_pos = self.new_pos(pos_dalek, direction)
            cell = self.cell_at(new_pos)
            if isinstance(cell, Dalek):
                if cell.move_count < self.turn:
                    self.move_dalek(pos_doctor, new_pos)
                else:
                    self.kill_at(pos_dalek)
                    self.junk_at(new_pos)
            elif isinstance(cell, Junk):
                self.kill_at(pos_dalek)
            else:
                self.make_move(pos_dalek, new_pos)
                self.cell_at(new_pos).move_count = self.turn # type: ignore
