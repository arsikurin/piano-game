import logging as log
import pygame
import sys
import numpy as np
import random
import time

clock = pygame.time.Clock()
times = np.linspace(0.35, 0.6)


class Piano:
    # pygame.font.init()
    key_height = 120
    size = width, height = 600, 1000
    surface = pygame.display.set_mode(size)
    amount = 0
    points = 0
    rects = []
    surface.fill((255, 255, 255))
    pygame.draw.line(surface, (0, 255, 0), [200, 0], [200, 1000], 5)
    pygame.draw.line(surface, (0, 255, 0), [400, 0], [400, 1000], 5)
    pygame.draw.line(surface, (255, 0, 0), [0, 800], [600, 800], 5)
    pygame.display.update()

    # my_font = pygame.font.Font(None, 24)

    @classmethod
    def handle_events(cls) -> None:
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
                        log.debug("RIGHT")
                    # else:
                    #     log.debug("MISS")

    @classmethod
    def left_create(cls) -> None:
        rect = pygame.rect.Rect((0, 0, 198, cls.key_height))
        pygame.draw.rect(cls.surface, (0, 0, 0), rect)
        cls.rects.append(rect)
        cls.amount += 1

    @classmethod
    def middle_create(cls) -> None:
        rect = pygame.rect.Rect((203, 0, 195, cls.key_height))
        pygame.draw.rect(cls.surface, (0, 0, 0), rect)
        cls.rects.append(rect)
        cls.amount += 1

    @classmethod
    def right_create(cls) -> None:
        rect = pygame.rect.Rect((403, 0, 200, cls.key_height))
        pygame.draw.rect(cls.surface, (0, 0, 0), rect)
        cls.rects.append(rect)
        cls.amount += 1

    @classmethod
    def mover(cls) -> None:
        for rect in cls.rects:
            pygame.draw.rect(cls.surface, (255, 255, 255), rect)
            rect.move_ip(0, 1)
            pygame.draw.rect(cls.surface, (0, 0, 0), rect)
            pygame.draw.line(cls.surface, (255, 0, 0), [0, 800], [600, 800], 5)

    @classmethod
    def clear_rects(cls) -> None:
        if cls.amount > 20:
            pygame.draw.rect(cls.surface, (255, 255, 255), cls.rects[0])
            del cls.rects[0]
            cls.amount -= 1


def keys_generator() -> None:
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


def init_user(nickname: str, conn, c):
    """
    initialize new user

    :param nickname: user's nickname
    """
    with conn:
        c.execute(
            "INSERT INTO users VALUES (:nickname, :password, :points, :lvl)",
            {"nickname": nickname, "password": None, "points": None, "lvl": 1})


# def update_nickname(nickname: str, nickname: int) -> None:
#     """
#     update user's nickname
#
#     :param nickname:
#     :param nickname: id of the user
#     """
#     from main import conn, c
#     with conn:
#         c.execute("UPDATE users SET nickname = :nickname WHERE nickname = :nickname",
#                   {"nickname": nickname, "nickname": nickname})


def update_password(password: str, nickname: str, conn, c) -> None:
    """
    update user's password

    :param password: mail password
    :param nickname: id of the user
    """
    with conn:
        c.execute("UPDATE users SET password = :password WHERE nickname = :nickname",
                  {"password": password, "nickname": nickname})


def update_lvl(lvl: int, nickname: str, conn, c) -> None:
    """
    update user's level

    :param lvl: letovo analytics password
    :param nickname: id of the user
    """
    with conn:
        c.execute("UPDATE users SET lvl = :lvl WHERE nickname = :nickname",
                  {"lvl": lvl, "nickname": nickname})


def update_points(points: int, nickname: str, conn, c) -> None:
    """
    update user's points

    :param points: letovo analytics login
    :param nickname: id of the user
    """
    with conn:
        c.execute("UPDATE users SET points = :points WHERE nickname = :nickname",
                  {"points": points, "nickname": nickname})


def delete_user(nickname: str, conn, c) -> None:
    """
    delete user from DB

    :param nickname:
    :param conn:
    :param c:
    """
    with conn:
        c.execute("delete from users where nickname=:nickname", {"nickname": nickname})


def get_user(nickname: str, conn, c) -> tuple:
    """
    get user data

    :param nickname: user's nickname
    :return: user data
    """
    with conn:
        c.execute("SELECT * FROM users WHERE nickname=:nickname", {"nickname": nickname})
        return c.fetchone()
