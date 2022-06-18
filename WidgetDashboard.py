from kivy.event import EventDispatcher
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout 
import math

class WidgetDashboard(DragBehavior,FloatLayout,EventDispatcher):

    def __init__(self,**kwargs):
        super(WidgetDashboard, self).__init__(**kwargs)
        self.size_hint = (1,1)
        self.orientation = "vertical"
    
    def on_ble_update_event(self, *args):
        print("WidgetDashboard.on_ble_update_event");
        
        _station = args[1][0]
        _beacons = args[1][1]

        for i in _station:
            print("СТАНЦИЯ:")
            print(i)

        for j in _beacons:
            print("МАРКЕРЫ:")
            print(j)

        pass

#
# Drag & Drop
#
    def handle_drag_release(self, index, drag_widget):
        print("handle_drag_release")
        #self.add_widget(drag_widget, index)
        pass

    def updateBeaconPositions(self):
        # Beacons
#        beaconCoords = {};
#        if this.props.beacons:
#             b = self.props.beacons;
#            for key in b:
#                if(Object.keys(b[key]).length >= 3 && Object.keys(this.props.stations).length >= 3):
#                    // CALCULATE POSITION COORDINATES
#                    let coords = locate( b[key], this.props.stations, (this.props.width / this.props.widthMeters));
#                    if coords !== null:
#                        self.beaconCoords[key] = coords;
#                    else:
#                        console.log("Failed to locate:");
#                        console.debug(b[key]);
#                    pass
#                else:
#
#                pass
#            pass

        pass
#
# Трилатерация
#
    def locate (beacon, stations, px_meter):

        _keysSorted = reversed(sorted (beacon.keys()))

        _input =[
            [ stations[_keysSorted[0]].x, stations[_keysSorted[0]].y,  _ble_calculate_distance( beacon[_keysSorted[0]].rssi, px_meter)],
            [ stations[_keysSorted[1]].x, stations[_keysSorted[1]].y,  _ble_calculate_distance( beacon[_keysSorted[1]].rssi, px_meter)],
            [ stations[_keysSorted[2]].x, stations[_keysSorted[2]].y,  _ble_calculate_distance( beacon[_keysSorted[2]].rssi, px_meter)]
        ]

        _output = 0 #trilat(intpu)
        
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
