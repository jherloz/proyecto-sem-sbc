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
	ID_OK,
	MenuEvent,
)


from database import Database
from dialog_disease import DialogDisease
from dialog_login import DialogLogin
from dialog_patient import DialogPatient
from dialog_symptom import DialogSymptom
from dialog_sign import DialogSign
from dialog_user import DialogUser
from menubar import MenuBar
from notebook import Notebook
from user import User


class Frame(wxFrame):
	m_current_user: User | None = None

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

		self.Bind(EVT_CLOSE, self.OnClose, self)
		self.Bind(EVT_MENU, self.OnMenuItem)

	def InitAppLogic(self):
		self.ShowLoginDialog()

	def ShowLoginDialog(self):
		dialog = DialogLogin(self)

		if dialog.ShowModal() == ID_OK:
			self.m_current_user = dialog.GetUser()
			if self.m_current_user:
				self.m_current_user.select_by_id(self.m_current_user.m_id)
				self.SetStatusText(f"Bienvenido, {self.m_current_user.m_user}")
		else:
			if not self.m_current_user:
				self.Close()
		
		dialog.Destroy()
		self.ApplyUserRole()

	def ApplyUserRole(self):
		"""Aplica los cambios de UI basados en el rol (Menús y Pestañas)."""
		self.m_menuBar.UpdateRoles(self.m_current_user)
		self.m_notebook.BuildPagesForRole(self.m_current_user)
		self.Layout()

	def OnClose(self, event: Event):
		Database.close()
		event.Skip()

	def OnMenuItem(self, event: MenuEvent):
		evt_id = event.GetId()

		if evt_id == MenuBar.MENU_ITEM_USER_ADD:
			dialog = DialogUser(self)
			if dialog.ShowModal() == ID_OK:
				# Comprobar si la página existe antes de actualizar
				if self.m_notebook.m_page_crud:
					self.m_notebook.m_page_crud.m_crud_user.UpdateRows()
			dialog.Destroy()

		elif evt_id == MenuBar.MENU_ITEM_USER_LOG_IN:
			self.ShowLoginDialog()

		elif evt_id == MenuBar.MENU_ITEM_USER_LOG_OUT:
			self.m_current_user = None
			self.SetStatusText("Sesión cerrada.")
			self.ApplyUserRole() # Limpia las pestañas
			self.ShowLoginDialog()

		elif evt_id == MenuBar.MENU_ITEM_PATIENT_ADD:
			if self.m_current_user and self.m_current_user.is_medic():
				medic_id = self.m_current_user.m_role
				dialog = DialogPatient(self, medic_id)
				if dialog.ShowModal() == ID_OK:
					# Comprobar si las páginas existen
					if self.m_notebook.m_page_crud:
						self.m_notebook.m_page_crud.m_crud_patient.UpdateRows()
					if self.m_notebook.m_page_diagnose:
						self.m_notebook.m_page_diagnose.UpdatePatientList()
				dialog.Destroy()

		elif evt_id == MenuBar.MENU_ITEM_SYMPTOM_ADD:
			dialog = DialogSymptom(self)
			if dialog.ShowModal() == ID_OK:
				if self.m_notebook.m_page_crud:
					self.m_notebook.m_page_crud.m_crud_symptom.UpdateRows()
			dialog.Destroy()
		
		elif evt_id == MenuBar.MENU_ITEM_SIGN_ADD:
			dialog = DialogSign(self)
			if dialog.ShowModal() == ID_OK:
				if self.m_notebook.m_page_crud:
					self.m_notebook.m_page_crud.m_crud_sign.UpdateRows()
			dialog.Destroy()

		elif evt_id == MenuBar.MENU_ITEM_DISEASE_ADD:
			dialog = DialogDisease(self)
			if dialog.ShowModal() == ID_OK:
				if self.m_notebook.m_page_crud:
					self.m_notebook.m_page_crud.m_crud_disease.UpdateRows()
			dialog.Destroy()

		event.Skip()