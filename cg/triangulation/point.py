class Point(object):
    
    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y
    
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
    
    def is_below(self, point):
        return self.__y < point.y or (self.__y == point.y and self.__x > point.x)
    
    def is_above(self, point):
        return self.__y > point.y or (self.__y == point.y and self.__x < point.x)
        
    def __eq__(self, point):
        if type(self) <> type(point):
            return False
        return self.__x == point.x and self.__y == point.y