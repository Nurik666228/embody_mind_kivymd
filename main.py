from kivy.config import Config

# конфигурация окна (добавлен ради тестировки, будет убран при релизе)
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '600')

from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.graphics import Color, Rectangle


class MainMenu(Screen):  # главное меню
    quit_dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        label = MDLabel(text='Embody Mind', pos_hint={'center_x': 0.5, 'center_y': 0.9},
                        size_hint=(0.5, 0.1), halign='center', font_style="H5")
        self.add_widget(label)
        # остальные кнопки в kv file

    def show_quit_dialog(self):  # показывает диалоговое окно закрытия приложения
        if not self.quit_dialog:
            self.quit_dialog = MDDialog(
                title="Are you sure?",
                buttons=[
                    MDFlatButton(text="Cancel", font_style="Button", on_release=self.close_quit_dialog),
                    MDFlatButton(text="Yes", font_style="Button", on_release=self.close_app)
                ]
            )

        self.quit_dialog.open()

    def close_quit_dialog(self, obj):  # закрытие диалога (отмена)
        self.quit_dialog.dismiss()

    def close_app(self, obj):  # закрытие приложения
        MDApp.get_running_app().stop()

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
