from curses import has_key
from genericpath import exists
import sys
import time
import threading
import json as json_parser
import paho.mqtt.client as mqtt
from random import random
import math

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.config import Config
from kivy.factory import Factory
from kivy.animation import Animation

from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from datetime import datetime
import MyDashboardWidget

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '400')

class RootWidget(BoxLayout):

    stop    = threading.Event()
    client  = mqtt.Client("client-001")

    errors = [];
    beacons = {};
    stations = [];


    @mainthread
    def connect_to_broker(self):
        if self.stop.is_set() == False:
            threading.Thread(target=self.thread_mqtt_loop).start()

    def thread_mqtt_loop(self):
        connack_rc = -1
        try:
            self.client.on_connect=self.on_mqtt_connect
            self.client.on_message=self.on_mqtt_message
            self.client.connect('192.168.4.1')

            self.client.loop_start()
            while connack_rc == -1:
                if self.stop.is_set(): # флаг на выход
                    return
                time.sleep(0.5)
            print("CONNACK reason code: %d" % (connack_rc))
            self.client.loop_stop()
            
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")

    def on_mqtt_connect(self, userdata, flags, rc, t1):
        print("Connected with result code "+str(rc))
        self.client.subscribe('/beacons/office')
    
    def on_mqtt_message(self, userdata, rc1, message ):
        json_str = str(message.payload.decode("utf-8"))
        json_obj = None
        print("received message =",json_str)
        json_obj = json_parser.loads( json_str )
        #
        for i in range(len(json_obj['e'])):
            mac     = json_obj['e'][i]['m'];
            station = json_obj['st'];
            print(mac)
            #
            if station in self.stations:
                print("this will execute")
            else:
                 self.stations.append(station)

            if mac in self.stations:
                # Dont measure stations rssi
                # with other stations.
                pass
            else:
                if {mac, station} <= self.beacons.keys():
                    # Remove old record
                    del (self.beacons[mac][station]) 
                # Insert new record
                self.beacons[mac] = {}
                self.beacons[mac][station] = {
                    'rssi':  json_obj['e'][i]['r'],
                    'timestamp': datetime.now()
                }

            #print(self.beacons)

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

# entry_point
if __name__ == '__main__':
    Application().run()