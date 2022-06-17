import sys
import time
import threading
import math

import json as json_parser
import paho.mqtt.client as mqtt

from kivy.factory import Factory
from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock, mainthread
from kivy.event import EventDispatcher

from datetime import datetime

class RootWidget(BoxLayout,EventDispatcher):

    stop    = threading.Event()         # флаг выхода из потока
    client  = mqtt.Client("client-001")

    errors = [];    #
    beacons = {};   # 
    stations = [];  #

    def __init__(self, **kwargs):
        self.register_event_type('on_ble_update_event')  
        super(RootWidget, self).__init__(**kwargs)

    @mainthread
    def cmd_connect(self):
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
            self.client.disconnect()
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")

    def on_mqtt_connect(self, userdata, flags, rc, t1):
        print("Connected with result code "+str(rc))
        self.client.subscribe('/beacons/office')
    
    def on_mqtt_message(self, userdata, rc1, message ):
        json_str = str(message.payload.decode("utf-8"))
        json_obj = None
        #print("received message =",json_str)
        json_obj = json_parser.loads( json_str )
        
        # 
        for i in range(len(json_obj['e'])):
            # Обход dict по индексу
            mac     = json_obj['e'][i]['m'];    # Вытаскиваем MAC vzrjd
            station = json_obj['st'];
            # Игнорим известные станции иначе запоминаем
            if station in self.stations:
                pass
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
                
                # Новая запись
                self.beacons[mac] = {}
                self.beacons[mac][station] = {
                    'rssi':  json_obj['e'][i]['r'],
                    'timestamp': datetime.now().timestamp
                }

            # Сообщение что данные готовы
            self.dispatch('on_ble_update_event', 'test message')
            for child in self.children[:]:
                    if child.dispatch('on_ble_update_event', 'test'):
                        return True

    def on_ble_update_event(self, *args):
        return False
