from wx import (
	ALIGN_CENTRE_HORIZONTAL,
	ALIGN_CENTRE_VERTICAL,
	ALL,
	EVT_BUTTON,
	EXPAND,
	ID_CANCEL,
	ID_OK,
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
)


from user import User


class DialogUser(Dialog):
	def __init__(self, parent: Window):
		super().__init__(parent, ID_ANY, "Agregar Usuario")

		gbSizer = GridBagSizer()
		sizer = BoxSizer()
		self.m_textCtrl_user = TextCtrl(
			self, ID_ANY, "", DefaultPosition, Size(250, -1)
		)
		self.m_textCtrl_password = TextCtrl(
			self, ID_ANY, "", DefaultPosition, Size(250, -1)
		)
		self.m_button_ok = Button(self, ID_ANY, "Agregar")
		self.m_button_cancel = Button(self, ID_ANY, "Cancelar")

		gbSizer.Add(
			StaticText(self, ID_ANY, "Usuario:"),
			GBPosition(0, 0),
			DefaultSpan,
			ALL | ALIGN_CENTRE_VERTICAL,
			5,
		)
		gbSizer.Add(
			self.m_textCtrl_user, GBPosition(0, 1), DefaultSpan, EXPAND | ALL, 5
		)
		gbSizer.Add(
			StaticText(self, ID_ANY, "Contraseña:"),
			GBPosition(1, 0),
			DefaultSpan,
			ALL | ALIGN_CENTRE_VERTICAL,
			5,
		)
		gbSizer.Add(
			self.m_textCtrl_password, GBPosition(1, 1), DefaultSpan, EXPAND | ALL, 5
		)
		gbSizer.Add(
			sizer,
			GBPosition(2, 0),
			GBSpan(1, 2),
			EXPAND | ALL | ALIGN_CENTRE_HORIZONTAL,
			5,
		)
		sizer.Add(self.m_button_ok, 0, RIGHT, 25)
		sizer.Add(self.m_button_cancel)

		self.SetSizerAndFit(gbSizer)

		self.Bind(EVT_BUTTON, self.OnButtonClick)

	def OnButtonClick(self, event: CommandEvent):
		if event.GetId() == self.m_button_ok.GetId():
			user = User(
				0,
				self.m_textCtrl_user.GetValue(),
				self.m_textCtrl_password.GetValue(),
			)

			if user:
				user.insert()
				self.EndModal(ID_OK)

		if event.GetId() == self.m_button_cancel.GetId():
			self.EndModal(ID_CANCEL)

		event.Skip()
