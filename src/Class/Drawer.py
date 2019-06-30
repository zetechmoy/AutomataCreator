from Class.IO import IO
from Class.Transition import Transition
from Class.State import State
from Class.mozia import MOZIA
from Class.Gen import Gen
from Class.VectorTools import VectorTools

from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen, QDrag, QPalette, QImage, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QWidget, QAction, QFrame, QLabel, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, QSize, QPointF

##Class which handle the automata draw
class Drawer:

	##Init stuff
	def __init__(self, scene, painter):

		self.label = "nouvelle_tomate"

		#zoomfactor
		self.zoom = 1

		#List of states
		self.states = []

		#List of transitions
		self.transitions = []

		#To manage project
		self.manager = IO(self)

		#To set states and transitions ids
		self.ids = 0 #states
		self.idt= 0 #transitions

		#To draw things
		self.scene = scene
		self.painter = painter
		self.score = 0.0

		self.mozia = MOZIA()
		self.vect = VectorTools()

	##Add State
	##@param preview boolean which says if the state contains latex (to preview) or not
	##@param magnet boolean which says if the State is magnetized of not
	##@return the added state
	def addState(self, id = -1, label = "", radius = 50, color = (0, 0, 0), background_color = (255, 255, 255), contour = "simple", preview=False, magnet=False, pos=QPointF(0,0)):
		if id==-1:
			id=self.ids
		new_state = State(id, label, radius, color, background_color, contour, preview, magnet,pos)
		self.scene.addItem(new_state)

		new_state.showInfos()
		self.states.append(new_state)

		self.ids += 1
		return new_state

	##Set name of selected states
	##@param label string which is the name of states
	def setStateLabel(self, label):
		for item in self.scene.selectedItems():
				item.setLabel(label)

	##Set radius of selected states
	##@param radius int which is the new radius of states
	def setRadiusSelected(self, radius):
		for item in self.scene.selectedItems():
				if(isinstance(item, State)):
					item.setRadius(radius)

	##Set to initial the selected items
	def setInitialSelected(self):
		for item in self.scene.selectedItems():
				if(isinstance(item, State)):
					item.setInitial()

	##Set to final the selected items
	def setFinalSelected(self):
		for item in self.scene.selectedItems():
				if(isinstance(item, State)):
					item.setFinal()

	##Delete selected items
	def deleteSelected(self):
		for item in self.scene.selectedItems():
			if isinstance(item, State):
				self.delState(item)
			# elif isinstance(item, Transition):
			# 	self.delTransition(item)

	##Delete a state
	##@param state The state to delete
	def delState(self, state):
		if (state in self.states):
			#print("-- my transitions are : ",[t.getId() for t in state.transitions])
			while state.getTransitions()!=[]:
				self.delTransition(state.getTransitions()[0])
			self.states.remove(state)
			self.scene.removeItem(state)
		#else:
		#	print("State already deleted")

	##Delete a transition
	##@param transition The transition to delete
	def delTransition(self, transition):
		if(transition in self.transitions):
			#print("deleting transition : ", transition.getId())
			if transition.src != transition.dest:
				if(transition.dest in self.states):
					transition.dest.removeTransition(transition)
				if(transition.src in self.states):
					transition.src.removeTransition(transition)
			else:
				if(transition.dest in self.states):
					transition.dest.removeTransition(transition)
			self.transitions.remove(transition)
			self.scene.removeItem(transition)
		#else :
		#	print("transition already deleted.")

	##Add a transition between n1 and n2
	##@param n1 The src State
	##@param n2 The dst State
	##@param preview Does is have a formula in his label ?
	##@return added transition
	def addTransition(self, n1, n2, id=-1, label = "", color = (0, 0, 0), height = 0, preview=False, dx=0, dy=0):
		for t in self.transitions :
			if(t.src == n1 and t.dest == n2):
				#print("THIS TRANSITION ALREADY EXISTS")
				return
		if id==-1:
			id=self.idt
		new_transition = Transition(self.idt, src=n1, dest=n2, preview=preview, dx=dx, dy=dy)
		self.scene.addItem(new_transition)
		if not new_transition in n1.transitions:
			n1.transitions.append(new_transition)
		if(n1!=n2 and not new_transition in n2.transitions):
			n2.transitions.append(new_transition)
		self.transitions.append(new_transition)
		self.idt +=1
		new_transition.showInfos()
		return new_transition

	##Set to straight selected transition
	def straightSelected(self):
		for item in self.scene.selectedItems():
			if isinstance(item, Transition):
				item.setStraight()

	##Call for the Genetic Algorithm
	def autoPosition(self):
		mygen = Gen()
		mygen.load(self)
		mygen.autoPosition()

	## Remove all states and transitions from this drawer and his scene.
	def clears(self):
		self.states.clear()
		self.transitions.clear()
		self.scene.clears()

	##Save the current automata
	##@param output_file_name The path of the .otmt file
	def save(self, output_file_name, verbose=False):
		self.manager.save(output_file_name, verbose)

	##Load a model from a .otmt file
	##@param input_file_name The path of the .otmt file
	def load(self, input_file_name):
		self.manager.load(input_file_name)

	##Export the current automata to LaTeX
	def export(self, output_file_name):
		self.manager.export(output_file_name)

	##Set name of the current automata Project
	##@param label Name of the project
	def setLabel(self, label):
		self.label = label

	##Reset the automata
	def reset(self):
		self.clears()
		self.states = []
		self.transitions = []
		self.ids = 0
		self.idt = 0

	##What about having all states of the Project ?
	##@return states of the project
	def getStates(self):
		return self.states

	##What about having all transitions of the Project ?
	##@return transitions of the project
	def getTransitions(self):
		return self.transitions

	##Show infos of the current automata
	def showInfos(self):
		print("label : "+str(self.label))
		print("states len : "+str(len(self.states)))
		print("ids : "+str(self.ids))
		print("idt : "+str(self.idt))
		for state in self.states:
			state.showInfos()

	##Get number of states
	def getNumberState(self):
		return len(self.states)

		for transition in self.transitions:
			transition.showInfos()

	##Call for the Automatic Replacement with MozIA
	##@param states States to replace
	def aiAlignStates(self, states):
		new_points = self.mozia.moveStates(states)
		for i in range(0, len(states)):
			states[i].setPos(new_points[i][0], new_points[i][1])
			for transition in states[i].getTransitions():
				transition.setStraight()

	##Get the current scene
	##@return The scene
	def getScene(self):
		return self.scene
