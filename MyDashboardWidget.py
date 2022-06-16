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
  
    def compare_pos_to_widget(self, widget, pos):
        #if self.orientation == 'vertical':
        #    return 'before' if pos[1] >= widget.center_y else 'after'
        #return 'before' if pos[0] < widget.center_x else 'after'
        pass

    #def handle_drag_release(self, index, drag_widget):
    #    #self.add_widget(drag_widget, index)

class DashboardIcon(DragBehavior, Image):

    def __init__(self, **kwargs):
        super(DashboardIcon, self).__init__(**kwargs)
        self.drag_timeout = 10000000
        self.drag_distance = 0
        self.drag_rectangle = [self.x, self.y, self.width, self.height]
        self.size_hint = (0.1,0.1)

    def on_pos(self, *args):
        self.drag_rectangle = [self.x, self.y, self.width, self.height]

    def on_size(self, *args):
        self.drag_rectangle = [self.x, self.y, self.width, self.height]

    def initiate_drag(self):
        # during a drag, we remove the widget from the original location
        self.parent.remove_widget(self)





class MyDashboardWidget(Widget):

    def on_touch_down(self, touch):
        print("on_touch_down")

    def on_touch_move(self,touch):
        print("on_touch_move")

    def on_touch_up(self,touch):
        print("on_touch_up")