import wx
from wx import Panel, BoxSizer, EXPAND, ALL, ID_ANY
from wx.dataview import (
    DataViewListCtrl,
    DATAVIEW_CELL_EDITABLE,
    DATAVIEW_CELL_INERT,
    EVT_DATAVIEW_ITEM_VALUE_CHANGED,
)
from patient import get_patients, Patient


class CRUDPatient(Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = BoxSizer()
        self.m_dataview = DataViewListCtrl(self, ID_ANY, style=0)

        # columnas según la tabla real
        self.m_dataview.AppendTextColumn("ID", width=50, mode=DATAVIEW_CELL_INERT)
        self.m_dataview.AppendTextColumn("Médico", width=80, mode=DATAVIEW_CELL_EDITABLE)
        self.m_dataview.AppendTextColumn("Nombre", width=150, mode=DATAVIEW_CELL_EDITABLE)
        self.m_dataview.AppendTextColumn("Apellido", width=150, mode=DATAVIEW_CELL_EDITABLE)
        self.m_dataview.AppendTextColumn("CURP", width=150, mode=DATAVIEW_CELL_EDITABLE)
        self.m_dataview.AppendToggleColumn("Activo", width=70)

        sizer.Add(self.m_dataview, 1, EXPAND | ALL, 5)
        self.SetSizer(sizer)

        self.Bind(EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnItemEdit, self.m_dataview)
        self.UpdateRows()

    def UpdateRows(self):
        self.m_dataview.DeleteAllItems()
        for p in get_patients():
            self.m_dataview.AppendItem(p.to_list())

    def OnItemEdit(self, event):
        row = self.m_dataview.ItemToRow(event.GetItem())
        col = event.GetColumn()
        value = self.m_dataview.GetValue(row, col)
        if value is None:
            value = ""

        patient_id = int(self.m_dataview.GetValue(row, 0))
        patient = Patient()
        patient.select_by_id(patient_id)

        try:
            if col == 1:
                # médico (entero)
                patient.update_medic(int(value) if value else None)
            elif col == 2:
                patient.update_name(value)
            elif col == 3:
                patient.update_lastname(value)
            elif col == 4:
                patient.update_curp(value)
            elif col == 5:
                if value is not None:
                    patient.update_active(1 if bool(value) else 0)
        except Exception as e:
            wx.MessageBox(
                f"Error al actualizar:\n{e}",
                "Error de Base de Datos",
                wx.OK | wx.ICON_ERROR,
            )

        self.UpdateRows()
        event.Skip()
