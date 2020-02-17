#!/home/adonis/anaconda3/bin/python		
# -*- coding: utf-8 -*-
# check Python version




"""
import sys                                                                           
from PySide2 import QtCore, QtWidgets                                                
                                                                                     
# Create a Qt application                                                            
app = QtWidgets.QApplication(sys.argv)                                               
                                                                                     
# Create a Window                                                                    
mywindow = QtWidgets.QWidget()                                                       
mywindow.resize(320, 240)                                                                             
mywindow.setWindowTitle('Hello World!')                                                 
                                                                                        
# Create a label and display it all together                                            
mylabel = QtWidgets.QLabel(mywindow)                                                    
mylabel.setText('Hello World!')                                                         
mylabel.setGeometry(QtCore.QRect(200, 200, 200, 200))       
                            
mywindow.show()                                                                         
                                                                                        
# Enter Qt application main loop                                                        
sys.exit(app.exec_())


import sys
import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtGui import *#QColor,QBrush,QMainWindow,QApplication

class MainWindow2(QMainWindow):
	count = 0
	
	def __init__(self, parent = None):
		super(MainWindow2, self).__init__(parent)
		self.mdi = QMdiArea()
		self.setCentralWidget(self.mdi)
		bar = self.menuBar()
		
		file = bar.addMenu("File")
		file.addAction("New")
		file.addAction("cascade")
		file.addAction("Tiled")
		file.triggered[QAction].connect(self.windowaction)
		self.setWindowTitle("MDI demo")
		
	def windowaction(self, q):
		print ("triggered")

		if q.text() == "New":
			MainWindow2.count = MainWindow2.count+1
			sub = QMdiSubWindow()
			sub.setWidget(QTextEdit())
			sub.setWindowTitle("subwindow"+str(MainWindow2.count))
			self.mdi.addSubWindow(sub)
			sub.show()

		if q.text() == "cascade":
			self.mdi.cascadeSubWindows()

		if q.text() == "Tiled":
			self.mdi.tileSubWindows()
		

app = QApplication(sys.argv)
ex = MainWindow2()
ex.show()
sys.exit(app.exec_())
	
#######################


Hi,

I am the author of PyQwt, I do not use it anymore, and I removed PyQwt
from my computers.

I recommend http://www.pyqtgraph.org/

Best regards -- Gerard

pyqtgraph does supoort PyQt5.  From https://github.com/pyqtgraph/pyqtgraph/blob/b700a1ad3d0f9696768774ba47f9a2f07fecd812/README.md:
"""

#######################
import sys,os
os.environ['QT_API']="pyqt"
# os.chdir("/home/adonis/python/matplotlib")
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm
import pylab as pl
from pylab import (c_,clip,rand,r_,randn,unique,uniform,float32,float64,poisson,real, \
			sqrt,ravel,exp,ones_like,arange,int32,empty,linspace,argsort,meshgrid,array)#,shape,cos,pi,reshape,dot,zeros
#from pylab import *
#from numpy.random import randn, multivariate_normal,gamma,rand,beta
from scipy.stats import chi2,norm
#from scipy.stats import gamma as gamscipy
#from scipy.stats import t as studentdis
#from threading import Timer

#from matplotlib.backends.backend_qt5agg import FigureCanvas,NavigationToolbar2QT as NavigationToolbar
######## agg = antigrain rendering ######## 


#import pylab,scipy
#from pyct3d import wishart,initRng,chol_invert
#from numpy.linalg import inv,cholesky
#~ import Image 
#import GibbsDP
#from time import time,sleep
from scipy.linalg import cho_solve,cho_factor
#from scipy.signal import savgol_coeffs
#from scipy.interpolate import griddata#,UnivariateSpline,Rbf, InterpolatedUnivariateSpline
#from scipy.special import betaln,gammaln
#import PySide

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5.QtGui import QColor,QAction,QBrush,QMainWindow,QApplication,QWidget,QVBoxLayout#QPolygonF,QTextEdit, QPen, QPainter,QMouseEvent
from PyQt5.QtCore import Qt,QT_VERSION_STR, pyqtSlot#,QTimer, QObject, pyqtSignal, QEvent
from PyQt5.QtWidgets import QColorDialog,QMdiSubWindow#,QProgressDialog,QGridLayout
#from matplotlib.backends.backend_qt5agg.QtCore import Qt, pyqtSlot, QObject, pyqtSignal, QEvent,QT_VERSION_STR#,QTimer
#from matplotlib.backends.backend_qt5agg import QtCore#.pyqtSignal as pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas,NavigationToolbar2QT as NavigationToolbar
#from PyQt5.QtWidgets import QWidget           
                            #QGraphicsScene, QGraphicsView, QGraphicsItem, \
                            #QGraphicsEllipseItem, QColorDialog,QGridLayout
from  matplotlibwidget import TraitsQWidget                  
from PyQt5.uic import loadUi
# traits
from traits.api import HasTraits, Instance, on_trait_change,Str,Float,Range,Enum,Button,List,Bool,Property,Int,Array,Tuple,ReadOnly
from traitsui.api import View, Group,HGroup,VGroup,HSplit,SetEditor,ButtonEditor,MenuBar,Item,RangeEditor,Label, \
    Handler,EnumEditor,StatusItem,CheckListEditor#,LEDEditor
from traitsui.menu import NoButtons,OKButton,OKCancelButtons, CancelButton,RevertButton 

import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from traitsui.qt4.editor import Editor
from traitsui.qt4.basic_editor_factory import BasicEditorFactory
from traitsui.qt4.ui_editor import UIEditor

class _TLBFigureEditor(UIEditor):
	figure=ReadOnly
	fig=Instance(Figure)
	#~ scrollable  = True
	
	def init(self, parent):
		"""MPL toolbar constructor"""
				
		self.figure=self.factory.figure
		self.control = self._create_tlb(parent)
		self.set_tooltip()
		
	def update_editor(self):
		pass

	def _create_tlb(self, parent,):
		""" Create the TLB for a particular backend. """
		# matplotlib commands to create a canvas 	
		#~ fig = Figure()
		#~ fig = self.object.figscatt
		self.sync_value(self.figure, 'fig', 'from')		
		mpl_canvas = self.fig.canvas  
		panel = QWidget()
		mpl_toolbar = NavigationToolbar(mpl_canvas,panel)
		vbox = QVBoxLayout()
		vbox.addWidget(mpl_toolbar,0)#,0)
		panel.setMaximumHeight(30)
		panel.setLayout(vbox)

		return panel    
class TLBFigureEditor(BasicEditorFactory):
	"""	Instanciation of _TLBFigureEditor class."""
	figure=ReadOnly
	fig=Instance(Figure)
	klass = _TLBFigureEditor

class _MPLFigureEditor(Editor):
	"""
	Custom Traits Editor for Matplotlib canvas integration
	in the traits GUI environment. Qt and WxPython backends are provided.
	"""
	scrollable  = True

	def init(self, parent):
		"""
		MPL canvas constructor.
		"""
		self.control = self._create_canvas(parent)
		self.set_tooltip()

	def update_editor(self):
		pass

	def _create_canvas(self, parent):
		"""
		Create the MPL canvas for a particular backend.
		"""	
		# matplotlib commands to create a canvas 
		panel = QWidget()
		mpl_canvas = FigureCanvas(self.value)
		mpl_canvas.setParent(panel)
		#~ mpl_toolbar = NavigationToolbar2(mpl_canvas,panel)
		vbox = QVBoxLayout()
		vbox.addWidget(mpl_canvas,1)#,0)		
		#~ vbox.addWidget(mpl_toolbar,1,0)
		panel.setLayout(vbox)

		return panel 
		   
class MPLFigureEditor(BasicEditorFactory):
		klass = _MPLFigureEditor
	

class C1(HasTraits):
	calcul=Button
	intensite=Range(low=0,high=8,value=2)
	b=List(Array(float64, (1,3),value=[[100.,500.,8.]]))
	#c=Range(0,10)
	figure=Instance(Figure,())
	tlb=Instance(NavigationToolbar)	

	def __init__(self,papa):
		super(C1, self).__init__()
		print("init C1")	
		#self.figure.subplots_adjust(left=0.05, bottom=.06, right=0.9, top=0.9,   wspace=0.1, hspace=0.06)
		#self.figure.patch.set_facecolor('blue')
		self.gs_all = GridSpec(ncols=1, nrows=1)
		self.ax=self.figure.add_subplot(self.gs_all[0,0])
		#self.ax.cla()
		#self.trace,=self.ax.plot(randn(81))
		self.papa=papa

	@on_trait_change("calcul,intensite")
	def dessin(self,  value):
		#print(self.b)
		#self.trace.set_ydata(randn(81)+value)
		self.ax.clear()
		tx=arange(1000)
		hst=ones_like(tx)*1.
		for pic in self.b:
			intensite,moyenne,sigma=ravel(pic)
			#print(intensite,moyenne,sigma)
			hst+=intensite*norm.pdf(tx,moyenne,sigma)
		hst=poisson(3**self.intensite*hst)
		self.ax.plot(hst)
		self.figure.canvas.draw_idle()
		#self.papa.mpl.axs[1].plot(hst)
		#self.papa.mpl.figure.canvas.draw_idle()
		self.data=hst

class MonGraph(pg.GraphItem):
	def __init__(self,scene):
		self.dragPoint = None
		self.dragOffset = None
		self.textItems = []
		pg.GraphItem.__init__(self)
		
#		#self.scatter.sigClicked.connect(self.clicked)
#		proxy = pg.SignalProxy(scene.sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
		scene.sigMouseMoved.connect(self.mouseMoved)

	def mouseMoved(self,evt):
		
		vb=self.getViewBox()
		mousePoint = vb.mapSceneToView(evt)
		pts = self.scatter.pointsAt(mousePoint)
		if len(pts): self.setCursor(Qt.PointingHandCursor)
		else:			self.setCursor(Qt.ArrowCursor)

		print("mouseMoved",len(pts))

	  
	def setData(self, **kwds):
		print("setData",kwds)
		self.text = kwds.pop('text', [])
		self.data = kwds
		if 'pos' in self.data:
			npts = self.data['pos'].shape[0]
			self.data['data'] = empty(npts, dtype=[('index', int)])
			self.data['data']['index'] = arange(npts)
		else:
			print("pas de pos!!")
			return
		# self.setTexts(self.text)
		self.updateGraph()

	def setTexts(self, text):
		for i in self.textItems:
			i.scene().removeItem(i)
		self.textItems = []
		for t in text:
			item = pg.TextItem(t)
			self.textItems.append(item)
			item.setParentItem(self)
	  
	def updateGraph(self):
		srt=argsort(self.data['pos'][:,0])
		self.data['adj']=c_[srt[:-1],srt[1:]]
		print("updateGraph")
		pg.GraphItem.setData(self, **self.data)
		#for i,item in enumerate(self.textItems):
			#item.setPos(*self.data['pos'][i])
	# def HoverEvent(self, ev):
		# print("HoverEvent",ev)
	
	def wheelEvent(self, ev):
		print("wheelEvent",ev.delta() )
		ev.ignore()

	def mouseClickEvent(self, ev):
		print("mouseClickEvent",ev )
		ev.ignore()
		#if ev.button()==2:
			#print(ev.buttonDownPos())
			#print("suppression!!")
			#ev.accept()
		#else:
			#ev.ignore()
			
	def mouseReleaseEvent(self, ev):
		print("mouseReleaseEvent")
			
	def mousePressEvent(self, ev):
		pos = ev.buttonDownPos(pg.QtCore.Qt.LeftButton)
		pts = self.scatter.pointsAt(pos)
		print("mousePressEvent",pos,ev.button(),len(pts))
		if len(pts) == 0 or ev.button()!=2:
			 ev.ignore()
			 return
		ind = pts[0].data()[0]

		self.data['pos']=r_[self.data['pos'][:ind],self.data['pos'][ind+1:]]
		#self.data['brush']=r_[self.data['brush'][:ind],self.data['brush'][ind+1:]]

#		self.data['brush'][ind]=Qt.blue#QColor("#219221")
		self.setData(pos=self.data['pos'])#, brush=self.data['brush'])
		ev.accept()
		
	def mouseDoubleClickEvent(self, ev):
		pos=ev.pos() 
		print("mouseDoubleClickEvent",ev,[pos.x(),pos.y()])
		self.data['pos']=r_[self.data['pos'],[[pos.x(),pos.y()]]]
		#self.data['brush']=r_[self.data['brush'],[Qt.blue]]
		self.setData(pos=self.data['pos'])
		#ev.accept()
		ev.ignore()
		
	def mouseMoveEvent(self, ev):
		print("mouseMoveEvent"),ev
		ev.ignore()
	  
	def mouseDragEvent(self, ev):
		print("mouseDragEvent",ev)
		if ev.button() != pg.QtCore.Qt.LeftButton:
			ev.ignore()
			return

		if ev.isStart():
			# We are already one step into the drag.
			# Find the point(s) at the mouse cursor when the button was first 
			# pressed:
			pos = ev.buttonDownPos()
			pts = self.scatter.pointsAt(pos)
			print("***",pts)
			if len(pts) == 0:
				 ev.ignore()
				 return
			self.dragPoint = pts[0]
			ind = pts[0].data()[0]
			print(pts[0].data())
			self.dragOffset = self.data['pos'][ind] - pos
		elif ev.isFinish():
			ind = self.dragPoint.data()[0]
			#self.data['brush'][ind]=QColor("#FF0000")
			self.dragPoint = None
			self.updateGraph()
			return
		else:
			if self.dragPoint is None:
				 ev.ignore()
				 return

		ind = self.dragPoint.data()[0]
		newpt = ev.pos() + self.dragOffset
		newpt[0]=clip(newpt[0],0,1)
		self.data['pos'][ind]=newpt
		#print(ev.pos(),self.dragOffset)
		self.updateGraph()
		ev.accept()

	def clicked(self, pts):	  print("clicked: %s" % pts)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		loadUi("dispo.ui", self)
		self.show()
		n=300
		mongraph = MonGraph(self.vue1.scene())
#		vb=g.getViewBox()		
		self.vue1.addItem(mongraph)

		roi=pg.PolyLineROI([[.1,.5],[.4,.8],[.56,.1]],pen='b', closed=True)
		self.vue1.addItem(roi)

#		self.vue1.addViewBox(row=1, col=0, lockAspect=True)
#		self.vue1.scene().sigMouseMoved.connect(self.mouseMoved)
#		print(self.vue1.vb)

		pos=[(0,1),(.5,0),(.75,0.8),(1,1)]#rand(5,2)
		mongraph.setData(pos=array(pos), brush=QColor("#FF0050"),#, text="du text"
		 pen=pg.mkPen(pg.mkColor("#FFFF00"), width=2))#, adj=adj, size=.2, symbol=symbols, pxMode=False, text=texts)
		
		sub1 = QMdiSubWindow()
		sub1.setWindowTitle("subw 1")
		self.mdi.addSubWindow(sub1)
		sub1.show()
		self.vuex = pg.PlotWidget(sub1)
		sub1.setWidget(self.vuex)
		self.vuex.setObjectName("vuex")
		self.vuex.scene()
		
		sub2 = QMdiSubWindow()
		sub2.setWindowTitle("subw 3d")
		self.mdi.addSubWindow(sub2)
		sub2.show()
		self.pggl = gl.GLViewWidget(sub2)
		sub2.setWidget(self.pggl)
		
		#sub3 = QMdiSubWindow()
		#sub3.setWindowTitle("subw traits")
		#self.mdi.addSubWindow(sub3)
		#sub3.show()
		#self.tr2 = TraitsQWidget(sub3)
		#sub3.setWidget(self.tr2)
		print(self.mpl)
		

		self.pggl.setObjectName("pg_3d")
		self.pggl.setCameraPosition(distance=50)
		z = pg.gaussianFilter(randn(30,30)*3, (1,1))
		
		p2 = gl.GLSurfacePlotItem(z=z, shader='shaded', color=QColor("#FFA500"))
		p2.scale(16./49., 16./49., 2.0)
		p2.translate(-20, -20, 0)
		self.pggl.addItem(p2)
		
		
		self.mdi.tileSubWindows()
		
		v1=self.vuex
		#v2=self.vue2
		self.ty=randn(n)
		self.ts=self.ty*0
		self.tl=self.ty*0
		v1.setBackgroundBrush(QBrush(QColor("#938080"),Qt.Dense3Pattern)) # la classe PlotWidget est un GraphicsWidget qui est un QGraphics View
		
		bar = self.menuBar()
		fl = bar.addMenu("File")
		fl.addAction("New")
		fl.addAction("cascade")
		fl.addAction("Tiled")
		fl.triggered[QAction].connect(self.windowaction)
		self.setWindowTitle("MDI demo")

		#self.vue1.addLegend()
		self.l = v1.plot(self.ty,pen=pg.mkPen("#EA1515", width=3, style=Qt.SolidLine), name='red plot')
		self.ls = v1.plot(self.ts,pen=pg.mkPen("#EAFF00", width=5, style=Qt.SolidLine))
		#self.lj = v2.plot(self.tl,pen='y')

		self.pg3d.setCameraPosition(distance=50)
		self.pg3d.setBackgroundColor(QColor("#EDEDD7"))
		#z = pg.gaussianFilter(randn(50,50), (1,1))
		#p1.scale(16./49., 16./49., 1.0)
		#p1.translate(-18, 2, 0)
		self.tx=r_[-10:10:100J]

		x,y=meshgrid(self.tx,r_[-4:4:100J])
		#def fpf(e): return e**3+e**2+e+1
		#def fpf(e): return ((e-2)*(e*e+e+4))*.1
		self.grille=x+1J*y
		z=real(self.fpf(self.grille))
		z=exp(-.2*(x**2+y**2))*abs(x-y)
		
		self.surface = gl.GLSurfacePlotItem(x=self.tx,y=self.tx,z=z,shader='shaded', color=pg.glColor(QColor("#F10E0E")))
		self.pg3d.addItem(self.surface)
		
		self.pg3d.addItem(gl.GLAxisItem())
		self.pg3d.addItem(gl.GLGridItem())
		
		self.lignepol=gl.GLLinePlotItem(pos=c_[self.tx*0,self.tx,abs(self.fpf(self.tx))],color=pg.glColor(QColor("#1AA51A")), width=4., antialias=True)
		self.pg3d.addItem(self.lignepol)


#c1 = plt.plot([1,3,2,4], pen='r', symbol='o', symbolPen='r', symbolBrush=0.5, name='red plot')
		
		deg=2
		self.lgmin=deg#2
		lgmax=200

		M=self.M=[]
		tabj=-unique(int32((linspace(sqrt(self.lgmin),sqrt(lgmax),50)**2).round()))
		#tabj=arange(-lgmin,-lgmax-1,-1)
		print(tabj)
		#exit()
		jm=1#2
		X=empty((deg+1,0))#arange(-lgmin+1,2)**arange(deg)[:,None]
		for i,j in enumerate(tabj):#arange(-lgmin-1,-lgmax,-1):
			X=c_[(arange(j,jm))**arange(deg+1)[:,None],X]
			fm=cho_solve(cho_factor(X@X.T),X)
			M.append([j,X.T@fm,fm[1]])
			jm=j
		self.biais=0.
		self.inc=0.
		
		#self.mpl.axs[0].imshow(randn(10,10))
		self.mpl.axs[0].plot(rand(100), 'o', picker=5)  # 5 points tolerance
		self.l1,=self.mpl.axs[1].plot(randn(100))#, picker=5)
		self.mpl.axs[2].imshow(randn(50,50))#, picker=5)
		
		#self.toolbar = NavigationToolbar(self.mpl, self)
		#self.gridLayout.addWidget(self.toolbar, 2, 0, 1, 1)
		#self.mpl.axes.plot(randn(80))
		
		self.cid_scroll = self.mpl.canvas.mpl_connect('scroll_event', self._on_scroll)   
		self.cid_move   = self.mpl.canvas.mpl_connect('motion_notify_event', self._mouse_move)
		#self.cid_press  = self.mpl.canvas.mpl_connect('button_press_event', self._on_press)
		#self.cid_release  = self.mpl.canvas.mpl_connect('button_release_event', self._on_release)
		self.cid_pick  =  self.mpl.canvas.mpl_connect('pick_event', self._on_pick)

		#self.timer=self.startTimer(1000)
		
	def fpf(self,v,a=1.5,b=-2,c=-100,d=134,e=500):
		 return (a*v**4+b*v**3+c*v**2+d*v+e)*.001
		
	@pyqtSlot(int)
	def on_monslider_valueChanged(self,val):
		print("slider:",val)
		v=5*(val-500)
		self.lignepol.setData(pos=c_[self.tx*0,self.tx,(self.fpf(v=self.tx,e=v))])
		self.surface.setData(z=abs(self.fpf(v=self.grille,e=v)))
		
	def windowaction(self, q):
		print ("triggered")

		#if q.text() == "New":
			#MainWindow2.count = MainWindow2.count+1
			#sub = QMdiSubWindow()
			#sub.setWidget(QTextEdit())
			#sub.setWindowTitle("subwindow"+str(MainWindow2.count))
			#self.mdi.addSubWindow(sub)
			#sub.show()

		if q.text() == "cascade":
			self.mdi.cascadeSubWindows()

		if q.text() == "Tiled":
			self.mdi.tileSubWindows()
		
		
	def _on_pick(self,event):
		thisline = event.artist
		xdata = thisline.get_xdata()
		ydata = thisline.get_ydata()
		ind = event.ind
		points = tuple(zip(xdata[ind], ydata[ind]))
		print('onpick points:', ind,points)
		
	def _on_release(self, event):
		print("_on_release",event.button)
		
	def _on_press(self, event):
		print("_on_press",event.inaxes,event.button)
		
	def _on_scroll(self, event):
		print("_on_scroll",event.inaxes,event.step)
		
	def _mouse_move(self, event):
		print("mouse_move",event.inaxes,event.xdata,event.ydata)
		
	@pyqtSlot()
	def on_pushButtonChangerCouleur_clicked(self):
		couleurInit = QColor("#A54141")
		couleur = QColorDialog.getColor(couleurInit,self,'Changer la couleur')
		if couleur.isValid():
			pinceau = QBrush(couleur)
			self.vue1.setBackgroundBrush(pinceau) # la classe PlotWidget est un GraphicsWidget qui est un QGraphics View
			
		
	@pyqtSlot(str)
	def on_lineEditTexte_textChanged(self,msg):
	  print(msg)
		
	@pyqtSlot(int)
	def on_dialRotation_valueChanged(self,v):		print("dial:",v)
	
	@pyqtSlot()
	def on_pushButtonCreerDisque_clicked(self):
		print("on_pushButtonCreerDisque_clicked")
		c1=C1(papa=self)
		c1.edit_traits(parent=self, kind='live',
			view=View(
					HGroup(
						VGroup(
							#Item("calcul",show_label=False),
							Item("intensite",show_label=False),
							"_",
							Item("b",style="custom",width=280,show_label=False)
						),
						VGroup(
							Item("figure",show_label=False, editor=MPLFigureEditor()),
							Item('tlb',editor=TLBFigureEditor(figure='figure')  ,show_label=False,resizable=False)
						)
					),
				resizable = True,
				#buttons = [OKButton, CancelButton]
			)
		)
		#print(c1.data)

	def timerEvent(self, e):
		#print(self.tr1.visualization.efficiency)
		#self.l1.set_ydata(randn(100))
		#self.mpl.canvas.draw()
		seuilX2=.99#.98

		self.ty=r_[self.ty[1:],self.biais+randn()]
		self.biais+=self.inc
		self.inc+=randn()*.05
		self.inc=clip(self.inc,-.2,.2)
		if(rand()<.01):	self.biais+=uniform(-10,10)
		for j,m,d in self.M[::-1]:
			y=self.ty[j-1:]
			yp=m@y
			err=((yp-y)**2)#[-8:]
			dof=len(err)
			if (chi2.cdf(sum(err),dof)<seuilX2) or (j==-self.lgmin):
				self.ts=r_[self.ts[1:],yp[-1]]
				break
		#print(-j,self.inc)

		self.tl=r_[self.tl[1:],-j]
		self.l.setData(self.ty)
		self.ls.setData(self.ts)
		#self.lj.setData(self.tl)

if __name__ == '__main__': 
	print(sys.version)
	print("QT VERSION:",QT_VERSION_STR)
	print("matplotlib VERSION:",mpl.__version__)
	app = QApplication(sys.argv)
	#fen = Fenetre()
	mainWindow = MainWindow()
	sys.exit(app.exec_())
	
#!/home/adonis/anaconda3/envs/env27/bin/python
# coding=utf-8
#.colorConverter
