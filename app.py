from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config

from kivy.uix.button import Button
from kivy.uix.widget import Widget

from random import random
 
import MyDashboardWidget

import threading
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.uix.boxlayout import BoxLayout

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800') 
Config.set('graphics', 'height', '400')


class RootWidget(BoxLayout):

    stop = threading.Event()

    def start_second_thread(self, l_text):
        threading.Thread(target=self.second_thread, args=(l_text,)).start()

    def second_thread(self, label_text):
        # Start a new thread with an infinite loop and stop the current one.
        threading.Thread(target=self.infinite_loop).start()

    @mainthread
    def update_label_text(self, new_text):
        self.lab_2.text = new_text

    def infinite_loop(self):
        iteration = 0
        while True:
            if self.stop.is_set():
                # Stop running this thread so the main Python process can exit.
                return
            iteration += 1
            print('Infinite loop, iteration {}.'.format(iteration))
            time.sleep(1)


class Application(App):

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.root.stop.set()

    def build(self):
        return Builder.load_file("views/main.kv")

    def clear_canvas(self, obj):
        self.painter.canvas.clear()


if __name__ == '__main__':
    Application().run()