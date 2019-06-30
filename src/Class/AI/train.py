import pandas as pd
import random

from sklearn.model_selection import train_test_split

from keras.layers import Dropout
from keras.layers import LSTM
from keras import layers


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Reshape
from keras.layers import Input
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D

from keras import metrics
from keras.callbacks import ModelCheckpoint
from keras import optimizers
from keras.utils import to_categorical
from keras import callbacks
from keras import regularizers
import numpy as np
from DatasetManager import DatasetManager

dm = DatasetManager()

class colors:
    ok = '\033[92m'
    fail = '\033[91m'
    close = '\033[0m'

#First model with classical push forward neural network
def getModel(input_shape):
	model = Sequential()

	model.add(Conv1D(64, kernel_size=1, activation='relu', input_shape=input_shape))
	model.add(Flatten())
	model.add(Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001)))

	model.add(Dense(len(y[0]), activation='softmax', kernel_regularizer=regularizers.l2(0.001)))
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	#model.summary()
	return model

#Second model with first layer as a convolutionnal layer
def getModelConv(input_shape):
	model = Sequential()

	model.add(Conv1D(128, 2, activation='relu', input_shape=input_shape))
	model.add(Conv1D(64, 1, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
	model.add(GlobalAveragePooling1D())

	model.add(Dense(len(y[0]), activation='softmax', kernel_regularizer=regularizers.l2(0.01)))
	model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
	#model.summary()
	return model

#Thrird model with LSTM model
def getLSTMModel(input_shape):
	model = Sequential()
	model.add(LSTM(128, input_shape=input_shape, return_sequences=True))
	model.add(Dropout(0.01))
	model.add(LSTM(64))
	model.add(Dropout(0.01))
	model.add(Dense(len(y[0]), activation='softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
	#model.summary()
	return model
	
##Predict the type of automata
##@param output_len the len of the output vector
def predict(data, output_len):
	res = model.predict(np.array([data]))
	correct_res = [0 for _ in range(0, output_len)]
	res = res[0].tolist()
	max_index = res.index(max(res))
	correct_res[max_index] = 1
	return correct_res

max_nb_of_state = 8
tbCallBack = callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)
esCallBack = callbacks.EarlyStopping(monitor='loss', min_delta=0, patience=5, verbose=1, mode='auto')

dataset_size = 3000

for nb_state in range(3, max_nb_of_state+1):
	print("Training model for "+str(nb_state)+" states")
	x, y = dm.createClassificationDataset(nb_state, dsize=dataset_size)
	x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

	print(x_train[0])
	print(y_train[0])

	print("Generating model ...")
	model = getLSTMModel(np.array(x_train[0]).shape)

	print("Fitting ...")
	for _ in range(1, 3):
		print("########"+str(_))
		model.fit(np.array(x_train), np.array(y_train), epochs=3, batch_size=512, callbacks=[tbCallBack, esCallBack])
		# evaluate the model
		scores = model.evaluate(np.array(x_test), np.array(y_test))
		print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
		for __ in range(0, 10):
			index = random.randint(0, len(x_test)-1)
			data = x_test[index]
			correct = y_test[index]
			res = predict(data, len(y_test[0]))
			print('C', correct, end=' ')
			print('P', res, end=' ')

			if dm.compareResults(correct, res):
				print(colors.ok + '☑' + colors.close, end=' ')
			else:
				print(colors.fail + '☒' + colors.close, end=' ')

			print("Found "+dm.getModelName(res)+" is "+dm.getModelName(correct))
	model.save("models/otmt_"+str(nb_state)+"states_1000_lstmv5.h5")
