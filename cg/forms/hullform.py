from PyQt4 import QtGui, QtCore

from cg.basic.algorithms import convex_hull
from cg.polygons.polygon import Polygon
from cg.polygons.drawer import PolygonQtDrawer

class HullForm(QtGui.QWidget):
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.points = []
        self.convex_hull = None
        self.drawer = PolygonQtDrawer()
        self.drawer.pen.setWidth(3)        
        self.drawPolygon = False
        
        self.buildHullBtn = QtGui.QPushButton(u'Build convex hull', self)
        self.buildHullBtn.clicked.connect(self.build_hull)
        
        self.clearScreenBtn = QtGui.QPushButton(u'Clear screen', self)
        self.clearScreenBtn.clicked.connect(self.clear_screen)
        
        self.buttons = []
        self.buttons.append(self.buildHullBtn)
        self.buttons.append(self.clearScreenBtn)
        
        self.setGeometry(100, 100, 1000, 600)
        self.set_position()
      
    def mousePressEvent(self, event):
        self.points.append((event.x(), event.y()))
        self.repaint()     
    
    def paintEvent(self, event):
        self.drawer.draw(self, QtCore.Qt.blue, points=self.points)
        self.drawer.draw(self, QtCore.Qt.blue, polygon=self.convex_hull)
    
    def resizeEvent(self, event):
        self.set_position()
    
    def build_hull(self):        
        self.convex_hull = Polygon(convex_hull(*self.points))        
        self.repaint()
    
    def clear_screen(self):
        self.points = []
        self.convex_hull = None
        self.repaint()
               
    def set_position(self):
        w, h = self.geometry().width(), self.geometry().height()  
        upperMargin = h - 100
        for k in range(0, len(self.buttons)):
            self.buttons[k].setGeometry(w - 150, upperMargin + k*35, 120, 30)
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = HullForm()
    form.setWindowTitle(u'Graham scan algorithm of building convex hulls')
    form.show()
    sys.exit(app.exec_())