'''
Created on Jan 29, 2013
@author: Daniel Kats

This file draws the graph, in all its glory.
'''

from Tkinter import *

class PathDrawer(Frame):
	'''
	Main class for drawing the graph. Main frame of Tkinter app.
	'''
	
	# dimensions
	_height = 600
	_width = 600
	
	# size for nodes
	_node_radius = 10
	
	# distance between paths
	_road_offset = 3
	
	# colors for paths
	_path_colors = ["red", "orange",  "purple", "cyan", "green", "grey", "lightgreen", "yellow", "blue"]
	
	_node_colors = {
		"unvisited" : "white",
		"visited" : "grey",
		"explored" : "black",
		"frontier" : "yellow",
		"active" : "red",
	}

	def __init__(self, root, model):
		Frame.__init__(self, root)
		self.pack()
		
		self._root = root
		
		self._canvas = Canvas(self, height=self._height, width=self._width)
		self._canvas.pack()
		
		# a model to keep nodes in
		self._node_sprites = []
		self._visual_debugger = False
		
		self._engine = model
		
		self.draw()
		
	def set_node_state(self, i, state):
		'''Set a node to be visited.
		i is the node index.'''
		
		# print "!!!" + self._node_colors[state]
		self._canvas.itemconfigure(self._node_sprites[i], fill=self._node_colors[state])
		
	def clear_graph(self):
		'''Remove all graph-related drawings from canvas.'''
		
		for item in self._canvas.find_withtag("road"):
			self._canvas.delete(item)
			
		for item in self._canvas.find_withtag("path"):
			self._canvas.delete(item)
			
		#for item in self._canvas.find_withtag("node"):
		#	self._canvas.delete(item)
		
	def redraw_graph(self):
		self.clear_graph()
		self.draw(redraw=True)
		
	def draw(self, redraw=False):
		'''Draw everything.'''
		
		# draw all the roads
		for road in self._engine.get_roads():
			self.draw_road(road[0], road[1])
		
		if not redraw:
			# draw all the nodes
			for node in self._engine.get_nodes():
				self.draw_node(node)
				
		if not redraw:
			# add the controller button
			self.add_road_buttons()
		
		# draw all the paths
		self.draw_paths()
		
	def set_longest_road_length(self):
		self._longest_road.set("Longest road length: %d" % self._engine.get_longest_path_length(False))
		self._num_roads_placed.set("Number of roads placed: %d" % self._engine.get_num_roads_placed())
		
	def update_nodes(self):
		nodes = self._engine.get_nodes()
		
		for i, node in enumerate(nodes):
			self.set_node_state(i, "unvisited")
			
		for node in self._engine.get_visited_nodes():
			i = nodes.index(node)
			self.set_node_state(i, "explored")
		
		for node in self._engine.get_frontier_nodes():
			i = nodes.index(node)
			self.set_node_state(i, "frontier")
			
			
		node = self._engine.get_active_node()
		print "Active node = {}".format(node)
		if node is not None:
			i = nodes.index(node)
			self.set_node_state(i, "active")
		
		
	def next_step(self):
		'''Show next step in debugger.'''
		
		more = self._engine.next_step()
		self.update_nodes()
		self.set_longest_road_length()
		
		if not more:
			self._road_step_button.config(text="Stop Visual Debugger")
			self._road_step_button.config(command=self.disable_vis_debugger)
			
	def enable_vis_debugger(self):
		self._road_step_button.config(text="Step")
		self._road_step_button.config(command=self.next_step)
		self._visual_debugger_status_label.set("Visual debugger is on")
		
	def disable_vis_debugger(self):
		self._road_step_button.config(text="Start Visual Debugger")
		self._road_step_button.config(command=self.enable_vis_debugger)
		self._road_step_button.config(state=DISABLED)
		self._visual_debugger_status_label.set("Visual debugger is off")
		self._engine.reset_path_search_vars()
		self.update_nodes()
		self.redraw_graph()
		
	def add_next_road(self):
		'''Show the addition of another path.
		TODO for now turn into step...'''
		
		self._engine.add_road()
		self._road_step_button.config(state=NORMAL)
		
		self.update_nodes()
		self.redraw_graph()
		
			
	def draw_paths(self):
		'''Draw all the paths as a series of roads.
		Each path is represented by a different color.'''
		
		print "There are {} paths".format(self._engine.get_paths())
		
		
		for path_index, path in enumerate(self._engine.get_paths()):
			#for road_index in range(len(path) - 1):
			#self.draw_road(path[road_index], path[road_index + 1], path_index + 1)
			for road in path:
				self.draw_road(road[0], road[1], path_index + 1)
				
		#print "**** Drawing ****"
		#for p in self._paths:
		#	print p
		#print "**** End drawing ****"
		
	def create_longest_road_label(self):
		self._longest_road = StringVar()
		self._longest_road.set("No roads added")
		
		return Label(
			self,
			textvar=self._longest_road
		)
		
	def remove_last_road(self):
		'''Remove the last added road.'''
		
		self._engine.remove_last_road()
		self.set_longest_road_length()
		
		# remove the paths already on the canvas
		for item in self._canvas.find_withtag("path"):
			self._canvas.delete(item)
			
		self.draw_paths()
		
	def add_road_buttons(self):
		'''Add a button to control addition of new roads.'''
		
		self._road_button = Button(
			self,
			text="Add Road",
			command=self.add_next_road
		)
		
		self._road_step_button = Button(
			self,
			text="Enable Visual Debugger",
			command=self.enable_vis_debugger,
			state=DISABLED
		)
		
		self._no_road_button = Button(
			self,
			text="Remove Road",
			command=self.remove_last_road
		)
		
		# more or less arbitrary placement
		self._canvas.create_window(100, 500, window=self._road_button, anchor=W)
		self._canvas.create_window(250, 500, window=self._no_road_button, anchor=W)
		self._canvas.create_window(400, 500, window=self._road_step_button, anchor=W)
		self._canvas.create_window(200, 550, window=self.create_longest_road_label(), anchor=E)
		self._canvas.create_window(400, 550, window=self.create_num_roads_placed_label(), anchor=E)
		self._canvas.create_window(self._width - 200, 20, window=self.create_vis_debugger_label(), anchor=W)
		
	def create_vis_debugger_label(self):
		self._visual_debugger_status_label=StringVar()
		self._visual_debugger_status_label.set("Visual debugger is off")
	
		return Label(
			self,
			textvar=self._visual_debugger_status_label
		)
		
	def create_num_roads_placed_label(self):
		self._num_roads_placed = StringVar()
		self._num_roads_placed.set("No roads added")
		
		return Label(
			self,
			textvar=self._num_roads_placed
		)
		
	def draw_nodes(self, nodelist):
		for node in nodelist:
			self.draw_node(node)
			
	def draw_road(self, v1, v2, index=0):
		'''Draw a road from v1 to v2, colors are optional.
		The index refers to the offset from the other roads.'''
		
		self._canvas.create_line(
			v1[0], 
			v1[1] + index * self._road_offset, 
			v2[0], 
			v2[1] + index * self._road_offset, 
			fill=self._path_colors[index % len(self._path_colors)], 
			width=1.5, 
			tags="road" if index == 0 else "path"
		)
		
		# also label the roads
		# if index == 0:
			# n = self._engine.get_roads().index((v1, v2))
			# l = Label(self, text=str(n))
			# self._canvas.create_window((v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2 + 5, window=l)
		
	def draw_node(self, v):
		'''Draw a node at v.'''
		
		n = self._engine.get_nodes().index(v)
		
		l = Label(self, text=str(n))#chr(n + 65))
		self._canvas.create_window(v[0] - self._node_radius, v[1] - self._node_radius - 15, window=l)
		self._node_sprites.append(
			self._canvas.create_oval(
				v[0] + self._node_radius, 
				v[1] + self._node_radius, 
				v[0] - self._node_radius, 
				v[1] - self._node_radius, 
				#fill="black",
				tags="node"
			)
		)
		
		self.set_node_state(n, "unvisited")
		