from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.behaviors import DragBehavior

class DashboardCanvas(DragBehavior,FloatLayout):

    def __init__(self,**kwargs):
        super(DashboardCanvas, self).__init__(**kwargs)
        self.size_hint = (1,1)
        self.orientation = "vertical"
  
    def handle_drag_release(self, index, drag_widget):
        #self.add_widget(drag_widget, index)
        print('drag stop')

    def on_ble_update_event(self, *args):
        pass

    def on_parent(self, parent,a1):
        pass
        if parent:
            parent.bind(on_ble_update_event=self.on_ble_update_event)
            print('test')

