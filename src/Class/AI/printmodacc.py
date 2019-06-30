from keras.models import load_model
from DatasetManager import DatasetManager
import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from VectorTools import VectorTools

dm = DatasetManager()
#Test all model
for i in range(3, 9):
	x_r_test, y_r_trues = dm.createClassificationDataset(i, dsize=100)

	dm.showModel(x_r_test[0])
	sorted_input = sorted(x_r_test[0], key = lambda x: int(x[0]))
	dm.showModel(sorted_input)

	model = load_model('models/otmt_'+str(i)+'states_1000_lstmv4.h5')

	scores = model.evaluate(np.array(x_r_test), np.array(y_r_trues))
	print("\nmodel_%i_state : %s: %.2f%%" % (i, model.metrics_names[1], scores[1]*100))
