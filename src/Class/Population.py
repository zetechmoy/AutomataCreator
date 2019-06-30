from Class.State import State
from Class.Transition import Transition
from math import sqrt, floor
import random
from PyQt5.QtWidgets import QGraphicsItem

## This class modelizes an automata and is used in the genetic algorithm.
class Population:
	def __init__(self,id,drawer):
		self.id=id
		self.states=dict()
		self.transitions=dict()
		self.score=0
		self.drawer=drawer
		self.uptodate=False
		#print("Creation de la population",self.id)

	## Add a real state to this population.
	## @param state State A real state.
	def addRealState(self, state):
		infos_state={'id': state.getId(), 'x': state.getPosition().x(), 'y': state.getPosition().y()}
		self.states[int(infos_state['id'])]=infos_state
		self.uptodate=False

	## Add a modelized state to this population.
	## @param id int State ID.
	## @param x int x coordinates.
	## @param y int y coordinates.
	def addState(self,x,y,id):
		infos_state={'id': id, 'x': x, 'y': y}
		self.states[int(infos_state['id'])]=infos_state
		self.uptodate=False

	## Add a real transition to this population. You should have added every State involved before adding Transitions.
	## @param trans Transition A real transition
	def addRealTransition(self, trans):
		infos_trans={'id': trans.getId(), 'id_src': trans.getSrc().getId(), 'id_dest': trans.getDest().getId(), 'inflection_dx': trans.getInflectionPoint()[0], 'inflection_dy': trans.getInflectionPoint()[1]}
		self.transitions[int(infos_trans['id'])]=infos_trans
		self.uptodate=False

	## Add a modelized transition to this population. You should have added every State involved before adding Transitions.
	## @param id int Transition ID.
	## @param id_src int Source state id.
	## @param id_dest int Destination state id.
	## @param inflection_dx int Inflection dx.
	## @param inflection_dy int Inflection dy.
	def addTranstion(self,id,id_src,id_dest,inflection_dx,inflection_dy):
		infos_trans={'id': id, 'id_src': id_src, 'id_dest': id_dest, 'inflection_dx': inflection_dx, 'inflection_dy': inflection_dy}
		self.transitions[int(infos_trans['id'])]=infos_trans
		self.uptodate=False

	## Load a population into our program.
	## This will not work if you deleted a state or a transition in the program.
	def export_pop(self):
		for s in self.drawer.getStates():
			id=s.getId()
			s.setPosition(self.states[id]['x'],self.states[id]['y'])
		for t in self.drawer.getTransitions():
			id=t.getId()
			t.setInflectionPoint(self.transitions[id]['inflection_dx'],self.transitions[id]['inflection_dy'])

	## Score calculation method.
	## This method generate a score based on collision's quantity.
	## This method will also test if transitions are better straight or the way they are and set them accordingly.
	def calc_score(self): # à modifier, changement de fonctionnement
		moyenne=0
		test=0  # TO BE REMOVED
		self.uptodate=True
		self.export_pop()
		self.score=0
		#Calc nombre croisements + avec les states ! On retire 200 au score par collision (100 * 2)
		for trans in self.drawer.transitions :
			# On modifie la transition : l'objectif est de tester si le fait de mettre une transition "droite" a un impact ou non. S'il n'y en a pas ou que c'est mieux, on change
			if trans.getInflection_dx() !=0 or trans.getInflection_dy()!=0:
				temp=len(trans.collidingItems())
				trans.setStraight()
				if len(trans.collidingItems()) <= temp:
					self.transitions[trans.getId()].update({'inflection_dx':0})
					self.transitions[trans.getId()].update({'inflection_dy':0})
				else:
					trans.setInflection_dx(self.transitions[trans.getId()].get('inflection_dx'))
					trans.setInflection_dy(self.transitions[trans.getId()].get('inflection_dy'))
			for crois in trans.collidingItems():
				if isinstance(crois,Transition):
					self.score-=50
					test+=0.5
				if isinstance(crois,State) and crois.getId() != trans.getSrc().getId() and crois.getId() != trans.getDest().getId():
					self.score-=200
					test+=1
			# 	self.score-=abs(trans.getLength()-(trans.getSrc().distanceTo(trans.getDest())-trans.getSrc().getRadius()-trans.getDest().getRadius()))/50
			# self.score-=(abs(trans.getInflection_dx())+abs(trans.getInflection_dy()))/10
		#Nombre de croisements entre states. -4 par croisement
		meilleure_dist=0
		for st in self.drawer.states:
			for crois in st.collidingItems():
				if isinstance(crois,State):
					self.score-=200
					test+=0.5
			for st2 in self.drawer.states:
			 	if st.getId() != st2.getId():
			 		if meilleure_dist == 0:
			 			meilleure_dist = st.distanceTo(st2)
			 		else:
			 			meilleure_dist= min(st.distanceTo(st2),meilleure_dist)
			self.score-=abs(meilleure_dist-3*st.getRadius())
	# Calc distances et "écart type" peut être si c'est nécessaire


	## Generate a fully random population based on this population.
	## @param popid int Id of the population to generate.
	## @return The generated population.
	def gen_random_pop(self,popid):
		new_pop = Population(popid,self.drawer)
		#print("Generating population",popid)
		hauteur2=floor(self.drawer.getScene().height()/2)-100
		largeur2=floor(self.drawer.getScene().width()/2)-100
		for s in self.states.values():
			 new_pop.addState(random.randrange(-largeur2,largeur2,1),random.randrange(-hauteur2,hauteur2,1),s.get("id"))
		for trans in self.transitions.values():
			# WE SHOULD UPDATE THAT
			new_pop.addTranstion(trans.get('id'),trans.get('id_src'),trans.get('id_dest'),random.randrange(-500,500,1),random.randrange(-500,500,1))
		return new_pop

	## Generate a new population based on himself and another population. It also randomly introduce some mutations.
	## @param other_pop Population The other population used to generate.
	## @param id int Id of the population to generate.
	## @return The generated population.
	def croisements_mutations(self,other_pop,id):
		new_pop=Population(id,self.drawer)
		hauteur2=floor(self.drawer.getScene().height()/2)-100
		largeur2=floor(self.drawer.getScene().width()/2)-100
		for s in self.states.values():
			# Gestion des x
			r=random.randint(0,105)
			if(r>=100):
				#mutation : proba de - de 1%
				x=random.randrange(-largeur2,largeur2,1) #Should probably be changed
			elif(r<50): #pos x
				x=s.get('x')
			else:
				x=other_pop.getState(s.get('id')).get('x')
			# Gestion des y
			r=random.randint(0,105)
			if(r>=100):
				#mutation : proba de - de 1%
				y=random.randrange(-hauteur2,hauteur2,1) #Should probably be changed
			elif(r<50): #pos y
				y=s.get('y')
			else:
				y=other_pop.getState(s.get('id')).get('y')
			new_pop.addState(x,y,s.get('id'))
		for t in self.transitions.values():
			if t.get('inflection_dx') == 0 and t.get('inflection_dy')==0:
				if random.randint(0,20)<=1:
					dx=random.randrange(-500,500,1)
					dy=random.randrange(-500,500,1)
				else:
					dx=0
					dy=0
			else:
				#gestion des inflection_dx
				r=random.randint(0,105)
				if(r>=100):
					#mutation : proba de - de 1%
					dx=random.randrange(-500,500,1) #Should probably be changed
				elif(r<50): #pos x
					dx=t.get('inflection_dx')
				else:
					dx=other_pop.getTransitions(t.get('id')).get('inflection_dx')
				#gestion des inflection_dy
				r=random.randint(0,105)
				if(r>=100):
					#mutation : proba de - de 1%
					dy=random.randrange(-500,500,1) #Should probably be changed
				elif(r<50): #pos x
					dy=t.get('inflection_dy')
				else:
					dy=other_pop.getTransitions(t.get('id')).get('inflection_dy')
			new_pop.addTranstion(t.get('id'),t.get('id_src'),t.get('id_dest'),dx,dy)
		return new_pop

	## Returns Id of this Population.
	## @return id
	def getId(self):
		return self.id

	## Returns a list of modelized state in this Population.
	## @return modelized states list
	def getState(self,id):
		return self.states[id]

	## Returns a list of modelized transition in this Population.
	## @return modelized transition list
	def getTransitions(self,id):
		return self.transitions[id]

	## Returns this Population's score. If it has not been calculated, it calls self.calc_score().
	## @return int score
	def getScore(self):
		if not self.uptodate:
			self.calc_score()
		return self.score
