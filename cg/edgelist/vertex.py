from dcedgelist import DCEdgeList


class Vertex(object):

    def __init__(self, x=0, y=0, edge=DCEdgeList.NIL):
        self.__x = x
        self.__y = y
        self.__incidentEdge = edge
    
    @property
    def x(self):
        return self.__x
    
    @x.setter
    def x(self, value):
        self.__x = value
    
    @property
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, value):
        self.__y = value
    
    @property
    def incident_edge(self):
        return self.__incidentEdge
    
    @incident_edge.setter
    def incident_edge(self, value):
        self.__incidentEdge = value
        
    def __eq__(self, vertex):
        if type(self) <> type(vertex):
            return False
        return (self.__x == vertex.x and self.__y == vertex.y and 
                self.__incidentEdge == vertex.incident_edge)