import sys, os
from keras.models import load_model
import numpy as np
import math
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from Class.AI.DatasetManager import DatasetManager
from VectorTools import VectorTools

from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import Qt

class MOZIA(object):
	"""docstring for MOZIA."""
	def __init__(self):

		self.dm = DatasetManager()

		self.model_names = [
		"Class/AI/models/otmt_3states_1000_lstmv4.h5",
		"Class/AI/models/otmt_4states_1000_lstmv4.h5",
		"Class/AI/models/otmt_5states_1000_lstmv4.h5",
		"Class/AI/models/otmt_6states_1000_lstmv4.h5"
		#"Class/AI/models/otmt_7states_1000_lstmv4.h5",
		#"Class/AI/models/otmt_8states_1000_lstmv4.h5"
		]
		self.models = []


		self.vt = VectorTools()

		print("MOZIA : Got "+str(len(self.models))+" models")

	def getTypeOfModel(self, list_of_state_pos):
		"""Retourne le type du model des states passés en paramètre
			INPUT : List of State
			OUTPUT : list corresponding to the model class Ex : [0, 0, 0, 0, 0, 1, 0, 0]
		"""
		nb_states = len(list_of_state_pos)
		#state_pos = [[state.pos().x(), state.pos().y()] for state in list_of_state]
		#for state in list_of_state:
			#print(state.getLabel())
		#print(state_pos)
		model, model_name = self.getModelFromInput(nb_states)
		#print(model_name)
		return self.predict(model, list_of_state_pos)

	def moveStates(self, list_of_state):
		"""Return a list of correctly placed points"""
		if(self.models==[]):
			loading = QProgressDialog("Loading AI models...",None,0,100)
			loading.setWindowTitle("O'TomateMozzarella")
			loading.forceShow()
			loading.open()
			loading.setValue(0)
			for model_name in self.model_names:
				self.models.append(load_model(model_name))
				loading.setValue(loading.value()+25)

		new_points = []
		nb_states = len(list_of_state)

		init_state_pos = [[state.pos().x(), state.pos().y()] for state in list_of_state]
		self.dm.showModel(init_state_pos)

		normalized_state_pos = self.dm.normalizeInput(init_state_pos)
		self.dm.showModel(normalized_state_pos)

		sorted_state_pos = self.dm.sortInput(init_state_pos)
		#self.dm.showModel(sorted_state_pos)

		#print("init_state_pos" + str(init_state_pos))
		#print("sorted_state_pos" + str(sorted_state_pos))

		init_state_index = [] #remind the initial position of states => then sort them

		for pos in sorted_state_pos:
			#print(str(pos) + " was at "+str(init_state_pos.index(pos))+" and is now at "+str(sorted_state_pos.index(pos)))
			init_state_index.append(init_state_pos.index(pos))

		predicted_model = self.getTypeOfModel(normalized_state_pos)
		#print("Model is "+self.dm.getModelName(predicted_model))
		model_index = predicted_model.index(1)

		if model_index == 0:####################################################
			new_points = self.replaceAlignModel(sorted_state_pos)
		elif model_index == 1:
			new_points = self.replaceParalleleModel(sorted_state_pos)
		elif model_index == 2:
			new_points = self.replaceParallele2Model(sorted_state_pos)
		elif model_index == 3:
			new_points = self.replaceParallele3Model(sorted_state_pos)
		elif model_index == 4:
			new_points = self.replaceParallele4Model(sorted_state_pos)
		elif model_index == 5:
			new_points = self.replaceDiagonalModel(sorted_state_pos)
		elif model_index == 6:
			new_points = self.replaceLModel(sorted_state_pos)
		elif model_index == 7:
			new_points = self.replaceCircleModel(sorted_state_pos)
		elif model_index == 8:##################################################
			new_points = self.dm.reverseModelTopToBottom(self.replaceAlignModel(sorted_state_pos))
		elif model_index == 9:
			new_points = self.dm.reverseModelTopToBottom(self.replaceParalleleModel(sorted_state_pos))
		elif model_index == 10:
			new_points = self.dm.reverseModelTopToBottom(self.replaceParallele2Model(sorted_state_pos))
		elif model_index == 11:
			new_points = self.dm.reverseModelTopToBottom(self.replaceParallele3Model(sorted_state_pos))
		elif model_index == 12:
			new_points = self.dm.reverseModelTopToBottom(self.replaceParallele4Model(sorted_state_pos))
		elif model_index == 13:
			new_points = self.dm.reverseModelTopToBottom(self.replaceDiagonalModel(sorted_state_pos))
		elif model_index == 14:
			new_points = self.dm.reverseModelTopToBottom(self.replaceLModel(sorted_state_pos))
		elif model_index == 15:
			new_points = self.dm.reverseModelTopToBottom(self.replaceCircleModel(sorted_state_pos))
		elif model_index == 16:##################################################
			new_points = self.dm.reverseModelRightToLeft(self.replaceAlignModel(sorted_state_pos))
		elif model_index == 17:
			new_points = self.dm.reverseModelRightToLeft(self.replaceParalleleModel(sorted_state_pos))
		elif model_index == 18:
			new_points = self.dm.reverseModelRightToLeft(self.replaceParallele2Model(sorted_state_pos))
		elif model_index == 19:
			new_points = self.dm.reverseModelRightToLeft(self.replaceParallele3Model(sorted_state_pos))
		elif model_index == 20:
			new_points = self.dm.reverseModelRightToLeft(self.replaceParallele4Model(sorted_state_pos))
		elif model_index == 21:
			new_points = self.dm.reverseModelRightToLeft(self.replaceDiagonalModel(sorted_state_pos))
		elif model_index == 22:
			new_points = self.dm.reverseModelRightToLeft(self.replaceLModel(sorted_state_pos))
		elif model_index == 23:
			new_points = self.dm.reverseModelRightToLeft(self.replaceCircleModel(sorted_state_pos))
		elif model_index == 24:##################################################
			new_points = self.dm.reverseModelTopToBottom(self.dm.reverseModelRightToLeft(self.replaceAlignModel(sorted_state_pos)))
		elif model_index == 25:
			new_points = self.dm.reverseModelTopToBottom(self.dm.reverseModelRightToLeft(self.replaceParalleleModel(sorted_state_pos)))
		elif model_index == 26:
			new_points = self.dm.reverseModelTopToBottom(self.dm.reverseModelRightToLeft(self.replaceParallele2Model(sorted_state_pos)))
		elif model_index == 27:
			new_points = self.dm.reverseModelTopToBottom(self.dm.reverseModelRightToLeft(self.replaceParallele3Model(sorted_state_pos)))
		elif model_index == 28:
			new_points = self.dm.reverseModelTopToBottom(self.dm.reverseModelRightToLeft(self.replaceParallele4Model(sorted_state_pos)))
		elif model_index == 29:
			new_points = self.dm.reverseModelTopToBottom(self.dm.reverseModelRightToLeft(self.replaceDiagonalModel(sorted_state_pos)))
		elif model_index == 30:
			new_points = self.dm.reverseModelTopToBottom(self.dm.reverseModelRightToLeft(self.replaceLModel(sorted_state_pos)))
		elif model_index == 31:
			new_points = self.dm.reverseModelTopToBottom(self.dm.reverseModelRightToLeft(self.replaceCircleModel(sorted_state_pos)))

		indexed_new_points = [[] for _ in range(0, len(new_points))]
		for i, index in enumerate(init_state_index):
			#print(index, i)
			#print("Replacing "+str(new_points[i]) + " from "+str(i)+" to "+str(index))
			indexed_new_points[index] = new_points[i]

		return indexed_new_points


	def getModelFromInput(self, nb_states):
		"""Return (model, name_of_model) corresponding to input"""
		switcher = {
			3 : (self.models[0], self.model_names[0]),
			4 : (self.models[1], self.model_names[1]),
			5 : (self.models[2], self.model_names[2]),
			6 : (self.models[3], self.model_names[3])
			#7 : (self.models[4], self.model_names[4]),
			#8 : (self.models[5], self.model_names[5])
		}
		return switcher.get(nb_states)

	def predict(self, model, data):
		"""Return the prediction of the AI by the given model with input, output_len is the total nb of models"""
		output_len = model.layers[len(model.layers)-1].output.shape[1]
		res = model.predict(np.array([data]))
		correct_res = [0 for _ in range(0, output_len)]
		res = res[0].tolist()
		max_index = res.index(max(res))
		correct_res[max_index] = 1
		return correct_res

	def replaceAlignModel(self, state_pos):
		new_pos = []
		delta = self.vt.norme([state_pos[0][0]-state_pos[1][0], state_pos[0][1]-state_pos[1][1]])
		for i in range(0, len(state_pos)):
			new_pos.append([state_pos[0][0]+i*delta, state_pos[0][1]])
		return new_pos

	def replaceParalleleModel(self, state_pos):
		new_pos = []
		nb_state = len(state_pos)
		delta = self.vt.norme([state_pos[0][0]-state_pos[1][0], state_pos[0][1]-state_pos[1][1]])

		coef = 1

		isImpair = nb_state%2 != 0

		if isImpair:
			nb_state = nb_state - 1

		j = 0
		for i in range(0, nb_state, 2):
			new_pos.append([state_pos[0][0] + i*delta, state_pos[0][1]])
			new_pos.append([state_pos[0][0] + i*delta, state_pos[0][1] + delta*coef])
			j = i

		if isImpair:
			j += 2
			last_state = state_pos[-1]
			nearBottom = abs(state_pos[0][1] - last_state[1]) < abs(state_pos[0][1] + delta - last_state[1])
			if nearBottom:
				new_pos.append([state_pos[0][0] + j*delta, state_pos[0][1]])
			else:
				new_pos.append([state_pos[0][0] + j*delta, state_pos[0][1] + delta*coef])
		return new_pos

	def replaceParallele2Model(self, state_pos):
		new_pos = []
		nb_state = len(state_pos)
		delta = self.vt.norme([state_pos[0][0]-state_pos[2][0], state_pos[0][1]-state_pos[2][1]])

		coef = 1
		isImpair = nb_state%2 != 0

		if isImpair:
			nb_state = nb_state - 1

		j = 0
		for i in range(0, nb_state, 2):
			new_pos.append([state_pos[0][0] + i*delta, state_pos[0][1]])
			new_pos.append([state_pos[0][0] + i*delta, state_pos[0][1] + delta/coef])
			j = i

		if isImpair:
			j += 2
			last_state = state_pos[-1]
			nearBottom = abs(state_pos[0][1] - last_state[1]) < abs(state_pos[0][1] + delta - last_state[1])
			if nearBottom:
				new_pos.append([state_pos[0][0] + j*delta, state_pos[0][1]])
			else:
				new_pos.append([state_pos[0][0] + j*delta, state_pos[0][1] + delta/coef])
		return new_pos

	def replaceParallele3Model(self, state_pos):
		new_pos = []
		nb_state = len(state_pos)
		delta = self.vt.norme([state_pos[0][0]-state_pos[2][0], state_pos[0][1]-state_pos[2][1]])

		isImpair = nb_state%2 != 0
		coef = 1
		if isImpair:
			nb_state = nb_state - 1

		j = 0
		for i in range(0, nb_state, 2):
			new_pos.append([state_pos[0][0] + i*delta, state_pos[0][1]])
			new_pos.append([state_pos[0][0] + i*delta - delta, state_pos[0][1] + delta/coef])
			j = i

		if isImpair:
			j += 2
			last_state = state_pos[-1]
			nearBottom = abs(state_pos[0][1] - last_state[1]) < abs(state_pos[0][1] + delta - last_state[1])
			if nearBottom:
				new_pos.append([state_pos[0][0] + j*delta, state_pos[0][1]])
			else:
				new_pos.append([state_pos[0][0] + j*delta - delta, state_pos[0][1] + delta/coef])
		return new_pos

	def replaceParallele4Model(self, state_pos):
		new_pos = []
		nb_state = len(state_pos)
		delta = self.vt.norme([state_pos[0][0]-state_pos[2][0], state_pos[0][1]-state_pos[2][1]])

		isImpair = nb_state%2 != 0
		coef = 1
		if isImpair:
			nb_state = nb_state - 1

		j = 0
		for i in range(0, nb_state, 2):
			new_pos.append([state_pos[0][0] + i*delta, state_pos[0][1]])
			new_pos.append([state_pos[0][0] + i*delta - delta, state_pos[0][1] + delta*coef])
			j = i

		if isImpair:
			j += 2
			last_state = state_pos[-1]
			nearBottom = abs(state_pos[0][1] - last_state[1]) < abs(state_pos[0][1] + delta - last_state[1])
			if nearBottom:
				new_pos.append([state_pos[0][0] + j*delta, state_pos[0][1]])
			else:
				new_pos.append([state_pos[0][0] + j*delta - delta, state_pos[0][1] + delta*coef])
		return new_pos

	def replaceDiagonalModel(self, state_pos):
		new_pos = []
		delta = self.vt.norme([state_pos[0][0]-state_pos[1][0], state_pos[0][1]-state_pos[1][1]])
		for i in range(0, len(state_pos)):
			new_pos.append([state_pos[0][0]+i*delta, state_pos[0][1]]+i*delta)
		return new_pos

	def replaceLModel(self, state_pos):

		nb_state = len(state_pos)
		nb_col = int(math.sqrt(nb_state))
		new_pos = []

		delta = self.vt.norme([state_pos[0][0]-state_pos[1][0], state_pos[0][1]-state_pos[1][1]])
		center_x = state_pos[0][0]
		center_y = state_pos[0][1]

		remaining_nb_point = nb_state
		for i in range(0, nb_col):
			nb_point = random.randint(1, remaining_nb_point) if remaining_nb_point > 1 else 0
			remaining_nb_point -= nb_point
			for j in range(0, nb_point):
				new_pos.append([center_x + i*delta, center_y + j*delta])

		while remaining_nb_point > 0:
			new_pos.append([new_pos[0][0], new_pos[0][1]+delta])
			remaining_nb_point -= 1
		return new_pos

	def replaceCircleModel(self, state_pos):
		geocentre = self.vt.geo_centre(state_pos)
		rayon = self.vt.norme([state_pos[0][0]-geocentre[0], state_pos[0][1]-geocentre[1]])
		model = self.vt.pos_circle(state_pos, rayon)
		return model
