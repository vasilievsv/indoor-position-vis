import threading
import time
import sys

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from random import random
 
import MyDashboardWidget


Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '400')

import paho.mqtt.client as mqtt


class RootWidget(BoxLayout):

    stop = threading.Event()
    client= mqtt.Client("client-001")

    @mainthread
    def connect_to_broker(self):
        threading.Thread(target=self.infinite_loop).start()

    def on_mqtt_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe('beacons/office')
    
    def on_mqtt_message():
        print("received message =",str(message.payload.decode("utf-8")))


    def infinite_loop(self):
        try:
            self.client.connect('192.168.4.1')
            self.client.loop_start()
            self.client.on_connect=self.on_mqtt_connect
            self.client.on_message=self.on_mqtt_message
            
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")

        #iteration = 0
        #while True:
        #    if self.stop.is_set():
        #        # Stop running this thread so the main Python process can exit.
        #        return
        #    iteration += 1
        #    print('Infinite loop, iteration {}.'.format(iteration))
        #    time.sleep(1)

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