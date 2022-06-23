"""
    -----------------------------------------------------------
    RootWidget



    -----------------------------------------------------------
"""
import sys
import time
import threading
import math

import json as json_parser
import paho.mqtt.client as mqtt

from kivy.app import App
from kivy.factory import Factory
from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock, mainthread
from kivy.event import EventDispatcher

from datetime import datetime

class RootWidget(BoxLayout,EventDispatcher):

    stop    = threading.Event()         # флаг выхода из потока
    client  = mqtt.Client("client-001")

    errors          = [];    #
    beacons         = {};   # 
    stations        = {};  #
    sortedBeacons   = {}
    knownBeacons    = []

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        # Наши события
        self.register_event_type('on_ble_update_event')
        self.register_event_type('on_ble_new_station') 

   
    def cmd_connect(self):
        if self.stop.is_set() == False:
            threading.Thread(target=self.thread_mqtt_loop).start()
    #
    # Все элементы подготовлены
    #
    def on_kv_post(self, base_widget):
        
        # Поиск элементов с методом on_ble_update_event
        for child_id in self.ids:
            
            if hasattr(self.ids[child_id], "on_ble_update_event"):
                self.bind(on_ble_update_event=self.ids[child_id].on_ble_update_event)

            if hasattr(self.ids[child_id], "on_ble_new_station"):
                self.bind(on_ble_new_station=self.ids[child_id].on_ble_new_station)
        pass

    def thread_mqtt_loop(self):
        connack_rc = -1
        try:
            self.client.on_connect=self.on_mqtt_connect
            self.client.on_message=self.on_mqtt_message
            self.client.connect('192.168.4.1')

            self.client.loop_start()
            while connack_rc == -1:
                if self.stop.is_set(): # флаг выхода из потока
                    return
                time.sleep(0.5)
            print("CONNACK reason code: %d" % (connack_rc))
            self.client.disconnect()
            self.client.loop_stop()
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")

#
# Event Handler
#
    @mainthread
    def on_ble_update_event(self, *args):
        pass

    @mainthread
    def on_ble_new_station(self, *args):
        txt_mac = args[0]
        self.ids['id_station_enums'].add_widget( Label(size_hint_y=None, height=30, text=txt_mac) )
        pass

    def on_mqtt_connect(self, userdata, flags, rc, t1):
        print("*")
        print("* Connected with result code "+str(rc))
        print("*")
        self.client.subscribe('/beacons/office')
    
    #
    # Обработчик брокера
    #
    def on_mqtt_message(self, userdata, rc1, message ):
        json_str = str(message.payload.decode("utf-8"))
        json_obj = None
        
        # отладка
        # print("received message =",json_str)
        
        # Разбираем пакет и заполняем массивы
        # 
        json_obj = json_parser.loads( json_str )
        for i in range(len(json_obj['e'])):
            # Обход dict по индексу
            mac     = json_obj['e'][i]['m'];    # Вытаскиваем MAC адрес
            station = json_obj['st'];
            
            # Обработка станций
            if station in self.stations:
                pass
            else:
                print("new_station:" + station )
                self.stations[station] = {
                    'x':0,# Math.floor((Math.random() * 500) + 1)
                    'y':0 # Math.floor((Math.random() * 300) + 1)
                }
                self.dispatch('on_ble_new_station', station, self.stations[station])
            pass

            # Обработка маяков
            if mac in self.stations:
                # Dont measure stations rssi
                # with other stations.
                pass
            else:
                if {mac, station} <= self.beacons.keys():
                   del (self.beacons[mac][station])
                
                # Если ключа нет в списке, создаем
                if mac not in self.beacons :
                    self.beacons[mac] = {}
                
                self.beacons[mac][station] = {
                    'rssi':  json_obj['e'][i]['r'],
                    'timestamp': datetime.now().timestamp()
                }
        pass
        
        # данные готовы
        _tuple = (self.stations, self.beacons)
        self.dispatch('on_ble_update_event', _tuple)

        pass