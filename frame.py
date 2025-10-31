from wx import (
	ALL,
	EVT_CLOSE,
	EVT_MENU,
	EXPAND,
	CommandEvent,
	Event,
	Frame as wxFrame,
	GBPosition,
	GBSpan,
	GridBagSizer,
	ID_ANY,
	MenuEvent,
)


from database import Database
from dialog_disease import DialogDisease
from dialog_login import DialogLogin
from dialog_medic import DialogMedic
from dialog_patient import DialogPatient
from dialog_symptom import DialogSymptom
from dialog_user import DialogUser
from menubar import MenuBar
from notebook import Notebook


class Frame(wxFrame):
	def __init__(self, title: str):
		super().__init__(None, ID_ANY, title)

		gbSizer = GridBagSizer()
		self.m_menuBar = MenuBar()
		self.m_notebook = Notebook(self)

		gbSizer.Add(self.m_notebook, GBPosition(0, 0), GBSpan(1, 2), EXPAND | ALL, 5)
		gbSizer.AddGrowableRow(0, 1)
		gbSizer.AddGrowableCol(0, 1)

		self.SetMenuBar(self.m_menuBar)
		self.CreateStatusBar()
		self.SetSizerAndFit(gbSizer)
		self.SetSize(848, 480)
		self.SetMinSize(self.GetSize())

		self.m_notebook.Show(True)

		self.Bind(EVT_CLOSE, self.OnClose, self)
		self.Bind(EVT_MENU, self.OnMenuItem)

	def OnClose(self, event: Event):
		Database.close()
		event.Skip()

	def OnMenuItem(self, event: MenuEvent):
		if event.GetId() == MenuBar.MENU_ITEM_USER_ADD:
			dialog = DialogUser(self)

			dialog.ShowModal()
			dialog.Destroy()

			self.m_notebook.m_page_crud.m_crud_user.UpdateRows()

		if event.GetId() == MenuBar.MENU_ITEM_USER_LOG_IN:
			dialog = DialogLogin(self)

			dialog.ShowModal()
			dialog.Destroy()

		if event.GetId() == MenuBar.MENU_ITEM_USER_LOG_OUT:
			pass

		if event.GetId() == MenuBar.MENU_ITEM_PATIENT_ADD:
			dialog = DialogPatient(self)

			dialog.ShowModal()
			dialog.Destroy()

			self.m_notebook.m_page_crud.m_crud_patient.UpdateRows()

		if event.GetId() == MenuBar.MENU_ITEM_MEDIC_ADD:
			dialog = DialogMedic(self)

			dialog.ShowModal()
			dialog.Destroy()

			self.m_notebook.m_page_crud.m_crud_medic.UpdateRows()

		if event.GetId() == MenuBar.MENU_ITEM_SYMPTOM_ADD:
			dialog = DialogSymptom(self)

			dialog.ShowModal()
			dialog.Destroy()

			self.m_notebook.m_page_crud.m_crud_symptom.UpdateRows()

		if event.GetId() == MenuBar.MENU_ITEM_DISEASE_ADD:
			dialog = DialogDisease(self)

			dialog.ShowModal()
			dialog.Destroy()

			self.m_notebook.m_page_crud.m_crud_disease.UpdateRows()

		event.Skip()
