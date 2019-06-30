from Class.State import State
from Class.Transition import Transition
from Class.Population import Population
from math import sqrt
from PyQt5.QtWidgets import QGraphicsItem, QProgressDialog
from numpy.random import choice, shuffle
from numpy import append
from random import randint,sample

## This class manages the Genetic Algorithm and the different populations.
class Gen:
	def __init__(self):
		self.population_initiale=None
		self.populations = []
		self.nb_pop=0
		self.id=0
		self.nb_initial_generations=300

	## Load the actual automata in initial Population.
	## @param drawer Drawer The drawer containing the automata.
	def load(self, drawer):
		print("Loading original population...")
		self.population_initiale=Population(-1,drawer)
		self.populations.clear()
		self.nb_pop=0
		for s in drawer.getStates():
			self.population_initiale.addRealState(s)
		for t in drawer.getTransitions():
			self.population_initiale.addRealTransition(t)
		print("Le score de la population intiale est :",self.population_initiale.getScore())

	## Generate nb_initial_generations Populations randomly based on the initial population.
	def generate_first_pop(self):
		print("Generating firsts populations...")
		for i in range(self.nb_pop,self.nb_pop+self.nb_initial_generations):
			self.populations.append(self.population_initiale.gen_random_pop(self.id))
			self.id+=1
		self.nb_pop+=self.nb_initial_generations

	## Load the Population with the bestScore.
	def bestScore(self):
		score_max=self.populations[0].getScore()
		max=self.populations[0]

		for p in self.populations:
			if(p.getScore()>score_max):
				max=p
				score_max=p.getScore()
		print("The max score is pop",max.getId(),"with score", max.getScore())
		max.export_pop()

	## Evaluate populations, randomly select the populations meant to survive and make some mutations.
	def genetic(self):
		scores=[]
		somme_scores=0
		max_score=self.populations[0].getScore()
		min_score=0
		nb=0
		best_pop=None
		# Looking for max and min score.
		for p in self.populations:
			scores.append(p.getScore())
			if(p.getScore()<min_score):
				min_score=p.getScore()
			somme_scores+=p.getScore()
			if(p.getScore()>max_score):
				best_pop=p
				max_score=p.getScore()
			nb+=1
		#Preparing score balacing.
		for i in range(len(scores)):
			scores[i]=(scores[i]+abs(min_score))/(somme_scores+nb*abs(min_score))
		# Selecting
		echantillon = choice(self.populations,self.nb_pop//2,False,scores)
		self.nb_pop=self.nb_pop//2
		# If we didn't select the best Population, we add it to the sample.
		if best_pop not in echantillon:
			append(echantillon,best_pop)
			self.nb_pop+=1
		croisement=None
		# Suppression des éléments non séléctionnés
		for p in self.populations:
			if p not in echantillon:
				self.populations.remove(p)
		self.populations=sample(self.populations,self.nb_pop) # Shuffles populations
		population_temp=[]
		# Random cross-breeding. Two parents generate two childs.
		for p in self.populations:
			if croisement==None:
				croisement=p # Stock previous population
			else :
				pop1=p.croisements_mutations(croisement,self.id)
				pop2=croisement.croisements_mutations(p,self.id+1)
				population_temp.append(pop1)
				population_temp.append(pop2)
				self.id+=2
				self.nb_pop+=2
				croisement=None
		# We add the new populations to the list
		for p in population_temp:
			self.populations.append(p)

	## This function is the one to call if you want to use this code. You should use load() before.
	## It is basically genetic algorithm's manager.
	def autoPosition(self):
		if self.population_initiale != None:
			nb_iterations=100
			self.generate_first_pop()
			loading = QProgressDialog("Generating Populations...",None,0,100)
			loading.setWindowTitle("O'TomateMozzarella")
			loading.forceShow()
			loading.open()
			loading.setValue(0)
			for i in range(nb_iterations):
				self.genetic()
				loading.setValue((i/nb_iterations)*100)
				self.bestScore()
		else:
			print("You should load the base population before calling autoPosition")
