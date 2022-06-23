from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config

import WidgetRoot
import WidgetStation
import WidgetDashboard

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '840')
Config.set('graphics', 'height', '420')

class Application(App):

    def on_stop(self):
        #Выход из приложения и установка флага выхода из потока для дочерних потоков
        #в противном случае окно приложения закроется, но процесс Python будет
        #продолжайте работать до тех пор, пока все вторичные потоки не остановятся.
        self.root.stop.set()

    def build(self):
        return Builder.load_file("views/main.kv")

# entry_point
if __name__ == '__main__':
    Application().run()