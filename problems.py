# # # TODO Crosses
# # # import pygame
# # # import sys
# # #
# # #
# # # def draw():
# # #     global width, height
# # #     surface.fill((0, 0, 0))
# # #     pygame.draw.line(surface, (255, 255, 255), (0, 0), (width, height), width=10)
# # #     pygame.draw.line(surface, (255, 255, 255), (width, 0), (0, height), width=10)
# # #
# # #
# # # pygame.init()
# # # size = width, height = tuple(map(int, input().split()))
# # # surface = pygame.display.set_mode(size)
# # # pygame.display.set_caption("arsikurin crosses")
# # #
# # # while True:
# # #     for event in pygame.event.get():
# # #         if event.type == pygame.QUIT:
# # #             pygame.quit()
# # #             sys.exit()
# # #
# # #         draw()
# # #         pygame.display.flip()
# # # TODO Rectangle
# # # import pygame
# # # import sys
# # #
# # #
# # # def draw():
# # #     global width, height
# # #     surface.fill((0, 0, 0))
# # #     pygame.draw.rect(surface, (255, 0, 0), (1, 1, width - 2, height - 2), 0)
# # #
# # #
# # # pygame.init()
# # # size = width, height = tuple(map(int, input().split()))
# # # surface = pygame.display.set_mode(size)
# # # pygame.display.set_caption("arsikurin rectangle")
# # #
# # # while True:
# # #     for event in pygame.event.get():
# # #         if event.type == pygame.QUIT:
# # #             pygame.quit()
# # #             sys.exit()
# # #
# # #         draw()
# # #         pygame.display.flip()
# # # TODO Rain screensaver
# # # import pygame
# # # import sys
# # # import random
# # #
# # #
# # # def draw() -> None:
# # #     for i in range(100):
# # #         pygame.draw.circle(surface, color=colors[i], center=locations[i], radius=radius[i], width=0)
# # #         new_y = locations[i][1] + 2
# # #         new_x = locations[i][0] + 2
# # #         if new_x > 1920:
# # #             new_x -= 1920
# # #         if new_y > 1080:
# # #             new_y -= 1080
# # #         locations[i] = (new_x, new_y)
# # #
# # #
# # # pygame.init()
# # # size = width, height = (1920, 1080)
# # # surface = pygame.display.set_mode(size)
# # # pygame.display.set_caption("Screensaver")
# # # clock = pygame.time.Clock()
# # #
# # # locations = [[random.randint(0, width), random.randint(0, height)] for i in range(100)]
# # #
# # # colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for j in range(100)]
# # # radius = [random.randint(10, 15) for n in range(100)]
# # #
# # # while True:
# # #     # surface.fill((0, 0, 0))
# # #     for event in pygame.event.get():
# # #         if event.type == pygame.QUIT:
# # #             pygame.quit()
# # #             sys.exit()
# # #     draw()
# # #     pygame.display.flip()
# # #     clock.tick(60)
# # #
# # # import smtplib
# # # from email.minimumme.text import minimumMEText
# # # from email.minimumme.multipart import minimumMEMultipart
# # #
# # #
# # # class Stack:
# # #     def __init__(self):
# # #         self.items = []
# # #         self.__size = 0
# # #
# # #     def is_empty(self):
# # #         return self.items == []
# # #
# # #     def push(self, item):
# # #         self.items.append(item)
# # #         self.__size += 1
# # #
# # #     def pop(self):
# # #         if not self.is_empty():
# # #             self.__size -= 1
# # #             return self.items.pop()
# # #
# # #     def back(self):
# # #         if not self.is_empty():
# # #             return self.items[-1]
# # #
# # #     def size(self):
# # #         return self.__size
# # #
# # #     def clear(self):
# # #         self.items.clear()
# # #
# # #
# # # class Stack:
# # #     def __init__(self):
# # #         self.items = []
# # #
# # #     def is_empty(self):
# # #         return self.items == []
# # #
# # #     def push(self, item):
# # #         self.items.append(item)
# # #
# # #     def pop(self):
# # #         if not self.is_empty():
# # #             return self.items.pop()
# # #
# # #     def back(self):
# # #         if not self.is_empty():
# # #             return self.items[-1]
# # #
# # #     def size(self):
# # #         return len(self.items)
# # #
# # #     def clear(self):
# # #         self.items.clear()
# #
# # # def send_email(message):
# # #     msg = minimumMEMultipart()
# # #     password = "Qwerty2020"
# # #     msg['From'] = "noreply.arseny@gmail.com"
# # #     msg['To'] = "arseny.kurin@gmail.com"
# # #     msg['Subject'] = "Codes"
# # #     msg.attach(minimumMEText(message, 'plain'))
# # #     server = smtplib.SMTP('smtp.gmail.com: 587')
# # #     server.starttls()
# # #     server.login(msg['From'], password)
# # #     server.sendmail(msg['From'], msg['To'], msg.as_string())
# # #     server.quit()
# # #     print("successfully sent email to %s:" % (msg['To']))
# # #
# # #
# # # myStack = Stack()
# # # log = []
# # # message = []
# # # while True:
# # #     comm = input()
# # #     message.append(comm)
# # #     comm = comm.split()
# # #
# # #     if comm[0] == "push":
# # #         myStack.push(comm[1])
# # #         log.append("ok")
# # #
# # #     if comm[0] == "pop":
# # #         if not myStack.is_empty():
# # #             log.append(myStack.pop())
# # #         else:
# # #             log.append("error")
# # #
# # #     if comm[0] == "back":
# # #         if not myStack.is_empty():
# # #             log.append(myStack.back())
# # #         else:
# # #             log.append("error")
# # #
# # #     if comm[0] == "size":
# # #         log.append(myStack.size())
# # #
# # #     if comm[0] == "clear":
# # #         myStack.clear()
# # #         log.append("ok")
# # #
# # #     if comm[0] == "exit":
# # #         log.append("bye")
# # #         for i in log:
# # #             print(i)
# # #         break
# # # send_email(str(message))
#
# import pygame
# import sys
# import random
#
#
# def draw() -> None:
#     for i in range(1):
#         pygame.draw.circle(surface, color=colors[i], center=locations[i], radius=radius[i], width=0)
#         new_y = locations[i][1] + 2
#         new_x = locations[i][0] + 2
#         if new_x > 1920:
#             new_x -= 1920
#         if new_y > 1080:
#             new_y -= 1080
#         locations[i] = (new_x, new_y)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#
#
# pygame.init()
# size = width, height = (1920, 1080)
# surface = pygame.display.set_mode(size)
# pygame.display.set_caption("Screensaver")
# clock = pygame.time.Clock()
#
# locations = [[random.randint(0, width), random.randint(0, height)] for i in range(1)]
#
# colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for j in range(100)]
# radius = [random.randint(10, 15) for n in range(100)]
#
# while True:
#     # surface.fill((0, 0, 0))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     draw()
#     pygame.display.flip()
#     clock.tick(60)

def init_user(chat_id):
    """
    initialize new user

    :param chat_id: id of the user
    """
    from LetovoAnalyticsBot import conn, c
    with conn:
        c.execute(
            "INSERT INTO users VALUES (:mail_address, :mail_password, :analytics_password, :analytics_login, :chat_id)",
            {"mail_address": None, "mail_password": None, "analytics_password": None, "analytics_login": None,
             "chat_id": chat_id})


def update_mail_address(mail_address, chat_id):
    """
    update student's mail address

    :param mail_address: mail address
    :param chat_id: id of the user
    """
    from LetovoAnalyticsBot import conn, c
    with conn:
        c.execute("UPDATE users SET mail_address = :mail_address WHERE chat_id = :chat_id",
                  {"mail_address": mail_address, "chat_id": chat_id})


def update_mail_password(mail_password, chat_id):
    """
    update student's mail password

    :param mail_password: mail password
    :param chat_id: id of the user
    """
    from LetovoAnalyticsBot import conn, c
    with conn:
        c.execute("UPDATE users SET mail_password = :mail_password WHERE chat_id = :chat_id",
                  {"mail_password": mail_password, "chat_id": chat_id})


def update_analytics_password(analytics_password, chat_id):
    """
    update student.letovo.ru password

    :param analytics_password: letovo analytics password
    :param chat_id: id of the user
    """
    from LetovoAnalyticsBot import conn, c
    with conn:
        c.execute("UPDATE users SET analytics_password = :analytics_password WHERE chat_id = :chat_id",
                  {"analytics_password": analytics_password, "chat_id": chat_id})


def update_analytics_login(analytics_login: str, chat_id: str) -> None:
    """
    update student.letovo.ru login

    :param analytics_login: letovo analytics login
    :param chat_id: id of the user
    """
    from LetovoAnalyticsBot import conn, c
    with conn:
        c.execute("UPDATE users SET analytics_login = :analytics_login WHERE chat_id = :chat_id",
                  {"analytics_login": analytics_login, "chat_id": chat_id})


def get_user(chat_id: int) -> tuple:
    """
    get user data

    :param chat_id: id of the user
    :return: user data
    """
    from LetovoAnalyticsBot import conn, c
    with conn:
        c.execute("SELECT * FROM users WHERE chat_id=:chat_id", {"chat_id": chat_id})
        return c.fetchone()
