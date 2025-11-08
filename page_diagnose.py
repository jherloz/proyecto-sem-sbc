import wx
from wx import (
	Panel,
	Window,
	BoxSizer,
	StaticBox,
	StaticBoxSizer,
	CheckListBox,
	Button,
	ComboBox,
	StaticText,
	TextCtrl,
	GridBagSizer,
	GBSpan,
	GBPosition,
	EXPAND,
	ALL,
	VERTICAL,
	HORIZONTAL,
	EVT_BUTTON,
	EVT_COMBOBOX,
	ALIGN_LEFT,
	ALIGN_CENTRE_VERTICAL,
	COL_WIDTH_AUTOSIZE,
	MessageBox,
	ID_OK,
	OK,
	ICON_INFORMATION,
	ICON_ERROR,
	Event,
	NOT_FOUND,
)
from wx.dataview import (
	DataViewListCtrl,
	DATAVIEW_CELL_INERT,
	DATAVIEW_COL_RESIZABLE,
	DATAVIEW_COL_SORTABLE,
)

from patient import Patient, get_patients_by_medic
from sign import Sign, get_signs
from symptom import Symptom, get_symptoms
from inference_engine import InferenceEngine
from diagnostico import Diagnostico
from user import User


class PageDiagnose(Panel):
	m_all_patients: list[Patient] = []
	m_all_signs: list[Sign] = []
	m_all_symptoms: list[Symptom] = []

	m_inference_engine: InferenceEngine

	def __init__(self, parent: Window):
		super().__init__(parent)

		self.m_inference_engine = InferenceEngine()

		mainSizer = BoxSizer(VERTICAL)

		topSizer = BoxSizer(HORIZONTAL)

		box_patient = StaticBox(self, label="1. Seleccionar Paciente")
		sizer_patient = StaticBoxSizer(box_patient, VERTICAL)
		self.m_combo_patient = ComboBox(box_patient, style=wx.CB_READONLY)
		sizer_patient.Add(self.m_combo_patient, 0, EXPAND | ALL, 5)

		topSizer.Add(sizer_patient, 1, EXPAND | ALL, 5)

		self.m_btn_diagnose = Button(self, label="2. Realizar Diagnóstico")
		topSizer.Add(self.m_btn_diagnose, 0, EXPAND | ALL, 5)

		mainSizer.Add(topSizer, 0, EXPAND | ALL, 5)

		box_factors = StaticBox(self, label="3. Seleccionar Factores")
		sizer_factors = BoxSizer(HORIZONTAL)

		# Sizer para Signos
		sizer_signs_box = BoxSizer(VERTICAL)
		sizer_signs_box.Add(StaticText(box_factors, label="Signos (Visibles):"), 0, ALL, 5)
		self.m_clb_signs = CheckListBox(box_factors)
		sizer_signs_box.Add(self.m_clb_signs, 1, EXPAND | ALL, 5)

		sizer_symptoms_box = BoxSizer(VERTICAL)
		sizer_symptoms_box.Add(
			StaticText(box_factors, label="Síntomas (Reportados):"), 0, ALL, 5
		)
		self.m_clb_symptoms = CheckListBox(box_factors)
		sizer_symptoms_box.Add(self.m_clb_symptoms, 1, EXPAND | ALL, 5)

		sizer_factors.Add(sizer_signs_box, 1, EXPAND | ALL, 5)
		sizer_factors.Add(sizer_symptoms_box, 1, EXPAND | ALL, 5)

		box_factors.SetSizer(sizer_factors)
		mainSizer.Add(box_factors, 1, EXPAND | ALL, 5)

		box_results = StaticBox(self, label="4. Resultados de Inferencia")
		sizer_results = StaticBoxSizer(box_results, VERTICAL)
		self.m_dvlc_results = DataViewListCtrl(box_results)
		self.m_dvlc_results.AppendTextColumn("Enfermedad", 0, width=200)
		self.m_dvlc_results.AppendProgressColumn("Probabilidad", 1, width=150)
		self.m_dvlc_results.AppendTextColumn("Detalles", 2, width=150)
		sizer_results.Add(self.m_dvlc_results, 1, EXPAND | ALL, 5)

		mainSizer.Add(sizer_results, 1, EXPAND | ALL, 5)

		box_save = StaticBox(self, label="5. Guardar Diagnóstico")
		sizer_save = GridBagSizer(5, 5)

		sizer_save.Add(
			StaticText(box_save, label="Tratamiento:"),
			GBPosition(0, 0),
			flag=ALL | ALIGN_CENTRE_VERTICAL,
		)
		self.m_txt_treatment = TextCtrl(box_save, style=wx.TE_MULTILINE)
		sizer_save.Add(self.m_txt_treatment, GBPosition(0, 1), GBSpan(2, 1), flag=EXPAND | ALL)
		self.m_btn_save = Button(box_save, label="Guardar Diagnóstico")
		sizer_save.Add(self.m_btn_save, GBPosition(1, 0), flag=EXPAND | ALL)
		sizer_save.AddGrowableCol(1)
		sizer_save.AddGrowableRow(0)
		box_save.SetSizer(sizer_save)

		mainSizer.Add(box_save, 0, EXPAND | ALL, 5)

		self.SetSizer(mainSizer)

		self.Bind(EVT_BUTTON, self.OnDiagnose, self.m_btn_diagnose)
		self.Bind(EVT_BUTTON, self.OnSave, self.m_btn_save)

	def GetCurrentUser(self) -> User | None:
		top_level_window = self.GetTopLevelParent()
		if hasattr(top_level_window, "m_current_user"):
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
		self.m_combo_patient.Clear()
		self.m_combo_patient.AppendItems(patient_names)

	def UpdateSignSymptomLists(self):
		self.m_all_signs = get_signs()
		self.m_all_symptoms = get_symptoms()

		sign_names = [s.m_name for s in self.m_all_signs]
		symptom_names = [s.m_name for s in self.m_all_symptoms]

		self.m_clb_signs.Clear()
		self.m_clb_signs.AppendItems(sign_names)
		self.m_clb_symptoms.Clear()
		self.m_clb_symptoms.AppendItems(symptom_names)

		self.m_inference_engine.refresh_knowledge_base()

	def OnDiagnose(self, event: Event):
		selected_sign_indices = self.m_clb_signs.GetCheckedItems()
		selected_symptom_indices = self.m_clb_symptoms.GetCheckedItems()

		patient_sign_ids = set(self.m_all_signs[i].m_id for i in selected_sign_indices)
		patient_symptom_ids = set(
			self.m_all_symptoms[i].m_id for i in selected_symptom_indices
		)

		if not patient_sign_ids and not patient_symptom_ids:
			MessageBox(
				"Seleccione al menos un signo o síntoma.", "Error", ICON_ERROR | OK
			)
			return

		results = self.m_inference_engine.diagnose(
			patient_sign_ids, patient_symptom_ids
		)

		self.m_dvlc_results.DeleteAllItems()
		if not results:
			MessageBox(
				"No se encontraron coincidencias.", "Info", ICON_INFORMATION | OK
			)
			return

		for res in results:
			item_data = res["disease_id"]
			score_percent = int(res["score"] * 100)
			self.m_dvlc_results.AppendItem(
				[res["disease_name"], score_percent, res["details"]], data=item_data
			)

	def OnSave(self, event: Event):
		user = self.GetCurrentUser()

		patient_idx = self.m_combo_patient.GetSelection()
		if patient_idx == NOT_FOUND:
			MessageBox("Seleccione un paciente.", "Error", ICON_ERROR | OK)
			return

		selected_row = self.m_dvlc_results.GetSelectedRow()
		if selected_row == NOT_FOUND:
			MessageBox(
				"Seleccione una enfermedad de la lista de resultados.",
				"Error",
				ICON_ERROR | OK,
			)
			return
		
		selected_item_object = self.m_dvlc_results.RowToItem(selected_row)

		if not (user and user.is_medic()):
			MessageBox("Error de usuario. No se puede guardar.", "Error", ICON_ERROR | OK)
			return

		patient_id = self.m_all_patients[patient_idx].m_id
		enfermedad_id = self.m_dvlc_results.GetItemData(selected_item_object)
		medic_id = user.m_role
		tratamiento = self.m_txt_treatment.GetValue()

		diag = Diagnostico(
			paciente_id=patient_id,
			medico_id=medic_id,
			enfermedad_id=enfermedad_id,
			tratamiento=tratamiento,
		)
		diag.insert()

		MessageBox("Diagnóstico guardado exitosamente.", "Éxito", ICON_INFORMATION | OK)

		self.m_txt_treatment.Clear()
		self.m_dvlc_results.DeleteAllItems()
		self.m_clb_signs.SetCheckedItems([])
		self.m_clb_symptoms.SetCheckedItems([])
		self.m_combo_patient.SetSelection(NOT_FOUND)