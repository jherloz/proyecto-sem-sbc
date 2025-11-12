import wx
from wx import Panel, BoxSizer, EXPAND, ALL, ID_ANY
from wx.dataview import (
    DataViewListCtrl,
    DATAVIEW_CELL_EDITABLE,
    DATAVIEW_CELL_INERT,
    EVT_DATAVIEW_ITEM_VALUE_CHANGED,
)
from disease import get_diseases, Disease


class CRUDDisease(Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = BoxSizer()
        self.m_dataview = DataViewListCtrl(self, ID_ANY, style=0)

        self.m_dataview.AppendTextColumn("ID", width=60, mode=DATAVIEW_CELL_INERT)
        self.m_dataview.AppendTextColumn("Nombre", width=250, mode=DATAVIEW_CELL_EDITABLE)
        self.m_dataview.AppendToggleColumn("Activo", width=70)

        sizer.Add(self.m_dataview, 1, EXPAND | ALL, 5)
        self.SetSizer(sizer)

        self.Bind(EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnItemEdit, self.m_dataview)
        self.UpdateRows()

    def UpdateRows(self):
        self.m_dataview.DeleteAllItems()
        for d in get_diseases():
            self.m_dataview.AppendItem(d.to_list())

    def OnItemEdit(self, event):
        row = self.m_dataview.ItemToRow(event.GetItem())
        col = event.GetColumn()
        value = self.m_dataview.GetValue(row, col)
        if value is None:
            value = ""

        disease_id = int(self.m_dataview.GetValue(row, 0))
        disease = Disease()
        disease.select_by_id(disease_id)

        try:
            if col == 1:
                disease.update_name(value)
            elif col == 2:
                if value is not None:
                    disease.update_active(1 if bool(value) else 0)
        except Exception as e:
            wx.MessageBox(
                f"Error al actualizar:\n{e}",
                "Error de Base de Datos",
                wx.OK | wx.ICON_ERROR,
            )

        self.UpdateRows()
        event.Skip()
