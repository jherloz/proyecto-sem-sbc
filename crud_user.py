from wx import (
	ALIGN_LEFT,
	ALL,
	COL_WIDTH_AUTOSIZE,
	EXPAND,
	BoxSizer,
	Panel,
	Window,
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
			"ID",
			DATAVIEW_CELL_INERT,
			COL_WIDTH_AUTOSIZE,
			ALIGN_LEFT,
			DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendTextColumn(
			"Usuario",
			DATAVIEW_CELL_EDITABLE,
			COL_WIDTH_AUTOSIZE,
			ALIGN_LEFT,
			DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendTextColumn(
			"Contraseña",
			DATAVIEW_CELL_EDITABLE,
			COL_WIDTH_AUTOSIZE,
			ALIGN_LEFT,
			DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendTextColumn(
			"Rol",
			DATAVIEW_CELL_EDITABLE,
			COL_WIDTH_AUTOSIZE,
			ALIGN_LEFT,
			DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendToggleColumn(
			"Activo",
			DATAVIEW_CELL_ACTIVATABLE,
			COL_WIDTH_AUTOSIZE,
			ALIGN_LEFT,
			DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)

		sizer.Add(self.m_dataview, 1, EXPAND | ALL)

		self.SetSizerAndFit(sizer)

		self.Bind(EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnItemEdit, self.m_dataview)

	def ClearRows(self):
		self.m_dataview.DeleteAllItems()

	def UpdateRows(self):
		rows = get_users()

		self.ClearRows()

		for i in rows:
			self.m_dataview.AppendItem(i.to_list())

	def OnItemEdit(self, event: DataViewEvent):
		row: int = self.m_dataview.ItemToRow(event.GetItem())
		col: int = event.GetColumn()
		aidi = self.m_dataview.GetValue(row, 0)
		value = self.m_dataview.GetValue(row, col)
		user = User()

		user.select_by_id(aidi)

		if col == 1:
			user.update_user(value)
		elif col == 2:
			user.update_password(value)
		elif col == 3:
			if int(aidi) != 1:
				user.update_role(value)
			else:
				self.UpdateRows()
		elif col == 4:
			if int(aidi) != 1:
				user.update_active(value)
			else:
				self.UpdateRows()

		self.UpdateRows()

		event.Skip()
