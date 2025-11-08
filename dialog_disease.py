from wx import (
	ALIGN_CENTRE_HORIZONTAL,
	ALIGN_CENTRE_VERTICAL,
	ALL,
	EVT_BUTTON,
	EXPAND,
	ID_CANCEL,
	ID_OK,
	RIGHT,
	BoxSizer,
	Button,
	CommandEvent,
	DefaultPosition,
	DefaultSpan,
	Dialog,
	ID_ANY,
	GBPosition,
	GBSpan,
	GridBagSizer,
	Size,
	StaticText,
	TextCtrl,
	Window,
	CheckListBox,
	StaticBox,
	StaticBoxSizer,
	VERTICAL
)


from disease import Disease
from sign import get_signs, Sign
from symptom import get_symptoms, Symptom


class DialogDisease(Dialog):
	
	m_all_signs: list[Sign] = []
	m_all_symptoms: list[Symptom] = []

	def __init__(self, parent: Window):
		super().__init__(parent, ID_ANY, "Agregar Enfermedad")

		#Sizers
		gbSizer = GridBagSizer(5, 5)
		buttonSizer = BoxSizer()
		
		#Controles
		self.m_textCtrl_name = TextCtrl(
			self, ID_ANY, "", DefaultPosition, Size(250, -1)
		)
		
		#Obtener Signos y Síntomas
		self.m_all_signs = get_signs()
		self.m_all_symptoms = get_symptoms()
		
		sign_names = [s.m_name for s in self.m_all_signs]
		symptom_names = [s.m_name for s in self.m_all_symptoms]
		
		#CheckListBoxes
		box_signs = StaticBox(self, label="Signos (Visibles)")
		sizer_signs = StaticBoxSizer(box_signs, VERTICAL)
		self.m_clb_signs = CheckListBox(self, choices=sign_names)
		sizer_signs.Add(self.m_clb_signs, 1, EXPAND | ALL, 5)
		
		box_symptoms = StaticBox(self, label="Síntomas (No visibles)")
		sizer_symptoms = StaticBoxSizer(box_symptoms, VERTICAL)
		self.m_clb_symptoms = CheckListBox(self, choices=symptom_names)
		sizer_symptoms.Add(self.m_clb_symptoms, 1, EXPAND | ALL, 5)
		
		#Botones
		self.m_button_ok = Button(self, ID_ANY, "Agregar")
		self.m_button_cancel = Button(self, ID_ANY, "Cancelar")
		buttonSizer.Add(self.m_button_ok, 0, RIGHT, 10)
		buttonSizer.Add(self.m_button_cancel)

		#Layou
		gbSizer.Add(
			StaticText(self, ID_ANY, "Nombre:"),
			GBPosition(0, 0),
			DefaultSpan,
			ALL | ALIGN_CENTRE_VERTICAL,
			5,
		)
		gbSizer.Add(
			self.m_textCtrl_name, GBPosition(0, 1), GBSpan(1, 2), EXPAND | ALL, 5
		)
		
		gbSizer.Add(
			sizer_signs,
			GBPosition(1, 0),
			GBSpan(1, 1),
			EXPAND | ALL,
			5
		)
		gbSizer.Add(
			sizer_symptoms,
			GBPosition(1, 1),
			GBSpan(1, 1),
			EXPAND | ALL,
			5
		)
		
		gbSizer.Add(
			buttonSizer,
			GBPosition(2, 0),
			GBSpan(1, 2),
			EXPAND | ALL | ALIGN_CENTRE_HORIZONTAL,
			5,
		)
		
		gbSizer.AddGrowableRow(1)
		gbSizer.AddGrowableCol(0)
		gbSizer.AddGrowableCol(1)

		self.SetSizerAndFit(gbSizer)
		self.SetSize(500, 400)
		self.CenterOnParent()

		self.Bind(EVT_BUTTON, self.OnButtonClick)

	def OnButtonClick(self, event: CommandEvent):
		if event.GetId() == self.m_button_ok.GetId():
			name = self.m_textCtrl_name.GetValue()
			if not name:
				return

			selected_sign_indices = self.m_clb_signs.GetCheckedItems()
			selected_symptom_indices = self.m_clb_symptoms.GetCheckedItems()
			
			selected_sign_ids = [self.m_all_signs[i].m_id for i in selected_sign_indices]
			selected_symptom_ids = [self.m_all_symptoms[i].m_id for i in selected_symptom_indices]

			disease = Disease(0, name)

			if disease:
				disease.insert_with_relations(selected_sign_ids, selected_symptom_ids)
				self.EndModal(ID_OK)

		if event.GetId() == self.m_button_cancel.GetId():
			self.EndModal(ID_CANCEL)

		event.Skip()