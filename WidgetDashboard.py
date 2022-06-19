import math
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
        _obj = args[1]
        _key = args[0]

        if _obj not in self.station_coords:
            self.station_coords[_key] = WidgetStation( source='assets/icon_1.png', pos=self.pos)
            self.add_widget( self.station_coords.get(_key) )
    
    @mainthread
    def on_ble_update_event(self, *args):
        #print("WidgetDashboard.on_ble_update_event");
        
        _station        = args[1][0]
        _beacons        = args[1][1]

        _widthMeters    = 1.85

        for key in _beacons:
            # CALCULATE POSITION COORDINATES
            if len(_beacons[key])  >= 3 and len(_station) >= 3:
                print(key+" :" + str(_beacons[key]) )
                
                if key not in self.beacon_coords:
                    tmp =  WidgetStation( source='assets/icon_2.png', pos=self.pos)
                    self.beacon_coords[key] = tmp
                    self.add_widget( tmp )
                    pass

                coords = self._ble_get_coord( _beacons[key], _station, ( 400 / _widthMeters) )
                if coords != None:
                    self.beacon_coords.get(key).pos.x = coords['x'];
                    self.beacon_coords.get(key).pos.y = coords['y'];
                else:
                    print("Failed to locate:"+key+str(_beacons[key]));
            pass
        pass

        for i in self.station_coords:
            print(self.station_coords.get(i).pos)

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

        _sorted = sorted (beacon.keys());
        _keysSorted = _sorted #reversed( )

        _input =[
            [ stations[_keysSorted[0]]['x'], stations[_keysSorted[0]]['y'],  self._ble_calculate_distance( beacon[_keysSorted[0]]['rssi'], px_meter)],
            [ stations[_keysSorted[1]]['x'], stations[_keysSorted[1]]['y'],  self._ble_calculate_distance( beacon[_keysSorted[1]]['rssi'], px_meter)],
            [ stations[_keysSorted[2]]['x'], stations[_keysSorted[2]]['y'],  self._ble_calculate_distance( beacon[_keysSorted[2]]['rssi'], px_meter)]
        ]

        _output = 0 #trilat(_input)
        
        _coord = {
        'x':int(math.floor(2.3)),
        'y':int(math.floor(2.3))
        }

        return _coord
    
    def _ble_calculate_distance(self, rssi, px_meter):
        # ITAG -70 ... -94
        #    Samsung -73 ... -95
        #
        # RSSI = TxPower - 10 * n * lg(d)
        # n = 2...4
        # d = 10^(TxPower - RSSI) / (10 * n))

        _P = -69 # @TODO This value should come from MQTT message
        _n = 3
        _d = math.pow(10, ((_P-int(rssi)) / (10*_n)) ) # (n ranges from 2 to 4)
        
        return _d*px_meter