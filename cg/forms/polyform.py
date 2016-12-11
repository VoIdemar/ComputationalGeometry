from PyQt4 import QtGui, QtCore

from cg.basic.primitives import point2d
from cg.polygons.polygon import Polygon
from cg.polygons.drawer import PolygonQtDrawer
from cg.clipping.algorithms import sutherland_hodgman

class PolygonsForm(QtGui.QWidget):
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.currentPolygon = None
        self.polygons = []
        self.intersection = []
        self.drawer = PolygonQtDrawer()
        self.drawPolygon = False
        
        self.createPolygonBtn = QtGui.QPushButton(u'Create polygon', self)
        self.createPolygonBtn.clicked.connect(self.create_polygon)
        
        self.finishPolygonCreationBtn = QtGui.QPushButton(u'Finish', self)
        self.finishPolygonCreationBtn.clicked.connect(self.finish_polygon)
        self.finishPolygonCreationBtn.setEnabled(False)
        
        self.createRandomPolygonBtn = QtGui.QPushButton(u'Random polygon', self)        
        self.createRandomPolygonBtn.clicked.connect(self.create_random_polygon)
        
        self.findIntersectionBtn = QtGui.QPushButton(u'Find intersection', self)
        self.findIntersectionBtn.clicked.connect(self.find_intersection)
        
        self.deletePolygonsBtn = QtGui.QPushButton(u'Delete polygons', self)
        self.deletePolygonsBtn.clicked.connect(self.delete_polygons)
        
        self.buttons = []
        self.buttons.append(self.findIntersectionBtn)
        self.buttons.append(self.createPolygonBtn)
        self.buttons.append(self.finishPolygonCreationBtn)
        self.buttons.append(self.deletePolygonsBtn)
        self.buttons.append(self.createRandomPolygonBtn)
        
        self.xEdit = QtGui.QLineEdit(u'300', self)
        self.yEdit = QtGui.QLineEdit(u'300', self) 
        self.aEdit = QtGui.QLineEdit(u'50', self)
        self.bEdit = QtGui.QLineEdit(u'100', self)
        self.thetaEdit = QtGui.QLineEdit(u'150', self)
        
        self.radioDefault = QtGui.QRadioButton(u'Default algorithm', self)
        self.radioSutherland = QtGui.QRadioButton(u'Sutherland-Hodgman algorithm', self)
        self.radioDefault.setChecked(True)
        
        self.radioButtonGroup = QtGui.QGroupBox('Algorithms', self)
        self.radioButtons = []
        self.radioButtons.append(self.radioDefault)
        self.radioButtons.append(self.radioSutherland)
        
        self.textBoxes = []
        self.textBoxes.append(self.xEdit)
        self.textBoxes.append(self.yEdit)
        self.textBoxes.append(self.aEdit)
        self.textBoxes.append(self.bEdit)
        self.textBoxes.append(self.thetaEdit)
        
        self.propsLabel = QtGui.QLabel(u'Random polygon properties:', self)
        self.xLabel = QtGui.QLabel(u'x: ', self)
        self.yLabel = QtGui.QLabel(u'y: ', self)
        self.aLabel = QtGui.QLabel(u'a: ', self)
        self.bLabel = QtGui.QLabel(u'b: ', self)
        self.thetaLabel = QtGui.QLabel(u'Theta: ', self)
        
        self.propsLabels = []
        self.propsLabels.append(self.xLabel)
        self.propsLabels.append(self.yLabel)
        self.propsLabels.append(self.aLabel)
        self.propsLabels.append(self.bLabel)
        self.propsLabels.append(self.thetaLabel)
        
        self.labelsLayout = QtGui.QGridLayout()
        for i in range(0, len(self.propsLabels)):
            self.labelsLayout.addWidget(self.propsLabels[i], i, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignHCenter)
        for i in range(0, len(self.textBoxes)):
            self.labelsLayout.addWidget(self.textBoxes[i], i, 1, QtCore.Qt.AlignLeft | QtCore.Qt.AlignHCenter)
        
        self.randomPolygonPropsPanelWidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self.randomPolygonPropsPanelWidget)
        self.verticalLayout.addWidget(self.propsLabel)
        self.verticalLayout.addLayout(self.labelsLayout)
        
        self.radioGroupLayout = QtGui.QVBoxLayout(self)
        for button in self.radioButtons:
            self.radioGroupLayout.addWidget(button)
        self.radioButtonGroup.setLayout(self.radioGroupLayout)
        
        self.setGeometry(100, 100, 1000, 600)
        self.set_position()
      
    def mousePressEvent(self, event):
        if self.drawPolygon:
            self.currentPolygon.points.append(point2d(event.x(), event.y()))
            self.repaint()     
    
    def paintEvent(self, event):
        for polygon in self.polygons:
            self.drawer.draw(self, QtCore.Qt.black, polygon=polygon)
        for polygon in self.intersection:
            self.drawer.draw(self, QtCore.Qt.red, polygon=polygon)
    
    def resizeEvent(self, event):
        self.set_position()
    
    def find_intersection(self):
        
        intersect_polygons = ((lambda p1, p2: p1.find_intersection(p2)) if self.radioDefault.isChecked() else
                              (lambda p1, p2: [sutherland_hodgman(p1, p2)]) if self.radioSutherland.isChecked() else
                              lambda p1, p2: p1)
        
        if len(self.polygons) > 1:
            self.intersection = intersect_polygons(self.polygons[0], self.polygons[1])
            for polygon in self.polygons[2:]:
                newIntersect = []
                for intersect in self.intersection:
                    newIntersect = newIntersect + intersect_polygons(intersect, polygon)                    
                self.intersection = newIntersect
            self.repaint()
    
    def create_polygon(self):
        self.currentPolygon = Polygon()
        self.polygons.append(self.currentPolygon)
        self.drawPolygon = True
        for button in self.buttons:
            button.setEnabled(False)
        self.finishPolygonCreationBtn.setEnabled(True)
        for textBox in self.textBoxes:
            textBox.setEnabled(False)
    
    def delete_polygons(self):
        self.polygons = []
        self.currentPolygon = None
        self.intersection = []
        self.repaint()
    
    def finish_polygon(self):
        self.currentPolygon = None
        self.drawPolygon = False
        for button in self.buttons:
            button.setEnabled(True)
        self.finishPolygonCreationBtn.setEnabled(False)
        for textBox in self.textBoxes:
            textBox.setEnabled(True)
    
    def create_random_polygon(self):
        try:
            x, y = float(self.xEdit.text()), float(self.yEdit.text())
            a, b = float(self.aEdit.text()), float(self.bEdit.text())
            theta = float(self.thetaEdit.text())
            self.polygons.append(Polygon.create_random_polygon( (x, y), a, b, theta ))
            self.repaint()
        except ValueError:
            QtGui.QMessageBox.about(self, u'Data format error', u'Wrong format of random polygon properties, they should be floating-point numbers')
               
    def set_position(self):
        w, h = self.geometry().width(), self.geometry().height()  
        upperMargin = h - 330
        self.radioButtonGroup.setGeometry(w - 200, upperMargin-100, 190, 80)
        for k in range(0, len(self.buttons)):
            self.buttons[k].setGeometry(w - 150, upperMargin + k*35, 120, 30)
        self.randomPolygonPropsPanelWidget.setGeometry(w - 200, upperMargin + len(self.buttons)*35, 200, 150)