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


from medic import Medic, get_medics


class CRUDMedic(Panel):
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
			"Nombre",
			DATAVIEW_CELL_EDITABLE,
			COL_WIDTH_AUTOSIZE,
			ALIGN_LEFT,
			DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendTextColumn(
			"Apellido",
			DATAVIEW_CELL_EDITABLE,
			COL_WIDTH_AUTOSIZE,
			ALIGN_LEFT,
			DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendTextColumn(
			"Especialidad",
			DATAVIEW_CELL_EDITABLE,
			COL_WIDTH_AUTOSIZE,
			ALIGN_LEFT,
			DATAVIEW_COL_RESIZABLE | DATAVIEW_COL_SORTABLE,
		)
		self.m_dataview.AppendTextColumn(
			"Cédula",
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
		rows = get_medics()

		self.ClearRows()

		for i in rows:
			self.m_dataview.AppendItem(i.to_list())

	def OnItemEdit(self, event: DataViewEvent):
		row: int = self.m_dataview.ItemToRow(event.GetItem())
		col: int = event.GetColumn()
		aidi = self.m_dataview.GetValue(row, 0)
		value = self.m_dataview.GetValue(row, col)
		medic = Medic()

		medic.select_by_id(aidi)

		if col == 1:
			medic.update_name(value)
		elif col == 2:
			medic.update_lastname(value)
		elif col == 3:
			medic.update_specialty(value)
		elif col == 4:
			medic.update_certificate(value)
		elif col == 5:
			medic.update_active(value)

		self.UpdateRows()

		event.Skip()
