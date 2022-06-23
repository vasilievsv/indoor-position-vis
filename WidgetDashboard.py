import math
import numpy as np
from math import exp 

from kivy.clock import Clock, mainthread
from kivy.event import EventDispatcher
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout 

from WidgetStation import WidgetStation


class WidgetDashboard(FloatLayout,EventDispatcher):

    def __init__(self,**kwargs):
        super(WidgetDashboard, self).__init__(**kwargs)
        self.size_hint = (1,1)
        self.orientation = "vertical"

    beacon_coords    = {}
    station_coords   = {}

    _widthMeters    = 1.85
    _screenw=100
    _power = -69

    _A = -90
    _N = -67.1

#
# Event Handler
#
    @mainthread
    def on_ble_new_station(self, *args):
        _key = args[1]
        _obj = args[2]

        if _key not in self.station_coords:
            self.station_coords[_key] = WidgetStation( source='assets/icon_1.png', pos=self.pos)
            self.add_widget( self.station_coords.get(_key) )

        # расстановка станций по углам
        _l = len(self.station_coords)
        print(_key)
        if "CC" in  _key:
            self.station_coords[_key].pos = (100,100)
        if "88" in  _key:
            self.station_coords[_key].pos = (1,100)
        if "4C" in  _key:
            self.station_coords[_key].pos = (100,1)

    @mainthread
    def on_ble_update_event(self, *args):
        _station        = args[1][0]
        _beacons        = args[1][1]



        for key in _beacons:
            if len(_beacons[key])  >= 3 and len(_station) >= 3:
                
                # Если не наша метка пропускаем
                if key != "9c:9c:1f:10:1b:46":
                    continue
                
                #print(key+" :" + str(_beacons[key]) )

                # Добавляем картинку если новый объект
                if key not in self.beacon_coords:
                    self.beacon_coords[key] =  WidgetStation( source='assets/icon_2.png', pos=self.pos, size=(10,10))
                    self.add_widget( self.beacon_coords.get(key) )
                    pass

                # CALCULATE POSITION COORDINATES
                coords = self.FindPosition( _beacons[key], _station, float(self._screenw / 1.85) )

                if coords != None:
                   self.beacon_coords.get(key).pos = coords
                else:
                    print("Failed to locate:"+key+str(_beacons[key]));
            pass
        pass

#
# Drag & Drop
#
    def handle_drag_release(self, index, drag_widget):
        print("handle_drag_release")
        #self.add_widget(drag_widget, index)
        pass

#
# Трилатерация
#
    def FindPosition(self, beacon, stations, px_meter):

        _beacons =  sorted (beacon.keys());
        pt = self.station_coords
        
        # Станция 1
        node_1_x = pt[_beacons[0]].pos[0]
        node_1_y = pt[_beacons[0]].pos[1] 
        node_1_dst = self.CalculateDistance( beacon[_beacons[0]]['rssi'], px_meter ) 
        # Станция 2
        node_2_x = pt[_beacons[1]].pos[0]
        node_2_y = pt[_beacons[1]].pos[1] 
        node_2_dst = self.CalculateDistance( beacon[_beacons[1]]['rssi'], px_meter ) 
        # Станция 3
        node_3_x = pt[_beacons[2]].pos[0]
        node_3_y = pt[_beacons[2]].pos[1] 
        node_3_dst = self.CalculateDistance( beacon[_beacons[2]]['rssi'], px_meter ) 

    
        _input =[
            [ node_1_x, node_1_y, node_1_dst],
            [ node_2_x, node_2_y, node_2_dst],
            [ node_3_x, node_2_y, node_3_dst]
        ]

        _output = self.Trilat(_input)
        
        _coord = (
            int(math.floor( _output[0] )),
            int(math.floor( _output[1] ))
        )

        return _coord
    
    def CalculateDistance(self, rssi, px_meter):
        
    # Вариант 1
        #расчет через опорную точку
        A = self._A#-47.370
        N = self._N#-67.1
        return exp((int(rssi)-A)/N)*px_meter

    # Вариант 2
        #_P = self._A #-69 # @TODO This value should come from MQTT message
        #_n = 4.7
        #_d = math.pow(10, ((int(rssi)-_P) / (10*_n)) ) # (n ranges from 2 to 4)
        #return _d*px_meter

    def Trilat(self, input):
        try:
            # Координаиты 1 станции
            Xa = input[0][0] 
            Ya = input[0][1]

            # Координаиты 2 станции
            Xb = input[1][0]
            Yb = input[1][1]


            # Координаиты 3 станции
            Xc = input[2][0]
            Yc = input[2][1]


            dist_A = input[0][2]
            dist_B = input[1][2]
            dist_C = input[2][2]
            
            print(dist_A,dist_B,dist_C)
            print(self._A,self._N, self._widthMeters)

            Va = ((Xc**2 - Xb**2) + (Yc**2 - Yb**2)  + (dist_B**2 - dist_C**2))/2
            Vb = ((Xa**2 - Xb**2) + (Ya**2 - Yb**2) + (dist_B**2 - dist_A**2))/2

            y = (Vb*(Xb-Xc)-Va*(Xb-Xa))/((Ya-Yb)*(Xb-Xc)-(Yc-Yb)*(Xb-Xc))
            x = -1 * (Va+y*(Yb-Yc))/(Xb-Xc)

            return (x,y)
        except:
            print("divide error") 
         
    
        return (0,0)
