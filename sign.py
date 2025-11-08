from typing import Any


from database import Database


class Sign:
	def __init__(
		self,
		aidi: int = 0,
		name: str = "",
		active: int = 1,
	):
		self.m_id: int = aidi
		self.m_name: str = name
		self.m_active: int = active

	def insert(self):
		Database.execute("INSERT INTO signo(nombre) VALUES(%s);", [self.m_name])

	def select_by_id(self, aidi: int):
		Database.execute("SELECT * FROM signo WHERE id=%s;", [aidi])

		res = Database.fetchone()

		if res:
			sign = dict_to_sign(res)

			self.m_id = sign.m_id
			self.m_name = sign.m_name
			self.m_active = sign.m_active

	def to_list(self) -> list[Any]:
		return [str(self.m_id), self.m_name, bool(self.m_active)]

	def update_name(self, name: str):
		Database.execute("UPDATE signo SET nombre=%s WHERE id=%s;", [name, self.m_id])

	def update_active(self, active: int):
		Database.execute(
			"UPDATE signo SET activo=%s WHERE id=%s;", [active, self.m_id]
		)

	def __bool__(self):
		if self.m_name:
			return True

		return False


def dict_to_sign(sign: dict[str, Any]):
	return Sign(sign["id"], sign["nombre"], sign["activo"])


def get_signs() -> list[Sign]:
	signs: list[Sign] = []

	Database.execute("SELECT * FROM signo WHERE activo = 1;")

	for i in Database.fetchall():
		signs.append(dict_to_sign(i))

	return signs