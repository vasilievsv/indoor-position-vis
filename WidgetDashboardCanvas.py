from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout 

class DashboardCanvas(FloatLayout):

    def __init__(self,**kwargs):
        super(DashboardCanvas, self).__init__(**kwargs)
        self.size_hint = (1,1)
        self.orientation = "vertical"
  
    def handle_drag_release(self, index, drag_widget):
        #self.add_widget(drag_widget, index)
        print('drag stop')