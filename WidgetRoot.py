"""
    -----------------------------------------------------------
    RootWidget



    -----------------------------------------------------------
"""
import sys
import time
import threading
import math
import numpy as np
from collections import deque

from filterpy.kalman import KalmanFilter 

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

class RingBuffer(deque):
    """
    inherits deque, pops the oldest data to make room
    for the newest data when size is reached
    """
    def __init__(self, size):
        deque.__init__(self)
        self.size = size
        
    def full_append(self, item):
        deque.append(self, item)
        # full, pop the oldest item, left most item
        self.popleft()
        
    def append(self, item):
        deque.append(self, item)
        # max size reached, append becomes full_append
        if len(self) == self.size:
            self.append = self.full_append
    
    def get(self):
        """returns a list of size items (newest items)"""
        return list(self)




class RootWidget(BoxLayout,EventDispatcher):

    stop    = threading.Event()         # флаг выхода из потока
    client  = mqtt.Client("client-001")

    errors          = [];    #
    beacons         = {};   # 
    stations        = {};  #
    sortedBeacons   = {}
    knownBeacons    = []


    blemacid = {"9c:9c:1f:10:1b:46": KalmanFilter(1,1)}

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
        print("**")
        print("** Connected with result code "+str(rc))
        print("**")
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
                    'x':0,
                    'y':0
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
                
                # Если ключа нет в списке, 
                # создаем новую запись
                if mac not in self.beacons :
                    self.beacons[mac] = {}
                
                _rssi = int(json_obj['e'][i]['r'])

                ###
                ## Use math  filter by station
                #
                if station not in self.blemacid:
                    self.blemacid[station]= RingBuffer(10)
                self.blemacid[station].append( _rssi )
                                
                #_rssi = self.kalman_filter(self.blemacid[station].get(), A=2, H=2, Q=1, R=1)
                #_rssi = sum(self.blemacid[station]) / len(self.blemacid[station])
                _rssi = max( self.blemacid[station] )
                self.beacons[mac][station] = {
                    'rssi': math.floor(_rssi),
                    'timestamp': 0 
                }
        pass
        
        # данные готовы
        _tuple = (self.stations, self.beacons)
        self.dispatch('on_ble_update_event', _tuple)

        pass

    # https://github.com/philipiv/rssi-filtering-kalman
    def kalman_block(self, x, P, s, A, H, Q, R):

        """
        Prediction and update in Kalman filter
        input:
            - signal: signal to be filtered
            - x: previous mean state
            - P: previous variance state
            - s: current observation
            - A, H, Q, R: kalman filter parameters
        output:
            - x: mean state prediction
            - P: variance state prediction
        """

        # check laaraiedh2209 for further understand these equations

        x_mean = A * x + np.random.normal(0, Q, 1)
        P_mean = A * P * A + Q

        K = P_mean * H * (1 / (H * P_mean * H + R))
        x = x_mean + K * (s - H * x_mean)
        P = (1 - K * H) * P_mean

        return x, P
        
    # https://github.com/philipiv/rssi-filtering-kalman
    def kalman_filter(self, signal, A, H, Q, R):

        """
        Implementation of Kalman filter.
        Takes a signal and filter parameters and returns the filtered signal.
        input:
            - signal: signal to be filtered
            - A, H, Q, R: kalman filter parameters
        output:
            - filtered signal
        """

        predicted_signal = []

        x = signal[0]                                 # takes first value as first filter prediction
        P = 0                                         # set first covariance state value to zero

        predicted_signal.append(x)
        for j, s in enumerate(signal[1:]):            # iterates on the entire signal, except the first element

            x, P = self.kalman_block( x, P, s, A, H, Q, R)  # calculates next state prediction

            predicted_signal.append(x)                # update predicted signal with this step calculation

        return int(x)