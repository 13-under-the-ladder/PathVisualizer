from collections import deque
from sys import stderr

'''
Note that when representing the path, it might be easier to represent it as a sequence of roads instead...
Or not...
'''

def print_dict(d):
    '''Return intuitive textual representation for a dict.'''
    
    s = ""
    
    for k, v in d.iteritems():
        s += "{} ---> {}\n".format(k, v)
        
    return s

class Graph(object):
    

    def __init__(self):
        self._road_queue = deque()
        
        #TODO for now
        self._nodes = []#set([])
        self._roads = set([])
        self._adjacency_list = {}
        
        self._all_paths = set([])
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
        # is that it???
        self.adjacent_add(v1, v2)
    
    def queue_road(self, v1, v2):
        road = (v1, v2)
        self._road_queue.append(road)
        self._roads.add(road)
        
        #TODO for now
        if v1 not in self._nodes:
            self._nodes.append(v1)
        if v2 not in self._nodes:
            self._nodes.append(v2)
        
    def get_longest_path_length(self):
        '''Return the length of the longest path in this graph.
        Makes sure all disconnected portions of the graph are visited.
        Q: Accounts for cycles???'''
        
        if self._changed:
            self._all_paths = self.get_paths()
        
        if len(self._all_paths) == 0:
            return 0
        else:
            print "::"
            for path in self._all_paths:
                #TODO for now
                self.simple_print_path(path)
        
            # -1 because path_length = nodes_on_path - 1
            return max([len(path) for path in self._all_paths]) - 1
        
    def path_to_str(self, path):
        return ", ".join([str(self._nodes.index(node)) for node in path])
        
    def simple_print_path(self, path):
        try:
            print self.path_to_str(path)
        except ValueError:
#            print >>stderr, node
            print >>stderr, self._nodes
            
    def path_to_roads(self, path):
        for i in range(len(path) - 1):
            yield (path[i], path[i + 1])
            
    def cut_loop(self, path):
        '''Return None if cutting the loop leads to a retarded road.
        Return the road resulting in cutting a loop.'''
        
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
        
#        if has_loop:
        new_path = [new_roads[0][0]]
        # now make sure it still makes sense
        for i in range(1, len(new_roads)):
            if new_roads[i - 1][1] == new_roads[i][0]:
                new_path.append(new_roads[i][0])
            else:
                return None
                
        return tuple(new_path + [new_roads[-1][1]])
#        else:
#            return path
        
    def merge(self, v_seed, path_set):
        '''Modify the pathset.'''
        
        print "*** start merge ***"
        print "@ {}".format(self._nodes.index(v_seed))
        
        path_list = list(path_set)
        combo = []
        
        #TODO for debugging
        print "Before merge:"
        for p in path_list:
            self.simple_print_path(p)
        
        for i in range(len(path_list)):
            for j in range(i + 1, len(path_list)):
                if v_seed in path_list[i] and v_seed in path_list[j]:
                    # then combine them
                    index_i = path_list[i].index(v_seed)
                    index_j = path_list[j].index(v_seed)
                    p1_old = tuple(reversed(path_list[j][index_j : ])) + path_list[i][index_i + 1:]
                    p1 = self.cut_loop(p1_old)
                    if p1_old != p1:
                        print "L- " + self.path_to_str(p1_old)
                        if p1:
                            print "L+ " + self.path_to_str(p1)
#                    # fixes looping
#                    start_loop = end_loop = None
#                    
#                    # from the front
#                    for node_i, node in enumerate(p1):
#                        if p1.count(node) > 1:
#                            if start_loop is None:
#                                start_loop = node_i
##                                print "L %d" % node_i 
#                            end_loop = node_i
#                        else:
#                            break
#                    if start_loop is None:
#                        for node_i in range(len(p1) - 1, -1, -1):
#                            node = p1[node_i]
#                            if p1.count(node) > 1:
#                                if start_loop is None:
#                                    start_loop = node_i
#                                end_loop = node_i
#                            else:
#                                break
                        
#                    if start_loop is not None and end_loop is not None:
#                        if start_loop > 0 and p1.count(p1[-1]) == 1: 
#                            # cannot cut in the middle of the thing
#                            continue
#                        print "L- " + self.path_to_str(p1)
#                        p1 = p1[:start_loop] + p1[end_loop:]
#                        print "L {}, {}".format(start_loop, end_loop)
#                        print "L+ " + self.path_to_str(p1)
                    
                    if p1 is not None and self.can_merge(path_list[i], path_list[j], v_seed):
                        if index_i == index_j == 0:
                            print "X %s" % self.path_to_str(path_list[i])
                            print "X %s" % self.path_to_str(path_list[j])
                            path_set.discard(path_list[i])
                            path_set.discard(path_list[j])
                        if tuple(reversed(p1)) not in path_set:
                            path_set.add(p1)
                        print "+ %s" % self.path_to_str(p1)
                        combo.append(p1)
        
        if len(combo) > 0:
            print "Result:"
            for path in path_set:
                self.simple_print_path(path)
        print "*** end merge ***"
        
    def get_all_paths(self, v_seed, path=None, visited=None):
        root = (path is None)
        
        if root:
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
        '''DO NOT MERGE CYCLES'''
        
        ti_1 = p1.index(mergept)
        ti_2 = p2.index(mergept)
        return p1[ti_1] == p2[ti_2] and p1[ti_1 + 1] != p2[ti_2 + 1]
        
    def add_next_road(self):
        if len(self._road_queue) == 0:
            return False
        else:
            r = self._road_queue.popleft()
            print "#" * 20
            
            print "added :"
            self.simple_print_path(r)
            
            self.add_road(*r)
            self._changed = True
            return True
        
    def get_num_roads_placed(self):
        return len(self._roads) - len(self._road_queue)
        
    def get_nodes(self):
        return self._nodes
    
    def get_roads(self):
        return self._roads
    
    def cleanup(self, path_set):
        '''Runs in really bad time. Final cleanup operation to remove subsets.
        Make sure when we talk about subsets, we are talking about roads, not vertices.'''
        
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
                    print "- " + self.path_to_str(sorted_path_list[i])
    
    def get_paths(self):
        if self._changed:
            d = set(self._adjacency_list.keys())
            self._all_paths = set([])
            
            while len(d) > 0:
                v_seed = d.pop()
                all_paths_v, all_visited_v = self.get_all_paths(v_seed)
                self._all_paths.update(all_paths_v)
                d.difference_update(all_visited_v)
                
            self._changed = False
        
        #for p in self._all_paths:
        #    print p
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
    
    
        
        