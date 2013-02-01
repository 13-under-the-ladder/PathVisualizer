from collections import deque
from graph_creator import *

class Graph():
	def __init__(self):
		# internal graph representation
		self._adjacency_list = {}
	
		self._prev_ps = []
		self._ps = []
	
		self.reset_path_search_vars()
		
		self._road_list = []
		self._node_list = []
		self._added_index = 0
	
		self._translation = None
		
	def set_translation(self, t):
		self._translation = t
		
	def path_to_nodes(self, path):
		'''Return the a list of nodes (in order) along the length of this path.'''
	
		nodes = []
		
		for road in path:
			nodes.append(road[0])
			
		if len(path) > 0:
			nodes.append(path[-1][1])
		return nodes
		
	def merge_at_node(self, node):
		'''Try to merge everything in self._ps at the given road.'''
		
		# path_list = list(self._ps)
		# m = False
		
		for i, p1 in enumerate(self._ps):
			p1_nodes = self.path_to_nodes(p1)
			# print p1_nodes
		
			if node not in p1_nodes:
				# print "{} not in {}".format(node, p1_nodes)
				continue
		
			for j, p2 in enumerate(self._ps[i + 1:]):
				p2_nodes = self.path_to_nodes(p2)
				# print ":", 
				# print p2_nodes
			
				if node not in p2_nodes:
					# print "{} not in {}".format(node, p2_nodes)
					continue
					
				# alrighty, then...
				# so definitely the same road node in both guys...
				p1_i = p1_nodes.index(node)
				p2_i = p2_nodes.index(node)
				
				# m = True
				
				if self.can_merge(p1[p1_i:], p2[p2_i:]):
					# create a new path
					p_new = tuple([tuple(reversed(road)) for road in p1[p1_i:]])
					p_new += p2[p2_i:]
					# print "+ {}".format(p_new)
					if not self.is_connected(p_new):
						print "** Tried to merge {} and {} @ {}".format(p1, p2, node)
						print "** Got disconncted road {}".format(p_new)
						print "** {} + {}".format(tuple([tuple(reversed(road)) for road in p1[p1_i:]]), p2[p2_i:])
					self.add_to_path_set(p_new)
				
		# if not m:
			# print "No merge occured"
		# else:
			# print "hooray for merge!"
			
	def is_connected(self, path):
		'''Return True iff the given path is connected.'''
		
		for i in range(len(path) - 1):
			if path[i][1] != path[i + 1][0]: # obviously 2 endpoints don't matter
				return False
		return True
			
	def add_to_path_set(self, new_path):
		if new_path in self._ps:
			return False
		else:
			if new_path in self._prev_ps and self._prev_ps.index(new_path) < len(self._ps):
				self._ps.insert(self._prev_ps.index(new_path), new_path)
			else:
				self._ps.append(new_path)
			return True
			
			
	def can_merge(self, p1, p2):
		'''Return True iff path p1 and path p2 can merge.
		Requirements:
			- these paths cannot have any roads in common
		'''
		
		p1_roads = set(p1)
		p1_roads.update(set(reversed(p1)))
		p2_roads = set(p2)
		p2_roads.update(set(reversed(p2)))
		
		return len(p1_roads.intersection(p2_roads)) == 0
				
	def queue_road(self, v1, v2):
		self._road_list.append((v1, v2))
		self.add_node(v1)
		self.add_node(v2)
		
	def add_node(self, v):
		if v not in self._node_list:
			self._node_list.append(v)
				
	def reset_path_search_vars(self):
		self._f = set([]) # the frontier set of roads (only useful for visual debugger; this is culled to get self._n)
		self.p = tuple([]) # the current path
		self._pi = 0 # the index along that path
		self._v = set([]) # set of visited roads
		if len(self._ps) > 0:
			self._prev_ps = self._ps[:]
		self._ps = [] # LIST!!! of added paths
		self._n = None # next road to look at
		self._a = None # current road
		self._needs_reset = False # whether the whole thing has been stepped through
				
	def can_add_road(self):
		'''Return True iff there are more queued roads to add.'''
		
		return self._added_index < len(self._road_list)
		
	def can_remove_road(self):
		'''Return True iff there are more added roads to remove.'''
	
		return self._added_index > 0
	
	def add_road(self):
		'''Add a queued road.
		Many things reset.'''
			
		if self.can_add_road():
			self.adjacent_add(*self._road_list[self._added_index])
			self._added_index += 1
			self.reset_path_search_vars()
			return True
		else:
			return False
		
	def remove_last_road(self):
		if self.can_remove_road():
			self._added_index -= 1
			self.adjacent_remove(*self._road_list[self._added_index])
			self.reset_path_search_vars()
			return True
		else:
			return False
	def adjacent_remove(self, v1, v2):
		self._adjacency_list[v1].discard(v2)
		self._adjacency_list[v2].discard(v1)
				
	def adjacent_add(self, v1, v2):
		'''Add v1, v2 to adjacency list.'''
		
		if v1 not in self._adjacency_list:
			self._adjacency_list[v1] = set([])
		if v2 not in self._adjacency_list:
			self._adjacency_list[v2] = set([])
		
		self._adjacency_list[v1].add(v2)
		self._adjacency_list[v2].add(v1)
		
	def add_link(self, v1, v2):
		'''assume this is all kosher.'''
		
		if (v1, v2) not in self.p:
			# when you add a link, don't keep the stuff after the position of the link
			self.p = self.p[:self._pi] + ((v1, v2), ) #+ self.p[self._pi + 1:]

	def get_frontier(self):
		frontier = set([(self._a[1], v) for v in self._adjacency_list[self._a[1]]])
		frontier.difference_update(set(self.p)) # remove everything in the current set
		frontier.difference_update(set([tuple(reversed(road)) for road in self.p]))
		#print set([tuple(reversed(road)) for road in self.p])
		frontier.difference_update(self._v)
		return frontier
		
	def get_seed(self):
		'''Return a starting road. Prefer roads with fewest links.
		If no roads are added, return None.'''
	
		if self._added_index == 0:
			return None
			
		choices = sorted(list(self._adjacency_list.items()), key=lambda item: len(item[1]))
		
		for v1, v2_set in choices:
			for v2 in v2_set:
				if (v1, v2) not in self._v:
					return (v1, v2)
		return None # all visited
	
		# old stuff
		# for v, adj_set in self._adjacency_list.iteritems():
			# if len(adj_set) == 1:
				# link = (v, list(adj_set)[0])
				# if link not in self._v:
					# return link
		# k = self._adjacency_list.keys()[0] # random dude
		# return (k, list(self._adjacency_list[k])[0])
		
	def next_step(self):
		if self._added_index == 0:
			return False # we're done if there are no roads
		if self._needs_reset:
			return False
	
		if self._n is None:
			self._n = self._seed = self.get_seed()
			#self._front = True
			
		# transfer from next_step to active
		self._a = self._n
		self.add_link(*self._a)
			
		self._f = list(self.get_frontier())
		
		if len(self._f) == 0:
			self._pi -= 1
			self._v.add(self._a)
			self._v.add(tuple(reversed(self._a)))
			self.add_to_path_set(self.p)
			
			# print self._adjacency_list[self._a[0]]
			# do a merge, but only if there is branching here
			if len(self._adjacency_list[self._a[0]]) == 3 or \
			(len(self._adjacency_list[self._a[0]]) == 2 and self._pi < 0):
				# print "Merge condition activated @ {}".format(self._a[0])
				self.merge_at_node(self._a[0])
			
			if self._pi < 0:
				# start somewhere else
				seed = self.get_seed()
				if seed is None:
					self._needs_reset = True
					return False # means we're done (back at the seed, and nowhere to go)
				else:
					# keep ps the same, active node updated later, frontier updated later, keep visited same
					self.p = tuple([]) # new path
					self._pi = 0 # new index on path
					self._seed = self._n = seed
					return True # means we're not done yet
			
			# this has to be behind the exit check otherwise bad pointer on self.p
			self._n = self.p[self._pi]
			#self._front = False
		else:
			self._pi += 1
			self._n = self._f[0]
			#self._front = True
			
		return True # means we're not done yet
		

	def get_roads(self):
		return self.translate_roads(self._road_list[:self._added_index])
		
	def get_nodes(self):
		return self.translate_nodes(self._node_list)
		
	def get_node_label(self, index):
		if self._translation is None:
			return str(index)
		else:
			return str(self._node_list[index])
		
	def get_paths(self, compute_all=False):
		'''Just return current state of this variable.'''
	
		if compute_all:
			while self.next_step():
				pass
		
		return [self.translate_roads(path) for path in self._ps]
		
	def get_longest_path_length(self, recompute=False):
		if len(self._ps) == 0:
			return 0
		else:
			sorted_paths = sorted(self._ps, key=lambda p: len(p)) # make sure this is not in-place
			print "Longest path = {}".format(sorted_paths[-1])
			return len(sorted_paths[-1])
			# return max(map(len, self._ps))
			
	def get_num_roads_placed(self):
		return self._added_index
		
	def get_active_node(self):
		if self._a is None:
			return None
		else:
			return self.translate_nodes([self._a[0]])[0]
			
	def translate_roads(self, roads):
		if self._translation is None:
			return roads
		else:
			return tuple([tuple([self._translation[node] for node in road]) for road in roads])
			
	def translate_nodes(self, nodes):
		if self._translation is None:
			return nodes
		else:
			return [self._translation[node] for node in nodes]
		
	def get_frontier_nodes(self):
		return self.translate_nodes([road[0] for road in self._f])
		
	def get_visited_nodes(self):
		return self.translate_nodes([road[0] for road in self._v])
		
if __name__ == "__main__":	
	g = Graph()
	# load_loop(g)
	load_ship_wheel(g)
	
	while g.add_road():
		pass
		
	# print g.get_seed()
	# exit(0)
	
	s = ""
	keep_going = True
	debug = False
	
	if debug:
		while s != "quit" and keep_going:
			s = raw_input(" ****************** Type 'quit' to stop: ")
			if s != "quit":
				keep_going = g.next_step()
				
				print "Active = {}".format(g._a)
				# print "Next = {}".format(g._n)
				# print "Visited = {}".format(g._v)
				# print "Path = {}".format(g.p)
				print "Path set = {}".format(g._ps)
				print "Longest road = {}".format(g.get_longest_path_length())
				# print "Path Index = {}".format(g._pi)
				# print "Frontier = {}".format(g._f)
	else:
		while g.next_step():
			pass
			
	print "#" * 20 + " DONE! " + "#" * 20
	print "Final Path set:"
	for path in g.get_paths():
		if not isinstance(path, tuple):
			print "!!!!!"
		print path
	
	