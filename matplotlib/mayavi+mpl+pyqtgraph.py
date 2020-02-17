
import sys
import os
import glob

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QFileDialog, QVBoxLayout
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable, Qt, QThreadPool  # *
from PyQt5.uic import loadUi
# import shutil


# from PySide2 import __version__ as PySide2Version
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *
# from PySide2.QtCore import *
# from PySide2.QtUiTools import QUiLoader
# from PySide2.QtWebEngineWidgets import QWebEngineView

import pyqtgraph as pg
# pg.setConfigOption('background', 'g')


# from pyqtgraph.console import ConsoleWidget
from pyqtgraph.dockarea import Dock, DockArea
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget  # ,NavigationToolbar
from matplotlib.widgets import Cursor, LassoSelector
# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np
import matplotlib as mpl
import mplcursors
# matplotlib.use("Qt5Agg")

# MAYAVI
# os.environ['ETS_TOOLKIT'] = 'qt4'
# from mayavi.mlab import contour3d, points3d, colorbar
from mayavi import mlab

# mlab.test_volume_slice_anim()
# mlab.show()
# exit()

#from pyface.qt import QtGui, QtCore
from traits.api import (Array, Bool, Button, Enum, Float, HasTraits, HasPrivateTraits, Instance,
                        Int, List, Property, Range, ReadOnly, Str, Tuple, on_trait_change)
from traitsui.api import (ButtonEditor, CheckListEditor,  
                          EnumEditor, Group, Handler, HGroup, VGroup, HSplit, Item,
                          Label, MenuBar, RangeEditor, SetEditor, StatusItem,
                          TextEditor, ValueEditor, View)
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor

import qdarkstyle

import numba as nb
import numpy as np
import pylab as pl
from scipy.integrate import odeint
# pl.plt.style.use('dark_background')

from pylab import (arange, transpose, clip,  # ,scatter,show#,shape,cos,pi,reshape,dot,zeros
                   argsort, array, c_,  empty, exp, float32, int32, plt,
                   float64, hstack, int32, linspace, load, log, log10,
                   logical_and, logspace, meshgrid,  ones_like, cos, sin, pi,
                   poisson, poly1d, polyfit, r_, rand, randn, ravel, real,
                   sqrt, subplots, uniform, unique, zeros, zeros_like, loadtxt, where)
import pandas as pd

import time
import traceback
##################################################
dirpath = os.getcwd()
print("current directory is : " + dirpath)
foldername = os.path.basename(dirpath)
print("Directory name is : " + foldername)
scriptpath = os.path.realpath(__file__)
print("Script path is : " + scriptpath)
dirfile, _ = os.path.split(scriptpath)
os.chdir(dirfile)
print("Now, current directory is : " + os.getcwd())

# from silx.gui.plot import Plot1D as silxPlot1D

# def gradient(f, x, y, z, d=0.01):
#     """ Return the gradient of f in (x, y, z). """
#     fx  = f(x+d, y, z)
#     fx_ = f(x-d, y, z)
#     fy  = f(x, y+d, z)
#     fy_ = f(x, y-d, z)
#     fz  = f(x, y, z+d)
#     fz_ = f(x, y, z-d)
#     return (fx-fx_)/(2*d), (fy-fy_)/(2*d), (fz-fz_)/(2*d)

# def V(x, y, z):
#     """ A 3D sinusoidal lattice with a parabolic confinement. """
#     return np.cos(10*x) + np.cos(10*y) + np.cos(10*z) + 2*(x**2 + y**2 + z**2)

# def flow(r, t):
#     """ The dynamical flow of the system """
#     x, y, z, vx, vy, vz = r
#     fx, fy, fz = gradient(V, x-.2*np.sin(6*t), y-.2*np.sin(6*t+1), z-.2*np.sin(6*t+2))
#     return np.array((vx, vy, vz, -fx - 0.3*vx, -fy - 0.3*vy, -fz - 0.3*vz))


def curve(n_mer, n_long):
    phi = linspace(0, 2*pi, 2000)
    return [cos(phi*n_mer) * (1 + 0.5*cos(n_long*phi)),
            sin(phi*n_mer) * (1 + 0.5*cos(n_long*phi)),
            0.5*sin(n_long*phi),
            sin(phi*n_mer)]


class Visualization3d(HasTraits):

    my_scene = Instance(MlabSceneModel, ())
    label_1 = Float(1e6, desc='Maximal storage')
    meridional = Range(1, 30,  6)
    transverse = Range(0, 30, 11)

    def _meridional_default(self): #call at initialization
        return 14

    def __init__(self):
        super(Visualization3d, self).__init__()
        print("init Visualization3d")
        
    #     pass

    @on_trait_change('my_scene.activated')
    def activation_plot(self):
        """ initialisation 3d cf. https://docs.enthought.com/mayavi/mayavi/building_applications.html"""
        x, y, z, s = curve(4, 6)
        self.maya_plot = mlab.plot3d(x, y, z, s)
        self.colorbar = mlab.colorbar(
            self.maya_plot, title='XX', orientation='vertical')
        # Initial conditions
        # R0 = (0, 0, 0, 0, 0, 0)
        # t = np.linspace(0, 50, 500)
        # R = odeint(flow, R0, t)
        # x, y, z, vx, vy, vz = R.T
        # X, Y, Z = np.mgrid[-2:2:100j, -2:2:100j, -2:2:100j]
        # mlab.contour3d(X, Y, Z, V)
        # trajectory = mlab.plot3d(x, y, z, t, colormap='hot',
        #                     tube_radius=None)
        # mlab.colorbar(trajectory, title='Time', orientation='vertical')

        # x, y, z = np.ogrid[-3:3:60j, -3:3:60j, -3:3:60j]
        # t = 0
        # Pf = 0.45+((x*cos(t))*(x*cos(t)) + (y*cos(t))
        #            * (y*cos(t))-(z*cos(t))*(z*cos(t)))
        # obj = mlab.contour3d(Pf, contours=[0], transparent=False)

    @on_trait_change(" meridional, transverse")
    def update_3dplot(self, name, value):
        # def _transverse_changed(self,  name, old, new):
        print(f"{name} = {value}")
        x, y, z, t = curve(self.meridional, self.transverse)
        self.maya_plot.mlab_source.trait_set(x=x, y=y, z=z, scalars=t)

    # def _anytrait_changed(self, name, old, new):
    #     print(name, ' changed from %s to %s ' % (old, new))

    view = View(VGroup(HGroup('meridional', 'transverse', 'label_1'),
                       '_',
                       Item('my_scene', editor=SceneEditor(scene_class=MayaviScene),
                            height=250, width=300, show_label=False)
                       ),
                resizable=True
                )

    # height=250, width=300,


class MayaviQWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(5)
        self.visu = Visualization3d()

        self.ui = self.visu.edit_traits(parent=self,
                                        kind='subpanel', scrollable=True).control
        layout.addWidget(self.ui)
        self.ui.setParent(self)


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    # progress = pyqtSignal(int)
    progress = pyqtSignal(int, float, object)

    # finished = Signal()
    # error = Signal(tuple)
    # result = Signal(object)
    # progress = Signal(int)


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    # @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
            # print("------------------")
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()  # Done


class MainWindow(QMainWindow):
    """ MainWindow """

    def __init__(self, ui_file, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi(ui_file, self)
        self.show()

        # w = pg.GraphicsLayoutWidget()#QWidget()

        # self.setCentralWidget(w)

        # self.area = DockArea(w)
        # gridLayout = QGridLayout(w)
        # gridLayout.setObjectName("gridLayout")
        # gridLayout.addWidget(self.area)

        # self.area comes from ui file
        d1 = Dock("full view", closable=False)
        self.area.addDock(d1)

        # self.plotWidget=pg.PlotWidget()
        # p1=self.plotWidget.getPlotItem()
        # self.imv = pg.ImageItem()
        # imv = self.imv
        # p1.addItem(imv)

        self.imv = pg.ImageView()
        imv = self.imv
        d1.addWidget(imv)
        # p1= d1.addPlot(title='titre')
        imageItem = imv.getImageItem()
        # view= imv.getView()

        def imageHoverEvent(event):
            """
            Show the position, pixel, and value under the mouse cursor.
            """
            if event.isExit():
                self.labelCoordonates.setText(f"hors cadre")
                return
            pos = event.pos()
            # i, j = pos.y(), pos.x()
            # i = int(np.clip(i, 0, data.shape[0] - 1))
            # j = int(np.clip(j, 0, data.shape[1] - 1))
            # val = data[i, j]
            ppos = imageItem.mapToParent(pos)
            x, y = ppos.x(), ppos.y()
            self.labelCoordonates.setText(f"{int(x)} {int(y)}")
        imageItem.hoverEvent = imageHoverEvent

        # d2 = Dock("zoom", closable=False)
        # profilsView = pg.PlotWidget(title="profils")
        # profilsView.setLogMode(x=False, y=False)
        # d2.addWidget(profilsView)

        # d3 = Dock("silx", closable=False)
        # plotsilx = silxPlot1D()  # Create the plot widget
        # plotsilx.addCurve(x=(1, 2, 3), y=(1.5, 2, 1), legend='curve')
        # d3.addWidget(plotsilx)

        # mayavi widget
        dock_mayavi = Dock("mayavi", closable=False)
        self.mayavi_widget = MayaviQWidget()
        dock_mayavi.addWidget(self.mayavi_widget)
        self.area.addDock(dock_mayavi, 'above', d1)

        # matplotlib widget
        dmpl = Dock("mpl", closable=False)
        mplwidget = MatplotlibWidget()
        mplfigure = mplwidget.getFigure()

        gs1 = mpl.gridspec.GridSpec(1, 1)
        subplot = mplfigure.add_subplot(gs1[0])
        data = np.outer(range(10), range(1, 5))

        lines = subplot.plot(data)
        mplcursors.cursor(lines)  # or just mplcursors.cursor()

        # curseurs horizontal et vertical
        # self.h_and_v_Cursors = Cursor(subplot, useblit=True, color='red', linewidth=1)

        # def onSelect(xp):
        #     print(xp)
        # LASSO:
        # self.lasso = LassoSelector( ax=subplot, onselect=lambda xp: print(xp),
        #  lineprops={'color': 'green', 'linewidth': 2, 'alpha': 0.8}, button=1)

        mplwidget.draw()
        dmpl.addWidget(mplwidget)
        gs1.tight_layout(mplfigure, rect=[0, 0, 1, 1], pad=1.)

        self.area.addDock(dmpl, 'right', d1)
        # self.area.addDock(d2, 'bottom')
        # self.area.addDock(d3, 'right')

        # df = pd.read_csv("../spectres/csv/pechblend.csv", header=None)
        """
        def dialPriorWeightChanged(v):
            self.labelPriorWeight.setNum(10**(.1*v))
        self.dialPriorWeight.valueChanged.connect(
            dialPriorWeightChanged  # self.labelPriorParameter.setNum
        )
        dialPriorWeightChanged(self.dialPriorWeight.value())

        def dialPriorScaleChanged(v):
            self.labelPriorScale.setNum(10**(.1*v))
        self.dialPriorScale.valueChanged.connect(
            dialPriorScaleChanged  # self.labelPriorParameter.setNum
        )
        dialPriorScaleChanged(self.dialPriorScale.value())

        def dialPriorAuxiliaryImageChanged(v):
            self.labelPriorAuxiliaryImage.setNum(10**(.1*v))
        self.dialPriorAuxiliaryImage.valueChanged.connect(
            dialPriorAuxiliaryImageChanged  # self.labelPriorParameter.setNum
        )
        dialPriorAuxiliaryImageChanged(self.dialPriorAuxiliaryImage.value())
        # self.labelPriorParameter.setNum(self.dialPriorParameter.value())

        self.threadpool = QThreadPool()
        print(
            f"Multithreading with maximum {self.threadpool.maxThreadCount()} threads ")

        # self.start_compute_thread()
        """

    @pyqtSlot(int)
    def on_n1_valueChanged(self, val):
        x, y, z, t = curve(7, val)
        print(val)
        self.mayavi_widget.visu.maya_plot.mlab_source.trait_set(
            x=x, y=y, z=z, scalars=t)

    @pyqtSlot()
    def on_pauseButton_clicked(self):
        print("on_pauseButton_clicked")

#############################################################################
    """
        w = QWidget()

        self.setCentralWidget(w)

        self.counter = 0

        layout = QVBoxLayout()
        self.bar = QProgressBar() 
        self.area = DockArea(w)

        d1 = Dock("vp", closable=False)
        d2 = Dock("vz", closable=False)
        v1 = pg.PlotWidget(title="vue 1")
        d1.addWidget(v1)
        v2 = pg.PlotWidget(title="vue 2")
        d2.addWidget(v2)
        self.area.addDock(d1, 'left')
        self.area.addDock(d2, 'right')
        mongraph = MonGraph(v1.scene())
        pos = [(0, 1), (.5, 0), (.75, 0.8), (1, 1)]  # rand(5,2)
        mongraph.setData(pos=np.array(pos), brush=QColor("#FF0050"),  # , text="du text"
                         pen=pg.mkPen(pg.mkColor("#FFFF00"), width=2))  # , adj=adj, size=.2, symbol=symbols, pxMode=False, text=texts)
        v1.addItem(mongraph)

        layout.addWidget(self.l)
        layout.addWidget(b)
        layout.addWidget(self.bar)
        # layout.addWidget(self.browser)
        layout.addWidget(self.area)
        w.setLayout(layout)
        # QFileDialog.getOpenFileName(self,'Open file')
        # gridLayout = QGridLayout()
        # gridLayout.setObjectName("gridLayout")
        # gridLayout.addWidget(self.area)

        self.show()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" %
              self.threadpool.maxThreadCount())

        # self.timer = QTimer()
        # self.timer.setInterval(1000)
        # self.timer.timeout.connect(self.recurring_timer)
        # self.timer.start()

        self.start_compute_thread()

    """

    """
    def progress_fn(self, it, llk, data):
        # self.bar.setValue(n)
        print(it, llk)
        self.imv.setImage(data)

    def MAPEM(self, progress_callback, paramGibbs):
        # -----------------------------------------

        filename, proj, sensibilite, obs, cijlbd0, r_scatter, im0,\
            lg2_in, lg_in, lg2_out, lg_out = get_data(
                # proj_file="137Cs_51_Voxels_Rg7_E4",
                proj_file="241Am_51_Voxels_Rg7_E4",
                simulation=True)
        self.setWindowTitle(filename)

        # initialisation
        lbd = pl.ones(lg2_in)
        lbd *= obs.sum()/lbd.sum()
        lbd /= sensibilite
        cijlbd = proj@lbd+r_scatter
        lastllkem = sum(obs*log(cijlbd)-cijlbd)
        # cijlbd0 = cijlbd0.clip(1e-10)
        # llk0 = sum(obs*log(cijlbd0)-cijlbd0)
        # beta_penalty = 1.e-3  # Am
        # beta_penalty = 1.e-5
        # sc = 1.e-5
        nbiter = 50000
        t0 = 0

        @nb.njit(parallel=True)
        def elbo(_obs, _proj, _lbd, _cijlbd, _sensibilite):
            return (_proj.T@(_obs/_cijlbd))*_lbd/_sensibilite

        for it in arange(nbiter):
            while self.pauseButton.isChecked():
                time.sleep(.5)
            prior_weight_penalty = float(self.labelPriorWeight.text())
            prior_scale_penalty = float(self.labelPriorScale.text())
            prior_auxiliary_image_penalty = float(
                self.labelPriorAuxiliaryImage.text())
            ####################
            lb_EM = (proj.T@(obs/cijlbd))*lbd/sensibilite  # E step=nj/pj
            # lb_EM=elbo(obs,proj,lbd,cijlbd,sensibilite)
            # gibbs field  ######################
            #  lbd=lb_EM #MLEM
            # lbd = opt_transfer(lbd, lb_EM, sensibilite, beta_penalty=prior_weight_penalty,
            #                    sc=prior_scale_penalty)  # MAPEM
            lbd = opt_transfer_with_auxiliary_image(lbd, lb_EM, sensibilite,
                                                    beta_penalty=prior_weight_penalty,
                                                    sc_auxiliary_image=prior_auxiliary_image_penalty,
                                                    auxiliary_image=im0.ravel(),
                                                    sc=prior_scale_penalty)
            # sigmaj = sqrt(lbd/sensibilite)

            cijlbd = proj@lbd+r_scatter

            llk_em = sum(obs*log(cijlbd)-cijlbd)
            tps = time.time()
            if tps-t0 > 1:
                t0 = tps
                # print(it, llk_em, llk_em-lastllkem, llk_em >= lastllkem,
                #       "llkdata", llk0)  # , "d_U", d_U.min(), d_U.max())
                progress_callback.emit(
                    it, llk_em, lbd.reshape((lg_in, lg_in)))
            lastllkem = llk_em

        return "Done."

    def print_output(self, s):
        print("resultat:", s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def start_compute_thread(self):
        # Pass the function to execute
        # Any other args, kwargs are passed to the run function
        paramGibbs = None
        worker = Worker(self.MAPEM, paramGibbs=paramGibbs)

        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)
    """


print(sys.version)
# print("QT VERSION:", PySide2Version)
print("matplotlib VERSION:", mpl.__version__)
print("pyqtgraph version", pg.__version__)
app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
window = MainWindow("../matplotlib/ui_file.ui")
# window = MainWindow2("sinbad5.ui")
app.exec_()

# app = QApplication([])
# window = MainWindow()
# app.exec_()
