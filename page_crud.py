from wx import (
	ALL,
	EVT_NOTEBOOK_PAGE_CHANGING,
	EXPAND,
	BookCtrlEvent,
	BoxSizer,
	Notebook,
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
		self.m_notebook: Notebook = Notebook(self)
		self.m_crud_user = CRUDUser(self.m_notebook)
		self.m_crud_patient = CRUDPatient(self.m_notebook)
		self.m_crud_symptom = CRUDSymptom(self.m_notebook)
		self.m_crud_sign = CRUDSign(self.m_notebook)
		self.m_crud_disease = CRUDDisease(self.m_notebook)

		self.m_notebook.AddPage(self.m_crud_user, "Usuario")
		self.m_notebook.AddPage(self.m_crud_patient, "Paciente")
		self.m_notebook.AddPage(self.m_crud_symptom, "Síntoma")
		self.m_notebook.AddPage(self.m_crud_sign, "Signo")
		self.m_notebook.AddPage(self.m_crud_disease, "Enfermedad")

		sizer.Add(self.m_notebook, 1, EXPAND | ALL)
		self.Bind(EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChange, self.m_notebook)

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

		page = self.m_notebook.GetPage(page_index)
		if page:
			page.SetFocus()

		event.Skip()
