from typing import Any


from database import Database


class Symptom:
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
		Database.execute("INSERT INTO sintoma(nombre) VALUES(%s);", [self.m_name])

	def select_by_id(self, aidi: int):
		Database.execute("SELECT * FROM sintoma WHERE id=%s;", [aidi])

		res = Database.fetchone()

		if res:
			symptom = dict_to_symptom(res)

			self.m_id = symptom.m_id
			self.m_name = symptom.m_name
			self.m_active = symptom.m_active

	def to_list(self) -> list[Any]:
		return [str(self.m_id), self.m_name, bool(self.m_active)]

	def update_name(self, name: str):
		Database.execute("UPDATE sintoma SET nombre=%s WHERE id=%s;", [name, self.m_id])

	def update_active(self, active: int):
		Database.execute(
			"UPDATE sintoma SET activo=%s WHERE id=%s;", [active, self.m_id]
		)

	def __bool__(self):
		if self.m_name:
			return True

		return False


def dict_to_symptom(symptom: dict[str, Any]):
	return Symptom(symptom["id"], symptom["nombre"], symptom["activo"])


def get_symptoms() -> list[Symptom]:
	symptoms: list[Symptom] = []

	Database.execute("SELECT * FROM sintoma;")

	for i in Database.fetchall():
		symptoms.append(dict_to_symptom(i))

	return symptoms
