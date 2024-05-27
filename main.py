from kivy.config import Config

# конфигурация окна (добавлен ради тестирования, будет убран при релизе)
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '600')

from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDRectangleFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, BooleanProperty
from types import SimpleNamespace
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

import json
# импортируются три файла с языками
from en import en
from ru import ru
from kaz import kaz

# открывает файл с параметрами и записывает текущий язык
with open("settings.json", "r") as f:
    settings = json.load(f)
    current_lang = settings["language"]


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

music = SoundLoader.load('audio/music1.wav')
click = SoundLoader.load('audio/click.mp3')
if settings["music_state"]:
    print("Sound found at %s" % music.source)
    print("Sound is %.3f seconds" % music.length)
    music.loop = True
    music.play()


class MainMenu(Screen):  # главное меню
    global text, current_lang, settings
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
        EmbodyMindApp().play_click_sound()
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
    global text, current_lang, settings, music
    change_lang_dialog = None
    # текст настроек
    title = StringProperty(text[current_lang].settings_menu.title)
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
        EmbodyMindApp().play_click_sound()
        self.manager.current = "MainMenu"

    def check_music_state(self):
        EmbodyMindApp().play_click_sound()
        if settings["music_state"]:
            settings["music_state"] = False
        else:
            settings["music_state"] = True

        if settings["music_state"]:
            music.loop = True
            music.play()
        else:
            music.stop()

        with open("settings.json", "w") as file:
            json.dump(settings, file)

    def check_sounds_state(self):
        if settings["sound_state"]:
            settings["sound_state"] = False
        else:
            settings["sound_state"] = True
            EmbodyMindApp().play_click_sound()

        with open("settings.json", "w") as file:
            json.dump(settings, file)

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
        EmbodyMindApp().play_click_sound()
        self.change_lang_dialog.dismiss()

    def close_app(self, obj):  # закрытие приложения
        # код перезаписывающий текущий язык на новый, смена языка требует перезагрузки программы
        settings["language"] = self.lang
        with open("settings.json", "w") as file:
            json.dump(settings, file)
        MDApp.get_running_app().stop()  # закрытие приложения

    # функция выполняется каждый раз когда изменяется размер окна
    def on_size(self, *args):
        # задний фон меню (перерисовывается каждый раз когда меняется размер окна)
        with self.canvas.before:
            Color(255 / 255, 229 / 255, 180 / 255)
            Rectangle(pos=self.pos, size=self.size)


class BigTouchSwitch(MDAnchorLayout):  # класс кастомного выключателя музыки и аудио
    active = BooleanProperty(True)
    music_state = BooleanProperty(settings["music_state"])
    sound_state = BooleanProperty(settings["sound_state"])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.active = not self.active
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            return True
        return super().on_touch_up(touch)


class GamesMenu(Screen):
    def return_to_main_menu(self):
        EmbodyMindApp().play_click_sound()
        self.manager.current = "MainMenu"

    # функция выполняется каждый раз когда изменяется размер окна
    def on_size(self, *args):
        # задний фон меню (перерисовывается каждый раз когда меняется размер окна)
        with self.canvas.before:
            Color(255 / 255, 229 / 255, 180 / 255)
            Rectangle(pos=self.pos, size=self.size)


class Game1Menu(Screen):
    def return_to_games_menu(self):
        EmbodyMindApp().play_click_sound()
        self.manager.current = "GamesMenu"


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.key_input)

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            if self.current != "MainMenu":
                self.current = self.previous()
            return True
        else:  # the key now does nothing
            return False


class EmbodyMindApp(MDApp):
    global settings, click

    def build(self):
        self.theme_cls.primary_palette = "Gray"  # цвет темы
        self.theme_cls.primary_hue = "A700"  # яркость цвета темы
        return WindowManager()

    def play_click_sound(self):
        if settings["sound_state"]:
            click.play()


if __name__ == "__main__":
    EmbodyMindApp().run()
