from typing import Any


from database import Database


class Medic:
	def __init__(
		self,
		aidi: int = 0,
		name: str = "",
		latname: str = "",
		specialty: str = "",
		certificate: str = "",
		active: int = 1,
	):
		self.m_id: int = aidi
		self.m_name: str = name
		self.m_latname: str = latname
		self.m_specialty: str = specialty
		self.m_certificate: str = certificate
		self.m_active: int = active

	def insert(self):
		Database.execute(
			"INSERT INTO medico(nombre, apellido, especialidad, cedula) VALUES(%s, %s, %s, %s);",
			[self.m_name, self.m_latname, self.m_specialty, self.m_certificate],
		)

	def select_by_id(self, aidi: int):
		Database.execute("SELECT * FROM medico WHERE id=%s;", [aidi])

		res = Database.fetchone()

		if res:
			medic = dict_to_medic(res)

			self.m_id = medic.m_id
			self.m_name = medic.m_name
			self.m_latname = medic.m_latname
			self.m_specialty = medic.m_specialty
			self.m_certificate = medic.m_certificate
			self.m_active = medic.m_active

	def to_list(self) -> list[Any]:
		return [
			str(self.m_id),
			self.m_name,
			self.m_latname,
			self.m_specialty,
			self.m_certificate,
			bool(self.m_active),
		]

	def update_name(self, name: str):
		Database.execute("UPDATE medico SET nombre=%s WHERE id=%s;", [name, self.m_id])

	def update_lastname(self, lastname: str):
		Database.execute(
			"UPDATE medico SET apellido=%s WHERE id=%s;", [lastname, self.m_id]
		)

	def update_specialty(self, specialty: str):
		Database.execute(
			"UPDATE medico SET especialidad=%s WHERE id=%s;", [specialty, self.m_id]
		)

	def update_certificate(self, certificate: str):
		Database.execute(
			"UPDATE medico SET cedula=%s WHERE id=%s;", [certificate, self.m_id]
		)

	def update_active(self, active: int):
		Database.execute(
			"UPDATE medico SET activo=%s WHERE id=%s;", [active, self.m_id]
		)

	def __bool__(self):
		if self.m_name and self.m_latname and self.m_specialty and self.m_certificate:
			return True

		return False


def dict_to_medic(medic: dict[str, Any]):
	return Medic(
		medic["id"],
		medic["nombre"],
		medic["apellido"],
		medic["especialidad"],
		medic["cedula"],
		medic["activo"],
	)


def get_medics() -> list[Medic]:
	medics: list[Medic] = []

	Database.execute("SELECT * FROM medico;")

	for i in Database.fetchall():
		medics.append(dict_to_medic(i))

	return medics
