#!/home/adonis/anaconda3/bin/python3
# -*- coding: utf-8 -*-

"""
Dynamic Range editor
Demonstrates how to dynamically modify the low and high limits of a Range Trait.
In the simple *Range Editor* example, we saw how to define a Range Trait, whose
values were restricted to a fixed range. Here, we show how the limits of the
range can be changed dynamically using the editor's *low_name* and *high_name*
attributes.
In this example, these range limits are set with sliders. In practice, the
limits would often be calculated from other user input or model data.
The demo is divided into three tabs:
 * A dynamic range using a simple slider.
 * A dynamic range using a large-range slider.
 * A dynamic range using a spinner.
In each section of the demo, the top-most 'value' trait can have its range
end points changed dynamically by modifying the 'low' and 'high' sliders
below it.
The large-range slider includes low-end and high-end arrows, which are used
to step the visible range through the full range, when the latter is too large
to be entirely visible.
This demo also illustrates how the value, label formatting and label
widths can also be specified if desired.
from traits.api     import HasTraits, Button, Range, Float 
from traitsui.api     import View, Item, Group, RangeEditor 
from traitsui.qt4.extra.bounds_editor import BoundsEditor 

class Parameters(HasTraits): 
    rgb_range = Range(0.,1.0) 
    range1 = rgb_range 
    range2 = rgb_range 
    low_val = Float(0.0) 
    high_val = Float(1.0) 
    eval_button = Button("Eval") 

    traits_view= View(
     Item('range1', editor=RangeEditor()), 
     Item('range2', editor=BoundsEditor(low_name = 'low_val', high_name = 'high_val')), 
     Item('eval_button')) 


    def _range1_changed(self, value): 
     print(value) 

    def _low_val_changed(self): 
     print(self.low_val) 

    def _high_val_changed(self): 
     print(self.high_val) 

    def _eval_button_fired(self): 
     print(self.range1) 
     print(self.low_val) 
     print(self.high_val) 

alg = Parameters() 
alg.configure_traits() 
"""

# Imports:
from __future__ import absolute_import
from matplotlib.figure import Figure
from pyqtgraph.Qt import QtCore, QtGui  # ,  uic, QtWidgets
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget  # ,NavigationToolbar
import pyqtgraph as pg
# from pyqtgraph.widgets.

from traits.api import HasPrivateTraits, HasTraits, Float, Range, Int, on_trait_change, Any, Instance
from traitsui.editor import Editor
from traitsui.basic_editor_factory import BasicEditorFactory
from traitsui.qt4.editor import Editor as qt4Editor
from traitsui.qt4.basic_editor_factory import BasicEditorFactory as qt4BasicEditorFactory

from traitsui.api import View, Group, Item, Label, RangeEditor

from traitsui.qt4.extra.bounds_editor import BoundsEditor
from traitsui.qt4.extra.range_slider import RangeSlider

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar2
from matplotlib.backend_bases import Event
import pylab as pl


class _PGFigureEditor(Editor):
    """
    Custom Traits Editor for Matplotlib canvas integration
    in the traits GUI environment. Qt and WxPython backends are provided.
    """
    scrollable = True

    def init(self, parent):
        """
        MPL canvas constructor.
        """
        self.control = self._create_canvas(parent)
        # self.set_tooltip()

    def update_editor(self):
        pass

    def _create_canvas(self, parent):
        """
        Create the MPL canvas for a particular backend.
        """
        # matplotlib commands to create a canvas
        panel = QtGui.QWidget()


class _MPLFigureEditor(qt4Editor):
    """
    Custom Traits Editor for Matplotlib canvas integration
    in the traits GUI environment. Qt and WxPython backends are provided.
    """
    scrollable = True

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
        panel = QtGui.QWidget()
        mpl_canvas = FigureCanvas(self.value)
        mpl_canvas.setParent(panel)
        # ~ mpl_toolbar = NavigationToolbar2(mpl_canvas,panel)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(mpl_canvas, 1)  # ,0)
        #~ vbox.addWidget(mpl_toolbar,1,0)
        panel.setLayout(vbox)

        return panel


class MPLFigureEditor(qt4BasicEditorFactory):
    """
    Instanciation of _MPLFigureEditor class.
    """
    klass = _MPLFigureEditor


class PGFigureEditor(BasicEditorFactory):
    """
    Instanciation of _MPLFigureEditor class.
    """
    klass = _PGFigureEditor


class DynamicRangeEditor(HasTraits):
    """ Defines an editor for dynamic ranges (i.e. ranges whose bounds can be
        changed at run time).
    """
    rgb_range = Range(0., 1.0)
    range1 = rgb_range
    range2 = rgb_range
    mplfigure = Instance(Figure, ())
    pgfigure = Instance(pg.PlotWidget, ())

    mpw = MatplotlibWidget()

    # The value with the dynamic range:
    value = Float

    # This determines the low end of the range:
    low = Range(0.0, 10.0, 0.0)

    # This determines the high end of the range:
    high = Range(20.0, 100.0, 20.0)
    l = Float(0.)
    h = Float(1.)

    # An integer value:
    int_value = Int

    # This determines the low end of the integer range:
    int_low = Range(0, 10, 0)

    # This determines the high end of the range:
    int_high = Range(20, 100, 20)

    # Traits view definitions:
    traits_view = View(
        Group(
            # Item('rgb_range', editor=BoundsEditor(low_name = 'low', high_name = 'high')),
            Item('range1', editor=RangeEditor()),
            " ",
            Item('range2', editor=BoundsEditor(low_name='l', high_name='h')),
            Item('mplfigure', editor=MPLFigureEditor(),
                 show_label=False, resizable=True, height=450),
            #Item('pgfigure', editor=PGFigureEditor(), show_label=False, resizable=True, height=450),
        ),

        # Dynamic simple slider demo:
        Group(
            Item('value',
                 editor=RangeEditor(low_name='low',
                                    high_name='high',
                                    format='%.1f',
                                    label_width=28,
                                    mode='auto')
                 ),
            '_',
            Item('low'),
            Item('high'),
            '_',
            Label('Move the Low and High sliders to change the range of '
                  'Value.'),
            label='Simple Slider'
        ),

        # Dynamic large range slider demo:
        Group(
            Item('value',
                 editor=RangeEditor(low_name='low',
                                    high_name='high',
                                    format='%.1f',
                                    label_width=28,
                                    mode='xslider')
                 ),
            '_',
            Item('low'),
            Item('high'),
            '_',
            Label('Move the Low and High sliders to change the range of '
                  'Value.'),
            label='Large Range Slider'
        ),

        # Dynamic spinner demo:
        Group(
            Item('int_value',
                 editor=RangeEditor(low=0,
                                    high=20,
                                    low_name='int_low',
                                    high_name='int_high',
                                    format='%d',
                                    is_float=False,
                                    label_width=28,
                                    mode='spinner')
                 ),
            '_',
            Item('int_low'),
            Item('int_high'),
            '_',
            Label('Move the Low and High sliders to change the range of '
                  'Value.'),
            label='Spinner'
        ),
        title='Dynamic Range Editor Demonstration',
        buttons=['OK'],
        resizable=True
    )
    # def _range1_changed(self, value):
    # print(value)
    # def _anytrait_changed( self, name,old, new ):
    # print(name, ' changed from %s to %s ' % ( old, new ))

    def __init__(self):
        super(DynamicRangeEditor, self).__init__()
    # mplfigure = mpw.getFigure()
        subplot = self.mplfigure.add_subplot(111)
        subplot.plot(pl.randn(155))
        self.mpw.draw()
    # dmpl.addWidget(mpw)

    @on_trait_change("l, h")
    def updatelh(self, name, value):
        print('trait %s updated to %s' % (name, value))


# Create the demo:
demo = DynamicRangeEditor()

# Run the demo (if invoked from the command line):
# if __name__ == '__main__':
demo.configure_traits()
