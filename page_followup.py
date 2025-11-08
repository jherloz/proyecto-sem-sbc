import wx
from wx import (
	Panel,
	Window,
	BoxSizer,
	Button,
	EVT_BUTTON,
	VERTICAL,
	ALL,
	EXPAND,
	Event,
)

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

from diagnostico import get_graph_data

class PageFollowup(Panel):
	def __init__(self, parent: Window):
		super().__init__(parent)
		
		sizer = BoxSizer(VERTICAL)
		
		self.m_btn_refresh = Button(self, label="Actualizar Gráfica")
		
		self.figure = Figure()
		self.axes = self.figure.add_subplot(111)
		self.canvas = FigureCanvas(self, -1, self.figure)
		
		sizer.Add(self.m_btn_refresh, 0, ALL, 5)
		sizer.Add(self.canvas, 1, EXPAND | ALL, 5)
		
		self.SetSizer(sizer)
		
		self.Bind(EVT_BUTTON, self.OnRefresh, self.m_btn_refresh)

	def OnRefresh(self, event: Event | None):
		"""Obtiene los datos y dibuja la gráfica."""
		
		data = get_graph_data()
		
		if not data:
			self.axes.clear()
			self.axes.text(0.5, 0.5, "No hay datos de diagnóstico para mostrar.", 
						   horizontalalignment='center', verticalalignment='center',
						   transform=self.axes.transAxes)
			self.canvas.draw()
			return
			
		labels = list(data.keys())
		values = list(data.values())
		
		self.axes.clear()
		self.axes.bar(labels, values)
		
		self.axes.set_ylabel("Cantidad de Diagnósticos")
		self.axes.set_title("Frecuencia de Enfermedades Diagnosticadas")
		self.figure.autofmt_xdate(rotation=45) # Gira las etiquetas si son muchas
		
		self.canvas.draw()