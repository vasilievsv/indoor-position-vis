import sys
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config

import WidgetRoot
import WidgetDashboardIcon
import WidgetDashboardCanvas

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '400')

class Application(App):

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.root.stop.set()

    def build(self):
        return Builder.load_file("views/main.kv")

# entry_point
if __name__ == '__main__':
    Application().run()