from kivy.uix.image import Image
from kivy.uix.behaviors import DragBehavior


class WidgetStation(DragBehavior, Image):

    def __init__(self, **kwargs):
        super(WidgetStation, self).__init__(**kwargs)
        self.drag_timeout   = 10000000
        self.drag_distance  = 0
        self.drag_rectangle = [self.x, self.y, self.width, self.height]
        self.size       = (24, 24)
        self.size_hint  = (None, None)

    def on_pos(self, *args):
        self.drag_rectangle = [self.x, self.y, self.width, self.height]

    def on_size(self, *args):
        self.drag_rectangle = [self.x, self.y, self.width, self.height]

    def initiate_drag(self):
        # during a drag, we remove the widget from the original location
        #self.parent.remove_widget(self)
        print('initiate_drag')

#
# Drag & Drop
#
    #def on_touch_down(self, touch):
    #    if self.collide_point(*touch.pos):
    #        if touch.button == "right":
    #            pass
    #        elif touch.button == "left":
    #            print("on_touch_down")
    #        else:
    #            print(self.id)
    