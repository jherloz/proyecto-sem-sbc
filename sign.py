from typing import Any
from database import Database

class Sign:
	def __init__(self, aidi: int = 0, name: str = "", active: int = 1):
		self.m_id = aidi
		self.m_name = name
		self.m_active = active

	def insert(self):
		Database.execute("INSERT INTO signo(nombre) VALUES(%s);", [self.m_name])

	def select_by_id(self, aidi: int):
		Database.execute("SELECT * FROM signo WHERE id=%s;", [aidi])
		res = Database.fetchone()
		if res:
			s = dict_to_sign(res)
			self.__dict__.update(s.__dict__)

	def to_list(self) -> list[Any]:
		return [str(self.m_id), self.m_name, bool(self.m_active)]

	def update_name(self, name: str):
		Database.execute("UPDATE signo SET nombre=%s WHERE id=%s;", [name, self.m_id])
		self.m_name = name

	def update_active(self, active: int):
		Database.execute("UPDATE signo SET activo=%s WHERE id=%s;", [active, self.m_id])
		self.m_active = active

def dict_to_sign(s: dict[str, Any]) -> Sign:
	return Sign(s["id"], s["nombre"], s["activo"])

def get_signs() -> list[Sign]:
	signs = []
	Database.execute("SELECT * FROM signo;")
	for i in Database.fetchall():
		signs.append(dict_to_sign(i))
	return signs
