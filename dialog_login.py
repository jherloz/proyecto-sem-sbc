from wx import (
	ALIGN_CENTRE_HORIZONTAL,
	ALIGN_CENTRE_VERTICAL,
	ALL,
	EVT_BUTTON,
	EXPAND,
	ID_OK,
	TE_PASSWORD,
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


from user import log_in


class DialogLogin(Dialog):
	def __init__(self, parent: Window):
		super().__init__(parent, ID_ANY, "Iniciar Sesión")

		gbSizer = GridBagSizer()
		self.m_textCtrl_user = TextCtrl(
			self, ID_ANY, "", DefaultPosition, Size(250, -1)
		)
		self.m_textCtrl_password = TextCtrl(
			self, ID_ANY, "", DefaultPosition, Size(250, -1)
		)
		self.m_button_ok = Button(self, ID_ANY, "Iniciar Sesión")

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
			self.m_button_ok,
			GBPosition(2, 0),
			GBSpan(1, 2),
			EXPAND | ALL | ALIGN_CENTRE_HORIZONTAL,
			5,
		)

		self.m_textCtrl_password.SetWindowStyleFlag(TE_PASSWORD)

		self.SetSizerAndFit(gbSizer)

		self.Bind(EVT_BUTTON, self.OnButtonClick)

	def OnButtonClick(self, event: CommandEvent):
		user = self.m_textCtrl_user.GetValue()
		password = self.m_textCtrl_password.GetValue()

		if user and password:
			model = log_in(user, password)

			if model:
				self.EndModal(ID_OK)

		event.Skip()
