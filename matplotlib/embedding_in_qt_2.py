#!/home/adonis/anaconda3/bin/python3		
# -*- coding: utf-8 -*-

import sys
#from matplotlib.backends.qt_compat import is_pyqt5

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout,QSlider
from PyQt5 import QtCore

#from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
#if is_pyqt5():
    #from matplotlib.backends.backend_qt5agg import (
        #FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


import random

class Window(QDialog):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)

		# a figure instance to plot on
		self.figure = plt.figure()

		# this is the Canvas Widget that displays the `figure`
		# it takes the `figure` instance as a parameter to __init__
		self.canvas = FigureCanvas(self.figure)
		
		self.figure2 = plt.figure()
		self.canvas2 = FigureCanvas(self.figure2)

		# this is the Navigation widget
		# it takes the Canvas widget and a parent
		self.toolbar = NavigationToolbar(self.canvas, self)

		# Just some button connected to `plot` method
		self.button = QPushButton('Plot')
		self.button.clicked.connect(self.plot)

		self.slider = QSlider(QtCore.Qt.Horizontal)
		#self.slider.setOrientation(QtCore.Qt.Horizontal)
		self.slider.setMinimum(1)
		self.slider.setMaximum(1000)
		self.slider.setTickInterval(5)
		self.slider.valueChanged.connect(self.valueChangedSlider)
		print(self.slider.pageStep() )
		# set the layout
		layout = QVBoxLayout()
		layout2 = QHBoxLayout()
		
		layout.addWidget(self.toolbar)
		layout.addWidget(self.canvas)
		
		#layout.addWidget(layout2)
		#layout2.addWidget(self.canvas)
		#layout2.addWidget(self.canvas2)
		
		
		layout.addWidget(self.button)
		layout.addWidget(self.slider)
		self.setLayout(layout)
	
	def valueChangedSlider(self):
		print(self.slider.value())

	def plot(self):
	  ''' plot some random stuff '''
	  # random data
	  data = [random.random() for i in range(110)]

	  # instead of ax.hold(False)
	  self.figure.clear()

	  # create an axis
	  ax = self.figure.add_subplot(111)

	  # discards the old graph
	  # ax.hold(False) # deprecated, see above

	  # plot data
	  ax.plot(data, '*-')

	  # refresh canvas
	  self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
