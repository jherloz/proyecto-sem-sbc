from wx import App as wxApp


from database import Database
from user import User, count_users
from frame import Frame


class App(wxApp):
	def __init__(self):
		super().__init__()

	def OnInit(self) -> bool:
		frame = Frame("Seminario Sistemas Basados en Conocimientos: Proyecto")

		Database.open("localhost", "sbc_user", "12345", "sbc_db", 3306)

		if count_users() == 0:
			user = User(0, "admin", "admin")
			user.insert()

		frame.Show(True)

		return True


if __name__ == "__main__":
	app = App()
	app.MainLoop()
