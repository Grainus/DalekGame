# ----------------------------------------------------------------------------------------------------------------------#
# Written by : Christopher Perreault
# Date : 2022-09-17
# Description : This is the main file for the game's grid logic. It will create the grid, do the unit's movements, etc.
# Version : 0.2.2
# Contains : GameGrid, validate_move, make_move, request_move, summon_daleks, find_pos, dalek_to_junk_at, kill_at

# ----------------------------------------------------------------------------------------------------------------------#
import random
import __main__


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
				self.grid[i].append(' ')  # fill the height with A's

	def print_grid(self):  # print the grid, to be removed. Debug only.
		for i in range(self.height):
			for k in range(self.width):
				print(self.grid[i][k], end='/')
			print()


def summon_daleks(gamegrid, dalek_count):
	# summon the daleks on the grid, depending on how many asked.
	for i in range(dalek_count):
		gamegrid.grid[random.randint(0, gamegrid.height - 1)][random.randint(0, gamegrid.width - 1)] = 'D'  # summon a dalek


def summon_doctor(gamegrid):
	# summon the doctor on the grid
	x, y = random.randint(0, gamegrid.height - 1), random.randint(0, gamegrid.width - 1)

	# "Do while" which allows to know if the doctor is going to randomly spawn on a dalek, and if so not to.
	if gamegrid.grid[x][y] != 'D':  # if the position is not occupied by a dalek
		gamegrid.grid[x][y] = 'O'  # summon the doctor
	while gamegrid.grid[x][y] != 'O':
		if gamegrid.grid[x][y] != 'D':  # if the position is not occupied by a dalek
			gamegrid.grid[x][y] = 'O'  # summon the doctor


def find_pos(gamegrid, obj):
	# find the position of the object on the grid
	for i in range(gamegrid.height):  # loop through the grid
		for k in range(gamegrid.width):
			if gamegrid.grid[i][k] == obj:  # if the object is found
				pos = [i, k]
				return pos  # If found, return the position of the object
			else:
				return False


def find_doctor(gamegrid):
	# find the doctor on the grid
	for i in range(gamegrid.height):  # loop through the grid
		for k in range(gamegrid.width):
			if gamegrid.grid[i][k] == 'D':  # if the doctor is found
				pos = [i, k]
				return pos  # If found, return the position of the doctor
			else:
				return False


def dalek_to_junk_at(gamegrid, dalek_pos):
	# convert the dalek to junk at the position given
	gamegrid.grid[dalek_pos[0]][dalek_pos[1]] = 'J'


def kill_at(gamegrid, pos):
	# kill the object at the position given
	gamegrid.grid[pos[0]][pos[1]] = ' '


def make_move(gamegrid, move_from, move_to):
	# move the object from the move_from position to the move_to position
	gamegrid.grid[move_to[0]][move_to[1]] = gamegrid.grid[move_from[0]][move_from[1]]  # move the object
	gamegrid.grid[move_from[0]][move_from[1]] = ' '  # remove the object from the old position"


def request_move(gamegrid):
	# request the move to the user
	move = ""
	while move not in ['UP', 'UPRIGHT', 'UPLEFT', 'DOWN', 'DOWNRIGHT', 'DOWNLEFT', 'LEFT', 'RIGHT', 'TELEPORT', 'ZAP']:
		move = input("Move : ").upper()  # request the move to be replaced by ludwigs code
		if validate_move(gamegrid, move):
			return move


def validate_move(gamegrid, move_request):
	# {'UP': [0, -1], 'UPRIGHT': [1, -1], 'UPLEFT': [-1, -1], 'DOWN': [0, 1], 'DOWNRIGHT': [1, 1], 'DOWNLEFT': [-1, 1],
	# 'LEFT': [-1, 0], 'RIGHT': [1, 0]}
	pos = find_doctor(gamegrid)
	if move_request == 'UP':
		if pos[0]:  # if the object is not at the top of the grid
			return True
	elif move_request == 'UPRIGHT':
		if pos[0] and pos[1] != gamegrid.width - 1:  # if the object is not at the top right of the grid
			return True
	elif move_request == 'UPLEFT':  # if the object is not at the top left of the grid
		if pos[0] and pos[1]:
			return True
	elif move_request == 'DOWN':
		if pos[0] < gamegrid.height - 1:
			return True
	elif move_request == 'DOWNRIGHT':
		if pos[0] < gamegrid.height - 1 and pos[1] < gamegrid.width - 1:
			return True
	elif move_request == 'DOWNLEFT':
		if pos[0] < gamegrid.height - 1 and pos[1]:
			return True
	elif move_request == 'LEFT':
		if pos[1]:
			return True
	elif move_request == 'RIGHT':
		if pos[1] < gamegrid.width - 1:
			return True

	elif move_request == 'TELEPORT':
		return True
	elif move_request == 'ZAP':  # To be setup later
		pass

	return False


def dalek_direction_to_doctor(distance):
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


def dalek_direction(dalek_pos, directiontodoctor):
	# move the dalek
	if directiontodoctor == 'UP':
		dalek_pos[0] -= 1
	elif directiontodoctor == 'DOWN':
		dalek_pos[0] += 1
	elif directiontodoctor == 'LEFT':
		dalek_pos[1] -= 1
	elif directiontodoctor == 'RIGHT':
		dalek_pos[1] += 1
	elif directiontodoctor == 'UPRIGHT':
		dalek_pos[0] -= 1
		dalek_pos[1] += 1
	elif directiontodoctor == 'UPLEFT':
		dalek_pos[0] -= 1
		dalek_pos[1] -= 1
	elif directiontodoctor == 'DOWNRIGHT':
		dalek_pos[0] += 1
		dalek_pos[1] += 1
	elif directiontodoctor == 'DOWNLEFT':
		dalek_pos[0] += 1
		dalek_pos[1] -= 1
	elif directiontodoctor == 'NONE':
		pass
	return dalek_pos


def move_dalek(gamegrid, dalek_pos, doctor_pos):
	directiontodoctor = dalek_direction_to_doctor((doctor_pos[0] - dalek_pos[0], doctor_pos[1] - dalek_pos[1]))
	dalek_dir = dalek_direction(dalek_pos, directiontodoctor)
	if gamegrid.grid[dalek_dir] != 'D':  # if the dalek is not going to move on another d
		make_move(gamegrid, dalek_pos, dalek_dir)  # move the dalek
	else:
		# To add : If the Dalek blocking the way hasn't move yet, move it first
		move_dalek(gamegrid, dalek_dir, doctor_pos)
		make_move(gamegrid, dalek_pos, dalek_dir)


def move_all_daleks(gamegrid):
	# move all the daleks on the grid
	doctor_pos = find_doctor(gamegrid)
	for i in range(gamegrid.height):  # loop through the grid
		for k in range(gamegrid.width):
			if gamegrid.grid[i][k] == 'D':  # if the object is a dalek
				move_dalek(gamegrid, [i, k], doctor_pos)
