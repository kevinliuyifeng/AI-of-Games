
def think(state):
	possible_moves = state.get_moves()
	best_move = None
	best_score = -float('inf')

	for m in possible_moves:
		copy = state.copy()
		copy.apply_move(m)
		if (copy.get_score(state.get_whose_turn()) >= best_score):
			best_score = copy.get_score(state.get_whose_turn())
			best_move = m
	return best_move


	