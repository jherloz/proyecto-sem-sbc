import wx
from wx import (
    Panel, Window, BoxSizer, Button, ComboBox, StaticText,
    EVT_BUTTON, VERTICAL, HORIZONTAL, ALL, EXPAND, Event, NOT_FOUND
)
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

from diagnostico import get_graph_data_by_patient
from patient import get_patients_by_medic
from user import User


class PageFollowup(Panel):
    def __init__(self, parent: Window):
        super().__init__(parent)

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)

        self.m_combo_patient = ComboBox(self, style=wx.CB_READONLY)
        self.m_btn_refresh = Button(self, label="Actualizar Gráfica")

        topSizer = BoxSizer(HORIZONTAL)
        topSizer.Add(StaticText(self, label="Seleccionar Paciente:"), 0, ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        topSizer.Add(self.m_combo_patient, 1, EXPAND | ALL, 5)
        topSizer.Add(self.m_btn_refresh, 0, ALL, 5)

        mainSizer = BoxSizer(VERTICAL)
        mainSizer.Add(topSizer, 0, EXPAND | ALL, 5)
        mainSizer.Add(self.canvas, 1, EXPAND | ALL, 5)

        self.SetSizer(mainSizer)

        self.Bind(EVT_BUTTON, self.OnRefresh, self.m_btn_refresh)

        # Inicializa la lista de pacientes
        self.UpdatePatientList()

    def GetCurrentUser(self) -> User | None:
        """Obtiene el usuario logueado desde el frame principal."""
        top = self.GetTopLevelParent()
        if hasattr(top, "m_current_user"):
            return top.m_current_user
        return None

    def UpdatePatientList(self):
        """Rellena el combo con los pacientes del médico actual."""
        user = self.GetCurrentUser()
        if not (user and user.is_medic()):
            self.m_combo_patient.Clear()
            return

        medic_id = user.m_role
        self.m_all_patients = get_patients_by_medic(medic_id)
        patient_names = [p.get_full_name() for p in self.m_all_patients]
        self.m_combo_patient.Clear()
        self.m_combo_patient.AppendItems(patient_names)

    def OnRefresh(self, event: Event | None):
        """Obtiene los datos y dibuja la gráfica del paciente seleccionado."""
        selected_idx = self.m_combo_patient.GetSelection()
        if selected_idx == wx.NOT_FOUND:
            self.axes.clear()
            self.axes.text(
                0.5, 0.5,
                "Seleccione un paciente para ver su seguimiento.",
                horizontalalignment='center',
                verticalalignment='center',
                transform=self.axes.transAxes
            )
            self.canvas.draw()
            return

        patient_id = self.m_all_patients[selected_idx].m_id
        data = get_graph_data_by_patient(patient_id)

        self.axes.clear()
        if not data:
            self.axes.text(
                0.5, 0.5,
                "No hay datos de diagnóstico para este paciente.",
                horizontalalignment='center',
                verticalalignment='center',
                transform=self.axes.transAxes
            )
        else:
            labels = list(data.keys())
            values = list(data.values())

            self.axes.bar(labels, values)
            self.axes.set_ylabel("Cantidad de Diagnósticos")
            self.axes.set_title("Frecuencia de Enfermedades Diagnosticadas por Paciente")
            self.figure.autofmt_xdate(rotation=45)

        self.canvas.draw()