from dcedgelist import DCEdgeList


class Face(object):

    def __init__(self, outerComp=None, innerComps=[]):
        self.__outerComp = outerComp
        self.__innerComps = innerComps
        
    @property
    def outer_comp(self):
        return self.__outerComp
    
    @outer_comp.setter
    def outer_comp(self, value):
        self.__outerComp = value
        
    def get_inner_comps(self):
        return self.__innerComps[:]
    
    def add_inner_comp(self, innerComp):
        self.__innerComps.append(innerComp)
    
    def remove_inner_comp(self, innerComp):
        self.__innerComps.remove(innerComp)
    
    def __eq__(self, face):
        if type(self) <> type(face):
            return False
        return self.__outerComp == face.outer_comp and self.__innerComps == face.get_inner_comps()