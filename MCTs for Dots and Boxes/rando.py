from random import choice

def think(state):
	return choice(state.get_moves())