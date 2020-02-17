#!/home/adonis/anaconda3/bin/python3		
# -*- coding: utf-8 -*-

# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
import os
# os.environ['ETS_TOOLKIT'] = 'qt4'
# By default, the PySide binding will be used. If you want the PyQt bindings
# to be used, you need to set the QT_API environment variable to 'pyqt'
# os.environ['QT_API'] = 'pyqt'

# To be able to use PySide or PyQt4 and not run in conflicts with traits,
# we need to import QtGui and QtCore from pyface.qt
# from pyface.qt import QtGui, QtCore
# Alternatively, you can bypass this line, but you need to make sure that
# the following lines are executed before the import of PyQT:
#from PyQt4 import QtGui, QtCore
#import sip
#sip.setapi('QString', 2)
#from PySide import QtGui, QtCore

#from matplotlib.backends.backend_qt5agg import FigureCanvas,NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as MPLCanvas,NavigationToolbar2QT as NavigationToolbar

from traits.api import HasTraits, Instance, on_trait_change,Str,Float,Range
from traitsui.api import View, Item
from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from pylab import *
from mayavi import mlab

from matplotlib.pyplot import figure

		################################################################################
#The actual visualization
def curve(n_mer, n_long):
	dphi = pi/1000.
	phi = arange(0.0, 2*pi + 0.5*dphi, dphi, 'd')
	mu = phi*n_mer
	x = cos(mu) * (1 + cos(n_long * mu/n_mer)*0.5)
	y = sin(mu) * (1 + cos(n_long * mu/n_mer)*0.5)
	z = 0.5 * sin(n_long*mu/n_mer)
	t = sin(mu*4)
	return x, y, z, t

class Visualization(HasTraits):
	scene = Instance(MlabSceneModel, ())
	#plot = Instance(PipelineBase)
	#def __init__(self, parent=None):
		#print "self",self
		#self.scene = Instance(MlabSceneModel, ())
	# the layout of the dialog screated
	view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
						height=250, width=300, show_label=False),
				 resizable=True # We need this to resize with the parent widget
				 )
	def __init__(self, **traits):#(self, parent=None):
		super(Visualization, self).__init__(**traits)
		print ("self",self)

	@on_trait_change('scene.activated')
	def update_plot(self):
		print( "update_plot",self)
		# This function is called when the view is opened. We don't
		# populate the scene when the view is not yet open, as some
		# VTK features require a GLContext.
		
		# We can do normal mlab calls on the embedded scene.
		#self.scene.mlab.test_points3d_anim()
		#self.scene.mlab.test_mesh()
		
		#self.scene.mlab.test_simple_surf_anim()
		#self.scene.mlab.test_surf()
		#self.scene.mlab.test_fancy_mesh()
		#self.scene.mlab.test_quiver3d_2d_data()
		#self.scene.mlab.test_quiver3d()

		#x, y, z, t = curve(randint(10)+5, randint(10)+2)
		x, y, z, t = curve(10, 11)
		#if self.plot is None:
		print (len(x))
		self.plot = self.scene.mlab.plot3d(x*5, y*5, z*5+6, t,  tube_radius=0.1, colormap="winter",opacity=1)#'Spectral'
		#self.plot = self.scene.mlab.surf(x=arange(20),y=arange(20),s=randn(20,20),opacity=.8,representation='wireframe')
		self.nappe = self.scene.mlab.surf(randn(20,20),opacity=1,representation='wireframe')#'points')#

		#dphi, dtheta = pi / 250.0, pi / 250.0
		#[phi, theta] = mgrid[0:pi + dphi * 1.5:dphi,
								 #0:2 * pi + dtheta * 1.5:dtheta]
		#m0 = 4
		#m1 = 3
		#m2 = 2
		#m3 = 3
		#m4 = 6
		#m5 = 2
		#m6 = 6
		#m7 = 4
		#r = sin(m0 * phi) ** m1 + cos(m2 * phi) ** m3 + \
		#sin(m4 * theta) ** m5 + cos(m6 * theta) ** m7
		#x = r * sin(phi) * cos(theta)
		#y = r * cos(phi)
		#z = r * sin(phi) * sin(theta)
		#self.mesh = self.scene.mlab.mesh(x,y,z,opacity=1., colormap='bone')#'points')#
				
		#self.plot.mlab_source.set(x=x, y=y, z=z, scalars=t)

	
################################################################################
# The QWidget containing the visualization, this is pure PyQt4 code.
class Reservoir(HasTraits):
    name = Str
    max_storage = Float(1e6, desc='Maximal storage [hm3]')
    max_release = Float(10, desc='Maximal release [m3/s]')
    head = Float(10, desc='Hydraulic head [m]')
    efficiency = Range(0, 1.)

    traits_view = View(
        'name', 'max_storage', 'max_release', 'head', 'efficiency',
        title = 'Reservoir',
        resizable = True,
    )

    def energy_production(self, release):
        ''' Returns the energy production [Wh] for the given release [m3/s]
        '''
        power = 1000 * 9.81 * self.head * release * self.efficiency 
        return power * 3600
        
class TraitsQWidget(QtGui.QWidget):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self, parent)
		layout = QtGui.QVBoxLayout(self)
		layout.setContentsMargins(0,0,0,0)
		layout.setSpacing(0)
		self.visualization = Reservoir(
                        name = 'Project A',
                        max_storage = 30,
                        max_release = 100.0,
                        head = 60,
                        efficiency = 0.8
                    )
		self.ui = self.visualization.edit_traits(parent=self,
															 kind='subpanel').control
		layout.addWidget(self.ui)
		self.ui.setParent(self)
        
class MayaviQWidget(QtGui.QWidget):
	def __init__(self,parent=None, tmr=200):
		QtGui.QWidget.__init__(self, parent)
		layout = QtGui.QVBoxLayout(self)
		layout.setContentsMargins(0,0,0,0)
		layout.setSpacing(0)
		self.visualization = Visualization()

		# If you want to debug, beware that you need to remove the Qt
		# input hook.
		#QtCore.pyqtRemoveInputHook()
		#import pdb ; pdb.set_trace()
		#QtCore.pyqtRestoreInputHook()

		# The edit_traits call will generate the widget to embed.
		self.ui = self.visualization.edit_traits(parent=self,
															 kind='subpanel').control
		layout.addWidget(self.ui)
		self.ui.setParent(self)
		self.timer=self.startTimer(tmr)

	def timerEvent(self, e):#http://docs.enthought.com/mayavi/mayavi/mlab_animating.html
		print( "timerEvent")
		self.visualization.nappe.mlab_source.scalars =randn(20,20)
		#self.visualization.nappe.mlab_source.set(scalars =randn(20,20))
		
		#si les dimensions changent: reset
		#i=randint(8,16)
		#x, y = np.mgrid[0:3:1.0/(i+2),0:3:1.0/(i+2)]
		#sc = np.asarray(x*x*0.05*(i+1), 'd')
		#self.visualization.nappe.mlab_source.reset(x=x,y=y,scalars=sc)
		#self.visualization.scene.reset_zoom()
		#self.visualization.update_plot()
			
		

		#x, y, z, t = curve(randint(10)+5, randint(10)+2)
		#self.visualization.plot.mlab_source.set(x=x, y=y, z=z, scalars=t)
		#print mlab.surf(randn(15,15), figure=self.visualization.scene.mayavi_scene)

		pass
		

if __name__ == "__main__":
	# Don't create a new QApplication, it would unhook the Events
	# set by Traits on the existing QApplication. Simply use the
	# '.instance()' method to retrieve the existing one.
	app = QtGui.QApplication.instance()
	container = QtGui.QWidget()
	container.setWindowTitle("Embedding Mayavi in a PyQt4 Application")
	# define a "complex" layout to test the behaviour
	layout = QtGui.QGridLayout(container)
	
	# put some stuff around mayavi
	#label_list = []
	for i in range(3):
		for j in range(3):
			if (i==1 and j==1):	continue
			if (i==1 and j==2):	continue
			if (i==0 and j==2):	continue
			if (i==2) and (j==2):continue
			label = QtGui.QPushButton(container)
			label.setText("Your QWidget at (%d, %d)" % (i,j))
			#label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
			layout.addWidget(label, i, j)
			#label_list.append(label)
	mayavi_widget = MayaviQWidget(container,1000)
	layout.addWidget(mayavi_widget, 0, 1)
	traits_widget =    TraitsQWidget(container)
	layout.addWidget(traits_widget, 1, 1)
	fig,ax=subplots()
	canvas = MPLCanvas(fig)
	layout.addWidget(canvas, 1, 2)
	toolbar = NavigationToolbar(canvas,container)
	layout.addWidget(toolbar,2,2)
	ax.plot(randn(25))

	#mayavi_widget = MayaviQWidget(container,1000)
	#layout.addWidget(mayavi_widget, 1, 2)
	container.show()
	window = QtGui.QMainWindow()
	window.setCentralWidget(container)
	window.show()
	
	# Start the main event loop.
	app.exec_()
	
