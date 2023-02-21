import contextlib
import functools as ft
import logging as log
import random
import sys
import time
from threading import Thread

import numpy as np

with contextlib.redirect_stdout(None):
    import pygame
    import pygame_menu
from colourlib import Fg, Style

DEBUG = True
if DEBUG:
    log.basicConfig(
        format=f"{Fg.Green}{Style.Bold}%(asctime)s{Fg.Reset}{Style.Bold} %(message)s{Style.Reset}\n[%(name)s]\n",
        level=log.DEBUG)
else:
    log.basicConfig(
        format=f"{Fg.Green}{Style.Bold}%(asctime)s{Fg.Reset}{Style.Bold} %(message)s{Style.Reset}\n[%(name)s]\n",
        level=log.INFO)


class Piano:
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    _instance = None

    _gamemode = (("Endless", 1), 0)
    __highest_score = "0"
    font36 = pygame.font.SysFont("", 36)
    font30 = pygame.font.SysFont("", 30)
    _times = np.linspace(0.65, 0.7)
    _key_height = 120
    _score = 0
    _is_missed = False
    _rects = []
    _clock = pygame.time.Clock()
    _window_width, __window_height = 600, 1000

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, nickname):
        self.nickname = nickname
        self._surface = pygame.display.set_mode((self._window_width, self.__window_height))
        self._surface.fill((255, 255, 255))
        pygame.display.set_caption("Piano - game")
        pygame.draw.line(self._surface, (128, 128, 128), [200, 0], [200, 1000], 5)
        pygame.draw.line(self._surface, (128, 128, 128), [400, 0], [400, 1000], 5)
        pygame.draw.line(self._surface, (128, 128, 128), [0, 52], [600, 52], 5)
        pygame.draw.line(self._surface, (255, 0, 0), [0, 800], [600, 800], 5)
        pygame.display.update()

    def __handle_key_events(self, event_key: int):
        if event_key == 49:
            arg1 = 100
            arg2 = 0
        elif event_key == 50:
            arg1 = 400
            arg2 = 100
        elif event_key == 51:
            arg1 = 600
            arg2 = 500
        else:
            return

        for rect in self._rects:
            mid, bottom = rect.midbottom
            if arg1 > mid > arg2 and bottom >= 800 >= bottom - self._key_height:
                pygame.draw.rect(self._surface, (255, 255, 255), rect)
                self._rects.remove(rect)
                self._score += 1
                self._is_missed = False
                break

        if self._is_missed and self._score > 0:
            self._score -= 1
        self._is_missed = True

    def start_events_handler(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                case pygame.KEYDOWN:
                    if event.key == 49:
                        self.__handle_key_events(event_key=49)

                    elif event.key == 50:
                        self.__handle_key_events(event_key=50)

                    elif event.key == 51:
                        self.__handle_key_events(event_key=51)

                case pygame.MOUSEBUTTONDOWN:
                    mouse_y, mouse_x = pygame.mouse.get_pos()
                    if 0 < mouse_y < 200:
                        self.__handle_key_events(event_key=49)

                    elif 201 < mouse_y < 400:
                        self.__handle_key_events(event_key=50)

                    elif 401 < mouse_y < 601:
                        self.__handle_key_events(event_key=51)

    def move_keys(self):
        for rect in self._rects:
            pygame.draw.rect(self._surface, (255, 255, 255), rect)
            rect.move_ip(0, 1)
            pygame.draw.rect(self._surface, (0, 0, 0), rect)
            pygame.draw.line(self._surface, (255, 0, 0), [0, 800], [600, 800], 5)
            pygame.draw.line(self._surface, (128, 128, 128), [0, 52], [600, 52], 5)
            if rect.midbottom[1] > 1150:
                pygame.draw.rect(self._surface, (255, 255, 255), rect)
                log.debug("missed a key")
                self._rects.remove(rect)
                if self._score:
                    self._score -= 1

    def _render_key(self, key_pos_name):
        time.sleep(float(random.choice(self._times)))
        if key_pos_name == "right":
            rect = pygame.rect.Rect((403, 50, 200, self._key_height))
        elif key_pos_name == "middle":
            rect = pygame.rect.Rect((203, 50, 195, self._key_height))
        elif key_pos_name == "left":
            rect = pygame.rect.Rect((0, 50, 198, self._key_height))
        else:
            log.error("unknown key_pos_name")
            return
        pygame.draw.rect(self._surface, (0, 0, 0), rect)
        self._rects.append(rect)

    def clear_rects(self):
        if len(self._rects) > 20:
            pygame.draw.rect(self._surface, (255, 255, 255), self._rects[0])
            del self._rects[0]

    @classmethod
    def set_gamemode(cls, gm: tuple[tuple[str, int], int], _: int):
        cls._gamemode = gm

    @staticmethod
    def set_music(file: str):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)

    def start_keys_renderer(self):
        log.debug("keys renderer thread started")
        while True:
            choose = random.randint(0, 2)
            if choose == 0:
                self._render_key(key_pos_name="left")
            elif choose == 1:
                self._render_key(key_pos_name="middle")
            else:
                self._render_key(key_pos_name="right")

    def render_text(self) -> None:
        # score
        pygame.draw.rect(self._surface, (255, 255, 255), (0, 0, 600, 50))
        self._surface.blit(
            self.font36.render(f"HI {self.__highest_score}   {int(self._score)}", True, (255, 0, 0)),
            (5, 0))

        # nickname
        nickname_text = self.font30.render(f"{self.nickname}", True, (255, 0, 0))
        nickname_text_width = nickname_text.get_rect().width
        self._surface.blit(nickname_text, (self._window_width - nickname_text_width - 5, 7))

    def set_speed(self):
        if self._score < 10:
            self._clock.tick(120)
            self._times = np.linspace(0.65, 0.7)
        elif self._score < 25:
            self._clock.tick(180)
            self._times = np.linspace(2, 2)
        elif self._score < 50:
            self._clock.tick(240)
            self._times = np.linspace(2, 2)
        elif self._score < 75:
            self._clock.tick(300)
            self._times = np.linspace(2, 2)
        else:
            self._clock.tick(360)
            self._times = np.linspace(2, 2)

    @staticmethod
    def show_menu():
        menu_surface = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Piano - menu")
        solarized_dark_theme = pygame_menu.Theme(
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
            theme=solarized_dark_theme,
            title="Piano",
            width=600
        )
        settings_menu = pygame_menu.Menu(
            height=400,
            theme=solarized_dark_theme,
            title="Settings",
            width=600
        )
        user_nickname = landing_menu.add.text_input("Nickname: ", default="3p1c Cl1ck3r", maxchar=24)
        for func, kwargs in [
            (landing_menu.add.selector,
             {"title": "Game mode: ", "items": [("Endless", 1), ("Normal", 2), ("Hardcore", 3)],
              "onchange": Piano.set_gamemode}),
            (landing_menu.add.button,
             {"title": "Play", "action": Piano.run, "nickname": user_nickname, "accept_kwargs": True}),
            (landing_menu.add.button, {"title": "Settings »", "accept_kwargs": True,
                                       "action": ft.partial(settings_menu.mainloop, menu_surface)}),
            (landing_menu.add.label, {"title": "", "font_size": 17}),
            (landing_menu.add.label, {"title": "Made by arsikurin and yabich", "font_size": 17}),
            (settings_menu.add.text_input, {"title": "Left key: ", "default": "1", "maxchar": 1}),
            (settings_menu.add.text_input, {"title": "Middle key: ", "default": "2", "maxchar": 1}),
            (settings_menu.add.text_input, {"title": "Right key: ", "default": "3", "maxchar": 1}),
            (settings_menu.add.button, {"title": "« Back", "action": ft.partial(landing_menu.mainloop, menu_surface)}),
        ]:
            func(**kwargs)

        landing_menu.mainloop(menu_surface)

    @classmethod
    def run(cls, nickname: pygame_menu.widgets.widget.textinput.TextInput):
        self = cls(nickname.get_value())
        keys_renderer_thread = Thread(target=self.start_keys_renderer, daemon=True)
        keys_renderer_thread.start()
        cls.set_music("stal-c418.wav")

        try:
            while True:
                self.render_text()
                self.set_speed()
                self.move_keys()
                self.start_events_handler()
                self.clear_rects()
                pygame.display.flip()
        except KeyboardInterrupt:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    Piano.show_menu()
