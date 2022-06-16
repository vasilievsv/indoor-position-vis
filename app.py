from kivy.app import App
from kivy.lang import Builder

from kivy.uix.button import Button
from kivy.uix.widget import Widget

from random import random
from kivy.config import Config
 

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800') 
Config.set('graphics', 'height', '400')


class MyDashboardWidget(Widget):

    def on_touch_down(self, touch):
        print("on_touch_down")

    def on_touch_move(self,touch):
        print("on_touch_move")

    def on_touch_up(self,touch):
        print("on_touch_up")


class Application(App):

    def build(self):
        return Builder.load_file("views/main.kv")

        parent = Widget()
        self.painter = MyDashboardWidget()

        clearbtn = Button(text='Clear')
        clearbtn.bind(on_release=self.clear_canvas)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)

        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()


if __name__ == '__main__':
    Application().run()