import random
import greedo

ROLLOUT = 10
DEPTH = 100
def think(state):
	me = state.get_whose_turn()
	moves = state.get_moves()
	best_move = moves[0]
	best_score = float('-inf')



	for m in moves:
		total_score = 0.0
		score_opp = 0.0

		for r in range(ROLLOUT):
			rollout_state = state.copy()
			rollout_state.apply_move(m)

			for h in range(DEPTH):
				if rollout_state.is_terminal():
					break
				rollout_state.apply_move(greedo.think(rollout_state))

			total_score += rollout_state.get_score(me)
		

		if total_score >= best_score:
			best_score = total_score
			best_move = m

	return best_move



