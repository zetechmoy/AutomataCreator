from keras.models import load_model
from DatasetManager import DatasetManager
import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from VectorTools import VectorTools

##Colors in log
class colors:
	ok = '\033[92m'
	fail = '\033[91m'
	close = '\033[0m'

dm = DatasetManager()

##Predict the type of automata
##@param output_len the len of the output vector
def predict(data, output_len):
	res = model.predict(np.array([data]))
	correct_res = [0 for _ in range(0, output_len)]
	res = res[0].tolist()
	max_index = res.index(max(res))
	correct_res[max_index] = 1
	return correct_res

#Inputs and outputs to test
x_tests, y_trues, x_trues = dm.genInput(5)

#Load the emodel
model = load_model('models/otmt_5states_5000v2.h5')

print(x_tests[0])
print(y_trues[0])
print(x_trues[0])

#for i in range(0, len(x_tests)):
#	dm.showModelWithNoise(x_tests[i], x_trues[i])

correct_count = 0
for i in range(0, len(x_tests)):
	data = x_tests[i]
	#print(data)
	correct = y_trues[i]
	#print(correct)
	#print(x_trues[i])
	res = predict(data, len(correct))
	print('C', correct, end=' ')
	print('P', res, end=' ')
	dm.showModelWithNoise(x_trues[i], x_trues[i])#x_tests[i]
	if dm.compareResults(correct, res):
		print(colors.ok + '☑' + colors.close)
		correct_count += 1
	else:
		print(colors.fail + '☒' + colors.close)

	print("Found "+dm.getModelName(res)+" is "+dm.getModelName(correct))

print("Test ACC : {}%".format(round(correct_count/len(x_tests), 2)))

#x_r_test, y_r_trues = dm.createClassificationDataset(4)
#scores = model.evaluate(np.array(x_r_test), np.array(y_r_trues))
#print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
