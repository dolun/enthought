#!/home/adonis/anaconda3/bin/python
# -*- coding: utf-8 -*-
# QPolygonF,QTextEdit, QPen, QPainter,QMouseEvent
from traitsui.api import View, Group, HGroup, VGroup, HSplit, SetEditor, ButtonEditor, MenuBar, Item, RangeEditor, Label, \
    Handler, EnumEditor, StatusItem, CheckListEditor  # ,LEDEditor
from traits.api import HasTraits, Instance, on_trait_change, Str, Float, Range, Enum, Button, List, Bool, Property
from traitsui.menu import NoButtons, OKButton, OKCancelButtons, CancelButton, RevertButton
from PyQt5.QtWidgets import QSizePolicy, QDialog, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as MPLCanvas, NavigationToolbar2QT as NavigationToolbar
from pylab import subplots, figure, axes
from PyQt5.QtGui import QMainWindow, QApplication
from traitsui.ui_info import UIInfo
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rcParams
from PyQt5.QtCore import QSize
import pyqtgraph as pg
import os
#os.environ['ETS_TOOLKIT'] = 'qt4'
# By default, the PySide binding will be used. If you want the PyQt bindings
# to be used, you need to set the QT_API environment variable to 'pyqt'
os.environ['QT_API'] = 'pyqt'


#from matplotlib.figure import Figure
#from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
#from matplotlib.widgets import Slider, Button, RadioButtons
print(UIInfo)

rcParams['font.size'] = 12


class TC_Handler(Handler):

    def setattr(self, info, object, name, value):
        Handler.setattr(self, info, object, name, value)
        info.object._updated = True

    def object__updated_changed(self, info):
        if info.initialized:
            info.ui.title += "*"


class Rectangle(HasTraits):
    """ Simple rectangle class with two traits.   
    """
    # Width of the rectangle
    width = Float(1.0)
    # <----- Set default to 1.0
    # Height of the rectangle
    height = Float(2.0)
    choix = Enum(1, 2, 3)
    view = View("width",
                "height",
                Item("choix", style="custom"),
                Item("choix", style="readonly"),
                "_",
                Item("area",
                     style="readonly"  # "custom"#
                     ),
                buttons=OKCancelButtons  # [OKButton, CancelButton]
                )
    area = Property(depends_on=["width", "height"], cached=True)

    def _get_area(self):
        return self.width * self.height


class Reservoir(HasTraits):
    name = Str
    irrigated_areas = List(Str())
    ord_ma_set = List(editor=SetEditor(
        values=['pommes', 'berries', 'cantaloupe'],
        ordered=False,
        can_move_all=True,
        left_column_title='Available Fruit',
        right_column_title='Fruit Bowl'))

    max_storage = Float(1e6, desc='Maximal storage [hm3]')
    max_release = Float(10, desc='Maximal release [m3/s]')
    add_one = Button(editor=ButtonEditor(label='rrr'))
    controls_created = Bool(False)
    head = Float(10, desc='Hydraulic head [m]')
    gain = Enum(1, 2, 3, 8,
                desc="the gain index of the camera",
                label="gain", )

    efficiency = Range(0, 1.)
    # rectangle=Rectangle(width=3.56)
    rectangle = Instance(Rectangle, args=(), kw={"width": 3.3})
    # ui ui ui ui ui ui ui ui ui View

    traits_view = View(
        HGroup('controls_created',        'name', 'efficiency'),
        Group('ord_ma_set',
              #Item('ord_ma_set', style='simple'),
              label='selection',
              show_labels=False
              ),
        HGroup('max_storage', 'max_release', Item(
            'head', show_label=True),            Item("add_one"),      'gain'),
        "_",
        Item('irrigated_areas'),
        handler=TC_Handler(),
        #buttons = ['OK', 'Cancel'],
        #title = 'Reservoir',
        #resizable = True,
    )

    # ui ui ui ui ui ui ui ui ui
    # def _head_changed ( self, name,old, new ):
    #print( 'head changed from %s to %s ' % ( old, new ))

    # @on_trait_change("add_one, efficiency")
    # def update(self, name, value):
    #print( 'trait %s updated to %s' % (name, value)     )

    def _anytrait_changed(self, name, old, new):
        print(name, ' changed from %s to %s ' % (old, new))
        if name == "add_one":
            self.rectangle.edit_traits()

    # @on_trait_change('add_one')
    # def _add_one_fired(self):
        # print("_add_one_fired")

    # def _efficiency_changed ( self,  name,old, new ):
        #print(name, ' changed from %s to %s ' % ( old, new ))
        # print(self.efficiency)

    # def energy_production(self, release):
        # ''' Returns the energy production [Wh] for the given release [m3/s]
        # '''
        #power = 1000 * 9.81 * self.head * release * self.efficiency
        # return power * 3600


class Person(HasTraits):
    """ Example of restructuring a user interface by controlling visibility.
    """

    # General traits:
    first_name = Str
    last_name = Str
    age = Range(0, 120)

    # Traits for children only:
    legal_guardian = Str
    school = Str
    grade = Range(1, 12)

    # Traits for adults only:
    marital_status = Enum('single', 'married', 'divorced', 'widowed')
    registered_voter = Bool(False)
    military_service = Bool(False)

    # Interface for attributes that are always visible in interface:
    gen_group = Group(
        Item(name='first_name'),
        Item(name='last_name'),
        Item(name='age'),
        label='General Info',
        show_border=True
    )

    # Interface for attributes of Persons under 18:
    child_group = Group(
        Item(name='legal_guardian'),
        Item(name='school'),
        Item(name='grade'),
        label='Additional Info for minors',
        show_border=True,
        visible_when='age < 18',
    )

    # Interface for attributes of Persons 18 and over:
    adult_group = Group(
        Item(name='marital_status'),
        Item(name='registered_voter'),
        Item(name='military_service'),
        label='Additional Info for adults',
        show_border=True,
        visible_when='age >= 18',
    )

    # A simple View is sufficient, since the Group definitions do all the work:
    view = View(
        Group(
            gen_group,
            '10',
            Label("Using 'visible_when':"),
            '10',
            child_group,
            adult_group
        ),
        title='Personal Information',
        resizable=True,
        buttons=['OK']
    )


class TraitsQWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.visualization = Reservoir(
            name='Project A',
            max_storage=30,
            max_release=100.0,
            head=60,
            efficiency=0.8
        )
        # self.visualization =  Person(
        # first_name="Samuel",
        # last_name="Johnson",
        # age=16
        # )
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.figure, self.axs = subplots(1, 3)
        self.canvas = MPLCanvas(self.figure)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        vbl = QVBoxLayout()
        vbl.addWidget(self.mpl_toolbar)
        vbl.addWidget(self.canvas)
        self.setLayout(vbl)
        self.setParent(parent)


class MatplotlibWidgetx(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.figure = figure()
        ax1 = self.figure.add_subplot(121)
        ax2 = self.figure.add_subplot(122, projection='3d')
        self.canvas = MPLCanvas(self.figure)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        #sfreq = Slider(axes([0.25, 0.1, 0.65, 0.03], axisbg='lightgoldenrodyellow'), 'Freq', 0.1, 30.0, valinit=3.)
        #def update(val):			print(val)
        # sfreq.on_changed(update)

        vbl = QVBoxLayout()
        vbl.addWidget(self.mpl_toolbar)
        vbl.addWidget(self.canvas)
        self.setLayout(vbl)
        self.setParent(parent)


class MatplotlibWidget3(MPLCanvas):
    def __init__(self, parent=None, title='', xlabel='', ylabel='',
                 xlim=None, ylim=None, xscale='linear', yscale='linear',
                 width=4, height=3, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title(title)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        if xscale is not None:
            self.axes.set_xscale(xscale)
        if yscale is not None:
            self.axes.set_yscale(yscale)
        if xlim is not None:
            self.axes.set_xlim(*xlim)
        if ylim is not None:
            self.axes.set_ylim(*ylim)

        super(MatplotlibWidget, self).__init__(self.figure)
        self.setParent(parent)
        super(MatplotlibWidget, self).setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        super(MatplotlibWidget, self).updateGeometry()

    def sizeHint(self):
        return QSize(*self.get_width_height())

    def minimumSizeHint(self):
        return QSize(10, 10)


class MatplotlibWidget2(MPLCanvas):
    def __init__(self, parent=None, title='', xlabel='', ylabel='',
                 xlim=None, ylim=None, xscale='linear', yscale='linear',
                 width=4, height=3, dpi=100):

        self.figure, axs = subplots(1, 3)
        #self.figure = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = self.figure.add_subplot(111)
        # self.axes.set_title(title)
        # self.axes.set_xlabel(xlabel)
        # self.axes.set_ylabel(ylabel)
        # if xscale is not None:
        # self.axes.set_xscale(xscale)
        # if yscale is not None:
        # self.axes.set_yscale(yscale)
        # if xlim is not None:
        # self.axes.set_xlim(*xlim)
        # if ylim is not None:
        # self.axes.set_ylim(*ylim)

        super(MatplotlibWidget, self).__init__(self.figure)
        self.setParent(parent)
        super(MatplotlibWidget, self).setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        super(MatplotlibWidget, self).updateGeometry()

    def sizeHint(self):
        return QSize(*self.get_width_height())

    def minimumSizeHint(self):
        return QSize(10, 10)


class MatplotlibWidgetb(QDialog):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        # a figure instance to plot on
        self.figure = Figure()

        # this is the MPLCanvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = MPLCanvas(self.figure)

        # this is the Navigation widget
        # it takes the MPLCanvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

# class MatplotlibWidgetc(QtWidgets.QMainWindow):
    # def __init__(self):
    #super(ApplicationWindow, self).__init__()
    #self._main = QtWidgets.QWidget()
    # self.setCentralWidget(self._main)
    #layout = QtWidgets.QVBoxLayout(self._main)

    #static_canvas = MPLCanvas(Figure(figsize=(5, 3)))
    # layout.addWidget(static_canvas)
    #self.addToolBar(NavigationToolbar(static_canvas, self))

    #dynamic_canvas = MPLCanvas(Figure(figsize=(5, 3)))
    # layout.addWidget(dynamic_canvas)
    # self.addToolBar(QtCore.Qt.BottomToolBarArea,
        # NavigationToolbar(dynamic_canvas, self))


if __name__ == "__main__":
    app = QApplication.instance()
    widget = TraitsQWidget()
    # container=MatplotlibWidget()
    window = QMainWindow()
    window.setCentralWidget(widget)
    window.show()
    app.exec_()
