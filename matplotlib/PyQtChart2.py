#!/home/adonis/anaconda3/bin/python3	
# -*- coding: utf-8 -*-

# test_scene.py
# integration avec les widgets

##

import sys
#from Ui_test_scene import Ui_MainWindow
from PyQt5.QtCore import Qt, pyqtSlot, QObject, pyqtSignal, QT_VERSION_STR
from PyQt5.QtGui import QPolygonF,QBrush, QPen, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow,                    \
                            QGraphicsScene, QGraphicsView, QGraphicsItem, \
                            QGraphicsEllipseItem, QColorDialog,QGridLayout
print(sys.version)
import numpy as np  
#from pylab import randn,arange                     

from PyQt5.uic import loadUi
from PyQt5.QtChart import QChart, QLineSeries,QSplineSeries, QChartView,PYQT_CHART_VERSION_STR
print("PYQT_CHART_VERSION:",PYQT_CHART_VERSION_STR)
print("QT VERSION:",QT_VERSION_STR)

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget

#class MainWindow(QMainWindow, Ui_MainWindow):
    #def __init__(self, parent=None):
        #super(MainWindow,self).__init__(parent)


def series_to_polyline(xdata, ydata):
    """Convert series data to QPolygon(F) polyline
    This code is derived from PythonQwt's function named 
    `qwt.plot_curve.series_to_polyline`"""
    size = len(xdata)
    polyline = QPolygonF(size)
    pointer = polyline.data()
    dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
    pointer.setsize(2*polyline.size()*tinfo(dtype).dtype.itemsize)
    memory = np.frombuffer(pointer, dtype)
    memory[:(size-1)*2+1:2] = xdata
    memory[1:(size-1)*2+2:2] = ydata
    return polyline  
      
class Chart(QChart):
        def __init__(self):
            super().__init__()

        def mouseMoveEvent(self, event):
            print("Chart.mouseMoveEvent", event.pos().x(), event.pos().y())
            return QChart.mouseMoveEvent(self, event)
       
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("test_scene.ui", self)
        #self.setupUi(self)
        self.scene = QGraphicsScene()
        self.remplirScene()
        self.show()
        for vue in (self.vuePrincipale, self.vueGlobale):
            vue.setScene(self.scene)
            vue.setRenderHints(QPainter.Antialiasing)
            vue.fitInView(self.rectGris,Qt.KeepAspectRatio)            
        self.vueGlobale.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vueGlobale.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vuePrincipale.setDragMode(QGraphicsView.RubberBandDrag)
        self.angleVue = 0.0
        self.zoomPctVue = 1.0
        self.dialRotation.setValue(0)
        self.horizontalSliderZoom.setValue(100)
        self.lineEditTexte.setText("Tous en scène gg!")
        self.scene.selectionChanged.connect(self.onSceneSelectionChanged)
        self.onSceneSelectionChanged()
        
        self.monQtChart=Chart()
        #self.monQtChart.setAnimationOptions(QChart.AllAnimations)
        maligne=QSplineSeries()#QLineSeries()
        tx,ty=np.arange(50),np.random.randn(50)
        maligne.append(series_to_polyline(tx,ty))
        self.monQtChart.addSeries(maligne)
        #maligne=QSplineSeries()#QLineSeries()
        #maligne.append(series_to_polyline(arange(50),randn(50)+1))
        #self.monQtChart.addSeries(maligne)
        #for pts in self.monQtChart.series()[0].pointsVector():  print(pts.x())
        for  marker in self.monQtChart.legend().markers():
          print(  marker)
          #QObject.disconnect(marker, SIGNAL(clicked()), this, SLOT(handleMarkerClicked()))
          #marker.fontChanged.connect(self.toto)
          marker.clicked.connect(self.toto)
        
        self.monQtChart.createDefaultAxes()
        self.monQtChart.legend().setVisible(1);
        #self.monQtChart.addAxis()
        self.monQtChart.setTitle("Simple spline chart example")
        #self.monQtChartView
        self.monQtChartView.setChart(self.monQtChart)
        self.monQtChartView.setRubberBand( QChartView.HorizontalRubberBand )
        
        #self.connect(self.monQtChartView, SIGNAL('activated(const QString &)'),self.colomboActivated)
        #self.monQtChartView.mouseMoved.connect(chartView.chart().mouseMoved)
        self.monpyqtgraph.plot(tx,ty)
        
    def remplirScene(self):
        scene = self.scene
        rectGris = scene.addRect(0,0,200,150,brush=QBrush(Qt.lightGray))
        self.rectGris = rectGris
        self.texte = scene.addText("")
        dy = rectGris.rect().height()-self.texte.sceneBoundingRect().height()
        self.texte.setPos(rectGris.x(),rectGris.y() + dy)
        self.texte.setDefaultTextColor(Qt.cyan)
        #scene.addItem(self.texte)
        d = 48. # diametre smiley
        ox = 4. # largeur oeil
        oy = 6. # hauteur oeil
        smiley = scene.addEllipse(-d/2,-d/2,d,d, brush=QBrush(Qt.yellow))
        yeux = [QGraphicsEllipseItem(-ox/2.,-oy/2.,ox,oy,parent=smiley) \
                for i in range(2)]
        yeux[0].setPos(-d/6,-d/8)
        yeux[1].setPos(+d/6,-d/8)
        brush = QBrush(Qt.black)
        for oeil in yeux:
            oeil.setBrush(brush)
        smiley.setPos(rectGris.mapToScene(rectGris.rect().center()))
        smiley.setRotation(20)
        smiley.setScale(1.5)
        for item in scene.items():
            item.setFlag(QGraphicsItem.ItemIsMovable)
            item.setFlag(QGraphicsItem.ItemIsSelectable)

    def toto(self):
      print("toto",self)
      for  marker in self.monQtChart.legend().markers():
       print(marker)
       marker.series().setVisible(not marker.series().isVisible())
       break
      
    #@pyqtSlot()
    #def on_monQtChartView_mouseMoveEvent(self,event):
     #print("on_monQtChartView_mouseMoveEvent")
       
    @pyqtSlot()
    def on_pushButtonCreerDisque_clicked(self):
        disque = self.scene.addEllipse(0,0,20,20,brush=QBrush(Qt.white),
                                                 pen=QPen(Qt.NoPen))
        disque.setFlag(QGraphicsItem.ItemIsMovable)
        disque.setFlag(QGraphicsItem.ItemIsSelectable)

    @pyqtSlot(str)
    def on_lineEditTexte_textChanged(self,msg):
        self.texte.setPlainText(msg)

    @pyqtSlot()
    def on_pushButtonChangerCouleur_clicked(self):
        itemsSelectionnes = self.scene.selectedItems()
        couleurInit = itemsSelectionnes[0].brush().color()
        couleur = QColorDialog.getColor(couleurInit,self,'Changer la couleur')
        if couleur.isValid():
            pinceau = QBrush(couleur)
            for item in itemsSelectionnes:
                 item.setBrush(pinceau)  

    def onSceneSelectionChanged(self):
        nbElementSelectionnes = len(self.scene.selectedItems())
        self.pushButtonChangerCouleur.setEnabled(nbElementSelectionnes > 0)
        msg = '%d éléments sélectionnés'%nbElementSelectionnes
        self.statusBar().showMessage(msg)

    @pyqtSlot(int)
    def on_dialRotation_valueChanged(self,nouvelAngleVue):
        self.vuePrincipale.rotate(nouvelAngleVue-self.angleVue)
        self.angleVue = nouvelAngleVue
    
    @pyqtSlot(int)
    def on_horizontalSliderZoom_valueChanged(self,nouvZoomPctVue):
        f = (nouvZoomPctVue/100.) / self.zoomPctVue
        self.vuePrincipale.scale(f,f)
        self.zoomPctVue = nouvZoomPctVue/100.


if __name__ == '__main__': 
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
