import math
import numpy as np

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
        if _l == 1:
            self.station_coords[_key].pos = (100,100)
        if _l == 2:
            self.station_coords[_key].pos = (0,100)
        if _l == 3:
            self.station_coords[_key].pos = (100,0)

    @mainthread
    def on_ble_update_event(self, *args):
        _station        = args[1][0]
        _beacons        = args[1][1]

        _widthMeters    = 1.85

        for key in _beacons:
            if len(_beacons[key])  >= 3 and len(_station) >= 3:
                
                print(key+" :" + str(_beacons[key]) )

                ### Если не наша метка пропускаем
                ##if key != "9c:9c:1f:10:22:8a":
                ##    continue


                # Добавляем картинку если новый объект
                if key not in self.beacon_coords:
                    self.beacon_coords[key] =  WidgetStation( source='assets/icon_2.png', pos=self.pos)
                    self.add_widget( self.beacon_coords.get(key) )
                    pass

                # CALCULATE POSITION COORDINATES
                coords = self._ble_get_coord( _beacons[key], _station, ( 200 / _widthMeters) )

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
    def _ble_get_coord(self, beacon, stations, px_meter):

        _beacons =  sorted (beacon.keys());
        st = self.station_coords

        _input =[
            [ st.get(_beacons[0]).pos[0],  st.get(_beacons[0]).pos[1],  self._ble_calculate_distance( beacon[_beacons[0]]['rssi'], px_meter )],
            [ st.get(_beacons[1]).pos[0],  st.get(_beacons[1]).pos[1],  self._ble_calculate_distance( beacon[_beacons[1]]['rssi'], px_meter )],
            [ st.get(_beacons[2]).pos[0],  st.get(_beacons[2]).pos[1],  self._ble_calculate_distance( beacon[_beacons[2]]['rssi'], px_meter )]
        ]

        _output = self.Trilat(_input)
        
        _coord = (
            int(math.floor( _output[0] )),
            int(math.floor( _output[1] ))
        )

        return _coord
    
    def _ble_calculate_distance(self, rssi, px_meter):
        # RSSI = TxPower - 10 * n * lg(d)
        # n = 2...4
        # d = 10^(TxPower - RSSI) / (10 * n))

        _P = -69 # @TODO This value should come from MQTT message
        _n = 3
        _d = math.pow(10, ((_P-int(rssi)) / (10*_n)) ) # (n ranges from 2 to 4)
        
        return _d*px_meter

    def Trilat(self, input):
       # _tuple = (0,0)
        try:
            A = -24.514
            N = -15.41

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
            
            Va = ((Xc**2 - Xb**2) + (Yc**2 - Yb**2)  + (dist_B**2 - dist_C**2))/2
            Vb = ((Xa**2 - Xb**2) + (Ya**2 - Yb**2) + (dist_B**2 - dist_A**2))/2

            y = (Vb*(Xb-Xc)-Va*(Xb-Xa))/((Ya-Yb)*(Xb-Xc)-(Yc-Yb)*(Xb-Xc))
            x = -1 * (Va+y*(Yb-Yc))/(Xb-Xc)

            _tuple = (x,y)
        except:
            _tuple = (0,0)
            print("divide error") 
            print("dist_A"+str(int(dist_A)))
            print("dist_B"+str(int(dist_B)))
            print("dist_C"+str(int(dist_C)))
            return (0,0)
    
        return _tuple
