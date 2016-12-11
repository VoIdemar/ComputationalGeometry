import sys

sys.path.insert(0, '/cg')

if __name__ == '__main__':
    
    from PyQt4 import QtGui
    from cg.forms.polyform import PolygonsForm   
    
    app = QtGui.QApplication(sys.argv)
    form = PolygonsForm()
    form.setWindowTitle(u'Polygons')
    form.show()
    sys.exit(app.exec_())
