from path_graphics import PathDrawer
#from path_engine import PathEngine
from Tkinter import Tk
# from graph import Graph
from graph import Graph
from graph_creator import *

'''
The double-hexagon reveals a problem in my program: it doesn't detect the figure-8 path.
Not sure what causes this bug, but it's not really a priority.
'''

def connect_nodes(nodes):
	'''Connect the nodes consecutively.'''
	
	roads = []
	
	for i in range(len(nodes) - 1):
		roads.append((nodes[i], nodes[i + 1]))
		
	return roads

def create_road_nexus():
	'''Road systems meeting.'''
	
	nodes = [
		 (50, 50),
		 (150, 50),
		 (200, 100),
		 (250, 150)
	]
	
	roads = connect_nodes(nodes)
	roads.append(((200, 100), (250, 50)))
	
	nodes = [
		 (300, 50),
		 (350, 50),
		 (400, 100),
		 (450, 150)
	]
	
	roads.extend(connect_nodes(nodes))
	roads.append(((400, 100), (450, 50)))
	
	# and connect them
	roads.append(((250, 50), (300, 50)))
	
	return roads

def create_double_hexagon():
	'''Create a figure-8.'''
	
	# first settlement and associated building
	v1 = [
		(100, 100),
		(200, 100),
		(250, 150),
		# now build away from the hex, maybe down
		(350, 150),
		(400, 200),
		(350, 250)
	]
	
	roads = connect_nodes(v1)
	
	v2 = [
		(100, 200),
		(200, 200),
		(250, 250)#,
		#(200, 300)
	]
	
	
	roads.extend(connect_nodes(v2))
	
	# connect first hexagon
	roads.append(((250, 250), (350, 250)))
	# connect at branch
	roads.append(((200, 200), (250, 150)))
	# connect second hexagon
	roads.append(((100, 200), (50, 150)))
	roads.append(((50, 150), (100, 100)))
	return roads

def create_road_octopus():
	'''Create a road with many branches.'''
	
	nodes = [
		# straight-forward line
		(50, 100),
		(150, 100),
		(200, 150),
		(250, 150),
		(300, 200),
		(400, 200),
		(450, 150)
	]
	
	roads = connect_nodes(nodes)
	
	# branch 1
	roads.append(((200, 150), (150, 200)))
	# branch 2
	roads.append(((300, 200), (250, 250)))
	# branch 3
	roads.append(((400, 200), (450, 250)))
	# branch 4
	roads.append(((250, 150), (300, 100)))
	
	return roads

def late_connected_hexagon():
	# first settlement and associated building
	v1 = [
		(100, 100),
		(200, 100),
		(250, 150),
		# now build away from the hex, maybe down
		(350, 150),
		(400, 200),
		(350, 250)
	]
	
	roads = connect_nodes(v1)
	
	v2 = [
		(100, 200),
		(200, 200),
		(250, 250),
		(200, 300),
		(100, 300)
	]
	
	roads.extend(connect_nodes(v2))
	# connect at branch
	roads.append(((200, 200), (250, 150)))
	# connect at start
	roads.append(((100, 200), (50, 150)))
	roads.append(((50, 150), (100, 100)))
	return roads

def create_roads_hexagon():
	'''Create a complete hexagon (loop)'''
	
	v = [
		(100, 100),
		(200, 100),
		(250, 150),
		(200, 200),
		(100, 200),
		(50, 150)
	]
	
	return connect_nodes(v)

def create_hexagon_on_stick():
	r = create_roads_hexagon()
	r.append(((250, 150), (350, 150)))
	return r

def create_roads():
	'''Create the roads that will later be added.
	Return them as a list.'''
	
	# first settlement
	s0 = (100, 100)
	
	# second settlement
	s1 = (100, 300)
	
	return [
	   # G1
	   # one way from s0
	   (s0, (150, 100)),
	   # other way from s0
	   (s0, (50, 150)),
	   # extend from 150
	   ((150, 100), (200, 100)),
	   # branch at 150 
	   ((150, 100), (200, 150)),
	   # extend branch
	   ((200, 150), (250, 150)),
	   # discontinuous site (G2)
	   (s1, (150, 250)),
	   (s1, (50, 250)),
	   # extend G2
	   ((150, 250), (100, 200)),
	   ((100, 200), (50, 150)),
	   ((100, 200), (150, 200)),
	   # branch off G2
	   ((150, 250), (200, 250)),
	   ((200, 250), (250, 200)),
	   
	   # join G2 to G1 at middle
	   #((250, 200), (200, 150)),
	   # another branch off G2
	   ((200, 250), (250, 250)),
	]

if __name__ == "__main__":
	root = Tk()
	graph = Graph()
	
	# for road in create_double_hexagon():
		# graph.queue_road(*road)
	load_loop(graph)
	
	
	g = PathDrawer(root, graph)
	
	root.mainloop()