class EventQueueEntry(object):
    
    def __init__(self):
        self.__eventpoint = None
        self.__segments = []
       
    @property 
    def eventpoint(self):
        return self.__eventpoint
    
    @eventpoint.setter
    def eventpoint(self, value):
        self.__eventpoint = value
    
    @property
    def segments(self):
        return self.__segments
    
    @segments.setter
    def segments(self, value):
        self.__segments = value
        
    def __lt__(self, entry):
        return self.__eventpoint < entry.eventpoint
    
    def __eq__(self, entry):
        return self.__eventpoint == entry.eventpoint
    
    def __cmp__(self, entry):
        return (-1 if self < entry else
                 0 if self == entry else
                 1)