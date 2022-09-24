# ----------------------------------------------------------------------------------------------------------------------#
# Written by : Christopher Perreault
# Date : 2022-09-17
# Description : This is the main file for the game's grid logic. It will create the grid, do the unit's movements, etc.
# Version : 0.2.2
# Contains : GameGrid, validate_move, make_move, request_move, summon_daleks, find_pos, dalek_to_junk_at, kill_at

# ----------------------------------------------------------------------------------------------------------------------#
import random

class GameGrid:
	def __init__(self, width=8,height=6):
		self.width = width
		self.height = height
		self.grid = []
		self.turn = 0;
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

def summon_daleks(gameGrid, dalek_count):
	# summon the daleks on the grid, depending on how many asked.
	for i in range(dalek_count):
		gameGrid.grid[random.randint(0, gameGrid.height - 1)][random.randint(0, gameGrid.width - 1)] = 'D'  # summon a dalek

def summon_doctor(gameGrid):
	# summon the doctor on the grid
	x, y = random.randint(0, gameGrid.height - 1), random.randint(0, gameGrid.width - 1)

	# "Do while" which allows to know if the doctor is going to randomly spawn on a dalek, and if so not to.
	if gameGrid.grid[x][y] != 'D':  # if the position is not occupied by a dalek
		gameGrid.grid[x][y] = 'O'  # summon the doctor
	while gameGrid.grid[x][y] != 'O':
		if gameGrid.grid[x][y] != 'D':  # if the position is not occupied by a dalek
			gameGrid.grid[x][y] = 'O' # summon the doctor

def find_pos(gameGrid, object):
	#find the position of the object on the grid
	for i in range(gameGrid.height):  # loop through the grid
		for k in range(gameGrid.width):
			if gameGrid.grid[i][k] == object:  # if the object is found
				pos = [i, k]
				return pos  # If found, return the position of the object
			else :
				return False

def find_doctor(gameGrid):
	# find the doctor on the grid
	for i in range(gameGrid.height):  # loop through the grid
		for k in range(gameGrid.width):
			if gameGrid.grid[i][k] == 'D':  # if the doctor is found
				pos = [i, k]
				return pos  # If found, return the position of the doctor
			else :
				return False

def dalek_to_junk_at(gameGrid, dalek_pos):
	# convert the dalek to junk at the position given
	gameGrid.grid[dalek_pos[0]][dalek_pos[1]] = 'J'

def kill_at(gameGrid, pos):
	# kill the object at the position given
	gameGrid.grid[pos[0]][pos[1]] = ' '

def make_move(gameGrid, move_from, move_to):
	# move the object from the move_from position to the move_to position
	gameGrid.grid[move_to[0]][move_to[1]] = gameGrid.grid[move_from[0]][move_from[1]]  # move the object
	gameGrid.grid[move_from[0]][move_from[1]] = ' '  # remove the object from the old position"

def request_move(gameGrid):
	# request the move to the user
	move = ""
	while move not in ['UP', 'UPRIGHT', 'UPLEFT', 'DOWN', 'DOWNRIGHT', 'DOWNLEFT', 'LEFT', 'RIGHT', 'TELEPORT', 'ZAP']:
		move = input("Move : ").upper() # request the move to be replaced by ludwigs code
		if validate_move(gameGrid, move):
			return move

def validate_move(gameGrid, move_request):

	pos = find_doctor(gameGrid)
	if move_request == 'UP':
		if pos[0]:  # if the object is not at the top of the grid
			return True
	elif move_request == 'UPRIGHT':
		if pos[0] and pos[1] != gameGrid.width - 1:  # if the object is not at the top right of the grid
			return True
	elif move_request == 'UPLEFT':  # if the object is not at the top left of the grid
		if pos[0] and pos[1]:
			return True
	elif move_request == 'DOWN':
		if pos[0] < gameGrid.height - 1:
			return True
	elif move_request == 'DOWNRIGHT':
		if pos[0] < gameGrid.height - 1 and pos[1] < gameGrid.width - 1:
			return True
	elif move_request == 'DOWNLEFT':
		if pos[0] < gameGrid.height - 1 and pos[1]:
			return True
	elif move_request == 'LEFT':
		if pos[1]:
			return True
	elif move_request == 'RIGHT':
		if pos[1] < gameGrid.width - 1:
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

def dalek_direction(dalek_pos, directionToDoctor):
	# move the dalek
	if directionToDoctor == 'UP':
		dalek_pos[0] -= 1
	elif directionToDoctor == 'DOWN':
		dalek_pos[0] += 1
	elif directionToDoctor == 'LEFT':
		dalek_pos[1] -= 1
	elif directionToDoctor == 'RIGHT':
		dalek_pos[1] += 1
	elif directionToDoctor == 'UPRIGHT':
		dalek_pos[0] -= 1
		dalek_pos[1] += 1
	elif directionToDoctor == 'UPLEFT':
		dalek_pos[0] -= 1
		dalek_pos[1] -= 1
	elif directionToDoctor == 'DOWNRIGHT':
		dalek_pos[0] += 1
		dalek_pos[1] += 1
	elif directionToDoctor == 'DOWNLEFT':
		dalek_pos[0] += 1
		dalek_pos[1] -= 1
	elif directionToDoctor == 'NONE':
		pass

def move_dalek(gameGrid, dalek_pos, doctor_pos):
	directionToDoctor = dalek_direction_to_doctor((doctor_pos[0] - dalek_pos[0], doctor_pos[1] - dalek_pos[1]))
	dalek_dir = dalek_direction(dalek_pos, directionToDoctor)
	if gameGrid.grid[dalek_direction[0]][dalek_direction[1]] != 'D':  # if the dalek is not going to move on another d
		make_move(gameGrid,dalek_pos, dalek_dir)  # move the dalek
	else:
		# To add : If the Dalek blocking the way hasn't move yet, move it first
		move_dalek(gameGrid, dalek_dir, doctor_pos)
		make_move(gameGrid, dalek_pos, dalek_dir)

def move_all_daleks(gameGrid):
	# move all the daleks on the grid
	doctor_pos = find_doctor(gameGrid)
	for i in range(gameGrid.height):  # loop through the grid
		for k in range(gameGrid.width):
			if gameGrid.grid[i][k] == 'D':  # if the object is a dalek
				move_dalek(gameGrid, [i, k], doctor_pos)
		# if gameGrid.grid[i][k] == 'D':  # if the object is a dalek
			#	directionToDoctor = dalek_direction_to_doctor((doctor_pos[0] - i, doctor_pos[1] - k))
			#	dalek_direction = dalek_direction([i, k], directionToDoctor)
		#		if gameGrid.grid[dalek_direction[0]][dalek_direction[1]] != 'D':  #  if the dalek is not going to move on another dalek
		#			make_move(gameGrid, [i, k], dalek_direction)  # move the dalek
		#		else:
		#			# To add : If the Dalek blocking the way hasn't move yet, move it first
		#			move_dalek()
