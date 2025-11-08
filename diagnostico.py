from typing import Any
from database import Database
from datetime import datetime


class Diagnostico:
	def __init__(
		self,
		aidi: int = 0,
		paciente_id: int = 0,
		medico_id: int = 0,
		enfermedad_id: int = 0,
		tratamiento: str = "",
		fecha: datetime | None = None,
	):
		self.m_id: int = aidi
		self.m_paciente_id: int = paciente_id
		self.m_medico_id: int = medico_id
		self.m_enfermedad_id: int = enfermedad_id
		self.m_tratamiento: str = tratamiento
		self.m_fecha: datetime | None = fecha

	def insert(self):
		Database.execute(
			"INSERT INTO diagnostico(paciente_id, medico_id, enfermedad_id, tratamiento, fecha) "
			"VALUES(%s, %s, %s, %s, NOW());",
			[
				self.m_paciente_id,
				self.m_medico_id,
				self.m_enfermedad_id,
				self.m_tratamiento,
			],
		)
	
	def to_list_history(self) -> list[Any]:
		"""Formato para la tabla de historial (se usa en get_for_patient)."""
		return [
			self.m_fecha.strftime("%Y-%m-%d %H:%M"),
			self.m_medico_id,
			self.m_enfermedad_id, 
			self.m_tratamiento,
		]


def dict_to_diagnostico(diag: dict[str, Any]) -> Diagnostico:
	"""Convierte un dict simple de la BD a un objeto Diagnostico."""
	return Diagnostico(
		diag.get("id", 0),
		diag.get("paciente_id", 0),
		diag.get("medico_id", 0),
		diag.get("enfermedad_id", 0),
		diag.get("tratamiento", ""),
		diag.get("fecha", None),
	)

def dict_to_diagnostico_history(diag: dict[str, Any]) -> Diagnostico:
	"""Convierte un dict de la consulta JOIN del historial."""

	return Diagnostico(
		fecha=diag.get("fecha", None),
		medico_id=diag.get("medico_nombre", "N/A"),
		enfermedad_id=diag.get("enfermedad_nombre", "N/A"),
		tratamiento=diag.get("tratamiento", ""),
	)


def get_for_patient(patient_id: int) -> list[Diagnostico]:
	"""Obtiene el historial de diagnósticos para un paciente con nombres."""
	history: list[Diagnostico] = []
	
	query = (
		"SELECT d.fecha, d.tratamiento, "
		"CONCAT(m.nombre, ' ', m.apellido) AS medico_nombre, "
		"e.nombre AS enfermedad_nombre "
		"FROM diagnostico d "
		"JOIN medico m ON d.medico_id = m.id "
		"JOIN enfermedad e ON d.enfermedad_id = e.id "
		"WHERE d.paciente_id = %s "
		"ORDER BY d.fecha DESC;"
	)
	
	Database.execute(query, [patient_id])

	for i in Database.fetchall():
		history.append(dict_to_diagnostico_history(i))

	return history


def get_graph_data() -> dict[str, int]:
	"""Obtiene el conteo de cada enfermedad diagnosticada."""
	Database.execute(
		"SELECT e.nombre, COUNT(d.id) AS count "
		"FROM diagnostico d "
		"JOIN enfermedad e ON d.enfermedad_id = e.id "
		"GROUP BY e.nombre "
		"ORDER BY count DESC;"
	)
	
	return {row['nombre']: int(row['count']) for row in Database.fetchall()}