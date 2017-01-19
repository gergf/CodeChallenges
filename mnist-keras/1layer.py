import numpy
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
import matplotlib.pyplot as plt

def baseline_model():
	#create model 
	model = Sequential()
	model.add(Dense(num_pixels, input_dim=num_pixels, init='normal', activation='relu'))
	model.add(Dense(num_classes, init='normal', activation='softmax'))

	#Compile model 
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model 


if __name__ == "__main__":
	# fix seed 
	numpy.random.seed(7)

	# X_train array with images
	(X_train, lab_train), (X_test, lab_test) = mnist.load_data()

	# 28*28 images to 784 vector
	num_pixels = X_train.shape[1] * X_train.shape[2]
	num_samples_train = X_train.shape[0]
	num_samples_test = X_test.shape[0]

	X_train = X_train.reshape(num_samples_train, num_pixels).astype('float32')
	X_test = X_test.reshape(num_samples_test, num_pixels).astype('float32')

	# Normalize from 0-255 to 0-1
	X_train = X_train / 255
	X_test = X_test / 255

	# one hot encode outputs 
	lab_train = np_utils.to_categorical(lab_train)
	lab_test = np_utils.to_categorical(lab_test)
	num_classes = lab_test.shape[1]

	# build model 
	model = baseline_model()

	# fit model 
	model.fit(X_train, lab_train, validation_data=(X_test, lab_test), nb_epoch=10, batch_size=200, verbose=2)
	#Final evaluation of the model 
	scores = model.evaluate(X_test, lab_test, verbose=0)
	print("Baseline Error: %.2f%%" % (100-scores[1]*100))