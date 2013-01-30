'''
Created on Jan 29, 2013

@author: dan
'''

from Tkinter import *

class PathDrawer(Frame):
    '''
    classdocs
    '''
    
    _height = 600
    _width = 600
    
    _node_radius = 5
    
    _road_offset = 3
    
    _path_colors = ["red", "orange",  "purple", "cyan", "green", "grey", "lightgreen", "yellow", "blue"]


    def __init__(self, root, model):
        Frame.__init__(self, root)
        self.pack()
        
        self._root = root
        
        self._canvas = Canvas(self, height=self._height, width=self._width)
        self._canvas.pack()
        
        self._engine = model
        
        self.draw()
        
    def draw(self):
        '''Draw everything.'''
        
        # draw all the roads
        for road in self._engine.get_roads():
            self.draw_road(road[0], road[1])
            
        # draw all the nodes
        for node in self._engine.get_nodes():
            self.draw_node(node)
            
        # add the controller button
        self.add_road_buttons()
        
        # draw all the paths
        self.draw_paths()
        
    def set_longest_road_length(self):
        self._longest_road.set("Longest road length: %d" % self._engine.get_longest_path_length())
        self._num_roads_placed.set("Number of roads placed: %d" % self._engine.get_num_roads_placed())
        
    def add_next_road(self):
        '''Show the addition of another path.'''
        
        self._engine.add_next_road()
        self.set_longest_road_length()
        
        # remove the paths already on the canvas
        for item in self._canvas.find_withtag("path"):
            self._canvas.delete(item)
            
        self.draw_paths()
        
            
    def draw_paths(self):
        '''Draw all the paths as a series of roads.
        Each path is represented by a different color.'''
        
        for path_index, path in enumerate(self._engine.get_paths()):
            for road_index in range(len(path) - 1):
                self.draw_road(path[road_index], path[road_index + 1], path_index + 1)
                
        #print "**** Drawing ****"
        #for p in self._paths:
        #    print p
        #print "**** End drawing ****"
        
    def create_longest_road_label(self):
        self._longest_road = StringVar()
        self._longest_road.set("No roads added")
        
        return Label(
            self,
            textvar=self._longest_road
        )
        
    def add_road_buttons(self):
        '''Add a button to control addition of new roads.'''
        
        self._road_button = Button(
            self,
            text="Add Road",
            command=self.add_next_road
        )
        
        # more or less arbitrary placement
        self._canvas.create_window(100, 500, window=self._road_button, anchor=S)
        self._canvas.create_window(200, 550, window=self.create_longest_road_label(), anchor=E)
        self._canvas.create_window(400, 550, window=self.create_num_roads_placed_label(), anchor=E)
        
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
        
    def draw_node(self, v):
        '''Draw a node at v.'''
        
        n = self._engine.get_nodes().index(v)
        
        l = Label(self, text=str(n))
        self._canvas.create_window(v[0] - self._node_radius - 10, v[1] - self._node_radius - 10, window=l)
        self._canvas.create_oval(v[0] + self._node_radius, v[1] + self._node_radius, v[0] - self._node_radius, v[1] - self._node_radius, fill="black")
        