import json
from heapq import heappush, heappop
import time

with open('minecraft.json') as f:
	domain = json.load(f)

item_index = {}
i = 0
Items = domain['Items']
for item in domain['Items']:
	item_index[item] = i
	i = i + 1

from collections import namedtuple

state = ()
state_dict = {}
Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])
all_recipes = []

def state_to_dict(state):
	return {name: state[i] for i,name in enumerate(Items) if state[i] > 0}

def make_goal_checker(goal):
	def check(state):
		for item in goal:
			index = item_index[item]
			i_check = state[index]
			#print goal[item]
			if i_check < goal[item]:
				return False
		return True
	return check

is_goal = make_goal_checker(domain['Goal'])

def make_checker(rule):
	consumes = rule.get('Consumes', {})
	requires = rule.get('Requires', {})
	consumes_index = [(item_index[item], consumes[item]) for item in consumes]
	requirement_index = [(item_index[item], 1) for item in requires]
	result = consumes_index + requirement_index
	def check(state):
		return all([state[i] >= v for i, v in result])
	return check


def make_effector(rule):
	produces, consumes = rule.get('Produces', {}), rule.get('Consumes', {})
	delta_pair = []
	for item in sorted(item_index):
		value = 0
		if item in produces:
			value += produces[item]
		if item in consumes:
			value -= consumes[item]
		delta_pair.append(tuple([item_index[item], value]))
	def effect(state):
		return tuple([state[i] + delta for i, delta in delta_pair])
	return effect

for name, rule in domain['Recipes'].items():
	checker = make_checker(rule)
	effector = make_effector(rule)
	recipe = Recipe(name, checker, effector, rule['Time'])
	all_recipes.append(recipe)

def get_edges(state):
	for r in all_recipes:
		if r.check(state):
			yield (r.name, r.effect(state), r.cost)



def default_heuristic(state):
	return 0


def search(get_edges, initial, is_goal, limit, heuristic):
	dist = {}
	dist[initial] = 0
	prev = {}
	prev[initial] = None
	actions = {}
	actions[initial] = None
	queue = []
	heappush(queue, (dist[initial], initial))
	is_finished = False


	time_start = time.time()
	t_limit = time_start + limit

	while queue:
		bdist, state = heappop(queue)
		#print "bdist: " + str(bdist) + "state:" + str(state)
		if is_goal(state):
			print "success"
			is_finished = True
			break
		neighbors = get_edges(state)
		#print "Neighbors: " + str(neighbors)

		for n in neighbors:
			alt = bdist + n[2] + heuristic(n[1])
			
			if n[1] not in dist or alt < dist[n[1]]:
				dist[n[1]] = alt
				prev[n[1]] = state
				actions[n[1]] = n[0]
				
				heappush(queue, (dist[n[1]], n[1]))
		t_end = time.time()



	if is_finished:
		plan = []
		total_cost = bdist
		while state:
			print actions[state], state_to_dict(state)
			plan.append(state)
			state = prev[state]
		plan.reverse()
	else:
		print "No valid path found"
		plan = []
		total_cost = 0

	return total_cost, plan

def make_initial_state(d):
	return tuple(d.get(name, 0) for i,name in enumerate(Items))

initial_state = make_initial_state(domain['Initial'])



print search(get_edges, initial_state, is_goal, 30, default_heuristic)


# test
'''
t_initial = 'a'
t_limit = 20

edges = {'a': {'b':1, 'c':20}, 'b':{'c':1}}

def t_graph(state):
	for next_state, cost in edges[state].items():
		yield ((state, next_state), next_state, cost)

def t_is_goal(state):
	return state == 'c'

def t_heuristic(state):
	return 0

print (search(t_graph, t_initial, t_is_goal, t_limit, t_heuristic))

'''




































