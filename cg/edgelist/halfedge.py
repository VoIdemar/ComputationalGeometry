from dcedgelist import DCEdgeList


class HalfEdge(object):

    def __init__(self):
        self.__origin = None
        self.__twin = None
        self.__incidentFace = DCEdgeList.NIL
        self.__prev = None
        self.__next = None
    
    @property
    def origin(self):
        return self.__origin

    @origin.setter
    def origin(self, value):
        self.__origin = value

    @property
    def twin(self):
        return self.__twin

    @twin.setter
    def twin(self, value):
        self.__twin = value
    
    @property
    def incident_face(self):
        return self.__incidentFace

    @incident_face.setter
    def incident_face(self, value):
        self.__incidentFace = value
    
    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, value):
        self.__next = value
    
    @property
    def prev(self):
        return self.__prev

    @prev.setter
    def prev(self, value):
        self.__prev = value
    
    def __eq__(self, halfedge):
        if type(self) <> type(halfedge):
            return False
        