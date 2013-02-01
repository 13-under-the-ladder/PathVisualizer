'''
This file creates some sample graphs.
'''

from graph_geo import *

# translation of a double-loop
d = {
	0 : (50, 100),
	1 : (80, 50),
	2 : (160, 50),
	3 : (190, 100),
	4 : (160, 150),
	5 : (80, 150),
	6 : (270, 100),
	7 : (300, 150),
	8 : (270, 200),
	9 : (190, 200),
	10 : (300, 50),
	11 : (380, 150),
	12 : (300, 250),
	13 : (160, 250),
}

def translate_roads(roads):
	return [[d[v] for v in road] for road in roads]
		
def queue_roads(g, roads):
	g.set_translation(d)

	# let g be None for debugging
	if g is not None:
		for road in roads:
			g.queue_road(*road)
			
def load_ship_wheel(g):
	'''Branching at each point on the hexagon loop.'''
	
	roads = [
		(3, 2),
		(4, 5),
		(6, 10),
		(7, 11),
		(8, 12),
		(9, 13)
	]
	
	#roads = translate_roads(roads)
	queue_roads(g, roads)
	# add a hex in the middle
	roads.extend(load_other_loop(g))	
	return roads

def load_octopus(g):
	'''Complex branching.'''
	
	roads = []
	
	# branch 1 at 3
	roads.append((3, 6))
	# 2 branches at 6
	roads.append((6, 7))
	roads.append((6, 10))
	
	# branch 2 at 3
	roads.append((3, 4))
	# 2 branches at 4
	roads.append((4, 5))
	roads.append((4, 9))
	
	# branch 3 at 3
	roads.append((3, 2))
	# 1 branch at 2
	roads.append((2, 1))
	
	# roads.append((7, 9))
	
	#roads = translate_roads(roads)
	queue_roads(g, roads)
	return roads

def load_other_loop(g):
	'''Load the hex loop in the middle.'''
	
	roads = []
	
	roads.append((3, 4))
	roads.append((4, 9))
	roads.append((9, 8))
	roads.append((8, 7))
	roads.append((7, 6))
	roads.append((6, 3))
	
	#roads = translate_roads(roads)
	queue_roads(g, roads)
	return roads
	
def load_loop(g):
	'''Simple hexagonal loop.'''
	
	roads = []
	
	roads.append((0, 1))
	roads.append((1, 2))
	roads.append((2, 3))
	roads.append((3, 4))
	roads.append((4, 5))
	roads.append((5, 0))
	
	#roads = translate_roads(roads)
	queue_roads(g, roads)
	return roads
	
def load_line(g):
	'''No branches.'''
	
	roads = [
		(0, 1)
	]
	
	#do not translate for this simple case
	queue_roads(g, roads)
	return roads
	
def load_long_line(g):
	'''No branches. More links.'''
	
	roads = [
		(0, 1),
		(1, 2),
		(2, 3),
		(3, 4),
		(4, 5)
	]
	
	queue_roads(g, roads)
	return roads
	
def load_simple_branch(g):
	'''One branch.'''
	
	roads = []
	
	roads.append((0, 1))
	roads.append((1, 2))
	# branches at 2
	roads.append((2, 3))
	roads.append((2, 4))
	
	#roads = translate_roads(roads)
	queue_roads(g, roads)
	return roads
	
if __name__ == "__main__":
	print load_loop(None)
	