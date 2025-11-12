import wx
from wx import Panel, BoxSizer, EXPAND, ALL, ID_ANY
from wx.dataview import (
    DataViewListCtrl,
    DATAVIEW_CELL_EDITABLE,
    DATAVIEW_CELL_ACTIVATABLE,
    DATAVIEW_CELL_INERT,
    DATAVIEW_COL_RESIZABLE,
    DATAVIEW_COL_SORTABLE,
    EVT_DATAVIEW_ITEM_VALUE_CHANGED,
)
from user import get_users, User


class CRUDUser(Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = BoxSizer()
        self.m_dataview = DataViewListCtrl(self, ID_ANY, style=0)

        self.m_dataview.AppendTextColumn("ID (User)", width=70, mode=DATAVIEW_CELL_INERT)
        self.m_dataview.AppendTextColumn("Usuario", width=120, mode=DATAVIEW_CELL_EDITABLE)
        self.m_dataview.AppendTextColumn("Contraseña", width=120, mode=DATAVIEW_CELL_EDITABLE)
        self.m_dataview.AppendTextColumn("Rol", width=80, mode=DATAVIEW_CELL_INERT)
        self.m_dataview.AppendTextColumn("Nombre", width=130, mode=DATAVIEW_CELL_EDITABLE)
        self.m_dataview.AppendTextColumn("Apellido", width=130, mode=DATAVIEW_CELL_EDITABLE)
        self.m_dataview.AppendTextColumn("Especialidad", width=150, mode=DATAVIEW_CELL_EDITABLE)
        self.m_dataview.AppendTextColumn("Cédula", width=100, mode=DATAVIEW_CELL_EDITABLE)
        self.m_dataview.AppendToggleColumn("Activo", width=60)

        sizer.Add(self.m_dataview, 1, EXPAND | ALL, 5)
        self.SetSizer(sizer)

        self.Bind(EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnItemEdit, self.m_dataview)
        self.UpdateRows()

    def UpdateRows(self):
        self.m_dataview.DeleteAllItems()
        for u in get_users():
            self.m_dataview.AppendItem(u.to_list())

    def OnItemEdit(self, event):
        row = self.m_dataview.ItemToRow(event.GetItem())
        col = event.GetColumn()
        value = self.m_dataview.GetValue(row, col)
        if value is None:
            value = ""

        try:
            user_id = int(self.m_dataview.GetValue(row, 0))
        except Exception:
            return

        user = User()
        user.select_by_id(user_id)
        if not user or user.m_id == 0:
            return

        try:
            if col == 1:
                user.update_user(value)
            elif col == 2:
                user.update_password(value)
            elif col == 4:
                user.update_medic_name(value)
            elif col == 5:
                user.update_medic_lastname(value)
            elif col == 6:
                user.update_medic_specialty(value)
            elif col == 7:
                user.update_medic_certificate(value)
            elif col == 8:
                if value is not None:
                    user.update_active(1 if bool(value) else 0)
        except Exception as e:
            wx.MessageBox(
                f"Error al actualizar (¿Valor duplicado o conexión perdida?):\n{e}",
                "Error de Base de Datos",
                wx.OK | wx.ICON_ERROR,
            )

        self.UpdateRows()
        event.Skip()
