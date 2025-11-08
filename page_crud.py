from wx import (
	ALL,
	EVT_LISTBOOK_PAGE_CHANGING,
	EXPAND,
	BookCtrlEvent,
	BoxSizer,
	Listbook,
	Panel as wxPanel,
	Window,
)


from crud_disease import CRUDDisease
from crud_patient import CRUDPatient
from crud_symptom import CRUDSymptom
from crud_sign import CRUDSign
from crud_user import CRUDUser


class PageCRUD(wxPanel):
	def __init__(self, parent: Window):
		super().__init__(parent)

		sizer = BoxSizer()
		self.m_listbook: Listbook = Listbook(self)
		self.m_crud_user = CRUDUser(self)
		self.m_crud_patient = CRUDPatient(self)
		self.m_crud_symptom = CRUDSymptom(self)
		self.m_crud_sign = CRUDSign(self)
		self.m_crud_disease = CRUDDisease(self)

		self.m_listbook.AddPage(self.m_crud_user, "Usuario") # Aquí se gestionan médicos
		self.m_listbook.AddPage(self.m_crud_patient, "Paciente")
		# Página de Médico eliminada
		self.m_listbook.AddPage(self.m_crud_symptom, "Síntoma")
		self.m_listbook.AddPage(self.m_crud_sign, "Signo")
		self.m_listbook.AddPage(self.m_crud_disease, "Enfermedad")

		sizer.Add(self.m_listbook, 1, EXPAND | ALL)
		self.Bind(EVT_LISTBOOK_PAGE_CHANGING, self.OnPageChange, self.m_listbook)

		self.SetSizerAndFit(sizer)

	def UpdateRows(self):
		self.m_crud_disease.UpdateRows()
		self.m_crud_patient.UpdateRows()
		self.m_crud_symptom.UpdateRows()
		self.m_crud_sign.UpdateRows()
		self.m_crud_user.UpdateRows()

	def OnPageChange(self, event: BookCtrlEvent):
		page_index = event.GetSelection()
		
		if page_index == 0:
			self.m_crud_user.UpdateRows()
		elif page_index == 1:
			self.m_crud_patient.UpdateRows()
		elif page_index == 2:
			self.m_crud_symptom.UpdateRows()
		elif page_index == 3:
			self.m_crud_sign.UpdateRows()
		elif page_index == 4:
			self.m_crud_disease.UpdateRows()

		event.Skip()