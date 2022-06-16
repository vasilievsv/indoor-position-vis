from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout 

class DashboardIcon(DragBehavior, Image):

    def __init__(self, **kwargs):
        super(DashboardIcon, self).__init__(**kwargs)
        self.drag_timeout   = 10000000
        self.drag_distance  = 0
        self.drag_rectangle = [self.x, self.y, self.width, self.height]
        self.size       = (48, 48)
        self.size_hint  = (None, None)

    def on_pos(self, *args):
        self.drag_rectangle = [self.x, self.y, self.width, self.height]

    def on_size(self, *args):
        self.drag_rectangle = [self.x, self.y, self.width, self.height]

    def initiate_drag(self):
        # during a drag, we remove the widget from the original location
        #self.parent.remove_widget(self)
        print('sss')

    #def on_touch_down(self, touch):
    #    return True
    #    #if self.collide_point(*touch.pos):
    #    #    if touch.button == "right":
    #    #        print('Right mouse clicked on ')
    #    #    elif touch.button == "left":
    #    #        print('Left mouse clicked on ')
    #    #    else:
    #    #        print(self.id)
    #    #print("on_touch_down")