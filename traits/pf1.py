#!/home/adonis/anaconda3/bin/python
# -*- coding: utf-8 -*-

#-- Imports --------------------------------------------------------------

from pyface.api import GUI
from pyface.api import ApplicationWindow, HeadingText
from traits.api \
    import HasTraits, Str, Regex, List, Instance,Int,Enum
from traitsui.api \
    import TreeEditor, TreeNode, View, Item, VSplit, \
           HGroup, Handler, Group

class Person(HasTraits):
    """ Model class representing a person """

    #: the name of the person
    name = Str

    #: the age of the person
    age = Int(18)

    #: the gender of the person
    gender = Enum('female', 'male')

    # a default traits view
    view = View(
        Item('name', resizable=True),
        Item('age', resizable=True),
        Item('gender', resizable=True),
        resizable=True,
    )


class MainWindow(ApplicationWindow):
    """ The main application window. """

    # The size of the window.
    size = (320, 240)

    # The window title.
    title = 'TraitsUI Person'

    # The traits object to display
    person = Instance(Person, ())

    def _create_contents(self, parent):
        """ Create the editor. """
        self._ui = self.person.edit_traits(kind='panel', parent=parent)
        return self._ui.control

def main():
    # Create the GUI.
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()

# Application entry point.
if __name__ == '__main__':
    main()
