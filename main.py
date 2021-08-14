import pygame
import pygame_menu
import sys
import random
import numpy as np
import firebase_admin
import logging as log
import time
import datetime

from pprint import pprint
from pygame_menu.examples import create_example_window
from typing import Optional
from firebase_admin import credentials, firestore
from colourlib import Fg, Style
from threading import Thread

firebase_admin.initialize_app(
    credentials.Certificate("fbAdminConfig.json"))
db = firestore.client()

DEBUG = False
if DEBUG:
    log.basicConfig(
        format=f"{Fg.Green}{Style.Bold}%(asctime)s{Fg.Reset}{Style.Bold} %(message)s{Style.Reset}\n[%(name)s]\n",
        level=log.DEBUG)
else:
    log.basicConfig(
        format=f"{Fg.Green}{Style.Bold}%(asctime)s{Fg.Reset}{Style.Bold} %(message)s{Style.Reset}\n[%(name)s]\n",
        level=log.DEBUG)
    log.getLogger("urllib3.connectionpool").disabled = True
    log.getLogger("asyncio").disabled = True
    log.getLogger("root").disabled = True


class Piano:
    __gamemode = (("Endless", 1), 0)
    __is_offline = True  # Change if there is no internet
    __highest_score = "Offline"

    def __init__(self, nickname):
        self.__nickname = nickname
        if sys.platform == "linux":
            log.debug("linux detected")
            self.__segoeui_font_36 = pygame.font.Font("/usr/share/fonts/WindowsFonts/segoeui.ttf", 36)
            self.__segoeui_font_30 = pygame.font.Font("/usr/share/fonts/WindowsFonts/segoeui.ttf", 30)
        elif sys.platform == "win32":
            log.debug("windows detected")
            self.__segoeui_font_36 = pygame.font.Font("/Windows/Fonts/segoeui.ttf", 36)
            self.__segoeui_font_30 = pygame.font.Font("/Windows/Fonts/segoeui.ttf", 30)
        if not self.__is_offline:
            self.__highest_score = get_points(self.__nickname)
        self.__times = np.linspace(0.65, 0.7)
        self.__key_height = 120
        self.__keys_amount = 0
        self.__score = 0
        self.__is_missed = False
        self.__rects = []
        self.__jump = 1
        self.__clock = pygame.time.Clock()
        self.__window_width, self.__window_height = 600, 1000
        self.__surface = pygame.display.set_mode((self.__window_width, self.__window_height))
        self.__surface.fill((255, 255, 255))
        pygame.display.set_caption("Piano - game")
        pygame.draw.line(self.__surface, (128, 128, 128), [200, 0], [200, 1000], 5)
        pygame.draw.line(self.__surface, (128, 128, 128), [400, 0], [400, 1000], 5)
        pygame.draw.line(self.__surface, (128, 128, 128), [0, 52], [600, 52], 5)
        pygame.draw.line(self.__surface, (255, 0, 0), [0, 800], [600, 800], 5)
        pygame.display.update()

    def __handle_key_events(self, event_key: int, is_mouse: bool = False):
        arg3 = 1
        if event_key == 49:
            arg1 = 100
            arg2 = 0
            if is_mouse:
                arg3 = 0.5
            key_pos_name = "Left"
        elif event_key == 50:
            arg1 = 400
            arg2 = 100
            if is_mouse:
                arg3 = 0.5
            key_pos_name = "Middle"
        elif event_key == 51:
            arg1 = 600
            arg2 = 500
            if is_mouse:
                arg3 = 0.5
            key_pos_name = "Right"
        else:
            return

        for rect in self.__rects:
            mid, bottom = rect.midbottom
            if arg1 > mid > arg2 and bottom >= 800 >= bottom - self.__key_height:
                pygame.draw.rect(self.__surface, (255, 255, 255), rect)
                self.__rects.remove(rect)
                self.__keys_amount -= 1
                self.__score += 1
                log.debug(key_pos_name)
                self.__is_missed = False
                break
        if self.__is_missed:
            if self.__score:
                self.__score -= 1
            log.debug("Miss")
        else:
            self.__is_missed = True

    def start_events_handler(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not self.__is_offline and self.__highest_score < self.__score:
                    update_points(points=self.__score, nickname=self.__nickname)
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == 49:
                    self.__handle_key_events(event_key=49)

                elif event.key == 50:
                    self.__handle_key_events(event_key=50)

                elif event.key == 51:
                    self.__handle_key_events(event_key=51)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_y, mouse_x = pygame.mouse.get_pos()
                if 0 < mouse_y < 200:
                    self.__handle_key_events(event_key=49, is_mouse=True)

                elif 201 < mouse_y < 400:
                    self.__handle_key_events(event_key=50, is_mouse=True)

                elif 401 < mouse_y < 601:
                    self.__handle_key_events(event_key=51, is_mouse=True)

    def move_keys(self) -> None:
        for rect in self.__rects:
            pygame.draw.rect(self.__surface, (255, 255, 255), rect)
            rect.move_ip(0, self.__jump)
            pygame.draw.rect(self.__surface, (0, 0, 0), rect)
            pygame.draw.line(self.__surface, (255, 0, 0), [0, 800], [600, 800], 5)
            pygame.draw.line(self.__surface, (128, 128, 128), [0, 52], [600, 52], 5)
            if rect.midbottom[1] > 1150:
                pygame.draw.rect(self.__surface, (255, 255, 255), rect)
                self.__keys_amount -= 1
                log.debug("missed a key")
                self.__rects.remove(rect)
                if self.__score:
                    self.__score -= 1

    def __render_key(self, key_pos_name) -> None:
        time.sleep(float(random.choice(self.__times)))
        if key_pos_name == "right":
            rect = pygame.rect.Rect((403, 50, 200, self.__key_height))
        elif key_pos_name == "middle":
            rect = pygame.rect.Rect((203, 50, 195, self.__key_height))
        elif key_pos_name == "left":
            rect = pygame.rect.Rect((0, 50, 198, self.__key_height))
        else:
            return
        pygame.draw.rect(self.__surface, (0, 0, 0), rect)
        self.__rects.append(rect)
        self.__keys_amount += 1

    def clear_rects(self) -> None:
        if self.__keys_amount > 20:
            pygame.draw.rect(self.__surface, (255, 255, 255), self.__rects[0])
            del self.__rects[0]
            self.__keys_amount -= 1

    def get_nickname(self):
        return self.__nickname

    def get_highest_score(self):
        return self.__highest_score

    def get_score(self):
        return self.__score

    @classmethod
    def get_gamemode(cls):
        return cls.__gamemode

    @classmethod
    def set_gamemode(cls, gm: tuple[tuple[str, int], int], _: int):
        """
        :param gm: a tuple consisting of callback data and a tuple with name and position
        :param _: callback data
        """
        cls.__gamemode = gm

    @classmethod
    def get_offline_status(cls):
        return cls.__is_offline

    @classmethod
    def set_offline_status(cls, _: tuple[tuple[str, int], int], io: bool):
        """
        :param _: a tuple consisting of callback data and a tuple with name and position
        :param io: callback data
        """
        print(io)
        cls.__is_offline = io

    @classmethod
    def set_music(cls, file: str) -> None:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)

    def start_keys_renderer(self) -> None:
        log.debug("keys renderer thread started")
        while True:
            time.sleep(0.1)
            choose = random.randint(0, 2)
            if choose == 0:
                self.__render_key(key_pos_name="left")
            elif choose == 1:
                self.__render_key(key_pos_name="middle")
            else:
                self.__render_key(key_pos_name="right")

    def render_text(self) -> None:
        # score
        pygame.draw.rect(self.__surface, (255, 255, 255), (0, 0, 600, 50))
        self.__surface.blit(
            self.__segoeui_font_36.render(f"HI {self.__highest_score}   {int(self.__score)}", True, (255, 0, 0)),
            (5, 0))

        # nickname
        nickname_text = self.__segoeui_font_30.render(f"{self.__nickname}", True, (255, 0, 0))
        nickname_text_width = nickname_text.get_rect().width
        self.__surface.blit(nickname_text, (self.__window_width - nickname_text_width - 5, 7))

    def set_speed(self) -> None:
        """
        sets keys speed
        """
        self.__score = 250
        if self.__score < 10:
            self.__clock.tick(120)
            self.__times = np.linspace(0.65, 0.7)
            self.__jump = 1
        elif self.__score < 25:
            self.__clock.tick(180)
            self.__times = np.linspace(2, 2)
            self.__jump = 1
        elif self.__score < 50:
            self.__clock.tick(240)
            self.__times = np.linspace(2, 2)
            self.__jump = 1
        elif self.__score < 75:
            self.__clock.tick(300)
            self.__times = np.linspace(2, 2)
            self.__jump = 1
        elif self.__score < 100:
            self.__clock.tick(360)
            self.__times = np.linspace(2, 2)
            self.__jump = 1


def main(nickname: pygame_menu.widgets.widget.textinput.TextInput):
    piano = Piano(nickname.get_value())

    if not Piano.get_offline_status() and not get_points(nickname=piano.get_nickname()):
        update_points(nickname=piano.get_nickname(), points=0)

    log.debug(f"game is in {piano.get_gamemode()} mode\n{Fg.Red}Game modes are under development{Fg.Reset}")

    keys_renderer_thread = Thread(target=piano.start_keys_renderer, daemon=True)
    keys_renderer_thread.start()

    Piano.set_music("stal-c418.wav")

    log.debug("main thread started")
    try:
        while True:
            piano.render_text()
            piano.set_speed()
            piano.move_keys()
            piano.start_events_handler()
            piano.clear_rects()
            pygame.display.update()
    except KeyboardInterrupt:
        if not Piano.get_offline_status() and piano.get_highest_score() < piano.get_score():
            update_points(points=piano.get_score(), nickname=piano.get_nickname())
        pygame.quit()
        sys.exit()


def fibonacci(n):
    f = [0, 1]

    for i in range(2, n + 1):
        f.append(f[i - 1] + f[i - 2])
    return f[n]


def update_points(nickname: str, points: int) -> None:
    request_payload = {
        "points": points,
        "nickname": nickname
    }
    doc_ref = db.collection(u"users").document(nickname)
    doc_ref.set(request_payload, merge=True)


def get_points(nickname: str) -> Optional[int]:
    doc = db.collection(u"users").document(nickname).get()
    try:
        if doc.exists:
            return doc.to_dict()["points"]
    except KeyError:
        pass
    return None


def display_leaderboards():
    leaderboards_menu.mainloop(menu_surface)


def display_settings():
    settings_menu.mainloop(menu_surface)


def display_landing():
    landing_menu.mainloop(menu_surface)


def passs(*args, **kwargs):
    pass


pygame.init()
pygame.font.init()
pygame.mixer.init()
menu_surface = create_example_window("Piano - menu", (600, 400))

THEME_SOLARIZED_DARK = pygame_menu.Theme(
    background_color=(47, 48, 51),
    cursor_color=(123, 51, 86),
    cursor_selection_color=(146, 160, 160, 120),
    selection_color=(207, 62, 132),
    title_background_color=(4, 47, 58),
    title_font_color=(38, 158, 151),
    widget_font_color=(152, 172, 180)
)

landing_menu = pygame_menu.Menu(
    height=400,
    theme=THEME_SOLARIZED_DARK,
    title="Piano",
    width=600
)
user_nickname = landing_menu.add.text_input("Nickname: ", default="3p1c Cl1ck3r", maxchar=24)
landing_menu.add.selector("Game mode: ", [("Endless", 1), ("Normal", 2), ("Hardcore", 3)],
                          onchange=Piano.set_gamemode)
landing_menu.add.button("Play", main, user_nickname)
landing_menu.add.button("Leaderboards »", action=display_leaderboards)
landing_menu.add.button("Settings »", action=display_settings)
landing_menu.add.label("", font_size=17)
landing_menu.add.label("Made by arsikurin and yabich", font_size=17)

leaderboards_menu = pygame_menu.Menu(
    height=400,
    theme=THEME_SOLARIZED_DARK,
    title="Leaderboards",
    width=600
)
if not Piano.get_offline_status():
    leaderboards = [(doc.to_dict()["points"], doc.to_dict()["nickname"]) for doc in db.collection(u"users").get()]
    for pos, user in enumerate(sorted(leaderboards, key=lambda x: -x[0])):
        leaderboards_menu.add.label(f'{pos + 1}. {user[1]}: {user[0]}')
    leaderboards_menu.add.button("« Back", action=display_landing)
else:
    leaderboards_menu.add.label("You are Offline", font_size=30)
    leaderboards_menu.add.button("« Back", action=display_landing)

settings_menu = pygame_menu.Menu(
    height=400,
    theme=THEME_SOLARIZED_DARK,
    title="Settings",
    width=600
)
key1 = settings_menu.add.text_input("Left key: ", default="1", maxchar=1)
key2 = settings_menu.add.text_input("Middle key: ", default="2", maxchar=1)
key3 = settings_menu.add.text_input("Right key: ", default="3", maxchar=1)
settings_menu.add.selector("Offline mode: ", [("Off", False), ("On", True)], onchange=Piano.set_offline_status)
settings_menu.add.button("« Back", action=display_landing)

if __name__ == "__main__":
    display_landing()
