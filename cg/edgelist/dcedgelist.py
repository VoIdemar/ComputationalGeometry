class DCEdgeList(object):

    NIL = -1

    def __init__(self):
        self.__vertices = []
        self.__faces = []
        self.__halfedges = []
        
    def add_face(self, face):
        self.__faces.append(face)
        
    def add_vertex(self, vertex):
        self.__vertices.append(vertex)
    
    def add_halfedge(self, halfedge):
        self.__halfedges.append(halfedge)
        
    def get_face(self, index):
        return self.__faces[index]
    
    def get_vertex(self, index):
        return self.__vertices[index]
    
    def get_halfedge(self, index):
        return self.__halfedges[index]