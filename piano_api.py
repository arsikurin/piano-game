import logging as log
import sqlite3

import pygame
import threading
import sys
import numpy as np
import random
import time


def main() -> None:
    class Piano:
        pygame.font.init()
        clock = pygame.time.Clock()
        key_height = 120
        size = width, height = 600, 1000
        pygame.display.set_caption("Piano - game")
        surface = pygame.display.set_mode(size)
        amount = 0
        score = 0
        rects = []
        surface.fill((255, 255, 255))
        pygame.draw.line(surface, (128, 128, 128), [200, 0], [200, 1000], 5)
        pygame.draw.line(surface, (128, 128, 128), [400, 0], [400, 1000], 5)
        pygame.draw.line(surface, (128, 128, 128), [0, 52], [600, 52], 5)
        pygame.draw.line(surface, (255, 0, 0), [0, 800], [600, 800], 5)
        pygame.display.update()
        jump = 1
        log.debug("game set")

        @classmethod
        def handle_events(cls) -> None:
            """
            handles events
            """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and event.key == 49:
                    for rect in cls.rects:
                        mid, bottom = rect.midbottom
                        if mid < 100 and bottom >= 800 >= bottom - cls.key_height:
                            pygame.draw.rect(cls.surface, (255, 255, 255), rect)
                            cls.rects.remove(rect)
                            cls.amount -= 1
                            cls.score += 1
                            log.debug("LEFT")
                        # else:
                        #     log.debug("MISS")

                elif event.type == pygame.KEYDOWN and event.key == 50:
                    for rect in cls.rects:
                        mid, bottom = rect.midbottom
                        if 400 > mid > 100 and bottom >= 800 >= bottom - cls.key_height:
                            pygame.draw.rect(cls.surface, (255, 255, 255), rect)
                            cls.rects.remove(rect)
                            cls.amount -= 1
                            cls.score += 1
                            log.debug("MID")
                        # else:
                        #     log.debug("MISS")

                elif event.type == pygame.KEYDOWN and event.key == 51:
                    for rect in cls.rects:
                        mid, bottom = rect.midbottom
                        if mid > 500 and bottom >= 800 >= bottom - cls.key_height:
                            pygame.draw.rect(cls.surface, (255, 255, 255), rect)
                            cls.rects.remove(rect)
                            cls.amount -= 1
                            cls.score += 1
                            log.debug("RIGHT")
                        # else:
                        #     log.debug("MISS")

        @classmethod
        def left_create(cls) -> None:
            """
            creates left key
            """
            rect = pygame.rect.Rect((0, 50, 198, cls.key_height))
            pygame.draw.rect(cls.surface, (0, 0, 0), rect)
            cls.rects.append(rect)
            cls.amount += 1

        @classmethod
        def middle_create(cls) -> None:
            """
            creates middle key
            """
            rect = pygame.rect.Rect((203, 50, 195, cls.key_height))
            pygame.draw.rect(cls.surface, (0, 0, 0), rect)
            cls.rects.append(rect)
            cls.amount += 1

        @classmethod
        def right_create(cls) -> None:
            """
            creates right key
            """
            rect = pygame.rect.Rect((403, 50, 200, cls.key_height))
            pygame.draw.rect(cls.surface, (0, 0, 0), rect)
            cls.rects.append(rect)
            cls.amount += 1

        @classmethod
        def mover(cls) -> None:
            """
            moves keys
            """
            for rect in cls.rects:
                pygame.draw.rect(cls.surface, (255, 255, 255), rect)
                rect.move_ip(0, cls.jump)
                pygame.draw.rect(cls.surface, (0, 0, 0), rect)
                pygame.draw.line(cls.surface, (255, 0, 0), [0, 800], [600, 800], 5)
                pygame.draw.line(cls.surface, (128, 128, 128), [0, 52], [600, 52], 5)
                if rect.midbottom[1] > 1150:
                    pygame.draw.rect(cls.surface, (255, 255, 255), rect)
                    cls.amount -= 1
                    log.debug("missed a key")
                    cls.rects.remove(rect)
                    if cls.score:
                        cls.score -= 1

        @classmethod
        def clear_rects(cls) -> None:
            """
            clears excess keys
            """
            if cls.amount > 20:
                pygame.draw.rect(cls.surface, (255, 255, 255), cls.rects[0])
                del cls.rects[0]
                cls.amount -= 1

    def keys_generator() -> None:
        """
        generates keys
        """
        log.debug("keys generator thread started")
        while True:
            a = float(random.choice(times))
            time.sleep(a)
            choose = random.randint(0, 2)
            if choose == 0:
                Piano.left_create()
            elif choose == 1:
                Piano.middle_create()
            else:
                Piano.right_create()

    def speed_setter() -> None:
        """
        sets keys speed
        """
        global times
        # if Piano.score < 10:
        #     clock.tick(240)
        # times = np.linspace(0.6, 0.9)
        # elif Piano.score < 30:
        Piano.clock.tick(360)
        times = np.linspace(0.4, 0.6)
        # elif Piano.score < 80:
        #     Piano.jump = 2
        #     clock.tick(260)
        #     times = np.linspace(0.25, 0.3)
        # elif Piano.score < 120:
        #     Piano.jump = 4
        #     clock.tick(240)
        # elif Piano.score < 300:
        #     Piano.jump = 4
        #     clock.tick(360)

    times = np.linspace(0.4, 0.6)
    thread1 = threading.Thread(target=keys_generator, daemon=True)
    thread1.start()

    log.debug("game thread started")
    while True:
        font1 = pygame.font.Font("/usr/share/fonts/WindowsFonts/segoeui.ttf", 36)
        pygame.draw.rect(Piano.surface, (255, 255, 255), (0, 0, 600, 50))
        text1 = font1.render(f"Score: {Piano.score}", True, (255, 0, 0))
        Piano.surface.blit(text1, (2, 0))
        pygame.display.update()

        speed_setter()
        Piano.mover()
        Piano.handle_events()
        pygame.display.update()
        Piano.clear_rects()


def init_user(
        nickname: str,
        conn: sqlite3.Connection,
        c: sqlite3.Cursor
) -> None:
    """
    initialize new user

    :param c: cursor
    :param conn: connection to db
    :param nickname: user's nickname
    """
    with conn:
        c.execute(
            "INSERT INTO users VALUES (:nickname, :password, :points, :lvl)",
            {"nickname": nickname, "password": None, "points": None, "lvl": 1})


def update_password(
        password: str,
        nickname: str,
        conn: sqlite3.Connection,
        c: sqlite3.Cursor
) -> None:
    """
    update user's password

    :param c: cursor
    :param conn: connection to db
    :param password: user's password
    :param nickname: user's nickname
    """
    with conn:
        c.execute("UPDATE users SET password = :password WHERE nickname = :nickname",
                  {"password": password, "nickname": nickname})


def update_lvl(
        lvl: int,
        nickname: str,
        conn: sqlite3.Connection,
        c: sqlite3.Cursor
) -> None:
    """
    update user's level

    :param c: cursor
    :param conn: connection to db
    :param lvl: user's level
    :param nickname: user's nickname
    """
    with conn:
        c.execute("UPDATE users SET lvl = :lvl WHERE nickname = :nickname",
                  {"lvl": lvl, "nickname": nickname})


def update_points(
        points: int,
        nickname: str,
        conn: sqlite3.Connection,
        c: sqlite3.Cursor
) -> None:
    """
    update user's points

    :param c: cursor
    :param conn: connection to db
    :param points: user's points
    :param nickname: user's nickname
    """
    with conn:
        c.execute("UPDATE users SET points = :points WHERE nickname = :nickname",
                  {"points": points, "nickname": nickname})


def delete_user(
        nickname: str,
        conn: sqlite3.Connection,
        c: sqlite3.Cursor
) -> None:
    """
    delete user from db

    :param nickname: user's nickname
    :param conn: connection to db
    :param c: cursor
    """
    with conn:
        c.execute("delete from users where nickname=:nickname", {"nickname": nickname})


def get_user(
        nickname: str,
        conn: sqlite3.Connection,
        c: sqlite3.Cursor
) -> tuple:
    """
    get user data

    :param c: cursor
    :param conn: connection to db
    :param nickname: user's nickname
    :return: user data
    """
    with conn:
        c.execute("SELECT * FROM users WHERE nickname=:nickname", {"nickname": nickname})
        return c.fetchone()
