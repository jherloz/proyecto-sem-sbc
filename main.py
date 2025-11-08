from wx import App as wxApp
import wx 


from database import Database
from user import User, count_users
from frame import Frame


class App(wxApp):
	def __init__(self):
		super().__init__()

	def OnInit(self) -> bool:

		try:
			Database.open("localhost", "root", "", "sbc_db", 3306)
		except Exception as e:

			wx.MessageBox(
				f"Error fatal al conectar a la base de datos: {e}\nLa aplicación se cerrará.",
				"Error de Base de Datos",
				wx.ICON_ERROR | wx.ID_OK,
			)
			return False 

		frame = Frame("Seminario Sistemas Basados en Conocimientos: Proyecto")

		if count_users() == 0:
			user = User(0, "admin", "admin")
			user.insert()

		frame.Show(True)

		frame.InitAppLogic()

		return True


if __name__ == "__main__":
	app = App()
	app.MainLoop()