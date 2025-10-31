from wx import (
	EVT_MENU,
	ID_HIGHEST,
	ID_SEPARATOR,
	Menu,
	MenuBar as wxMenuBar,
	MenuEvent,
)


class MenuBar(wxMenuBar):
	MENU_ITEM_USER_ADD: int = ID_HIGHEST + 1
	MENU_ITEM_USER_LOG_IN: int = MENU_ITEM_USER_ADD + 1
	MENU_ITEM_USER_LOG_OUT: int = MENU_ITEM_USER_LOG_IN + 1
	MENU_ITEM_PATIENT_ADD: int = MENU_ITEM_USER_LOG_OUT + 1
	MENU_ITEM_MEDIC_ADD: int = MENU_ITEM_PATIENT_ADD + 1
	MENU_ITEM_SYMPTOM_ADD: int = MENU_ITEM_MEDIC_ADD + 1
	MENU_ITEM_DISEASE_ADD: int = MENU_ITEM_SYMPTOM_ADD + 1

	def __init__(self):
		super().__init__()

		self.m_menu_disease = Menu()
		self.m_menu_medic = Menu()
		self.m_menu_patient = Menu()
		self.m_menu_symptom = Menu()
		self.m_menu_user = Menu()

		self.m_menu_user.Append(MenuBar.MENU_ITEM_USER_ADD, "Agregar")
		self.m_menu_user.Append(ID_SEPARATOR)
		self.m_menu_user.Append(MenuBar.MENU_ITEM_USER_LOG_IN, "Iniciar Sesión")
		self.m_menu_user.Append(MenuBar.MENU_ITEM_USER_LOG_OUT, "Cerrar Sesión")
		self.Append(self.m_menu_user, "Usuario")
		self.m_menu_patient.Append(MenuBar.MENU_ITEM_PATIENT_ADD, "Agregar")
		self.Append(self.m_menu_patient, "Paciente")
		self.m_menu_medic.Append(MenuBar.MENU_ITEM_MEDIC_ADD, "Agregar")
		self.Append(self.m_menu_medic, "Médico")
		self.m_menu_symptom.Append(MenuBar.MENU_ITEM_SYMPTOM_ADD, "Agregar")
		self.Append(self.m_menu_symptom, "Síntoma")
		self.m_menu_disease.Append(MenuBar.MENU_ITEM_DISEASE_ADD, "Agregar")
		self.Append(self.m_menu_disease, "Enfermedad")
