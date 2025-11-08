from typing import Any


from database import Database


class Patient:
	def __init__(
		self,
		aidi: int = 0,
		medic: int = 0,
		name: str = "",
		lastname: str = "",
		curp: str = "",
		active: int = 1,
	):
		self.m_id: int = aidi
		self.m_medic: int = medic
		self.m_name: str = name
		self.m_lastname: str = lastname
		self.m_curp: str = curp
		self.m_active: int = active

	def insert(self):
		Database.execute(
			"INSERT INTO paciente(medico, nombre, apellido, curp) VALUES(%s, %s, %s, %s);",
			[self.m_medic, self.m_name, self.m_lastname, self.m_curp],
		)

	def select_by_id(self, aidi: int):
		Database.execute("SELECT * FROM paciente WHERE id=%s;", [aidi])

		res = Database.fetchone()

		if res:
			patient = dict_to_patient(res)

			self.m_id = patient.m_id
			self.m_medic = patient.m_medic
			self.m_name = patient.m_name
			self.m_lastname = patient.m_lastname
			self.m_curp = patient.m_curp
			self.m_active = patient.m_active

	def to_list(self) -> list[Any]:
		return [
			str(self.m_id),
			str(self.m_medic),
			self.m_name,
			self.m_lastname,
			self.m_curp,
			bool(self.m_active),
		]
	
	def get_full_name(self) -> str:
		return f"{self.m_name} {self.m_lastname}"

	def update_medic(self, medic: int):
		Database.execute(
			"UPDATE paciente SET medico=%s WHERE id=%s;", [medic, self.m_id]
		)

	def update_name(self, name: str):
		Database.execute(
			"UPDATE paciente SET nombre=%s WHERE id=%s;", [name, self.m_id]
		)

	def update_lastname(self, lastname: str):
		Database.execute(
			"UPDATE paciente SET apellido=%s WHERE id=%s;", [lastname, self.m_id]
		)

	def update_curp(self, curp: str):
		Database.execute("UPDATE paciente SET curp=%s WHERE id=%s;", [curp, self.m_id])

	def update_active(self, active: int):
		Database.execute(
			"UPDATE paciente SET activo=%s WHERE id=%s;", [active, self.m_id]
		)

	def __bool__(self):
		if self.m_name and self.m_lastname and self.m_curp:
			return True

		return False


def dict_to_patient(patient: dict[str, Any]):
	return Patient(
		patient["id"],
		patient["medico"],
		patient["nombre"],
		patient["apellido"],
		patient["curp"],
		patient["activo"],
	)


def get_patients() -> list[Patient]:
	patients: list[Patient] = []

	Database.execute("SELECT * FROM paciente;")

	for i in Database.fetchall():
		patients.append(dict_to_patient(i))

	return patients

#Obtener pacientes solo del médico actual
def get_patients_by_medic(medic_id: int) -> list[Patient]:
	patients: list[Patient] = []

	Database.execute("SELECT * FROM paciente WHERE medico=%s;", [medic_id])

	for i in Database.fetchall():
		patients.append(dict_to_patient(i))

	return patients