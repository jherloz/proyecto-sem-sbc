from wx import (
	Notebook as wxNotebook,
	Panel,
	Window,
)

from user import User

from page_crud import PageCRUD
from page_diagnose import PageDiagnose
from page_history import PageHistory
from page_followup import PageFollowup


class Notebook(wxNotebook):
	def __init__(self, parent: Window):
		super().__init__(parent)

		self.m_page_diagnose: PageDiagnose | None = None
		self.m_page_history: PageHistory | None = None
		self.m_page_followup: PageFollowup | None = None
		self.m_page_crud: PageCRUD | None = None
		
		self.Hide() 

	def BuildPagesForRole(self, user: User | None):

		self.DeleteAllPages()
		
		# Limpiar referencias
		self.m_page_diagnose = None
		self.m_page_history = None
		self.m_page_followup = None
		self.m_page_crud = None
		
		if not user:
			self.Hide()
			return
			
		self.Show()

		if user.is_medic():
			#Vistas disponibles para Médico
			self.m_page_diagnose = PageDiagnose(self)
			self.m_page_history = PageHistory(self)
			self.m_page_followup = PageFollowup(self)
			
			self.AddPage(self.m_page_diagnose, "Diagnóstico")
			self.AddPage(self.m_page_history, "Historial")
			self.AddPage(self.m_page_followup, "Seguimiento")
			
			self.m_page_diagnose.UpdatePatientList()
			self.m_page_diagnose.UpdateSignSymptomLists()
			self.m_page_history.UpdatePatientList()
			self.m_page_followup.OnRefresh(None)
			
		elif user.is_admin():
			#Vista disponible para Admin
			self.m_page_crud = PageCRUD(self)
			self.AddPage(self.m_page_crud, "CRUD")
			
			self.m_page_crud.UpdateRows()

		self.Layout()