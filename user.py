from typing import Any
from database import Database


class User:
	def __init__(
		self,
		aidi: int = 0,
		user: str = "",
		password: str = "",
		role: int = 0,
		active: int = 1,
	):
		self.m_id: int = aidi
		self.m_user: str = user
		self.m_password: str = password
		self.m_role: int = role
		self.m_active: int = active

	def insert(self):
		Database.execute(
			"INSERT INTO usuario(usuario, contrasena) VALUES(%s, %s);",
			[self.m_user, self.m_password],
		)

	def select_by_id(self, aidi: int):
		Database.execute("SELECT * FROM usuario WHERE id=%s;", [aidi])

		res = Database.fetchone()

		if res:
			user = dict_to_user(res)

			self.m_id = user.m_id
			self.m_user = user.m_user
			self.m_password = user.m_password
			self.m_role = user.m_role
			self.m_active = user.m_active

	def to_list(self) -> list[Any]:
		return [
			str(self.m_id),
			self.m_user,
			self.m_password,
			str(self.m_role),
			bool(self.m_active),
		]

	def update_user(self, user: str):
		Database.execute(
			"UPDATE usuario SET usuario=%s WHERE id=%s;", [user, self.m_id]
		)

	def update_password(self, password: str):
		Database.execute(
			"UPDATE usuario SET contrasena=%s WHERE id=%s;", [password, self.m_id]
		)

	def update_role(self, role: int | None):
		if role == 0:
			role = None

		Database.execute("UPDATE usuario SET rol=%s WHERE id=%s;", [role, self.m_id])

	def update_active(self, active: int):
		Database.execute(
			"UPDATE usuario SET activo=%s WHERE id=%s;", [active, self.m_id]
		)

	def __bool__(self):
		if self.m_user and self.m_password:
			return True

		return False


def count_users() -> int:
	Database.execute("SELECT COUNT(*) AS n FROM usuario;")
	res = Database.fetchone()

	if res:
		return int(res["n"])

	return 0


def dict_to_user(user: dict[str, Any]):
	return User(
		user["id"], user["usuario"], user["contrasena"], user["rol"], user["activo"]
	)


def get_users() -> list[User]:
	users: list[User] = []

	Database.execute("SELECT * FROM usuario;")

	for i in Database.fetchall():
		users.append(dict_to_user(i))

	return users


def log_in(user: str, password: str):
	Database.execute(
		"SELECT * FROM usuario WHERE usuario=%s AND contrasena=%s;", [user, password]
	)

	res = Database.fetchone()

	if res:
		return dict_to_user(res)

	return None
