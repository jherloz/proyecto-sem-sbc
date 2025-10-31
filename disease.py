from typing import Any


from database import Database


class Disease:
	def __init__(
		self,
		aidi: int = 0,
		name: str = "",
		active: int = 1,
	):
		self.m_id: int = aidi
		self.m_name: str = name
		self.m_active: int = active

	def select_by_id(self, aidi: int):
		Database.execute("SELECT * FROM enfermedad WHERE id=%s;", [aidi])

		res = Database.fetchone()

		if res:
			disease = dict_to_disease(res)

			self.m_id = disease.m_id
			self.m_name = disease.m_name
			self.m_active = disease.m_active

	def insert(self):
		Database.execute("INSERT INTO enfermedad(nombre) VALUES(%s);", [self.m_name])

	def to_list(self) -> list[Any]:
		return [str(self.m_id), self.m_name, bool(self.m_active)]

	def update_name(self, name: str):
		Database.execute(
			"UPDATE enfermedad SET nombre=%s WHERE id=%s;", [name, self.m_id]
		)

	def update_active(self, active: int):
		Database.execute(
			"UPDATE enfermedad SET activo=%s WHERE id=%s;", [active, self.m_id]
		)

	def __bool__(self):
		if self.m_name:
			return True

		return False


def dict_to_disease(disease: dict[str, Any]):
	return Disease(disease["id"], disease["nombre"], disease["activo"])


def get_diseases() -> list[Disease]:
	diseases: list[Disease] = []

	Database.execute("SELECT * FROM enfermedad;")

	for i in Database.fetchall():
		diseases.append(dict_to_disease(i))

	return diseases
