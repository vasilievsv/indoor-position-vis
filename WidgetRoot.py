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

    sortedBeacons   ={}
    knownBeacons    =[]

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        # Наши события
        self.register_event_type('on_ble_update_event')
        self.register_event_type('on_ble_station_update') 

    @mainthread
    def cmd_connect(self):
        if self.stop.is_set() == False:
            threading.Thread(target=self.thread_mqtt_loop).start()
    #
    # Все элементы подготовлены
    #
    def on_kv_post(self, base_widget):
        #
        # Поиск всех элементов с методом on_ble_update_event
        #
        for child_id in self.ids:
            
            if hasattr(self.ids[child_id], "on_ble_update_event"):
                self.bind(on_ble_update_event=self.ids[child_id].on_ble_update_event)
            
            if hasattr(self.ids[child_id], "on_ble_station_update"):
                self.bind(on_ble_update_event=self.ids[child_id].on_ble_station_update)
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

    def on_mqtt_connect(self, userdata, flags, rc, t1):
        print("Connected with result code "+str(rc))
        self.client.subscribe('/beacons/office')
    
    #
    # Обработчик брокера
    #
    def on_mqtt_message(self, userdata, rc1, message ):
        json_str = str(message.payload.decode("utf-8"))
        json_obj = None
        
        # отладка
        # print("received message =",json_str)
        
        # Разбор пакета
        json_obj = json_parser.loads( json_str )
        for i in range(len(json_obj['e'])):
            # Обход dict по индексу
            mac     = json_obj['e'][i]['m'];    # Вытаскиваем MAC адрес
            station = json_obj['st'];
            # Игнорим известные станции
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
                    del (self.beacons[mac][station])

                # Новая запись
                self.beacons[mac] = {}
                self.beacons[mac][station] = {
                    'rssi':  json_obj['e'][i]['r'],
                    'timestamp': datetime.now().timestamp()
                }
            
            self._updateStationMacList()
            self.sortedBeacons = self._beaconMacList()

        pass

        # данные готовы
        _tuple = (self.stations, self.beacons)
        self.dispatch('on_ble_update_event', _tuple)
        
#
# Event Handler
#
    def on_ble_update_event(self, *args):
        pass

    def on_child(self, parent,a1):
        print('on_child')
        pass

    def _beaconMacList (self): 
        objectList = {}
        list = []
        b = self.beacons
        
#        if(typeof b === 'undefined' || Object.keys(b).length === 0) 
#        {
#            return [];
#        }
#
#        for (let beacon in b) {
#            for (let mac in b[beacon]) {
#                if(typeof objectList[mac] !== 'undefined')
#                {
#                    if(objectList[mac].rssi < b[beacon][mac].rssi) 
#                    {
#                        objectList = merge(objectList, b[beacon]);
#                    }
#                } else 
#                {
#                    objectList = merge(objectList, b[beacon]);
#                }
#            }
#        }

#        for(let beacon in objectList) 
#        {
#            list.push({mac: beacon, rssi: objectList[beacon].rssi, timestamp: objectList[beacon].timestamp})
#        }
#
#        return list.sort(function(a, b)
#        {
#            return a.rssi - b.rssi;
#        }).reverse();

        pass
    
    #  Метод добавляет новую станцию в список 
    def _updateStationMacList (self): 
    
        beacon_list = self.beacons;
#        if(typeof beacon_list === 'undefined' || Object.keys(beacon_list).length === 0) {
#            return [];
#        }
#
        _station_list = self.stations;
        for  beacon in beacon_list[:]:
            for station in beacon_list[beacon]:
                if {station} <= _station_list.keys() == False:
                    _station_list[station] = {
                        'x':0,# Math.floor((Math.random() * 500) + 1)
                        'y':0 # Math.floor((Math.random() * 300) + 1)
                    }
                    self.stations = _station_list
                pass
            pass

        self.dispatch('on_ble_station_update', '')
        pass