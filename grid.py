# ----------------------------------------------------------------------------------------------------------------------#
# Written by : Christopher Perreault
# Date : 2022-09-17
# Description : This is the main file for the game's grid logic. It will create the grid, do the unit's movements, etc.
# Version : 0.2.2
# Contains : GameGrid, validate_move, make_move, request_move, summon_daleks, find_pos, dalek_to_junk_at, kill_at

# ----------------------------------------------------------------------------------------------------------------------#
from random import randint
from models import Doctor, Dalek, Junk


class GameGrid:
	def __init__(self, width=8, height=6):
		self.width = width
		self.height = height
		self.grid = []
		self.turn = 0
		self.create_grid()

	def create_grid(self):
		for i in range(self.height):
			self.grid.append([])  # create a new row
			for k in range(self.width):  # create a new height
				self.grid[i].append(' ')

def print_grid(gamegrid):
	# DEBUG ONLY -> print the grid
	for i in range(gamegrid.height):
		for k in range(gamegrid.width):
			if gamegrid.grid[i][k] == Doctor:
				print('D', end='/')
			elif gamegrid.grid[i][k] == Dalek:
				print('X', end='/')
			elif gamegrid.grid[i][k] == Junk:
				print('J', end='/')
			else:
				print(' ', end='/')
		print()


def summon_daleks(gamegrid, dalek_count : int) -> None:
	# summon the daleks on the grid, depending on how many were asked.
	for i in range(dalek_count):
		gamegrid.grid[randint(0, gamegrid.height - 1)][randint(0, gamegrid.width - 1)] = Dalek


def summon_doctor(gamegrid) -> None:
	# summon the doctor on the grid
	# "Do while" which allows to know if the doctor is going to randomly spawn on a dalek, and if so not to.
	x, y = [randint(0, gamegrid.height - 1), randint(0, gamegrid.width - 1)]
	while gamegrid.grid[x][y] != Doctor:
		if gamegrid.grid[x][y] != Dalek:  # if the position is not occupied by a dalek
			gamegrid.grid[x][y] = Doctor  # summon the doctor
		else:
			x, y = randint(0, gamegrid.height - 1), randint(0, gamegrid.width - 1)


def find_pos(gamegrid, obj : Doctor | Dalek | Junk) -> list | None:
	# find the position of the object given
	for i in range(gamegrid.height):
		for k in range(gamegrid.width):
			if gamegrid.grid[i][k] == obj:
				return [i, k]
	return None


def find_doctor(gamegrid) -> list | None:
	# find the doctor on the grid using find_pos, shortcut.
	print(find_pos(gamegrid, Doctor))
	return find_pos(gamegrid, Doctor)


def junk_at(gamegrid, dalek_pos : list) -> None:
	# convert the selected cell to junk, no matter what is on it.
	gamegrid.grid[dalek_pos[0]][dalek_pos[1]] = Junk


def kill_at(gamegrid, pos : list) -> None:
	# remove any object from the grid at the given position.
	gamegrid.grid[pos[0]][pos[1]] = None


def make_move(gamegrid, move_from : list, move_to : list) -> None:
	# move the object from the move_from position to the move_to position
	gamegrid.grid[move_to[0]][move_to[1]] = gamegrid.grid[move_from[0]][move_from[1]]
	gamegrid.grid[move_from[0]][move_from[1]] = ' '


def request_move(gamegrid) -> None:
	# request the move from the user, validates it and then makes the move if and only if it was validated.
	pos = find_doctor(gamegrid)
	newInput = ""
	while newInput not in {'UP', 'UPRIGHT', 'UPLEFT', 'DOWN', 'DOWNRIGHT', 'DOWNLEFT', 'LEFT', 'RIGHT', 'TELEPORT',
						   'ZAP'}:
		newInput = input("What is your move? (UP, DOWN, LEFT, RIGHT) ").upper()
		if validate_move(gamegrid, newInput, pos):
			newPos = new_pos(pos, newInput)
			make_move(gamegrid, find_doctor(gamegrid), newPos)
		else :
			newInput = ""


def validate_move(gamegrid, move_request, pos : list) -> bool: #To Add Direction Type Hint and Ludwigs code somehow with request move
	# validate the move requested by the user
	if move_request == "UP":
		if pos[0]:  # if the position is not on the top of the grid
			return True
	elif move_request == 'UPRIGHT':
		if pos[0] and pos[1] != gamegrid.width - 1:   # if the position is not on the top right of the grid
			return True
	elif move_request == 'UPLEFT':
		if pos[0] and pos[1]:  # if the position is not on the top left of the grid
			return True
	elif move_request == 'DOWN':
		if pos[0] < gamegrid.height - 1:  # if the position is not on the bottom of the grid
			return True
	elif move_request == 'DOWNRIGHT':
		if pos[0] < gamegrid.height - 1 and pos[1] < gamegrid.width - 1:  # if the position is not on the
			# bottom right of the grid
			return True
	elif move_request == 'DOWNLEFT':
		if pos[0] < gamegrid.height - 1 and pos[1]:  # if the position is not on the bottom left of the grid
			return True
	elif move_request == 'LEFT':  # if the position is not on the left of the grid
		if pos[1]:
			return True
	elif move_request == 'RIGHT':  # if the position is not on the right of the grid
		if pos[1] < gamegrid.width - 1:
			return True

	elif move_request == 'TELEPORT': # Always true if doctor
		if gamegrid.grid[pos[0]][pos[1]] == Doctor:
			return True

	elif move_request == 'ZAP':  # To be setup later
		if gamegrid.grid[pos[0]][pos[1]] == Doctor & gamegrid.grid[pos[0]][pos[1]].zapcount > 0:
			gamegrid.grid[pos[0]][pos[1]].zapcount -= 1
			return True

	return False


def dalek_direction_to_doctor(distance : list) -> str:
	# find the best route from the dalek to the doctor
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
	return direction


def new_pos(pos : list, direction : str) -> list:
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
	elif direction == 'TELEPORT':
		return [randint(0, GameGrid.height - 1), randint(0, GameGrid.width - 1)]

def get_all_daleks(gamegrid) -> list:
	# find all the daleks on the grid
	daleks = []
	for i in range(gamegrid.height):
		for k in range(gamegrid.width):
			if gamegrid.grid[i][k] == Dalek:
				daleks.append([i, k])
	return daleks

def move_all_daleks(gamegrid) -> None:
	# move all the daleks on the grid
	doctorPos = find_doctor(gamegrid)
	for dalek in get_all_daleks(gamegrid):
		move_dalek(gamegrid, dalek, doctorPos)

def move_dalek(gamegrid, dalek_pos, doctor_pos) -> None:
	# move the dalek on the grid
	distance = [doctor_pos[0] - dalek_pos[0], doctor_pos[1] - dalek_pos[1]]
	direction = dalek_direction_to_doctor(distance)
	newPos = new_pos(dalek_pos, direction)
	if gamegrid.grid[newPos[0]][newPos[1]] != Dalek:
		make_move(gamegrid, dalek_pos, newPos)
	elif gamegrid.grid[newPos[0]][newPos[1]] == Dalek:
		if False:
			pass # To be setup later, if the dalek is going to another dalek who hasn't move yet, he will move first.
		else:
			make_move(gamegrid, dalek_pos, newPos)
			junk_at(gamegrid, newPos)
	elif gamegrid.grid[newPos[0]][newPos[1]] == Junk:
		kill_at(gamegrid, dalek_pos)
