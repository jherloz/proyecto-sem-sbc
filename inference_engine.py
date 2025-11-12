from typing import Any 
from disease import Disease, get_diseases


class InferenceEngine:
	def __init__(self):
		self.m_diseases: list[Disease] = []
		self.refresh_knowledge_base()

	def refresh_knowledge_base(self):
		"""Carga todas las enfermedades y sus signos/síntomas."""
		self.m_diseases = get_diseases()

	def diagnose(
		self, patient_sign_ids: set[int], patient_symptom_ids: set[int]
	) -> list[dict[str, Any]]:
		"""
		Compara los signos/síntomas del paciente con la base de conocimientos.
		Usa un coeficiente de superposición: (Coincidencias) / (Total en Enfermedad)
		"""
		results: list[dict[str, Any]] = []

		for disease in self.m_diseases:
			# Obtenemos los IDs de los signos y síntomas de esta enfermedad
			disease_signs = set(s.m_id for s in disease.get_signs())
			disease_symptoms = set(s.m_id for s in disease.get_symptoms())

			total_disease_factors = len(disease_signs) + len(disease_symptoms)

			# Si la enfermedad no tiene signos/síntomas, la ignoramos
			if total_disease_factors == 0:
				continue

			# Calculamos las coincidencias
			matching_signs = len(patient_sign_ids.intersection(disease_signs))
			matching_symptoms = len(
				patient_symptom_ids.intersection(disease_symptoms)
			)

			total_matches = matching_signs + matching_symptoms

			# Si hay al menos una coincidencia, la añadimos
			if total_matches > 0:
				# Calculamos la puntuación
				score = total_matches / total_disease_factors

				results.append(
					{
						"disease_id": disease.m_id,
						"disease_name": disease.m_name,
						"score": score,
						"details": f"{total_matches} de {total_disease_factors} factores",
					}
				)

		# Devolvemos la lista ordenada
		return sorted(results, key=lambda x: x["score"], reverse=True)