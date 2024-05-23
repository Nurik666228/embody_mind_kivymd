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
from kivy.properties import StringProperty
from types import SimpleNamespace

# импорируются три файла с языками
from en import en
from ru import ru
from kaz import kaz

# открывает файл с заданным языком и записывает текущий язык
with open("selected_lang.txt") as file_object:
    language = file_object.read()
    current_lang = language.rstrip()


# класс создающий хорошо структурированный словарь со всеми языками
class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)


# создание словаря со всеми языками
text = {}
text.update({"en": NestedNamespace(en)})
text.update({"ru": NestedNamespace(ru)})
text.update({"kaz": NestedNamespace(kaz)})


class MainMenu(Screen):  # главное меню
    global text, current_lang
    quit_dialog = None

    # текст главного меню
    play_btn = StringProperty(text[current_lang].main_menu.play_btn)
    settings_btn = StringProperty(text[current_lang].main_menu.settings_btn)
    quit_btn = StringProperty(text[current_lang].main_menu.quit_btn)

    # текст диалогового окна закрытия приложения
    title = StringProperty(text[current_lang].quit_dialog.title)
    cancel_btn = StringProperty(text[current_lang].quit_dialog.cancel_btn)
    yes_btn = StringProperty(text[current_lang].quit_dialog.yes_btn)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        label = MDLabel(text='Embody Mind', pos_hint={'center_x': 0.5, 'center_y': 0.85},
                        size_hint=(0.5, 0.1), halign='center', font_style="H5")
        self.add_widget(label)
        # остальные кнопки в kv file

    def show_quit_dialog(self):  # показывает диалоговое окно закрытия приложения
        if not self.quit_dialog:
            self.quit_dialog = MDDialog(
                title=self.title,
                buttons=[
                    MDFlatButton(text=self.cancel_btn, font_style="Button", on_release=self.close_quit_dialog),
                    MDFlatButton(text=self.yes_btn, font_style="Button", on_release=self.close_app)
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


class SettingsMenu(Screen):
    global text, current_lang
    change_lang_dialog = None
    # текст настроек
    title = StringProperty(text[current_lang].settings_menu.music_label)
    music_label = StringProperty(text[current_lang].settings_menu.music_label)
    sounds_label = StringProperty(text[current_lang].settings_menu.sounds_label)
    language_label = StringProperty(text[current_lang].settings_menu.language_label)

    # текст диалогового окна смены языка
    dialog_title = StringProperty(text[current_lang].change_lang_dialog.title)
    dialog_text = StringProperty(text[current_lang].change_lang_dialog.text)
    cancel_btn = StringProperty(text[current_lang].change_lang_dialog.cancel_btn)
    yes_btn = StringProperty(text[current_lang].change_lang_dialog.yes_btn)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        music_label = MDLabel(text=self.music_label, pos_hint={'center_x': 0.25, 'center_y': 0.8},
                              size_hint=(0.5, 0.1), halign="center", font_style="H6")
        sound_label = MDLabel(text=self.sounds_label, pos_hint={'center_x': 0.25, 'center_y': 0.7},
                              size_hint=(0.5, 0.1), halign="center", font_style="H6")
        language_label = MDLabel(text=self.language_label, pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                 size_hint=(0.5, 0.1), halign="center", font_style="H6")
        self.add_widget(music_label)
        self.add_widget(sound_label)
        self.add_widget(language_label)

    def return_to_main_menu(self):
        self.manager.current = "MainMenu"

    def change_language(self, lang):
        self.lang = lang
        if current_lang == lang:
            pass
        else:
            return self.show_change_lang_dialog()

    def show_change_lang_dialog(self):
        if not self.change_lang_dialog:
            self.change_lang_dialog = MDDialog(
                title=self.dialog_title,
                text=self.dialog_text,
                buttons=[
                    MDFlatButton(text=self.cancel_btn, font_style="Button", on_release=self.close_restart_dialog),
                    MDFlatButton(text=self.yes_btn, font_style="Button", on_release=self.close_app)
                ]
            )
        self.change_lang_dialog.open()

    def close_restart_dialog(self, obj):  # закрытие диалога (отмена)
        self.change_lang_dialog.dismiss()

    def close_app(self, obj):  # закрытие приложения
        # код перезаписывающий текущий язык на новый, смена языка требует перезагрузки программы
        with open("selected_lang.txt", "w") as file:
            file.write(self.lang)
        MDApp.get_running_app().stop()  # закрытие приложения

    # функция выполняется каждый раз когда изменяется размер окна
    def on_size(self, *args):
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
