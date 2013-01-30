from collections import deque
from sys import stderr
from utils import *

'''
This file deals with the "model" representation of the graph/road visualizer.
'''

class Graph(object):
    '''The graph object.'''

    def __init__(self):
        '''Create a new graph object.'''
        
        # the queue of roads waiting to be added
        self._road_queue = deque()
        # the queue of added roads, not including queued roads above
        self._added_road_queue = deque()
        
        # this is a list instead of a set for easy node labelling
        self._nodes = [] # contains all nodes added or pending
        # this is not strictly-speaking needed... or used ... 
        self._roads = [] # contains all roads, added or pending
        # maps each node to a list of other nodes that node is adjacent to
        self._adjacency_list = {} # the representation by which paths are computed
        # set of all paths in the graph
        self._all_paths = set([]) 
        # True if I have to recompute self._all_paths
        self._changed = False
        
    def adjacent_add(self, v1, v2):
        '''Add v1, v2 to adjacency list.'''
        
        if v1 not in self._adjacency_list:
            self._adjacency_list[v1] = set([])
        if v2 not in self._adjacency_list:
            self._adjacency_list[v2] = set([])
            
        self._adjacency_list[v1].add(v2)
        self._adjacency_list[v2].add(v1)
        
    def add_road(self, v1, v2):
        '''This is a stub function for plug-and-play with pyCatan. Hope it has the right stuff in it...'''
        
        self.adjacent_add(v1, v2)
    
    def queue_road(self, v1, v2):
        '''Queue a road to be added.'''
        
        road = (v1, v2)
        self._road_queue.append(road)
        self._roads.append(road)
        
        if v1 not in self._nodes:
            self._nodes.append(v1)
        if v2 not in self._nodes:
            self._nodes.append(v2)
        
    def get_longest_path_length(self):
        '''Return the length of the longest path in this graph.
        Makes sure all disconnected portions of the graph are visited.'''
        
        if self._changed:
            # recompute paths
            self._all_paths = self.get_paths()
        
        if len(self._all_paths) == 0:
            return 0
        else:
#            for path in self._all_paths:
#                print "P: " + self.path_to_str(path)
        
            # -1 because path_length = nodes_on_path - 1
            return max([len(path) for path in self._all_paths]) - 1
        
    def path_to_str(self, path):
        '''Return string representation of the path based on the index of each node in the path.'''
        
        return ", ".join([str(self._nodes.index(node)) for node in path])
            
    def path_to_roads(self, path):
        '''Convert a path to a generator for roads, going node by node from beginning to end of path.'''
        
        for i in range(len(path) - 1):
            yield (path[i], path[i + 1])
            
    def cut_loop(self, path):
        '''Return None if cutting the loop leads to a retarded road (disconnected).
        Return the path resulting in cutting a loop otherwise.'''
        
        roads = tuple(self.path_to_roads(path))
        new_roads = []
        has_loop = False
        
        # this cuts out all looping roads
        for i, road in enumerate(roads):
            # make sure to check both directions for roads
            if road not in roads[i + 1:] and (road[1], road[0]) not in roads[i + 1:]:
                new_roads.append(road)
            elif not has_loop:
                has_loop = True
        
        # the has_loop variable isn't strictly necessary, but avoids extraneous computation
        if has_loop:
            new_path = [new_roads[0][0]]
            # now make sure it still makes sense
            for i in range(1, len(new_roads)):
                if new_roads[i - 1][1] == new_roads[i][0]:
                    new_path.append(new_roads[i][0])
                else:
                    return None
                    
            return tuple(new_path + [new_roads[-1][1]])
        else:
            return path
        
    def merge(self, v_seed, path_set):
        '''Modify the pathset. By looking for a merger of roads at node v_seed'''
        
#        print "*** start merge ***"
#        print "@ {}".format(self._nodes.index(v_seed))
#        combo = []
        path_list = list(path_set)
        
        for i in range(len(path_list)):
            for j in range(i + 1, len(path_list)):
                if v_seed in path_list[i] and v_seed in path_list[j]:
                    # then combine them
                    index_i = path_list[i].index(v_seed)
                    index_j = path_list[j].index(v_seed)
                    p1_old = tuple(reversed(path_list[j][index_j : ])) + path_list[i][index_i + 1:]
                    p1 = self.cut_loop(p1_old)
#                    if p1_old != p1:
#                        print "L- " + self.path_to_str(p1_old)
#                        if p1:
#                            print "L+ " + self.path_to_str(p1)
                    
                    if p1 is not None and self.can_merge(path_list[i], path_list[j], v_seed):
                        if index_i == index_j == 0:
#                            print "X %s" % self.path_to_str(path_list[i])
#                            print "X %s" % self.path_to_str(path_list[j])
                            path_set.discard(path_list[i])
                            path_set.discard(path_list[j])
                        if tuple(reversed(p1)) not in path_set:
                            path_set.add(p1)
#                        print "+ %s" % self.path_to_str(p1)
#                        combo.append(p1)
        
#        print "*** end merge ***"
        
    def get_all_paths(self, v_seed, path=None, visited=None, root=True):
        '''Return all the paths stemming from the given vertex.
        Paths may not have loops, but may *be* a single loop.
        v_seed - the seed vertex/node
        path - the path from the root node to this node
        visited - the set of visited nodes
        root - whether is the root node'''
        
        if path is None:
            path = []
        if visited is None:
            visited = set([])
        
        path_set = set([])
        visited.add(v_seed)
        
        try:
            for adj_v in self._adjacency_list[v_seed]:
                if adj_v not in path:
                    p_new = path[:] + [v_seed]
                    adj_path_set, adj_visited = self.get_all_paths(adj_v, p_new)
                    visited.update(adj_visited)
                    
                    path_set.update(adj_path_set) # path is an extension of p_new
        except KeyError:
            # should not happen, but for emergency, dump some info
            print >>stderr, "{} not in adjacency list".format(v_seed)
            print >>stderr, "Adjacency list:"
            print >>stderr, print_dict(self._adjacency_list)
                    
        if len(path_set) == 0:
            new_path = tuple(path + [v_seed])
            path_set.add(new_path)
        elif len(path_set) >= 2:
            self.merge(v_seed, path_set)
            
        if root:
            self.cleanup(path_set)
            
        return path_set, visited
    
    def can_merge(self, p1, p2, mergept):
        '''You can merge two points at the mergept if:
        - there is a mergept
        - the paths go in different directions after leaving the mergept.'''
        
        ti_1 = p1.index(mergept)
        ti_2 = p2.index(mergept)
        return p1[ti_1] == p2[ti_2] and p1[ti_1 + 1] != p2[ti_2 + 1]
    
    def remove_last_road(self):
        if len(self._added_road_queue) == 0:
            return False
        else:
            r = self._added_road_queue.pop()
            self._road_queue.appendleft(r)
            self.remove_road(*r)
            self._changed = True
            return True
        
    def remove_road(self, v1, v2):
        '''Remove the road given by (v1, v2) from the adjacency list.'''
        
        self._adjacency_list[v1].discard(v2)
        self._adjacency_list[v2].discard(v1)
        
    def add_next_road(self):
        '''Transfer a road from the queue and put it in the graph.
        Return True if a new road was added, False otherwise.'''
        
        if len(self._road_queue) == 0:
            return False
        else:
            r = self._road_queue.popleft()
            self._added_road_queue.append(r)
#            print "#" * 20
            self.add_road(*r)
            self._changed = True
            return True
        
    def get_num_roads_placed(self):
        '''Return the number of roads placed so far on the graph.'''
        
        return len(self._added_road_queue)
        
    def get_nodes(self):
        '''Return a list of all the nodes in the graph.'''
        
        return self._nodes
    
    def get_roads(self):
        '''Return the set of all roads/edges in the graph - placed and queued'''
        
        return self._roads
    
    def cleanup(self, path_set):
        '''Only run right before return. Eliminates subsets caused by loops with branches.
        Runs in really bad time. Final cleanup operation to remove subsets.
        When we talk about subsets, we are talking about roads, not vertices.'''
        
        sorted_path_list = sorted(path_set, key=tuple.__len__)
        full_path_list = []
        
        for path in sorted_path_list:
            s = set([])
            
            for i in range(len(path) - 1):
                # for algo to work, must add paths in both directions
                s.add((path[i], path[i + 1]))
                s.add((path[i + 1], path[i]))
                
            full_path_list.append(s)
        
        for i in range(len(full_path_list)):
            for j in range(len(full_path_list) - 1, i, -1):
                if full_path_list[i].issubset(full_path_list[j]):
                    path_set.discard(sorted_path_list[i])
#                    print "- " + self.path_to_str(sorted_path_list[i])
    
    def get_paths(self):
        '''Return a set of all paths found in this graph.
        Save this, and return the same set until more queued roads are placed on the graph.'''
        
        if self._changed:
            d = set(filter(lambda x: len(self._adjacency_list[x]) > 0, self._adjacency_list.keys()))
            self._all_paths = set([])
            
            while len(d) > 0:
                v_seed = d.pop()
                all_paths_v, all_visited_v = self.get_all_paths(v_seed)
                self._all_paths.update(all_paths_v)
                d.difference_update(all_visited_v)
                
            self._changed = False
        
        if len(self._all_paths) > 0:
            print "#" * 50
            for p in self._all_paths:
                print self.path_to_str(p)
        return self._all_paths
                    
if __name__ == "__main__":
    g = Graph()
    
    p = (0, 1, 2, 3, 4, 5, 8, 7, 2, 1, 0)
    print tuple(g.path_to_roads(p))
    print g.cut_loop(p)
    
#    g.queue_road((0, 0), (100, 100))
#    g.queue_road((100, 100), (150, 100))
#    g.queue_road((100, 100), (150, 150))
#    g.queue_road((150, 150), (200, 150))
#    
#    for i, node in enumerate(g.get_nodes()):
#        print "{} --> {}".format(i, node)
#    
#    while g.add_next_road():
#        pass
#    
#    print g.get_longest_path_length()
    
    
        
        