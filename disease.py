from typing import Any

from database import Database
from sign import Sign, dict_to_sign
from symptom import Symptom, dict_to_symptom


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

	def insert_with_relations(self, sign_ids: list[int], symptom_ids: list[int]):
		"""Inserta la enfermedad y luego sus relaciones M-M."""
		Database.execute("INSERT INTO enfermedad(nombre) VALUES(%s);", [self.m_name])
		self.m_id = Database.last_insert_id()

		# Insertar relaciones de signos
		for sign_id in sign_ids:
			Database.execute(
				"INSERT INTO enfermedad_signo(enfermedad_id, signo_id) VALUES (%s, %s);",
				[self.m_id, sign_id],
			)
		
		# Insertar relaciones de síntomas
		for symptom_id in symptom_ids:
			Database.execute(
				"INSERT INTO enfermedad_sintoma(enfermedad_id, sintoma_id) VALUES (%s, %s);",
				[self.m_id, symptom_id],
			)

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
	
	# Obtener signos de esta enfermedad
	def get_signs(self) -> list[Sign]:
		signs: list[Sign] = []
		Database.execute(
			"SELECT s.* FROM signo s "
			"JOIN enfermedad_signo es ON s.id = es.signo_id "
			"WHERE es.enfermedad_id = %s;",
			[self.m_id]
		)
		for i in Database.fetchall():
			signs.append(dict_to_sign(i))
		return signs
	
	#Obtener síntomas de esta enfermedad
	def get_symptoms(self) -> list[Symptom]:
		symptoms: list[Symptom] = []
		Database.execute(
			"SELECT s.* FROM sintoma s "
			"JOIN enfermedad_sintoma es ON s.id = es.sintoma_id "
			"WHERE es.enfermedad_id = %s;",
			[self.m_id]
		)
		for i in Database.fetchall():
			symptoms.append(dict_to_symptom(i))
		return symptoms

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