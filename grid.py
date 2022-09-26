# ----------------------------------------------------------------------------------------------------------------------#
# Written by : Christopher Perreault
# Date : 2022-09-25
# Description : This is the main file for the game's grid logic. It will create the grid, do the unit's movements, etc.
# Version : 0.3.9
# Contains :
#   - The grid class
#   - The grid's methods
#   - The grid's functions
#   - Logic for the movement of the units
# ----------------------------------------------------------------------------------------------------------------------#
from random import randint
from models import Dalek, Junk
from doctor import Doctor

class GameGrid:
	def __init__(self, width=8, height=6):
		self.width = width
		self.height = height
		self.grid = []
		self.turn = 0
		self.create_grid()

	def create_grid(self) -> None:
		for i in range(self.height):
			self.grid.append([])  # create a new row
			for k in range(self.width):  # create a new height
				self.grid[i].append(' ')

	def print_grid(self) -> None:
		# DEBUG ONLY -> print the grid
		for i in range(self.height):
			for k in range(self.width):
				if self.grid[i][k] == Doctor:
					print('D', end='/')
				elif self.grid[i][k] == Dalek:
					print('X', end='/')
				elif self.grid[i][k] == Junk:
					print('J', end='/')
				else:
					print(' ', end='/')
			print()

	def summon_daleks(self, dalek_count: int) -> None:
		# summon the daleks on the grid, depending on how many were asked.
		dalek_made = 0
		for i in range(dalek_count):
			x, y = [randint(0, self.height - 1), randint(0, self.width - 1)]
			while self.grid[x][y] == Dalek or self.grid[x][y] == Junk or self.grid[x][y] == Doctor:  # while the cell is a dalek
				x, y = [randint(0, self.height - 1), randint(0, self.width - 1)]  # get a new random position
			self.grid[x][y] = Dalek # summon the dalek

	def summon_doctor(self, zap_count) -> None:
		# summon the doctor on the grid
		# "Do while" which allows to know if the doctor is going to randomly spawn on a dalek, and if so not to.
		x, y = [randint(0, self.height - 1), randint(0, self.width - 1)]  # get a random position
		while self.grid[x][y] == Dalek or self.grid[x][y] == Junk:  # while the cell is a dalek or junk
			x, y = [randint(0, self.height - 1), randint(0, self.width - 1)]  # get a new random position
		self.grid[x][y] = Doctor  # summon the doctor

	def find_pos(self, obj: list) -> list or False:
		# find the position of the object given
		for i in range(self.height):
			for k in range(self.width):
				if self.grid[i][k] == obj:
					return [i, k]
		return False

	def find_doctor(self) -> list or False:
		# find the doctor on the grid using find_pos, shortcut.
		pos = self.find_pos(Doctor)
		return pos

	def junk_at(self, dalek_pos: list) -> None:
		# convert the selected cell to junk, no matter what is on it.
		self.grid[dalek_pos[0]][dalek_pos[1]] = Junk

	def kill_at(self, pos: list) -> None:
		# remove any object from the grid at the given position.
		self.grid[pos[0]][pos[1]] = None

	def make_move(self, move_from: list, move_to: list) -> None:
		# move the object from the move_from position to the move_to position
		self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]  # move the object
		self.grid[move_from[0]][move_from[1]] = None  # remove the object from the old position

	def request_move(self, move : str) -> bool:
		# get the move from the user, validates it and then makes the move if and only if it was validated.
		# Then return if the move was valid or not.
		pos = self.find_doctor()
		if move == 'TELEPORT':
			return True
		elif self.validate_move(pos, move):  # if the move is valid
			newPos = self.new_pos(pos, move)  # get the new position
			if self.grid[newPos[0]][newPos[1]] != Dalek or self.grid[newPos[0]][newPos[1]] != Junk:
				self.make_move(pos, newPos)  # move the doctor
				return True
		return False

	def validate_move(self, pos: list, move_request : str) -> bool:
		# validate the move requested by the user
		if move_request == "UP":
			if pos[0]:  # if the position is not on the top of the grid
				return True
		elif move_request == 'UPRIGHT':
			if pos[0] and pos[1] != self.width - 1:   # if the position is not on the top right of the grid
				return True
		elif move_request == 'UPLEFT':
			if pos[0] and pos[1]:  # if the position is not on the top left of the grid
				return True
		elif move_request == 'DOWN':
			if pos[0] < self.height - 1:  # if the position is not on the bottom of the grid
				return True
		elif move_request == 'DOWNRIGHT':
			if pos[0] < self.height - 1 and pos[1] < self.width - 1:  # if the position is not on the
				# bottom right of the grid
				return True
		elif move_request == 'DOWNLEFT':
			if pos[0] < self.height - 1 and pos[1]:  # if the position is not on the bottom left of the grid
				return True
		elif move_request == 'LEFT':  # if the position is not on the left of the grid
			if pos[1]:
				return True
		elif move_request == 'RIGHT':  # if the position is not on the right of the grid
			if pos[1] < self.width - 1:
				return True

		elif move_request == 'TELEPORT':  # Always true if doctor
			if self.grid[pos[0]][pos[1]] == Doctor:
				return True

		elif move_request == 'ZAP':  # To be setup later
			if self.grid[pos[0]][pos[1]] == Doctor:
				if self.grid[pos[0]][pos[1]].can_zap():
					self.grid[pos[0]][pos[1]].zapcount -= 1
					return True

		return False

	def dalek_direction_to_doctor(self, distance: list) -> str:
		# get the direction to the doctor from the distance between the dalek and the doctor
		if distance[0] > 0:  # if the doctor is below the dalek
			direction = 'DOWN'
			if distance[1] > 0:    # if the doctor is on the right of the dalek
				direction += 'RIGHT'
			elif distance[1] < 0:    # if the doctor is on the left of the dalek
				direction += 'LEFT'
		elif distance[0] < 0:  # if the doctor is above the dalek
			direction = 'UP'
			if distance[1] > 0:  # if the doctor is on the right of the dalek
				direction += 'RIGHT'
			elif distance[1] < 0:  # if the doctor is on the left of the dalek
				direction += 'LEFT'

		else:
			if distance[1] > 0:  # if the doctor is on the right of the dalek
				direction = 'RIGHT'
			elif distance[1] < 0:  # if the doctor is on the left of the dalek
				direction = 'LEFT'
			else:  # if the doctor is on the same position as the dalek or that the doctor is not there
				direction = 'NONE'
		return direction

	def new_pos(self, pos: list, direction: str) -> list:
		if direction == 'UP':
			return [pos[0] - 1, pos[1]]
		elif direction == 'UPRIGHT':
			return [pos[0] - 1, pos[1] + 1]
		elif direction == 'UPLEFT':
			return [pos[0] - 1, pos[1] - 1]
		elif direction == 'DOWN':
			return [pos[0] + 1, pos[1]]
		elif direction == 'DOWNRIGHT':
			return [pos[0] + 1, pos[1] + 1]
		elif direction == 'DOWNLEFT':
			return [pos[0] + 1, pos[1] - 1]
		elif direction == 'LEFT':
			return [pos[0], pos[1] - 1]
		elif direction == 'RIGHT':
			return [pos[0], pos[1] + 1]
		"""elif direction == 'TELEPORT':
			return [randint(0, GameGrid.height - 1), randint(0, GameGrid.width - 1)] -> See Aby's code in game instead"""

	def get_all_daleks(self) -> list or False:
		# get all the daleks in the grid
		daleks = []
		for i in range(self.height):
			for j in range(self.width):
				if self.grid[i][j] == Dalek:
					daleks.append([i, j])
		return daleks

	def move_all_daleks(self) -> None:
		# move all the daleks on the grid
		posdoctor = self.find_doctor()
		daleks = self.get_all_daleks()
		daleks.sort(key=lambda x: abs(x[0] - posdoctor[0]) + abs(x[1] - posdoctor[1])) # sort the daleks by distance to the doctor (Trouver en ligne)
		for dalek in daleks:
			if self.grid[dalek[0]][dalek[1]] == Dalek:  # if the dalek is still alive
				self.move_dalek(posdoctor, dalek)  # move the dalek

	def move_dalek(self, pos_doctor: list, pos_dalek: list) -> None:
		# move the dalek on the grid
		distance = [pos_doctor[0] - pos_dalek[0], pos_doctor[1] - pos_dalek[1]]  # distance between the dalek and the doctor
		direction = self.dalek_direction_to_doctor(distance)  # find the best route from the dalek to the doctor
		if self.validate_move(pos_dalek, direction):  # if the dalek can move in the direction
			new_pos = self.new_pos(pos_dalek, direction)
			if self.grid[new_pos[0]][new_pos[1]] == Dalek:  # if the dalek is on the same position as another dalek
				self.kill_at(pos_dalek)  # kill the dalek
				self.junk_at(new_pos)  # kill the other dalek and turn him into junk
			elif self.grid[new_pos[0]][new_pos[1]] == Junk:  # if the dalek is on the same position as junk
				self.kill_at(pos_dalek)  # kill the dalek
			else:
				self.make_move(pos_dalek, new_pos)  # move the dalek
