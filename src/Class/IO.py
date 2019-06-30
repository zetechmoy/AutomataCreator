import json
from math import *
from Class.State import State
from Class.Transition import Transition
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QLineF, QPointF

##Class which handle Input and Output
class IO:

	##Init stuff
	def __init__(self, drawer):

		self.drawer = drawer
		self.formats = "OTomate File (*.otmt)"
		self.format_extension = "otmt" # file.otmt


	##Load a project and fill the current drawer
	##@param input_file_name
	def load(self, input_file_name):
		file = open(input_file_name, "r")
		json_str = file.read()
		file.close()
		print(json_str)
		jid = json.loads(json_str)

		self.drawer.reset()

		self.drawer.label = jid["label"]
		self.drawer.ids = jid["ids"]
		self.drawer.idt = jid["idt"]
		for state_json in jid["states"]:
			state = self.jsonToState(state_json)
			if not self.stateIsInDrawer(state):
				s=self.drawer.addState(id=state.getId(),label=state.getLabel(),radius=state.getRadius())
				s.setPosition(state.x(), state.y())

		for transition_json in jid["transitions"]:
			transition = self.jsonToTransition(transition_json)

			if not self.stateIsInDrawer(transition.src):
				s=self.drawer.addState(id=transition.src.getId(),label=transition.src.getLabel(),radius=transition.src.getRadius())
				print("On a rien a foutre là")
			else:
				for s in self.drawer.states :
					if self.compareStates(s, transition.src):
						transition.setSrc(s)

			if not self.stateIsInDrawer(transition.dest):
				self.drawer.addState(id=transition.dest.getId(),label=transition.dest.getLabel(),radius=transition.dest.getRadius())
				print("On a rien a foutre là")
			else:
				for s in self.drawer.states :
					if self.compareStates(s, transition.dest):
						transition.setDest(s)

			add_transition = True
			for t in self.drawer.transitions :
				if(t.src == transition.src and t.dest == transition.dest):
					print("THIS TRANSITION ALREADY EXISTS")
					add_transition = False
			if(add_transition):
				self.drawer.addTransition(transition.getSrc(), transition.getDest(), id=transition.getId(),label=transition.getLabel(),dx=transition.getInflection_dx(),dy=transition.getInflection_dy())


		#self.drawer.showInfos()

	##Save a project to a file
	##@param output_file_name The path of the file to save the project
	##@param verbose Do you want to have all details ?
	def save(self, output_file_name, verbose):
		json_output_drawer = {
			"label" : self.drawer.label,
			"states" : [],
			"transitions" : [],
			"ids" : self.drawer.ids,
			"idt" : self.drawer.idt
		}

		for state in self.drawer.states:
			json_output_drawer['states'].append(self.stateToJson(state))

		for transition in self.drawer.transitions:
			json_output_drawer['transitions'].append(self.transitionToJson(transition))

		file = open(output_file_name, "a+")
		file.truncate(0) #erase everything
		file.seek(0) #cursor at the begining
		if verbose : print(json_output_drawer)
		file.write(json.dumps(json_output_drawer, sort_keys=True, indent=4, separators=(',', ': ')))
		file.close()

	def to_deg(self,a):
		return a * 180 / math.pi

	def get_angle(self,A,B,dI):
		C = [(A.x()+B.x())/2,(A.y()+B.y())/2]
		I = QPointF(C[0]+dI[0],C[1]+dI[1])
		# AI = [I[0]-A.x(),I[1]-A.y()]
		# BI = [I[0]-B.x(),I[1]-B.y()]
		# AB = [B.x()-A.x(),B.y()-A.y()]
		#
		# ##angle(AB = [1,0],AB)
		# if math.sqrt(AB[0]**2+AB[1]**2) != 0:
		# 	alpha = math.acos(AB[0]/math.sqrt(AB[0]**2+AB[1]**2))
		# alpha = int(self.to_deg(angles[0]))
		#
		# ##angle(AC = [1,0],AI)
		# if math.sqrt(AI[0]**2+AI[1]**2) != 0:
		# 	angles[0] = math.acos(AI[0]/math.sqrt(AI[0]**2+AI[1]**2))
		# angles[0] = int(self.to_deg(angles[0]))
		#
		#
		# ##angle(BC,BI)
		# if math.sqrt(BI[0]**2+BI[1]**2) != 0:
		# 	angles[1] = math.acos(BI[0]/math.sqrt(BI[0]**2+BI[1]**2))
		# angles[1] = int(self.to_deg(angles[1]))

		alpha = QLineF(A.x(), A.y(),I.x(), I.y()).angle()
		beta = QLineF(I.x(), I.y(),B.x(), B.y()).angle()
		angles = [-alpha,180-beta]
		return angles




	def export(self,  latex_file_name):
		"""Export project to LaTex"""
		json_latex = {
			"label" : self.drawer.label,
			"states" : [],
			"transitions" : []}

		for state in self.drawer.states:
			json_latex['states'].append(state)

		for transition in self.drawer.transitions:
			json_latex['transitions'].append(transition)

		file = open(latex_file_name, 'w')
		file.truncate(0)	#erase everything
		file.seek(0)		#cursor at the begining

		##head
		file.write("\\documentclass{article}\n")
		file.write("\\usepackage{tikz}\n")
		file.write("\\usetikzlibrary{arrows,automata}\n")
		file.write("\\begin{document}\n")
		file.write("\\begin{tikzpicture} [->,>=stealth',auto, semithick]\n\n")

		##states
		for state in json_latex["states"]:
			t = ''
			if state.isinitial: #etat "debut"
				t = ',initial'
			elif state.isfinal: #etat "final"
				t = ',accepting'

			file.write("\\node[state"+ t +"] ")
			file.write("(q"+str(state.getId())+") ")
			file.write("at ("+ str(state.getPosition().x()/100) +","+str(-state.getPosition().y()/100) + ") {$ ")
			if len(state.getLabel()) != 0:
				file.write(state.getLabel())
			file.write("$};\n")
		file.write("\n")

		##transitions
		for transition in json_latex["transitions"]:
			file.write("\\draw (q"+str(transition.getSrc().getId())+") edge ")
			if not (transition.getInflection_dx() == transition.getInflection_dy() == 0):
				A = QPointF(transition.getSrc().x(),-transition.getSrc().y())
				B = QPointF(transition.getDest().x(),-transition.getDest().y())
				dI =[transition.getInflection_dx(),-transition.getInflection_dy()]
				if(transition.getSrc()==transition.getDest()):
					dx=dI[0]
					dy=dI[1]
					m = max(abs(dx),abs(dy))
					if(m==abs(dx)):
						if(dx>0):
							side="right"
						else:
							side="left"
					else:
						if(dy>0):
							side="above"
						else:
							side="below"
					file.write("[loop "+side+"] ")
				else:
					angles = self.get_angle(A,B,dI)
					file.write("[out="+str(angles[0])+",in="+str(angles[1])+"] ")
			file.write("node ")
			file.write("{$ ")
			if len(transition.getLabel()) != 0:
				file.write(transition.getLabel())
			file.write("$} ")
			file.write("(q"+str(transition.getDest().getId())+");\n")
		file.write(";\n\n")

		##bottom
		file.write("\\end{tikzpicture}\n")
		file.write("\\end{document}\n")
		file.close()


	##Convert a jsonStateStructure to a real state
	##@param state_json The json of the state to create
	##@return The new State
	def jsonToState(self, state_json):
		n = State(state_json["id"])
		n.setLabel(label = state_json["label"])
		n.setRadius(radius = state_json["radius"])
		n.setColor(color = tuple(state_json["color"]))
		n.setBackgroundColor(color=tuple(state_json["background_color"]))
		n.setContour(state_json["contour"])
		n.setPosition(state_json["pos"][0], state_json["pos"][1])
		n.isfinal = state_json["final"]
		n.isinitial = state_json["initial"]
		return n

	##Convert a jsonTransitionStructure to a real Transition
	##@param transition_json The json of the Transition to create
	##@return The new Transition
	def jsonToTransition(self, transition_json):
		print(transition_json["src"])
		l = Transition(transition_json["id"])
		l.setLabel(transition_json["label"])
		l.setColor(tuple(transition_json["color"]))
		l.setSrc(self.jsonToState(transition_json["src"]),inscription=False)
		l.setDest(self.jsonToState(transition_json["dest"]),inscription=False)
		l.setHeight(transition_json["height"])
		l.setInflection_dx(transition_json["inflection_dx"])
		l.setInflection_dy(transition_json["inflection_dy"])
		return l

	##Convert a State object to json
	##@param state State to Convert
	##@return The Json of the State
	def stateToJson(self, state):
		print(state.pos())
		return {
				"id" : state.id,
				"label" : state.label,
				"radius" : state.radius,
				"pos" : [state.pos().x(), state.pos().y()],
				"color" : list(state.color),
				"background_color" : list(state.background_color),
				"contour" : state.contour,
				"final" : state.isfinal,
				"initial" : state.isinitial
			}

	##Convert a Transition object to json
	##@param state Transition to Convert
	##@return The Json of the Transition
	def transitionToJson(self, transition):
		return 	{
				"id" : transition.id,
				"label" : transition.label,
				"color" : list(transition.color),
				"src" : self.stateToJson(transition.src),
				"dest" : self.stateToJson(transition.dest),
				"height" : transition.height,
				"inflection_dx" : transition.inflection_dx,
				"inflection_dy" : transition.inflection_dy
				#"inflection" : transition.inflection_point
			}

	##Whether the state is in the drawer
	##@param state The state to check
	##@return if the state is in the drawer
	def stateIsInDrawer(self, state):
		for s in self.drawer.states:
			if self.compareStates(s, state):
				return True
		return False

	##Check if two states are the same
	##@param state1 The first state1
	##@param state2 The first state2
	##@return True if state1 = state2
	def compareStates(self, state1, state2):
		if isinstance(state1, State) and isinstance(state2, State):
			return state1.id == state2.id
		else:
			return False
