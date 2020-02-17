#!/home/mac/anaconda3/bin/python3
# -*- coding: utf-8 -*-

from threading import Thread
from time import sleep
from traits.api import HasTraits, Int, Button, Enum, Str, PythonValue, RGBColor
from traitsui.api import View, Item, VGroup, Group


class EMail (HasTraits):
    msg = Str
    spell_check = Button('Spell Check')
    view = View(Group(
        Group(
            Item('msg',
                 style='custom',
                 resizable=True),
            Item('spell_check'),
            show_labels=False)),
        height=.3)

    def _spell_check_fired(self):
        print("_spell_check_fired")


class ThreadDemo(HasTraits):

    # The thread specific counters:
    pv = PythonValue
    rgbc = RGBColor
    thread_0 = Int
    thread_1 = Int
    thread_2 = Int
    film_type = Enum("’35mm’", "’16mm’", "‘8mm’", "‘Polaroid’")

    # The button used to start the threads running:
    start = Button('Start Threads')

    # The count of how many threads ae currently running:
    running = Int

    view = View(
        VGroup(
            'rgbc',
            'pv',
            Item('film_type'),
            Group(Item('thread_0', style='readonly', label="toto 1", tooltip="th1"),
                  Item(label='*****')
                  ),
            Item('thread_1', style='readonly'),
            Item('thread_2', style='readonly'),
        ),
        '_',
        Item('start', show_label=False,
             enabled_when='running == 0'),
        resizable=True,
        width=250,
        title='Monitoring threads'
    )

    def _start_fired(self):
        for i in range(3):
            Thread(target=self.counter,
                   args=('thread_%d' % i, (i * 10 + 10) / 1000.0)).start()

    def counter(self, name, interval):
        self.running += 1
        count = 0
        for i in range(200):
            setattr(self, name, count)
            count += 1
            sleep(interval)
        self.running -= 1


# Create the demo:
demo = ThreadDemo()
# demo = EMail()

# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    demo.configure_traits()
