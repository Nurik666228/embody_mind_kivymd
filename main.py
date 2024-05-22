from kivy.config import Config

# конфигурация окна (добавлен ради тестировки, будет убран при релизе)
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '600')

from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, Rectangle


class MainMenu(Screen):  # главное меню
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        label = MDLabel(text='Embody Mind', pos_hint={'center_x': 0.5, 'center_y': 0.9},
                        size_hint=(0.5, 0.1), halign='center', font_style="H5")
        button_1 = MDRectangleFlatButton(text='Play', pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                         size_hint=(0.5, 0.09), line_width=1.5, font_style="Button")
        button_2 = MDRectangleFlatButton(text='Settings', pos_hint={'center_x': 0.5, 'center_y': 0.45},
                                         size_hint=(0.5, 0.09), line_width=1.5, font_style="Button")
        button_3 = MDRectangleFlatButton(text='Quit', pos_hint={'center_x': 0.5, 'center_y': 0.3},
                                         size_hint=(0.5, 0.09), line_width=1.5, font_style="Button")
        self.add_widget(label)
        self.add_widget(button_1)
        self.add_widget(button_2)
        self.add_widget(button_3)

    # функция выполняется каждый раз когда изменяется размер окна
    def on_size(self, *args):
        width = self.width
        height = self.height
        print(width, height)
        # задний фон меню (перерисовывается каждый раз когда меняется размер окна)
        with self.canvas.before:
            Color(255 / 255, 229 / 255, 180 / 255)
            Rectangle(pos=self.pos, size=self.size)


class WindowManager(ScreenManager):
    pass


class EmbodyMindApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Gray"  # цвет темы
        self.theme_cls.primary_hue = "A700"  # яркость цвета темы
        return WindowManager()


if __name__ == "__main__":
    EmbodyMindApp().run()
