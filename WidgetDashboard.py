"""
    -----------------------------------------------------------
    WidgetDashboard



    -----------------------------------------------------------
"""
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


class WidgetDashboard(FloatLayout):

    def __init__(self,**kwargs):
        super(WidgetDashboard, self).__init__(**kwargs)
        self.size_hint = (1,1)
        self.orientation = "vertical"

    beacon_coords   = {}
    station_coords  = {}



    _widthMeters    = 41
    px_scale_factor        = 300
    _power          = -69
    _A              = -41
    _N              = 4

#
# on_ble_new_station
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
        if "88" in  _key:
            self.station_coords[_key].pos = (20,20)
        if "CC" in  _key:
            self.station_coords[_key].pos = (300,300)
        if "4C" in  _key:
            self.station_coords[_key].pos = (300,20)

#
# on_ble_update_event
#
    @mainthread
    def on_ble_update_event(self, *args):
        _station        = args[1][0]
        _beacons        = args[1][1]

        for key in _beacons:
            if len(_beacons[key])  >= 3 and len(_station) >= 3:
                
                # Если не наша метка пропускаем
                if key != "9c:9c:1f:10:1b:46":
                    continue

        # Отладка
        #   значения RSSI до маячка с 3 станций
               #print("on_ble_data -> "+key+" :" + str(_beacons[key]) )

                # Добавляем картинку если новый объект
                if key not in self.beacon_coords:
                    self.beacon_coords[key] =  WidgetStation( source='assets/icon_2.png', pos=self.pos, size=(10,10))
                    self.add_widget( self.beacon_coords.get(key) )
                    pass

                # CALCULATE POSITION COORDINATES
                coords = self.FindPosition( _beacons[key], _station, float(self.px_scale_factor / 1.85) )
                #print(coords)

                if coords != None:
                   self.beacon_coords.get(key).pos = coords
                else:
                    print("Failed to locate:"+key+str(_beacons[key]));
            pass
        pass


#
# Трилатерация
#
    def FindPosition(self, beacon, stations, px_meter):

        _beacons =  sorted( beacon.keys() )
        _station = self.station_coords
        
        # Станция 1
        node_1_x = _station[_beacons[1]].pos[0]
        node_1_y = _station[_beacons[1]].pos[1]
        node_1_dst = self.CalculateDistance( beacon[_beacons[1]]['rssi'], px_meter ) 
        
        # Станция 2
        node_2_x = _station[_beacons[2]].pos[0]
        node_2_y = _station[_beacons[2]].pos[1] 
        node_2_dst = self.CalculateDistance( beacon[_beacons[2]]['rssi'], px_meter ) 
        
        # Станция 3
        node_3_x = _station[_beacons[0]].pos[0]
        node_3_y = _station[_beacons[0]].pos[1] 
        node_3_dst = self.CalculateDistance( beacon[_beacons[0]]['rssi'], px_meter )

        _input =[
            [ node_1_x, node_1_y, node_1_dst],
            [ node_2_x, node_2_y, node_2_dst],
            [ node_3_x, node_2_y, node_3_dst]
        ]

    # Отладка
        print("trilat_dist:",node_1_dst,node_2_dst,node_3_dst, self._A, self._N, self.px_scale_factor)

        _output = self.Trilat(_input)
        
        _coord = (
             _output[0],
             _output[1] 
        )

        return _coord

    #
    # CalculateDistance
    #
    def CalculateDistance(self, rssi, px_meter):
    
    # Вариант 1
    # https://medium.com/beingcoders/convert-rssi-value-of-the-ble-bluetooth-low-energy-beacons-to-meters-63259f307283
        _P = self._A            # beacon broadcast power in dBm at 1 m (Tx Power) 
        _S = int(rssi)          # measured signal value (RSSI) in dBm 
        _n = self._N            # environmental factor 
       
        #_d = math.pow(10, (_P-_S) / (10*_n))
        _d = math.pow(10,((_S-_P)/(-10*_n))) * px_meter
        return _d 

    # Вариант 2
        ###расчет через опорную точку ( координаты расчитаны )
        #A = self._A #-47.370
        #N = self._N #-67.1
        #return exp((A-int(rssi))/N) *px_meter
        
     # Вариант 3
     # От Android'a 
#        ratio = rssi*1.0/self._A;
#
#        if ratio < 1.0 :
#            return  math.pow(ratio, (_P-_S) / (10*_n)) *px_meter #math.pow(ratio,10)
#        else:
#            return ((0.89976)*math.pow(ratio,7.7095) + 0.111)*px_meter


    def Trilat(self, input):
        try:
            # Координаиты 1 станции
            x1 = Xa = input[0][0] 
            y1 = Ya = input[0][1]

            # Координаиты 2 станции
            x2 = Xb = input[1][0]
            y2 = Yb = input[1][1]

            # Координаиты 3 станции
            x3 = Xc = input[2][0]
            y3 = Yc = input[2][1]

            r1= dist_A = (input[0][2])
            r2= dist_B = (input[1][2])
            r3= dist_C = (input[2][2])
# ВАРИАНТ 1
#            Va = ((Xc**2 - Xb**2) + (Yc**2 - Yb**2) + (dist_B**2 - dist_C**2))/2
#            Vb = ((Xa**2 - Xb**2) + (Ya**2 - Yb**2) + (dist_B**2 - dist_A**2))/2
#
#            y = (Vb*(Xb-Xc)-Va*(Xb-Xa))/((Ya-Yb)*(Xb-Xc)-(Yc-Yb)*(Xb-Xc))
#            x = -1 * (Va+y*(Yb-Yc))/(Xb-Xc)
#

# ВАРИАНТ 2
            A = 2*x2 - 2*x1
            B = 2*y2 - 2*y1
            C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
            D = 2*x3 - 2*x2
            E = 2*y3 - 2*y2
            F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
            x = (C*E - F*B) / (E*A - B*D)
            y = (C*D - A*F) / (B*D - A*E)

            return (x,y)
        except:
            print("Trilateration: divide_error") 
         
        return (0,0)

#
# Drag & Drop
#
    def handle_drag_release(self, index, drag_widget):
        print("handle_drag_release")
        #self.add_widget(drag_widget, index)
        pass
