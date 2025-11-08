from wx import (
	EVT_MENU,
	ID_HIGHEST,
	ID_SEPARATOR,
	Menu,
	MenuBar as wxMenuBar,
	MenuEvent,
)

from user import User


class MenuBar(wxMenuBar):
	MENU_ITEM_USER_ADD: int = ID_HIGHEST + 1
	MENU_ITEM_USER_LOG_IN: int = MENU_ITEM_USER_ADD + 1
	MENU_ITEM_USER_LOG_OUT: int = MENU_ITEM_USER_LOG_IN + 1
	MENU_ITEM_PATIENT_ADD: int = MENU_ITEM_USER_LOG_OUT + 1
	MENU_ITEM_SYMPTOM_ADD: int = MENU_ITEM_PATIENT_ADD + 1
	MENU_ITEM_DISEASE_ADD: int = MENU_ITEM_SYMPTOM_ADD + 1
	MENU_ITEM_SIGN_ADD: int = MENU_ITEM_DISEASE_ADD + 1

	def __init__(self):
		super().__init__()

		self.m_menu_disease = Menu()
		self.m_menu_patient = Menu()
		self.m_menu_symptom = Menu()
		self.m_menu_sign = Menu()
		self.m_menu_user = Menu()

		# Menu Usuario
		self.m_menu_user.Append(MenuBar.MENU_ITEM_USER_ADD, "Agregar")
		self.m_menu_user.Append(ID_SEPARATOR)
		self.m_menu_user.Append(MenuBar.MENU_ITEM_USER_LOG_IN, "Iniciar Sesión")
		self.m_menu_user.Append(MenuBar.MENU_ITEM_USER_LOG_OUT, "Cerrar Sesión")
		self.Append(self.m_menu_user, "Usuario")
		
		# Menu Paciente
		self.m_menu_patient.Append(MenuBar.MENU_ITEM_PATIENT_ADD, "Agregar")
		self.Append(self.m_menu_patient, "Paciente")
		
		#Menu Síntoma
		self.m_menu_symptom.Append(MenuBar.MENU_ITEM_SYMPTOM_ADD, "Agregar")
		self.Append(self.m_menu_symptom, "Síntoma")
		
		#Menu Signo
		self.m_menu_sign.Append(MenuBar.MENU_ITEM_SIGN_ADD, "Agregar")
		self.Append(self.m_menu_sign, "Signo")
		
		# Menu Enfermedad
		self.m_menu_disease.Append(MenuBar.MENU_ITEM_DISEASE_ADD, "Agregar")
		self.Append(self.m_menu_disease, "Enfermedad")

		self.UpdateRoles(None)

	def UpdateRoles(self, user: User | None):
		is_admin = user.is_admin() if user else False
		is_medic = user.is_medic() if user else False
		is_logged_in = user is not None

		# Menú Usuario
		self.Enable(MenuBar.MENU_ITEM_USER_ADD, is_admin) # Solo Admin crea usuarios
		self.Enable(MenuBar.MENU_ITEM_USER_LOG_IN, not is_logged_in)
		self.Enable(MenuBar.MENU_ITEM_USER_LOG_OUT, is_logged_in)
		
		# Menú Paciente
		self.Enable(MenuBar.MENU_ITEM_PATIENT_ADD, is_medic)
		
		# Menús de Admin
		self.Enable(MenuBar.MENU_ITEM_SYMPTOM_ADD, is_admin)
		self.Enable(MenuBar.MENU_ITEM_SIGN_ADD, is_admin)
		self.Enable(MenuBar.MENU_ITEM_DISEASE_ADD, is_admin)