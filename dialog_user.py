from wx import (
	ALIGN_CENTRE_HORIZONTAL,
	ALIGN_CENTRE_VERTICAL,
	ALL,
	EVT_BUTTON,
	EVT_RADIOBOX,
	EXPAND,
	ID_CANCEL,
	ID_OK,
	OK,  # --- CORRECCIÓN ---
	RIGHT,
	BoxSizer,
	Button,
	CommandEvent,
	DefaultPosition,
	DefaultSpan,
	Dialog,
	ID_ANY,
	GBPosition,
	GBSpan,
	GridBagSizer,
	Size,
	StaticText,
	TextCtrl,
	Window,
	RadioBox,
	MessageBox,
	ICON_ERROR,
)
from database import Database
from medic import Medic
from user import User


class DialogUser(Dialog):
	def __init__(self, parent: Window):
		super().__init__(parent, ID_ANY, "Agregar Usuario")

		gbSizer = GridBagSizer(5, 5)

		# --- Controles Básicos ---
		self.m_textCtrl_user = TextCtrl(self, size=Size(250, -1))
		self.m_textCtrl_password = TextCtrl(self, size=Size(250, -1))
		self.m_radio_role = RadioBox(self, label="Rol", choices=["Admin", "Médico"])

		# --- Controles de Médico (ocultos al inicio) ---
		self.m_st_name = StaticText(self, label="Nombre:")
		self.m_textCtrl_name = TextCtrl(self, size=Size(250, -1))
		self.m_st_lastname = StaticText(self, label="Apellido:")
		self.m_textCtrl_lastname = TextCtrl(self, size=Size(250, -1))
		self.m_st_specialty = StaticText(self, label="Especialidad:")
		self.m_textCtrl_specialty = TextCtrl(self, size=Size(250, -1))
		self.m_st_certificate = StaticText(self, label="Cédula:")
		self.m_textCtrl_certificate = TextCtrl(self, size=Size(250, -1))

		self.m_medic_widgets = [
			self.m_st_name,
			self.m_textCtrl_name,
			self.m_st_lastname,
			self.m_textCtrl_lastname,
			self.m_st_specialty,
			self.m_textCtrl_specialty,
			self.m_st_certificate,
			self.m_textCtrl_certificate,
		]

		# --- Botones ---
		buttonSizer = BoxSizer()
		self.m_button_ok = Button(self, ID_ANY, "Agregar")
		self.m_button_cancel = Button(self, ID_ANY, "Cancelar")
		buttonSizer.Add(self.m_button_ok, 0, RIGHT, 10)
		buttonSizer.Add(self.m_button_cancel)

		# --- Layout ---
		gbSizer.Add(
			StaticText(self, label="Usuario:"),
			GBPosition(0, 0),
			flag=ALL | ALIGN_CENTRE_VERTICAL,
		)
		gbSizer.Add(self.m_textCtrl_user, GBPosition(0, 1), flag=EXPAND | ALL)

		gbSizer.Add(
			StaticText(self, label="Contraseña:"),
			GBPosition(1, 0),
			flag=ALL | ALIGN_CENTRE_VERTICAL,
		)
		gbSizer.Add(self.m_textCtrl_password, GBPosition(1, 1), flag=EXPAND | ALL)

		gbSizer.Add(self.m_radio_role, GBPosition(2, 0), GBSpan(1, 2), flag=EXPAND | ALL)

		# Campos de Médico
		gbSizer.Add(self.m_st_name, GBPosition(3, 0), flag=ALL | ALIGN_CENTRE_VERTICAL)
		gbSizer.Add(self.m_textCtrl_name, GBPosition(3, 1), flag=EXPAND | ALL)

		gbSizer.Add(
			self.m_st_lastname, GBPosition(4, 0), flag=ALL | ALIGN_CENTRE_VERTICAL
		)
		gbSizer.Add(self.m_textCtrl_lastname, GBPosition(4, 1), flag=EXPAND | ALL)

		gbSizer.Add(
			self.m_st_specialty, GBPosition(5, 0), flag=ALL | ALIGN_CENTRE_VERTICAL
		)
		gbSizer.Add(self.m_textCtrl_specialty, GBPosition(5, 1), flag=EXPAND | ALL)

		gbSizer.Add(
			self.m_st_certificate, GBPosition(6, 0), flag=ALL | ALIGN_CENTRE_VERTICAL
		)
		gbSizer.Add(self.m_textCtrl_certificate, GBPosition(6, 1), flag=EXPAND | ALL)

		# Botones
		gbSizer.Add(
			buttonSizer,
			GBPosition(7, 0),
			GBSpan(1, 2),
			flag=EXPAND | ALL | ALIGN_CENTRE_HORIZONTAL,
		)

		self.SetSizerAndFit(gbSizer)
		self.ShowMedicFields(False)
		self.CenterOnParent()

		# --- Bindings ---
		self.Bind(EVT_BUTTON, self.OnButtonClick)
		self.Bind(EVT_RADIOBOX, self.OnRoleChange, self.m_radio_role)

	def ShowMedicFields(self, show: bool):
		"""Muestra u oculta los campos de médico."""
		for widget in self.m_medic_widgets:
			widget.Show(show)
		self.GetSizer().Layout()
		self.Fit()

	def OnRoleChange(self, event: CommandEvent):
		is_medic = self.m_radio_role.GetSelection() == 1
		self.ShowMedicFields(is_medic)

	def OnButtonClick(self, event: CommandEvent):
		if event.GetId() == self.m_button_ok.GetId():
			username = self.m_textCtrl_user.GetValue()
			password = self.m_textCtrl_password.GetValue()

			if not username or not password:
				MessageBox(
					"Usuario y Contraseña no pueden estar vacíos.", "Error", ICON_ERROR | OK
				)
				return

			role_id: int | None = None
			is_medic = self.m_radio_role.GetSelection() == 1

			if is_medic:
				name = self.m_textCtrl_name.GetValue()
				lastname = self.m_textCtrl_lastname.GetValue()
				specialty = self.m_textCtrl_specialty.GetValue()
				certificate = self.m_textCtrl_certificate.GetValue()

				if not name or not lastname or not specialty or not certificate:
					MessageBox(
						"Todos los campos del médico son obligatorios.",
						"Error",
						ICON_ERROR | OK,
					)
					return

				medic = Medic(0, name, lastname, specialty, certificate)
				try:
					role_id = medic.insert()
				except Exception as e:
					MessageBox(
						f"Error al crear al médico (¿Cédula duplicada?):\n{e}",
						"Error de Base de Datos",
						ICON_ERROR | OK,
					)
					return

			user = User(0, username, password, role_id)
			try:
				user.insert()
				self.EndModal(ID_OK)
			except Exception as e:
				MessageBox(
					f"Error al crear el usuario (¿Usuario duplicado?):\n{e}",
					"Error de Base de Datos",
					ICON_ERROR | OK,
				)
				if role_id:
					Database.execute("DELETE FROM medico WHERE id=%s", [role_id])
				return

		if event.GetId() == self.m_button_cancel.GetId():
			self.EndModal(ID_CANCEL)

		event.Skip()