class EventPoint(object):
    
    __INCOMPATIBLE_TYPE_ERROR = 'Incompatible types: EventPoint and %(conflicted)s'
    
    def __init__(self, x, y):
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
        
    def __lt__(self, eventPoint):
        if type(self) <> type(eventPoint):
            raise TypeError(EventPoint.__INCOMPATIBLE_TYPE_ERROR % {'conflicted' : type(eventPoint).__name__})
        return (self.y > eventPoint.y) or (self.y == eventPoint.y and self.x < eventPoint.x)
    
    def __ge__(self, eventPoint):
        return not self < eventPoint
    
    def __eq__(self, eventPoint):
        if type(self) <> type(eventPoint):
            return False
        return self.x == eventPoint.x and self.y == eventPoint.y
    
    def __cmp__(self, eventPoint):
        return (-1 if self < eventPoint else
                 0 if self == eventPoint else
                 1)
        
    def __hash__(self):        
        return (self.__x, self.__y).__hash__()
        
    def __str__(self):
        return str((self.__x, self.__y))