from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout 
from kivy.event import EventDispatcher

class WidgetDashboard(DragBehavior,FloatLayout,EventDispatcher):

    def __init__(self,**kwargs):
        super(WidgetDashboard, self).__init__(**kwargs)
        self.size_hint = (1,1)
        self.orientation = "vertical"
  
    def on_parent(self, parent, _id):
        #if parent:
        #    parent.bind(on_ble_update_event=self.on_ble_update_event)
        if hasattr(parent, "id"):
            print('item: {}'.child.id)

        pass

    def on_ble_update_event(self, *args):
        print("WidgetDashboard.on_ble_update_event");
        pass

#
# Drag & Drop
#
    def handle_drag_release(self, index, drag_widget):
        pass
        #self.add_widget(drag_widget, index)
        #print('drag stop')
