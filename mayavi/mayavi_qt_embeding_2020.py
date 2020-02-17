#!/home/adonis/anaconda3/envs/plotenv/bin/python3		

from PyQt5 import  QtWidgets
import os
import numpy as np
from numpy import cos
from mayavi.mlab import contour3d

os.environ['ETS_TOOLKIT'] = 'qt4'
from pyface.qt import QtGui, QtCore
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor


## create Mayavi Widget and show

class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')
    def update_plot(self):
    ## PLot to Show        
        x, y, z = np.ogrid[-3:3:60j, -3:3:60j, -3:3:60j]
        t = 0
        Pf = 0.45+((x*cos(t))*(x*cos(t)) + (y*cos(t))*(y*cos(t))-(z*cos(t))*(z*cos(t)))
        obj = contour3d(Pf, contours=[0], transparent=False)

    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                resizable=True )

class MayaviQWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.visualization = Visualization()

        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)


#### PyQt5 GUI ####
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

    ## MAIN WINDOW
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(200,200,1100,700)

    ## CENTRAL WIDGET
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

    ## GRID LAYOUT
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")


    ## BUTTONS
        self.button_default = QtWidgets.QPushButton(self.centralwidget)
        self.button_default.setObjectName("button_default")
        self.gridLayout.addWidget(self.button_default, 0, 0, 1,1)

        self.button_previous_data = QtWidgets.QPushButton(self.centralwidget)
        self.button_previous_data.setObjectName("button_previous_data")
        self.gridLayout.addWidget(self.button_previous_data, 1, 1, 1,1)
    ## Mayavi Widget 1    
        container = QtGui.QWidget()
        mayavi_widget = MayaviQWidget(container)
        self.gridLayout.addWidget(mayavi_widget, 1, 0,1,1)
    ## Mayavi Widget 2
        container1 = QtGui.QWidget()
        mayavi_widget = MayaviQWidget(container1)
        self.gridLayout.addWidget(mayavi_widget, 0, 1,1,1)

    ## SET TEXT 
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Simulator"))
        self.button_default.setText(_translate("MainWindow","Default Values"))
        self.button_previous_data.setText(_translate("MainWindow","Previous Values"))
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
