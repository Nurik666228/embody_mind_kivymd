import random
import threading

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
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, Clock
from types import SimpleNamespace
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

from random import randint
import operator
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
    # print("Sound found at %s" % music.source)
    # print("Sound is %.3f seconds" % music.length)
    music.loop = True
    music.play()


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
    # убран с рабочего кода после рефакторинга, оставлен для возможных будущих целей
    """def on_size(self, *args):
        width = self.width
        height = self.height
        print(width, height)
        # задний фон меню (перерисовывается каждый раз когда меняется размер окна)
        with self.canvas.before:
            Color(255 / 255, 183 / 255, 80 / 255)
            Rectangle(pos=self.pos, size=self.size)
    """


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
    global text, current_lang
    top_title = StringProperty(text[current_lang].games_menu.top_title)
    guess_the_number_game = StringProperty(text[current_lang].games_menu.guess_the_number_game)
    true_false_math_game = StringProperty(text[current_lang].games_menu.true_false_math_game)

    def return_to_main_menu(self):
        EmbodyMindApp().play_click_sound()
        self.manager.current = "MainMenu"


class GuessTheNumberMenu(Screen):
    global text, current_lang
    top_title = StringProperty(text[current_lang].guess_the_number_menu.top_title)
    game_name = StringProperty(text[current_lang].guess_the_number_menu.game_name)
    game_description = StringProperty(text[current_lang].guess_the_number_menu.game_description)

    def return_to_games_menu(self):
        EmbodyMindApp().play_click_sound()
        self.manager.current = "GamesMenu"


class GuessTheNumberGame(Screen):
    restart_dialog = None
    global text, current_lang
    game_label_text = StringProperty(text[current_lang].guess_the_number_game.game_label_text)
    enter_btn = StringProperty(text[current_lang].guess_the_number_game.enter_btn)
    empty_textfield_mistake = StringProperty(text[current_lang].guess_the_number_game.empty_textfield_mistake)
    small_number_mistake = StringProperty(text[current_lang].guess_the_number_game.small_number_mistake)
    big_number_mistake = StringProperty(text[current_lang].guess_the_number_game.big_number_mistake)
    greater_number = StringProperty(text[current_lang].guess_the_number_game.greater_number)
    lesser_number = StringProperty(text[current_lang].guess_the_number_game.lesser_number)
    win_label = StringProperty(text[current_lang].guess_the_number_game.win_label)

    # текст диалогового окна перезагрузки мини игры
    dialog_title = StringProperty(text[current_lang].guess_the_number_reset_dialog.dialog_title)
    dialog_text = StringProperty(text[current_lang].guess_the_number_reset_dialog.dialog_text)
    cancel_btn = StringProperty(text[current_lang].guess_the_number_reset_dialog.cancel_btn)
    confirm_btn = StringProperty(text[current_lang].guess_the_number_reset_dialog.confirm_btn)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_random_number()
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.ids.number_input.focus and keycode == 40:  # 40 - Enter key pressed
            self.check_number()
            self.ids.number_input.text = ""

    def create_random_number(self):
        self.random_number = randint(1, 1000)
        print(self.random_number)

    def check_number(self, *args):
        global current_lang
        input_number = self.ids.number_input.text
        if input_number == "":
            self.game_label_text = self.empty_textfield_mistake
            pass
        else:
            input_number = int(input_number)

            if input_number <= 0:
                self.game_label_text = self.small_number_mistake
            elif input_number > 1000:
                self.game_label_text = self.big_number_mistake
            else:
                if input_number < self.random_number:
                    if current_lang == "kaz":
                        self.game_label_text = f"{input_number}, {self.lesser_number}"
                    else:
                        self.game_label_text = f"{self.greater_number} {input_number}"
                elif input_number > self.random_number:
                    if current_lang == "kaz":
                        self.game_label_text = f"{input_number}, {self.greater_number}"
                    else:
                        self.game_label_text = f"{self.lesser_number} {input_number}"
                else:
                    self.game_label_text = self.win_label
                    self.show_restart_dialog()

    def show_restart_dialog(self):  # показывает диалоговое окно закрытия приложения
        if not self.restart_dialog:
            self.restart_dialog = MDDialog(
                title=self.dialog_title,
                text=self.dialog_text,
                buttons=[
                    MDFlatButton(text=self.cancel_btn, font_style="Button", on_release=self.close_restart_dialog),
                    MDFlatButton(text=self.confirm_btn, font_style="Button", on_release=self.restart_game)
                ]
            )

        self.restart_dialog.open()

    def close_restart_dialog(self, obj):
        EmbodyMindApp().play_click_sound()
        self.restart_dialog.dismiss()
        self.manager.current = "GamesMenu"

    def restart_game(self, obj):
        EmbodyMindApp().play_click_sound()
        self.create_random_number()
        self.game_label_text = text[current_lang].guess_the_number_game.game_label_text
        self.ids.number_input.text = ""
        self.restart_dialog.dismiss()

    def exit_restart_game(self):
        self.create_random_number()
        self.game_label_text = text[current_lang].guess_the_number_game.game_label_text
        self.ids.number_input.text = ""

    def on_leave(self, *args):
        self.exit_restart_game()


class MathTrueFalseMenu(Screen):
    global text, current_lang
    top_title = StringProperty(text[current_lang].true_false_math_menu.top_title)
    game_name = StringProperty(text[current_lang].true_false_math_menu.game_name)
    game_description = StringProperty(text[current_lang].true_false_math_menu.game_description)

    def return_to_games_menu(self):
        EmbodyMindApp().play_click_sound()
        self.manager.current = "GamesMenu"


class MathTrueFalseGame(Screen):
    global text, current_lang
    score = StringProperty(text[current_lang].true_false_math_game.score)
    timer_text = StringProperty(text[current_lang].true_false_math_game.timer_text)
    false_btn = StringProperty(text[current_lang].true_false_math_game.false_btn)
    true_btn = StringProperty(text[current_lang].true_false_math_game.true_btn)

    # текст диалогового окна при поражении
    dialog_title = StringProperty(text[current_lang].true_false_math_lose_dialog.dialog_title)
    dialog_text_1 = StringProperty(text[current_lang].true_false_math_lose_dialog.dialog_text_1)
    dialog_text_2 = StringProperty(text[current_lang].true_false_math_lose_dialog.dialog_text_2)
    cancel_btn = StringProperty(text[current_lang].true_false_math_lose_dialog.cancel_btn)
    confirm_btn = StringProperty(text[current_lang].true_false_math_lose_dialog.confirm_btn)

    lose_dialog = None
    timer_value = 5
    timer = NumericProperty(timer_value)
    score_value = NumericProperty(0)
    # current_operator = None
    string_of_operator = None
    solution = None
    false_solution = None
    math_problem = StringProperty("")

    def on_enter(self, *args):
        print("entered screen")
        self.create_random_math_problem()
        self.score_value = 0
        self.clock_active = True
        self.timer_value = 5
        self.timer = 5
        self.ids.timer_bar.value = 5
        self.timer_start()

    def timer_start(self):
        # print("timer is on")
        Clock.schedule_once(self.decrease_timer, 1)

    def decrease_timer(self, dt):
        if self.clock_active:
            if self.timer <= 0:
                print("timer stopped")
                self.show_lose_dialog()
            else:
                self.timer -= 1
                self.ids.timer_bar.value -= 1
                # print(self.ids.timer_bar.value)
                self.timer_start()

    def on_leave(self, *args):
        self.clock_active = False

    def create_random_math_problem(self):
        number1 = randint(1, 20)
        number2 = randint(1, 20)
        # number3 = randint(1, 10)
        print(number1, number2)

        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,  # use operator.div for Python 2
        }

        random_operator = randint(1, 4)
        if random_operator == 1:
            self.string_of_operator = "+"
            print(self.string_of_operator)
        elif random_operator == 2:
            self.string_of_operator = "-"
            print(self.string_of_operator)
        elif random_operator == 3:
            self.string_of_operator = "*"
            print(self.string_of_operator)
        else:
            self.string_of_operator = "/"
            print(self.string_of_operator)

        if self.string_of_operator == "-":
            if number1 < number2:
                number1, number2 = number2, number1
                print(number1, number2)

        if self.string_of_operator == "*":
            number1 = randint(1, 10)
            number2 = randint(1, 10)

        if self.string_of_operator == "/":
            if number1 < number2:
                number1, number2 = number2, number1
                print(number1, number2)
            while number1 / number2 != number1 // number2:
                number1 += 1
                print(f"Incremented: {number1}")

        self.solution = ops[self.string_of_operator](number1, number2)
        true_chance = randint(1, 2)
        if true_chance == 1:
            self.false_solution = self.solution
        else:
            random_false_number_detail = randint(1, 2)  # 1: decrement 2: increment
            if random_false_number_detail == 1:
                self.false_solution = randint(self.solution - 5, self.solution - 1)
            else:
                self.false_solution = randint(self.solution + 1, self.solution + 5)

        self.math_problem = f"{number1} {self.string_of_operator} {number2} = {int(self.false_solution)}"

    def check_if_true(self):
        if self.solution == self.false_solution:
            self.correct()
        else:
            self.incorrect()

    def check_if_false(self):
        if self.solution != self.false_solution:
            self.correct()
        else:
            self.incorrect()

    def correct(self):
        self.score_value += 1
        self.create_random_math_problem()
        self.timer = self.timer_value
        self.ids.timer_bar.value = self.timer_value

    def incorrect(self):
        self.show_lose_dialog()
        self.clock_active = False

    def show_lose_dialog(self):
        if not self.lose_dialog:
            self.lose_dialog = MDDialog(
                title=self.dialog_title,
                text=f"{self.dialog_text_1} {self.score_value} \n{self.dialog_text_2}",
                buttons=[
                    MDFlatButton(text=self.cancel_btn, font_style="Button", on_release=self.close_lose_dialog),
                    MDFlatButton(text=self.confirm_btn, font_style="Button", on_release=self.restart_game)
                ]
            )

        self.lose_dialog.open()

    def close_lose_dialog(self, obj):
        EmbodyMindApp().play_click_sound()
        self.lose_dialog.dismiss()
        self.manager.current = "GamesMenu"

    def restart_game(self, obj):
        EmbodyMindApp().play_click_sound()
        self.lose_dialog.dismiss()
        self.score_value = 0
        self.create_random_math_problem()
        self.clock_active = True
        self.timer_value = 5
        self.timer = 5
        self.ids.timer_bar.value = 5
        self.timer_start()



class WindowManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.key_input)

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            if self.current != "MainMenu":
                if self.current == "GamesMenu":
                    self.current = "MainMenu"
                else:
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
