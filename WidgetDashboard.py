from kivy.event import EventDispatcher
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout 
from kivy.clock import Clock, mainthread
import math

class WidgetDashboard(DragBehavior,FloatLayout,EventDispatcher):

    def __init__(self,**kwargs):
        super(WidgetDashboard, self).__init__(**kwargs)
        self.size_hint = (1,1)
        self.orientation = "vertical"
#
# Event Handler
#
    @mainthread
    def on_ble_station_update(self, *args):
        obj = args[1]
        pass

    def on_ble_update_event(self, *args):
        print("WidgetDashboard.on_ble_update_event");
        
        _station        = args[1][0]
        _beacons        = args[1][1]
        beaconCoords    = {};
        _widthMeters    = 1.85

        for key in _beacons:
            #print(key+" st:"+str(len(_beacons[key])) )
            
            if len(_beacons[key])  >= 3 and  len(_station) >= 3:
                print(key+" :" + str(_beacons[key]) )
                #print("CALCULATE POSITION COORDINATES")
                #coords = get_coord( _beacons[key], _station, ( 400 / _widthMeters) )
                #if coords != None:
                #    self.beaconCoords[key] = coords;
                #else:
                #    print("Failed to locate:");
                #    print(_beacons[key]);
                pass
            else:
                pass
        pass

    def on_ble_station_update(self,*args):
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
    def get_coord (beacon, stations, px_meter):

        _keysSorted = reversed(sorted (beacon.keys()))

        _input =[
            [ stations[_keysSorted[0]].x, stations[_keysSorted[0]].y,  _ble_calculate_distance( beacon[_keysSorted[0]].rssi, px_meter)],
            [ stations[_keysSorted[1]].x, stations[_keysSorted[1]].y,  _ble_calculate_distance( beacon[_keysSorted[1]].rssi, px_meter)],
            [ stations[_keysSorted[2]].x, stations[_keysSorted[2]].y,  _ble_calculate_distance( beacon[_keysSorted[2]].rssi, px_meter)]
        ]

        _output = 0 #trilat(_input)
        
        _coord = {
        'x':int(math.floor(2.3)),
        'y':int(math.floor(2.3))
        }

        return _coord
    
    def _ble_calculate_distance(rssi, px_meter):
        #ITAG -70 ... -94
        #    Samsung -73 ... -95
        #
        #RSSI = TxPower - 10 * n * lg(d)
        #n = 2...4
        #d = 10^(TxPower - RSSI) / (10 * n))

        _P = -69 # @TODO This value should come from MQTT message
        _n = 3
        _d = math.pow(10, ((_P-rssi) / (10*_n)) ) # (n ranges from 2 to 4)
        
        return _d*px_meter



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