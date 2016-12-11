from PyQt4 import QtGui, QtCore

class PolygonQtDrawer(object):
       
    def __init__(self):        
        self.__drawer = QtGui.QPainter()
        self.__pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)        
        
    def draw(self, paintDevice, color, polygon=None, points=None):
        self.__drawer.begin(paintDevice)
        self.__pen.setColor(color)
        self.__drawer.setPen(self.__pen)
        self.__drawer.setRenderHint(self.__drawer.Antialiasing)
        self.__draw_polygon(polygon)
        self.__draw_points(points)
        self.__drawer.end()
    
    @property
    def pen(self):
        return self.__pen
    
    @property
    def painter(self):
        return self.__drawer
    
    def __draw_points(self, points):
        if not (points is None):
            for point in points:
                x, y = point
                self.__drawer.drawPoint(x, y)
    
    def __draw_polygon(self, polygon):
        if not (polygon is None):
            pointsCount = len(polygon.points)  
            if pointsCount > 0:
                (x, y) = polygon.points[0]             
                if pointsCount >= 2:
                    points = polygon.points + [(x, y)]
                    for i in range(0, pointsCount):
                        (x1, y1), (x2, y2) = points[i:i+2]
                        self.__drawer.drawLine(x1, y1, x2, y2)
                else:
                    self.__drawer.drawPoint(x, y)