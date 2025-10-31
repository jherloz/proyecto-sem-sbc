from wx import (
	BookCtrlEvent,
	EVT_NOTEBOOK_PAGE_CHANGING,
	Notebook as wxNotebook,
	Panel,
	Window,
)


from page_crud import PageCRUD


class Notebook(wxNotebook):
	def __init__(self, parent: Window):
		super().__init__(parent)

		self.m_page_diagnose = Panel(self)
		self.m_page_history = Panel(self)
		self.m_page_followup = Panel(self)
		self.m_page_crud = PageCRUD(self)

		self.AddPage(self.m_page_diagnose, "Diagnóstico")
		self.AddPage(self.m_page_history, "Historial")
		self.AddPage(self.m_page_followup, "Seguimiento")
		self.AddPage(self.m_page_crud, "CRUD")

		self.Bind(EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChange, self)

	def OnPageChange(self, event: BookCtrlEvent):
		if event.GetSelection() == 3:
			self.m_page_crud.UpdateRows()

		event.Skip()
