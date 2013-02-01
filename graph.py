from collections import deque
from graph_creator import *

class Graph():
	def __init__(self):
		# internal graph representation
		self._adjacency_list = {}
	
		self.reset_path_search_vars()
		
		self._road_list = []
		self._node_list = []
		self._added_index = 0
		
	def path_to_nodes(self, path):
		nodes = []
		
		for road in path:
			nodes.append(road[0])
			
		nodes.append(path[-1][1])
		return nodes
		
	def merge_at_node(self, node):
		'''Try to merge everything in self._ps at the given road.'''
		
		path_list = list(self._ps)
		# m = False
		
		for i, p1 in enumerate(path_list):
			p1_nodes = self.path_to_nodes(p1)
			# print p1_nodes
		
			if node not in p1_nodes:
				# print "{} not in {}".format(node, p1_nodes)
				continue
		
			for j, p2 in enumerate(path_list[i + 1:]):
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
				
				# create a new path
				p_new = tuple([tuple(reversed(road)) for road in p1[p1_i:]])
				p_new += p2[p2_i:]
				# print "+ {}".format(p_new)
				self._ps.add(p_new)
				
		# if not m:
			# print "No merge occured"
		# else:
			# print "hooray for merge!"
				
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
		self._ps = set([]) # set of added paths
		self._n = None # next road to look at
		self._a = None # current road
		self._needs_reset = False # whether the whole thing has been stepped through
				
	def can_add_road(self):
		'''Return True iff there are more queued roads to add.'''
		
		return self._added_index < len(self._road_list)
				
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
		if self._added_index > 0:
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
			self.p = self.p[:self._pi] + ((v1, v2), ) + self.p[self._pi + 1:]

	def get_frontier(self):
		frontier = set([(self._a[1], v) for v in self._adjacency_list[self._a[1]]])
		frontier.difference_update(set(self.p)) # remove everything in the current set
		frontier.difference_update(set([tuple(reversed(road)) for road in self.p]))
		#print set([tuple(reversed(road)) for road in self.p])
		frontier.difference_update(self._v)
		return frontier
		
	def get_seed(self):
		for v, adj_set in self._adjacency_list.iteritems():
			if len(adj_set) == 1:
				return (v, list(adj_set)[0])
		k = self._adjacency_list.keys()[0] # random dude
		return (k, list(self._adjacency_list[k])[0])
		
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
			self._ps.add(self.p)
			
			# print self._adjacency_list[self._a[0]]
			# do a merge, but only if there is branching here
			if len(self._adjacency_list[self._a[0]]) == 3 or \
			(len(self._adjacency_list[self._a[0]]) == 2 and self._pi < 0):
				# print "Merge condition activated @ {}".format(self._a[0])
				self.merge_at_node(self._a[0])
			
			if self._pi < 0:
				self._needs_reset = True
				return False # means we're done (back at the seed, and nowhere to go)
			
			self._n = self.p[self._pi]
			#self._front = False
		else:
			self._pi += 1
			self._n = self._f[0]
			#self._front = True
			
		return True # means we're not done yet
		

	def get_roads(self):
		return self._road_list[:self._added_index]
		
	def get_nodes(self):
		return self._node_list
		
	def get_paths(self, compute_all=False):
		'''Just return current state of this variable.'''
	
		if compute_all:
			while self.next_step():
				pass
			
		return self._ps
		
	def get_longest_path_length(self, recompute=False):
		if len(self._ps) == 0:
			return 0
		else:
			return max(map(len, self._ps))
			
	def get_num_roads_placed(self):
		return self._added_index
		
	def get_active_node(self):
		if self._a is None:
			return None
		else:
			return self._a[0]
		
	def get_frontier_nodes(self):
		return [road[0] for road in self._f]
		
	def get_visited_nodes(self):
		return [road[0] for road in self._v]
		
if __name__ == "__main__":	
	g = Graph()
	# load_loop(g)
	load_long_line(g)
	
	s = ""
	keep_going = True
	debug = True
	
	# there are only 2 roads
	g.add_road()
	#g.add_road()
	
	# now there are 3 roads
	#g.add_road()
	
	# and 4....
	#g.add_road()
	
	# and 5...
	#g.add_road()
	
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
	
	