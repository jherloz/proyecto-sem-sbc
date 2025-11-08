import wx
from wx import (
	Panel,
	Window,
	BoxSizer,
	ComboBox,
	EVT_COMBOBOX,
	EXPAND,
	ALL,
	VERTICAL,
	ALIGN_LEFT,
	COL_WIDTH_AUTOSIZE,
	Event,
)
from wx.dataview import (
	DataViewListCtrl,
	DATAVIEW_CELL_INERT,
	DATAVIEW_COL_RESIZABLE,
	DATAVIEW_COL_SORTABLE,
)

from patient import Patient, get_patients_by_medic
from diagnostico import get_for_patient
from user import User

class PageHistory(Panel):
	
	m_all_patients: list[Patient] = []
	
	def __init__(self, parent: Window):
		super().__init__(parent)
		
		sizer = BoxSizer(VERTICAL)
		
		self.m_combo_patient = ComboBox(self, style=wx.CB_READONLY, size=(-1, 30))
		
		self.m_dvlc_history = DataViewListCtrl(self)
		self.m_dvlc_history.AppendTextColumn("Fecha", 0, width=150)
		self.m_dvlc_history.AppendTextColumn("Médico", 1, width=200)
		self.m_dvlc_history.AppendTextColumn("Enfermedad", 2, width=200)
		self.m_dvlc_history.AppendTextColumn("Tratamiento", 3, width=300)
		
		sizer.Add(self.m_combo_patient, 0, EXPAND | ALL, 10)
		sizer.Add(self.m_dvlc_history, 1, EXPAND | ALL, 10)
		
		self.SetSizer(sizer)
		
		self.Bind(EVT_COMBOBOX, self.OnPatientSelect, self.m_combo_patient)
		
	def GetCurrentUser(self) -> User | None:
		"""Helper para obtener el usuario actual desde el Frame."""
		top_level_window = self.GetTopLevelParent()
		if hasattr(top_level_window, 'm_current_user'):
			return top_level_window.m_current_user
		return None

	def UpdatePatientList(self):
		user = self.GetCurrentUser()
		if not (user and user.is_medic()):
			self.m_all_patients = []
			self.m_combo_patient.Clear()
			return

		medic_id = user.m_role
		self.m_all_patients = get_patients_by_medic(medic_id)
		patient_names = [p.get_full_name() for p in self.m_all_patients]
		
		current_selection = self.m_combo_patient.GetValue()
		
		self.m_combo_patient.Clear()
		self.m_combo_patient.AppendItems(patient_names)
		
		# Restaurar selección si aún existe
		if current_selection in patient_names:
			self.m_combo_patient.SetValue(current_selection)
		else:
			self.m_dvlc_history.DeleteAllItems() # Limpia la tabla si el paciente ya no está

	def OnPatientSelect(self, event: Event):
		patient_idx = self.m_combo_patient.GetSelection()
		if patient_idx == wx.NOT_FOUND:
			return
			
		patient_id = self.m_all_patients[patient_idx].m_id
		
		# Obtener historial
		history_list = get_for_patient(patient_id)
		
		# Poblar la tabla
		self.m_dvlc_history.DeleteAllItems()
		for item in history_list:
			self.m_dvlc_history.AppendItem(item.to_list_history())