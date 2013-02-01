'''
This file contains a sample geometry for the graph.
It is 12 vertices arranged in more or less a double hexagon.
'''

import random

height = 50
width = 80
width_slant = 30
# the first hex starts here
hex_start_x = 50
hex_start_y = 100

def get_hexagon(left_center_x, left_center_y):
	return (
		(left_center_x, left_center_y),
		(left_center_x + width_slant, left_center_y - height),
		(left_center_x + width + width_slant, left_center_y - height),
		(left_center_x + width + 2 * width_slant, left_center_y),
		(left_center_x + width + width_slant, left_center_y + height),
		(left_center_x + width_slant, left_center_y + height),
	)
	
def connect_nodes(nodes):
	'''Connect the nodes in this node list together.'''
	
	roads = []
	
	for i in range(len(nodes) - 1):
		roads.append(nodes[i], nodes[i + 1])
		
	return roads
	
def get_geo_roads(nodes):
	# first hex
	roads = connect_nodes(nodes[:6])
	roads.extend(connect_nodes[6:])
	return roads
	
def get_geo_nodes():
	nodes = list(get_hexagon(hex_start_x, hex_start_y))
	# find start for second hex
	x, y = nodes[4]
	nodes.extend(get_hexagon(x, y))
	return nodes
	
def roads_to_nodes(roads):
	nodes = []
	
	for road in roads:
		nodes.append(road[0])
		
	nodes.append(roads[-1][1])
	return nodes
	
def to_adj_list(roads):
	adj_list = {}
	
	for road in roads:
		for v in road:
			if v not in adj_list:
				adj_list[v] = set([])
		adj_list[road[0]].add(road[1])
		adj_list[road[1]].add(road[0])
		
	return adj_list
	
if __name__ == "__main__":
	n = get_geo_nodes()
	print "d = {"
	for i, b in enumerate(n):
		print "\t{} : {},".format(i, b)
	print "}"
	
def get_translation(graph_roads):
	'''Return the basic translation map, which is actually just a list of roads.
	Suppose we have something like (0, 1). That translates to some road on here. Then (1, 0) will translate based on the coordinate for 1... etc.'''
	
	
	road_map = {}
	node_map = {}
	
	# get the scale version of roads and nodes
	scaled_nodes = get_geo_nodes()
	scaled_roads = get_geo_roads(scaled_nodes)
	
	# get adjacency lists...
	scaled_adj_list = to_adj_list(scaled_roads)
	graph_adj_list = to_adj_list(graph_roads)
	
	graph_nodes = roads_to_nodes(graph_roads)
	
	while len(road_map) < len(graph_roads):
		if len(road_map) == 0:
			scaled_road = scaled_roads.pop()
			
		graph_road = graph_roads.pop()
		road_map[graph_road] = scaled_road
		node_map[graph_road[0]] = scaled_road[0]
		node_map[graph_road[1]] = scaled_road[1]
		
		# now find another candidate
	