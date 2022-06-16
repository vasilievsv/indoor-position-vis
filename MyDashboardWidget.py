from kivy.uix.widget import Widget

class MyDashboardWidget(Widget):

    def on_touch_down(self, touch):
        print("on_touch_down")

    def on_touch_move(self,touch):
        print("on_touch_move")

    def on_touch_up(self,touch):
        print("on_touch_up")