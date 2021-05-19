import pygame
import sys


class Piano:
	pygame.font.init()
	size = width, height = 600, 1000
	screen = pygame.display.set_mode(size)
	spx = []
	spy = []
	amount = 0
	combo = 0
	points = 0
	my_font = pygame.font.Font(None, 24)

	def __init__(self):
		self.screen.fill((255, 255, 255))
		pygame.draw.line(self.screen, (0, 255, 0), [200, 0], [200, 1000], 5)
		pygame.draw.line(self.screen, (0, 255, 0), [400, 0], [400, 1000], 5)
		pygame.draw.line(self.screen, (255, 0, 0), [0, 800], [600, 800], 5)
		pygame.display.flip()

	def arseny(self):
		for event in pygame.event.get():
			keys = pygame.key.get_pressed()
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			elif keys[pygame.K_1]:
				for i in range(len(self.spx)):
					if self.spy[i] <= 800 <= self.spy[i] + 100 and self.spx[i] == 0:
						self.combo += 1
						self.points += 100 * (self.combo * 0.1)
						pygame.draw.rect(self.screen, (255, 255, 255), (self.spx[i], self.spy[i], 200, 100))
						pygame.display.flip()
						self.spy[i] = 2001
						self.amount -= 0.3
						print(1)

			elif keys[pygame.K_2]:
				for i in range(len(self.spx)):
					if self.spy[i] <= 800 <= self.spy[i] + 100 and self.spx[i] == 200:
						self.combo += 1
						self.points += 100 * (self.combo * 0.1)
						pygame.draw.rect(self.screen, (255, 255, 255), (self.spx[i], self.spy[i], 200, 100))
						pygame.display.flip()
						self.spy[i] = 2001
						self.amount -= 0.3
						pygame.Rect.move()
						print(2)

			elif keys[pygame.K_3]:
				for i in range(len(self.spx)):
					if self.spy[i] <= 800 <= self.spy[i] + 100 and self.spx[i] == 400:
						self.combo += 1
						self.points += 100 + (self.combo * 0.1)
						pygame.draw.rect(self.screen, (255, 255, 255), (self.spx[i], self.spy[i], 200, 100))
						pygame.display.flip()
						self.spy[i] = 2001
						self.amount -= 0.3
						print(3)

	# elif keys[pygame.K_ESCAPE]:

	def left_create(self, height):
		x, y = 0, 0
		pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 200, height))
		pygame.display.flip()
		self.amount += 0.3
		self.spx.append(x)
		self.spy.append(y)

	def middle_create(self, height):
		x, y = 200, 0
		pygame.draw.rect(self.screen, (0, 0, 0), (200, 0, 200, height))
		pygame.display.flip()
		self.spx.append(x)
		self.spy.append(y)
		self.amount += 0.3

	def right_create(self, height):
		x, y = 400, 0
		pygame.draw.rect(self.screen, (0, 0, 0), (400, 0, 200, height))
		pygame.display.flip()
		self.spx.append(x)
		self.spy.append(y)
		self.amount += 0.3

	def mover(self, speed, height):
		# text = self.my_font.render(str(int(self.points)), False, (0,0,0))
		# self.screen.blit(text,(0,0))
		pygame.display.flip()
		for i in range(len(self.spy)):
			if self.spy[i] <= 1000:
				pygame.draw.rect(self.screen, (255, 255, 255), (self.spx[i], self.spy[i], 200, height))
				pygame.draw.rect(self.screen, (0, 0, 0), (self.spx[i], self.spy[i] + 1 * speed, 200, height))
				self.spy[i] += 1 * speed
				pygame.draw.line(self.screen, (0, 255, 0), [200, 0], [200, 1000], 5)
				pygame.draw.line(self.screen, (0, 255, 0), [400, 0], [400, 1000], 5)
				pygame.draw.line(self.screen, (255, 0, 0), [0, 800], [600, 800], 5)

				pygame.display.flip()
			elif self.spy[i] >= 2000:
				pass
			else:
				self.amount -= 0.3
				self.spy[i] = 2001


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
#     update student's mail address
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
	update student's mail password

	:param password: mail password
	:param nickname: id of the user
	"""
	with conn:
		c.execute("UPDATE users SET password = :password WHERE nickname = :nickname",
		          {"password": password, "nickname": nickname})


def update_lvl(lvl: int, nickname: str, conn, c) -> None:
	"""
	update student.letovo.ru password

	:param lvl: letovo analytics password
	:param nickname: id of the user
	"""
	with conn:
		c.execute("UPDATE users SET lvl = :lvl WHERE nickname = :nickname",
		          {"lvl": lvl, "nickname": nickname})


def update_points(points: int, nickname: str, conn, c) -> None:
	"""
	update student.letovo.ru login

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
