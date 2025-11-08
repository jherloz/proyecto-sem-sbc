from wx import (
	ALIGN_LEFT,
	ALL,
	COL_WIDTH_AUTOSIZE,
	EXPAND,
	BoxSizer,
	Panel,
	Window,
	MessageBox,
	ICON_INFORMATION,
	ID_OK,
	OK, 
	ICON_ERROR,
)
from wx.dataview import (
	DATAVIEW_CELL_ACTIVATABLE,
	DATAVIEW_CELL_EDITABLE,
	DATAVIEW_CELL_INERT,
	DATAVIEW_COL_RESIZABLE,
	DATAVIEW_COL_SORTABLE,
	EVT_DATAVIEW_ITEM_VALUE_CHANGED,
	DataViewEvent,
	DataViewListCtrl,
)

from user import User, get_users


class CRUDUser(Panel):
	def __init__(self, parent: Window):
		super().__init__(parent)

		sizer = BoxSizer()
		self.m_dataview = DataViewListCtrl(self)

		self.m_dataview.AppendTextColumn(
			"ID (User)",
			width=COL_WIDTH_AUTOSIZE,
			mode=DATAVIEW_CELL_INERT,
			align=ALIGN_LEFT,
			flags=DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendTextColumn(
			"Usuario",
			width=120,
			mode=DATAVIEW_CELL_EDITABLE,
			align=ALIGN_LEFT,
			flags=DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendTextColumn(
			"Contraseña",
			width=100,
			mode=DATAVIEW_CELL_EDITABLE,
			align=ALIGN_LEFT,
			flags=DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendTextColumn(
			"Rol",
			width=80,
			mode=DATAVIEW_CELL_INERT,
			align=ALIGN_LEFT,
			flags=DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendTextColumn(
			"Nombre",
			width=120,
			mode=DATAVIEW_CELL_EDITABLE,
			align=ALIGN_LEFT,
			flags=DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendTextColumn(
			"Apellido",
			width=120,
			mode=DATAVIEW_CELL_EDITABLE,
			align=ALIGN_LEFT,
			flags=DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendTextColumn(
			"Especialidad",
			width=150,
			mode=DATAVIEW_CELL_EDITABLE,
			align=ALIGN_LEFT,
			flags=DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendTextColumn(
			"Cédula",
			width=100,
			mode=DATAVIEW_CELL_EDITABLE,
			align=ALIGN_LEFT,
			flags=DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendToggleColumn(
			"Activo",
			width=60,
			mode=DATAVIEW_CELL_ACTIVATABLE,
			align=ALIGN_LEFT,
			flags=DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)

		sizer.Add(self.m_dataview, 1, EXPAND | ALL)
		self.SetSizerAndFit(sizer)

		self.Bind(EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnItemEdit, self.m_dataview)
		self.UpdateRows()

	def ClearRows(self):
		self.m_dataview.DeleteAllItems()

	def UpdateRows(self):
		rows = get_users()
		self.ClearRows()
		for user_obj in rows:
			self.m_dataview.AppendItem(user_obj.to_list())

	def OnItemEdit(self, event: DataViewEvent):
		row: int = self.m_dataview.ItemToRow(event.GetItem())
		col: int = self.m_dataview.GetColumnIndex(event.GetColumn())
		value = event.GetValue()
		user_id = int(self.m_dataview.GetValue(row, 0))

		user = User()
		user.select_by_id(user_id)

		if user.m_id == 1 and col in [3, 4, 5, 6, 7, 8]:
			MessageBox(
				"El usuario 'admin' no puede ser modificado de esta forma.",
				"Protegido",
				ICON_INFORMATION | OK,
			)
			self.UpdateRows()
			return

		try:
			if col == 1:
				user.update_user(value)
			elif col == 2:
				user.update_password(value)
			elif col in [4, 5, 6, 7]:
				if not user.is_medic():
					MessageBox(
						"Solo los usuarios con rol 'Médico' pueden tener estos datos.",
						"Error",
						ICON_INFORMATION | OK,
					)
					self.UpdateRows()
					return

				if col == 4:
					user.update_medic_name(value)
				elif col == 5:
					user.update_medic_lastname(value)
				elif col == 6:
					user.update_medic_specialty(value)
				elif col == 7:
					user.update_medic_certificate(value)
			elif col == 8:
				user.update_active(int(value))

		except Exception as e:
			MessageBox(
				f"Error al actualizar (¿Valor duplicado?):\n{e}",
				"Error de Base de Datos",
				ICON_ERROR | OK,
			)

		self.UpdateRows()
		event.Skip()