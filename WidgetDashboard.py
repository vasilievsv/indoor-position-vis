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


class WidgetDashboard(DragBehavior,FloatLayout,EventDispatcher):

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
 
    @mainthread
    def on_ble_update_event(self, *args):
        _station        = args[1][0]
        _beacons        = args[1][1]

        _widthMeters    = 1.85

        for key in _beacons:
            if len(_beacons[key])  >= 3 and len(_station) >= 3:
                #print(key+" :" + str(_beacons[key]) )
                
                # Иконки 
                if key not in self.beacon_coords:
                    self.beacon_coords[key] =  WidgetStation( source='assets/icon_2.png', pos=self.pos)
                    self.add_widget( self.beacon_coords.get(key) )
                    pass

                # CALCULATE POSITION COORDINATES
                coords = self._ble_get_coord( _beacons[key], _station, ( 400 / _widthMeters) )
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

        print(_input)
        _output = self.trilateration(_input)
        
        _coord = (
            int(math.floor(2.3)),
            int(math.floor(2.3))
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

    def trilateration( self, data ):
        x1 = data[0][0]
        y1 = data[0][1]
        r1 = data[0][2]
        
        x2 = data[1][0]
        y2 = data[1][1]
        r2 = data[1][2]
        
        x3 = data[2][0]
        y3 = data[2][1]
        r3 = data[2][2]

        A = 2*x2 - 2*x1
        B = 2*y2 - 2*y1
        C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
        D = 2*x3 - 2*x2
        E = 2*y3 - 2*y2
        F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
        x = (C*E - F*B) / (E*A - B*D)
        y = (C*D - A*F) / (B*D - A*E)
        return (x,y)
