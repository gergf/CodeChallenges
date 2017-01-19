import numpy
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')

def baseline_model():
	# create model 
	model = Sequential()
	# 1 img 28x28 -> 32 img 24x24
	model.add(Convolution2D(32, 5, 5, border_mode="valid", input_shape=(1,28,28), activation="relu"))
	# 32 img 24x24 -> 32 img 12x12
	model.add(MaxPooling2D(pool_size=(2,2)))
	model.add(Dropout(0.2))
	# img 2d -> vector 
	model.add(Flatten())
	# layer 128, activation relu 
	model.add(Dense(128, activation='relu'))
	# layer output, activation softmax  
	model.add(Dense(num_classes, activation='softmax'))

	# Compile model 
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model 

if __name__ == "__main__":
	# fix random seed 
	numpy.random.seed(7)

	# load data 
	(X_train, y_train), (X_test, y_test) = mnist.load_data()

	# normalize 0 - 255 to 0 - 1 
	X_train = X_train / 255 
	X_test = X_test / 255

	# reshape data 
	X_train = X_train.reshape(X_train.shape[0], 1, 28, 28).astype('float32')
	X_test = X_test.reshape(X_test.shape[0], 1, 28, 28).astype('float32')

	# one-hot encoding 
	y_train = np_utils.to_categorical(y_train)
	y_test = np_utils.to_categorical(y_test)
	num_classes = y_train.shape[1]

	# get model 
	model = baseline_model()
	# fit model 
	model.fit(X_train, y_train, validation_data=(X_test, y_test), nb_epoch=10, batch_size=200, verbose=2)
	# final evaluation model 
	scores = model.evaluate(X_test, y_test, verbose=0)
	print("Baseline error: %.2f%%" % (100-scores[1]*100))