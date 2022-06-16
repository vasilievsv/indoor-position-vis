from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout 


class DashboardCanvas(DragBehavior, FloatLayout):

    def compare_pos_to_widget(self, widget, pos):
        #if self.orientation == 'vertical':
        #    return 'before' if pos[1] >= widget.center_y else 'after'
        #return 'before' if pos[0] < widget.center_x else 'after'
        pass

    def handle_drag_release(self, index, drag_widget):
        self.add_widget(drag_widget, index)

class DashboardIcon(DragBehavior, Image):

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