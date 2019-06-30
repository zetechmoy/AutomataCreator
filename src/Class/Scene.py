from Class.State import State
from PyQt5.QtWidgets import QGraphicsScene


##This is a custom QGraphicsScene
class Scene(QGraphicsScene):

	##Init stuff
	def __init__(self, window):
		super().__init__()
		self.window = window
		self.selection_mode_transition = False
		self.copiedItems=[]
		self.pressed=False

	##Handle mouse event
	##@param event the handled event
	def mousePressEvent(self, event):
		if self.pressed:
			p=event.buttonDownScenePos(event.button())
			self.window.makenewstate(pos=p)
			print("pressed")
		super().mousePressEvent(event)
		if self.selection_mode_transition :
			self.window.manage_transition_mode()


	def stateSelected(self):
		selected=[]
		for item in self.selectedItems():
			if(isinstance(item,State)):
				selected.append(item)
		return selected

	## Remove all items on the scene
	def clears(self):
		while (self.items() != []) :
			self.removeItem(self.items()[0])

	##Set the mode of transition
	##@param select The transition mode
	def setSelectionModeTransition(self,select):
		self.selection_mode_transition = select

	##Get the mode of transition
	##@return The transition mode
	def getSelectionModeTransition(self):
		return self.selection_mode_transition

	##Get the mode of transition
	##@return The transition mode
	def getPressed(self):
		return self.pressed

	##Set the mode of State
	##@param select The State mode
	def setPressed(self,pressed):
		self.pressed=pressed
