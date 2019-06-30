
import sys
import os.path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
#import State
import random
import math

import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from VectorTools import VectorTools

class DatasetManager:
	"""Manager dataset for AI"""
	def __init__(self):
		#delta is the geometric distance between 2 states
		self.max_delta = 50
		self.min_delta = 0

		#center_x and center_y are center of models, they allow to have center in dataset and no center in ai because there is random in center
		self.max_center_x = 1000//2
		self.max_center_y = 1000//2

		self.min_center_x = -1000//2
		self.min_center_y = -1000//2

		self.max_variance = 1
		self.min_variance = -1
		self.vt = VectorTools()

	"""
	y
	|
	|
	_______ x

	is the repere
	"""


	def getAlignModel(self, center_x, center_y, delta, nb_state):
		"""
			#MODELE1 aligned-points getAlignModel
			#0-0
			#0-0-0
			#0-0-0-0
			#0-0-0-0-0
			#0-0-0-0-0-0
			#0-0-0-0-0-0-0
			#0-0-0-0-0-0-0-0
		"""
		model = []
		for i in range(0, nb_state):
			model.append([center_x + i*delta, center_y])
		return model

	def getParalleleModel(self, center_x, center_y, delta, nb_state):
		model = []
		isImpair = nb_state%2 != 0
		coef = random.randint(1, 7)
		if isImpair:
			nb_state = nb_state - 1

		j = 0
		for i in range(0, nb_state, 2):
			model.append([center_x + i*delta, center_y])
			model.append([center_x + i*delta, center_y + delta*coef])
			j = i

		if isImpair:
			j += 2
			random_choice = random.randint(0, 1)
			if random_choice == 0:
				model.append([center_x + j*delta, center_y])
			else:
				model.append([center_x + j*delta, center_y + delta*coef])
		return model

	def getParallele2Model(self, center_x, center_y, delta, nb_state):
		model = []
		isImpair = nb_state%2 != 0
		coef = random.randint(1, 7)
		if isImpair:
			nb_state = nb_state - 1

		j = 0
		for i in range(0, nb_state, 2):
			model.append([center_x + i*delta, center_y])
			model.append([center_x + i*delta, center_y + delta/coef])
			j = i

		if isImpair:
			j += 2
			random_choice = random.randint(0, 1)
			if random_choice == 0:
				model.append([center_x + j*delta, center_y])
			else:
				model.append([center_x + j*delta, center_y + delta/coef])
		return model

	def getParallele3Model(self, center_x, center_y, delta, nb_state):
		model = []
		isImpair = nb_state%2 != 0
		coef = random.randint(1, 7)
		if isImpair:
			nb_state = nb_state - 1

		j = 0
		for i in range(0, nb_state, 2):
			model.append((center_x + i*delta, center_y))
			model.append((center_x + i*delta + delta, center_y + delta/coef))
			j = i

		if isImpair:
			j += 2
			random_choice = random.randint(0, 1)
			if random_choice == 0:
				model.append((center_x + j*delta, center_y))
			else:
				model.append([center_x + j*delta + delta, center_y + delta/coef])
		return model

	def getParallele4Model(self, center_x, center_y, delta, nb_state):
		model = []
		isImpair = nb_state%2 != 0
		coef = random.randint(1, 7)

		if isImpair:
			nb_state = nb_state - 1

		j = 0
		for i in range(0, nb_state, 2):
			model.append((center_x + i*delta, center_y))
			model.append((center_x + i*delta + delta, center_y + delta*coef))
			j = i

		if isImpair:
			j += 2
			random_choice = random.randint(0, 1)
			if random_choice == 0:
				model.append((center_x + j*delta, center_y))
			else:
				model.append([center_x + j*delta + delta, center_y + delta*coef])
		return model

	def getDiagonalModel(self, center_x, center_y, delta, nb_state):
		"""
		  0
		 0
		0
		"""
		model = []
		for i in range(0, nb_state):
			model.append([center_x + i*delta, center_y + i*delta])
		return model

	def getLModel(self, center_x, center_y, delta, nb_state):
		model = []

		nb_col = int(math.sqrt(nb_state))

		remaining_nb_point = nb_state
		for i in range(0, nb_col):
			nb_point = random.randint(1, remaining_nb_point) if remaining_nb_point > 1 else 0
			remaining_nb_point -= nb_point
			for j in range(0, nb_point):
				model.append([center_x + i*delta, center_y + j*delta])

		while remaining_nb_point > 0:
			model.append([model[0][0], model[0][1]+delta])
			remaining_nb_point -= 1
		return model

	def getCircleModel(self, center_x, center_y, delta, nb_state):
		model = []
		for i in range(0, nb_state):
			model.append([center_x, center_y])
		model = self.vt.pos_circle(model, delta)
		return model

	def reverseModelTopToBottom(self, model):
		center_x = sum([coord[0] for coord in model])/len(model)
		center_y = sum([coord[1] for coord in model])/len(model)

		new_model = []
		for coord in model:
			#print(str(coord)+"->"+str((self.getSymCoord((0, 0), (1, 0), coord))))
			new_model.append(self.vt.getSymCoord((0, 0), (1, 0), coord))

		return new_model

	def reverseModelRightToLeft(self, model):
		center_x = sum([coord[0] for coord in model])/len(model)
		center_y = sum([coord[1] for coord in model])/len(model)

		new_model = []
		for coord in model:
			#print(str(coord)+"->"+str((self.getSymCoord((0, 0), (1, 0), coord))))
			new_model.append(self.vt.getSymCoord((0, 0), (0, 1), coord))

		return new_model

	def getAllModels(self, center_x, center_y, delta, nb_state):
		models = []
		tmp_models = []
		mod1 = self.getAlignModel(center_x, center_y, delta, nb_state)
		mod2 = self.getParalleleModel(center_x, center_y, delta, nb_state)
		mod3 = self.getParallele2Model(center_x, center_y, delta, nb_state)
		mod4 = self.getParallele3Model(center_x, center_y, delta, nb_state)
		mod5 = self.getParallele4Model(center_x, center_y, delta, nb_state)
		mod6 = self.getDiagonalModel(center_x, center_y, delta, nb_state)
		mod7 = self.getCircleModel(center_x, center_y, delta, nb_state)
		mod8 = self.getLModel(center_x, center_y, delta, nb_state)
		models.append(mod1)
		models.append(mod2)
		models.append(mod3)
		models.append(mod4)
		models.append(mod5)
		models.append(mod6)
		models.append(mod7)
		models.append(mod8)
		tmp_models.append(mod1)
		tmp_models.append(mod2)
		tmp_models.append(mod3)
		tmp_models.append(mod4)
		tmp_models.append(mod5)
		tmp_models.append(mod6)
		tmp_models.append(mod7)
		tmp_models.append(mod8)
		for m in tmp_models:
			models.append(self.reverseModelTopToBottom(m))
			models.append(self.reverseModelRightToLeft(m))
			models.append(self.reverseModelTopToBottom(self.reverseModelRightToLeft(m)))

		return models

	def getAllModels2(self, center_x, center_y, delta, nb_state):
		models = []
		tmp_models = []

		mod1 = self.getAlignModel(center_x, center_y, delta, nb_state)
		mod2 = self.getParalleleModel(center_x, center_y, delta, nb_state)
		mod3 = self.getParallele2Model(center_x, center_y, delta, nb_state)
		mod4 = self.getParallele3Model(center_x, center_y, delta, nb_state)
		mod5 = self.getParallele4Model(center_x, center_y, delta, nb_state)
		mod6 = self.getDiagonalModel(center_x, center_y, delta, nb_state)
		mod7 = self.getCircleModel(center_x, center_y, delta, nb_state)
		mod8 = self.getLModel(center_x, center_y, delta, nb_state)

		mod12 = self.reverseModelTopToBottom(mod1)
		mod22 = self.reverseModelTopToBottom(mod2)
		mod32 = self.reverseModelTopToBottom(mod3)
		mod42 = self.reverseModelTopToBottom(mod4)
		mod52 = self.reverseModelTopToBottom(mod5)
		mod62 = self.reverseModelTopToBottom(mod6)
		mod72 = self.reverseModelTopToBottom(mod7)
		mod82 = self.reverseModelTopToBottom(mod8)

		mod13 = self.reverseModelRightToLeft(mod1)
		mod23 = self.reverseModelRightToLeft(mod2)
		mod33 = self.reverseModelRightToLeft(mod3)
		mod43 = self.reverseModelRightToLeft(mod4)
		mod53 = self.reverseModelRightToLeft(mod5)
		mod63 = self.reverseModelRightToLeft(mod6)
		mod73 = self.reverseModelRightToLeft(mod7)
		mod83 = self.reverseModelRightToLeft(mod8)

		mod14 = self.reverseModelTopToBottom(mod13)
		mod24 = self.reverseModelTopToBottom(mod23)
		mod34 = self.reverseModelTopToBottom(mod33)
		mod44 = self.reverseModelTopToBottom(mod43)
		mod54 = self.reverseModelTopToBottom(mod53)
		mod64 = self.reverseModelTopToBottom(mod63)
		mod74 = self.reverseModelTopToBottom(mod73)
		mod84 = self.reverseModelTopToBottom(mod83)

		models.append(mod1)
		models.append(mod2)
		models.append(mod3)
		models.append(mod4)
		models.append(mod5)
		models.append(mod6)
		models.append(mod7)
		models.append(mod8)
		models.append(mod12)
		models.append(mod22)
		models.append(mod32)
		models.append(mod42)
		models.append(mod52)
		models.append(mod62)
		models.append(mod72)
		models.append(mod82)
		models.append(mod13)
		models.append(mod23)
		models.append(mod33)
		models.append(mod43)
		models.append(mod53)
		models.append(mod63)
		models.append(mod73)
		models.append(mod83)
		models.append(mod14)
		models.append(mod24)
		models.append(mod34)
		models.append(mod44)
		models.append(mod54)
		models.append(mod64)
		models.append(mod74)
		models.append(mod84)

		return models

	def getAllClassModels(self, center_x, center_y, delta, nb_state):
		models = []
		tmp_models = []
		mod1 = self.getAlignModel(center_x, center_y, delta, nb_state)
		mod2 = self.getParalleleModel(center_x, center_y, delta, nb_state)
		mod3 = self.getParallele2Model(center_x, center_y, delta, nb_state)
		mod4 = self.getParallele3Model(center_x, center_y, delta, nb_state)
		mod5 = self.getParallele4Model(center_x, center_y, delta, nb_state)
		mod6 = self.getDiagonalModel(center_x, center_y, delta, nb_state)
		mod7 = self.getCircleModel(center_x, center_y, delta, nb_state)
		mod8 = self.getLModel(center_x, center_y, delta, nb_state)
		tmp_models.append(mod1)
		tmp_models.append(mod2)
		tmp_models.append(mod3)
		tmp_models.append(mod4)
		tmp_models.append(mod5)
		tmp_models.append(mod6)
		tmp_models.append(mod7)
		tmp_models.append(mod8)
		for index, m in enumerate(tmp_models):
			n_m = [0 for _ in range(0, len(tmp_models))]
			n_m[index] = 1
			models.append(n_m)

		for index, m in enumerate(tmp_models):
			n_m = [0 for _ in range(0, len(tmp_models))]
			n_m[index] = 1
			models.append(n_m)
			models.append(n_m)
			models.append(n_m)

		return models

	def getAllClassModels2(self, center_x, center_y, delta, nb_state):
		models = []
		tmp_models = []
		mod1 = self.getAlignModel(center_x, center_y, delta, nb_state)
		mod2 = self.getParalleleModel(center_x, center_y, delta, nb_state)
		mod3 = self.getParallele2Model(center_x, center_y, delta, nb_state)
		mod4 = self.getParallele3Model(center_x, center_y, delta, nb_state)
		mod5 = self.getParallele4Model(center_x, center_y, delta, nb_state)
		mod6 = self.getDiagonalModel(center_x, center_y, delta, nb_state)
		mod7 = self.getCircleModel(center_x, center_y, delta, nb_state)
		mod8 = self.getLModel(center_x, center_y, delta, nb_state)

		mod12 = self.reverseModelTopToBottom(mod1)
		mod22 = self.reverseModelTopToBottom(mod2)
		mod32 = self.reverseModelTopToBottom(mod3)
		mod42 = self.reverseModelTopToBottom(mod4)
		mod52 = self.reverseModelTopToBottom(mod5)
		mod62 = self.reverseModelTopToBottom(mod6)
		mod72 = self.reverseModelTopToBottom(mod7)
		mod82 = self.reverseModelTopToBottom(mod8)

		mod13 = self.reverseModelRightToLeft(mod1)
		mod23 = self.reverseModelRightToLeft(mod2)
		mod33 = self.reverseModelRightToLeft(mod3)
		mod43 = self.reverseModelRightToLeft(mod4)
		mod53 = self.reverseModelRightToLeft(mod5)
		mod63 = self.reverseModelRightToLeft(mod6)
		mod73 = self.reverseModelRightToLeft(mod7)
		mod83 = self.reverseModelRightToLeft(mod8)

		mod14 = self.reverseModelTopToBottom(mod13)
		mod24 = self.reverseModelTopToBottom(mod23)
		mod34 = self.reverseModelTopToBottom(mod33)
		mod44 = self.reverseModelTopToBottom(mod43)
		mod54 = self.reverseModelTopToBottom(mod53)
		mod64 = self.reverseModelTopToBottom(mod63)
		mod74 = self.reverseModelTopToBottom(mod73)
		mod84 = self.reverseModelTopToBottom(mod83)

		tmp_models.append(mod1)
		tmp_models.append(mod2)
		tmp_models.append(mod3)
		tmp_models.append(mod4)
		tmp_models.append(mod5)
		tmp_models.append(mod6)
		tmp_models.append(mod7)
		tmp_models.append(mod8)
		tmp_models.append(mod12)
		tmp_models.append(mod22)
		tmp_models.append(mod32)
		tmp_models.append(mod42)
		tmp_models.append(mod52)
		tmp_models.append(mod62)
		tmp_models.append(mod72)
		tmp_models.append(mod82)
		tmp_models.append(mod13)
		tmp_models.append(mod23)
		tmp_models.append(mod33)
		tmp_models.append(mod43)
		tmp_models.append(mod53)
		tmp_models.append(mod63)
		tmp_models.append(mod73)
		tmp_models.append(mod83)
		tmp_models.append(mod14)
		tmp_models.append(mod24)
		tmp_models.append(mod34)
		tmp_models.append(mod44)
		tmp_models.append(mod54)
		tmp_models.append(mod64)
		tmp_models.append(mod74)
		tmp_models.append(mod84)

		for index, m in enumerate(tmp_models):
			n_m = [0 for _ in range(0, len(tmp_models))]
			n_m[index] = 1
			models.append(n_m)

		return models

	def shuffle(self, x, y):
		c = list(zip(x, y))
		random.shuffle(c)
		a, b = zip(*c)

		return a, b

	def createClassificationDataset(self, nb_state, dsize=1000):

		"""On prend des modèles de base, puis on créé des modèles de base décalés (Y), puis dans l'autre sens.
		A partir de ces Y, on créé des différences de position par rapport à l'alignement parfait du modèle.
		Ces modèles imparfait représentes les états du modèles que l'utilisateur veut rendre parfait (X)"""

		print("Generating models...")
		models = []
		model_classes = []
		for _ in range(0, dsize):
			delta = random.randrange(self.min_delta, self.max_delta)
			center_x = random.randrange(self.min_center_x, self.max_center_x)
			center_y = random.randrange(self.min_center_y, self.max_center_y)
			models = models + self.getAllModels2(center_x, center_y, delta, nb_state)
			model_classes = model_classes + self.getAllClassModels2(center_x, center_y, delta, nb_state)

		print("Got "+str(len(models))+" models")
		print("Generating inputs...")
		x = []
		y = []

		for i in range(0, len(models)):
			model = models[i]
			model_class = model_classes[i]
			for _ in range(0, 10):
				n_m = []
				for coord in model:
					n_m.append([coord[0]+random.randint(self.min_variance, self.max_variance), coord[1]+random.randint(self.min_variance, self.max_variance)])
				#n_x, n_y = self.shuffle(n_m, model)
				#print(n_m)
				#print(n_y)
				x.append(self.normalizeInput(n_m))
				y.append(model_class)

		x, y = self.shuffle(x, y)
		print("Got "+str(len(x))+" samples")
		return x, y

	def createRegressionDataset(self, nb_state):

		"""On prend des modèles de base, puis on créé des modèles de base décalés (Y), puis dans l'autre sens.
		A partir de ces Y, on créé des différences de position par rapport à l'alignement parfait du modèle.
		Ces modèles imparfait représentes les états du modèles que l'utilisateur veut rendre parfait (X)"""

		print("Generating models...")
		models = []

		for _ in range(0, 400):
			delta = random.randrange(self.min_delta, self.max_delta)
			center_x = random.randrange(self.min_center_x, self.max_center_x)
			center_y = random.randrange(self.min_center_y, self.max_center_y)
			models = models + self.getAllModels(center_x, center_y, delta, nb_state)

		print("Got "+str(len(models))+" models")
		print("Generating inputs...")
		x = []
		y = []

		for model in models:
			for _ in range(0, 10):
				n_m = []
				for coord in model:
					n_m.append([coord[0]+random.randint(self.min_variance, self.max_variance), coord[1]+random.randint(self.min_variance, self.max_variance)])
				n_x, n_y = self.shuffle(n_m, model)
				x.append(n_x)
				y.append(n_y)

		x, y = self.shuffle(x, y)
		print("Got "+str(len(x))+" samples")
		return x, y


	def genInput(self, nb_state):
		delta = random.randrange(self.min_delta, self.max_delta)
		center_x = random.randrange(self.min_center_x, self.max_center_x)
		center_y = random.randrange(self.min_center_y, self.max_center_y)
		models = self.getAllModels(center_x, center_y, delta, nb_state)
		model_classes = self.getAllClassModels(center_x, center_y, delta, nb_state)

		print(models)
		print(model_classes)
		print("Got "+str(len(models))+" models")

		x = []
		y = []

		for i in range(0, len(models)):
			model = models[i]
			model_class = model_classes[i]
			n_m = []
			for coord in model:
				n_m.append([coord[0]+random.randint(self.min_variance, self.max_variance), coord[1]+random.randint(self.min_variance, self.max_variance)])
			x.append(n_m)
			y.append(model_class)

		return x, y, models #models with noise, model class, perfect models


	def showModel(self, model):
		labels = "abcdefghijklmnopqrstuvwxyz"
		xp = [coord[0] for coord in model]
		yp = [coord[1] for coord in model]
		plt.plot(xp, yp, 'ro')
		for label, x, y in zip(labels, xp, yp):
			plt.annotate(
				label,
				xy=(x, y), xytext=(-20, 20),
				textcoords='offset points', ha='right', va='bottom',
				bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
				arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
		plt.axis([-2000, 2000, -2000, 2000])
		plt.show()

	def showModelWithNoise(self, noisy_model, model):
		labels = "abcdefghijklmnopqrstuvwxyz"
		x = [coord[0] for coord in model]
		y = [coord[1] for coord in model]

		plt.plot(x, y, 'ro')

		for label, x, y in zip(labels, x, y):
			plt.annotate(
				label,
				xy=(x, y), xytext=(-20, 20),
				textcoords='offset points', ha='right', va='bottom',
				bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
				arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

		x_n = [coord[0] for coord in noisy_model]
		y_n = [coord[1] for coord in noisy_model]
		plt.plot(x_n, y_n, 'bo')
		for label, x, y in zip(labels, x_n, y_n):
			plt.annotate(
				label,
				xy=(x, y), xytext=(-20, 20),
				textcoords='offset points', ha='right', va='bottom',
				bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
				arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

		plt.axis([min(x+x_n)-1, max(x+x_n)+1, min(y+y_n)-1, max(y+y_n)+1])
		plt.show()

	def compareResults(self, res1, res2):
		if len(res1) == len(res2):
			for i in range(0, len(res1)):
				if res1[i] != res2[i]:
					return False
			return True
		else:
			return False

	def getModelName(self, model_class):
		model_names = ["AlignModel", "ParalleleModel", "Parallele2Model", "Parallele3Model", "Parallele4Model", "DiagonalModel", "CircleModel", "LModel", "AlignModel", "ParalleleModel", "Parallele2Model", "Parallele3Model", "Parallele4Model", "DiagonalModel", "CircleModel", "LModel", "AlignModel", "ParalleleModel", "Parallele2Model", "Parallele3Model", "Parallele4Model", "DiagonalModel", "CircleModel", "LModel", "AlignModel", "ParalleleModel", "Parallele2Model", "Parallele3Model", "Parallele4Model", "DiagonalModel", "CircleModel", "LModel"]
		return model_names[model_class.index(1)]

	def normalizeInput(self, input):
		sorted_input = self.sortInput(input)
		gc = self.vt.geo_centre(sorted_input)
		normalized_input = [[x[0]-gc[0], x[1]-gc[1]] for x in sorted_input]
		return normalized_input

	def sortInput(self, points):
		npoints = points.copy()
		sorted_input_x = sorted(points, key = lambda x: int(x[0]))
		sorted_input_y = sorted(points, key = lambda y: int(y[1]))

		topleftpoint = [sorted_input_x[0][0], sorted_input_y[len(sorted_input_y)-1][1]]
		downrightpoint = [sorted_input_x[len(sorted_input_x)-1][0], sorted_input_y[0][1]]

		projections = [self.vt.projectLine(topleftpoint, downrightpoint, p) for p in points]
		output_points = []

		while len(projections) != 0:
			min_x = projections[0][0]
			min_x_index = 0
			for i in range(0, len(projections)):
				if projections[i][0] < min_x:
					min_x = projections[i][0]
					min_x_index = i

			output_points.append(npoints[min_x_index])
			projections.pop(min_x_index)
			npoints.pop(min_x_index)

		return output_points
