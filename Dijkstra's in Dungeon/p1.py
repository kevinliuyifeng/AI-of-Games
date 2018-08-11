from heapq import heappush, heappop
import operator

from math import sqrt 
def load_level(filename):
	walls = {}
	spaces = {}
	waypoints = {}
	with open(filename, "r") as f:

		for j, line in enumerate(f.readlines()):
			for i, char in enumerate(line):
				if char == '\n':
					continue
				elif char.isupper():
					walls[(i,j)] = char
				else:
					spaces[(i,j)] = char
					if char.islower():
						waypoints[char] = (i,j)

	level = { 'walls': walls,
			'spaces': spaces,
			'waypoints': waypoints}
	return level


def show_level(level, path = []):

	xs, ys = zip(*(level['spaces'].keys() + level['walls'].keys()))
	x_lo = min(xs)
	x_hi = max(xs)
	y_lo = min(ys)
	y_hi = max(ys)

	path_cells = set(path)

	chars = []
	print(x_hi)
	print(y_hi)
	for j in range(y_lo, y_hi+1):
		for i in range(x_lo, x_hi+1):

			cell = (i,j)
			if cell in path_cells:
				chars.append('*')
			elif cell in level['walls']:
				chars.append(level['walls'][cell])
			elif cell in level['spaces']:
				chars.append(level['spaces'][cell])
			else:
				chars.append(' ')

		chars.append('\n')
	print ''.join(chars)

def navigation_edges(level, cell):
	deltas = {
	                'LEFT_DOWN':	(-1, -1), 
	                'LEFT':			(-1, 0), 
					'LEFT_UP':		(-1, 1), 
					'DOWN':			(0, -1), 
					'UP':			(0, 1), 
					'RIGHT_DOWN':	(1, -1), 
					'RIGHT':		(1, 0), 
					'RIGHT_UP':		(1, 1)
	    };

	validMoves = []
	for delta in deltas.values():
	    position = (cell[0] + delta[0], cell[1] + delta[1])
	        
	    if position in level['spaces']:
	        cost = sqrt(delta[0] ** 2 + delta[1] ** 2)
	        validMoves.append((position, cost))
	return validMoves   

#print validMoves

def dijkstras_shortest_path(src, dst, graph, adj):
	queue = []
	came_from = {}
	cost_so_far = {}
	came_from[src] = None 
	cost_so_far[src] = 0

	heappush(queue, (cost_so_far[src], src))

	while queue:
		path_cost, current = heappop(queue)
		if current == dst:
			break
		adjacent = adj(graph, current)
 
		for neighbor, cost in adjacent:
			total_cost = path_cost + cost
			if neighbor not in cost_so_far or total_cost < cost_so_far[neighbor]:
				cost_so_far[neighbor] = total_cost
				heappush(queue, (total_cost, neighbor))
				came_from[neighbor] = current

	path = []
	if current == dst:
		while current:#
			path.append(current)
			current = came_from[current]  #to parent
		path.append(src)
		path.reverse()
	print total_cost
	return path

def test_route(filename, src_waypoint, dst_waypoint):
	level = load_level(filename)
	show_level(level)
	src = level['waypoints'][src_waypoint]
	dst = level['waypoints'][dst_waypoint]
	path = dijkstras_shortest_path(src, dst, level, navigation_edges)

	if path:
		show_level(level, path)

	else:
		print "No path possible!"

if __name__ == '__main__':
	import sys
	_, filename, src_waypoint, dst_waypoint = sys.argv
	test_route(filename, src_waypoint, dst_waypoint)











































