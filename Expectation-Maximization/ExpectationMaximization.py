# Author: German A. Garcia Ferrando \\ gergarfe@inf.upv.es \\ https://github.com/gergf
# Universitat Politecnica de Valencia \\ Master en Inteligencia Artificial, Reconocimiento de Formas e Imagen Digital 
# ATTENTION: You are free to use/modify this software as you want, but when you will be enjoying the glory that cames
# with victory and fame; please, remember me, and link at least my github ;P 

import numpy as np 
from matplotlib import pyplot as plt 
import matplotlib.mlab as mlab

# Stuff for plot pretty 
np.set_printoptions(formatter={'float': '{: 0.6f}'.format})
colors = (('blue', 'b--'),('red', 'r--'),('green', 'g--'))

def plotData(K, points, theta):
	bins = np.linspace(-10,10,100)
	plt.hist(points, bins, normed=True, color="gray", alpha=0.5)
	for k in range(K):
		plt.plot(bins, (theta[k,0] * mlab.normpdf(bins, theta[k,1], theta[k,2])), colors[k][1], label="g-" + str(k))
	plt.legend(loc='upper left')

def getRandomPriors(k):
	N = np.random.uniform(size=(k,)) 
	return np.around(N / np.sum(N),7)

def getRandomMeans(k, low=-10, high=10):
	return np.around(np.random.uniform(low=low, high=high, size=(k,)), 7)

def getRandomSigma(k, low=0, high=4): 
	return np.around(np.random.uniform(low=low, high=high, size=(k,)), 7)

""" 
	This method computes the P(x|k) for a given x and k by using a normal distribution. 
"""
def computePx_k(x, mean, std):
	return (1 / np.sqrt(2*np.pi*(std**2))) * np.exp((-1/2) * (((x - mean)**2) / (std**2)) )

"""
	Computes the likelihood with the current parameters.
	sum_{M} log sum_{K} prior_k * Pk(X_m | Z_k ; \theta)
	where 
		Pk(X_m | Z_k ; \theta) = Gaussian density for the Kth mixture 
""" 
def log_likelihood(data, theta): 
	log_likelihood = 0 
	for x in data:
		likPoint = 0  
		for k in range(theta.shape[0]): 
			likPoint += theta[k][0] * computePx_k(x, theta[k][1], theta[k][2])
		log_likelihood += np.log(likPoint)
	return log_likelihood

""" 
	This is big daddy. 
"""
def EM(data, real_theta, fig, estimate_priors=True, 
	   estimate_means=False, estimate_sigmas=False, _K=2,  epsilon=0.000001):
	numPoints = len(data)
	iteration = 0 
	# Initialization Step # 
	print("Using K " + str(_K) + "...")
	print("Using epsilon " + str(epsilon) + "...")

	# Initialize theta # 
	theta = np.copy(real_theta)
	if estimate_priors:
		new_priors = getRandomPriors(_K)
		for k in range(_K):
			theta[k,0] = new_priors[k]
	if estimate_means:
		new_means = getRandomMeans(_K)
		for k in range(_K):
			theta[k,1] = new_means[k]
	if estimate_sigmas:
		new_sigmas = getRandomSigma(_K)
		for k in range(_K):
			theta[k,2] = new_sigmas[k]

	# Plot the initial distribution #
	ax = fig.add_subplot(1,3,2)
	ax.set_title("Initial")
	ax.set_ylim([0,0.25])
	plotData(_K, data, theta)

	# Initialize likelihood #
	oldLik = float('-inf')
	curLik = log_likelihood(data, theta)
	likMatrix = np.zeros((numPoints, _K)) # This matrix stores P(Z_k=1|x;\theta). Weights 

	print("Expectation-Maximization")
	print("Real  priors: ", real_theta[:,0])
	print("Real   means: ", real_theta[:,1])
	print("Real  sigmas: ", real_theta[:,2])
	print("Real log_likelihood: ", log_likelihood(data, real_theta))
	print("-----------------------------------------------------")
	print("Initial  priors: ", theta[:,0])
	print("Initial   means: ", theta[:,1])
	print("Initial  sigmas: ", theta[:,2])
	print("Initial log_likelihood: ", curLik)
	print("-----------------------------------------------------")

	# Until convergence #
	while (curLik - oldLik) > epsilon:
		
		# E-Step #
		# With the current theta we're going to estimate the hidden Z for each point. 
		# As we can not compute it directly, we make an estimation membership weight 
		for m in range(likMatrix.shape[0]): 
			for k in range(_K): 
				# Numerator: p(k) * p(x|k;\theta)
				likMatrix[m, k] = theta[k][0] * computePx_k(data[m], theta[k][1], theta[k][2]) 
			# Normalize probs: sum_{m=1}^{K} : p(m) * p(x|m;\theta) #
			likMatrix[m] /= np.sum(likMatrix[m])

		# M-Step #
		if estimate_priors:	
			# new_priors is a matrix with shape (k,) where each cell stores the 
			# sum of the membership of each point for each gaussian
			new_priors = np.sum(likMatrix, axis=0) / numPoints # Sum the columns
		
		if estimate_means:
			# The new mean of each gaussian is computed as a standard mean, by weighting 
			# each of the points for its membership to each gaussian 
			new_means = np.zeros((_K))
			for k in range(_K):
				# new_mu = (sum_{i}(Wik * Xi)) / (Nk)  
				new_means[k] = np.sum(data * likMatrix[:,k]) / np.sum(likMatrix[:,k], axis=0)
		
		if estimate_sigmas and estimate_means:
			# Same analogy that means
			new_sigmas = np.zeros((_K))
			for k in range(_K):
				square = (data - new_means[k])**2
				num = likMatrix[:,k] * square
				new_sigmas[k] = np.sqrt(np.sum(num) / np.sum(likMatrix[:,k], axis=0))
		elif estimate_sigmas and (not estimate_means): 
			new_sigmas = np.zeros((_K))
			for k in range(_K):
				square = (data - theta[k,1])**2
				num = likMatrix[:,k] * square
				new_sigmas[k] = np.sqrt(np.sum(num) / np.sum(likMatrix[:,k], axis=0))

		# Update theta #
		for k in range(_K): 
			if estimate_priors:	
				theta[k][0] = new_priors[k]
			if estimate_means:	
				theta[k][1] = new_means[k]
			if estimate_sigmas:	
				theta[k][2] = new_sigmas[k]

		# Get current Likelihood #
		oldLik = curLik
		curLik = log_likelihood(data, theta) 
		# Print iteration info #
		print("Iteration {:>4}".format(iteration) + ", Priors: " +
		str(np.around(theta[:,0],7))+ ", Means: " +
		str(np.around(theta[:,1],7)) + ", Sigmas: " +
		str(np.around(theta[:,2],7)) +" log_likelihood: " + str(curLik))
		# Next iteration # 
		iteration += 1

	# EM has finished #
	print("-----------------------------------------------------")
	print("Final log_likelihood: ", log_likelihood(data, theta))
	print("Final priors: ", np.around(theta[:,0],7))
	print("Final  means: ", np.around(theta[:,1],7))
	print("Final sigmas: ", np.around(theta[:,2],7))
	return theta

"""
	Always returns the same data from specified parameters. This is an academic example.
	If you want to use this with more than 2 gaussians, you should only manage the new data.
	Gaussian one: 
		prior 0.3 | mean 5 | std 1 
	Gaussian two 
		prior 0.7 | mean -2 | std 3  
"""
def getToyData(_K = 2):
	N1 = 3000 
	N2 = 7000
	real_theta = np.zeros((_K, 3))
	real_theta[0] = [0.3, 5, 1]
	real_theta[1] = [0.7, -2, 3]
	x1 = np.random.normal(real_theta[0,1], real_theta[0,2], N1)
	x2 = np.random.normal(real_theta[1,1], real_theta[1,2], N2)
	return np.array(x1), np.array(x2), real_theta

def run(estimate_priors, estimate_means, estimate_sigmas, _K = 2):
	fig = plt.figure()
	# Get data 
	x1, x2, real_theta = getToyData(_K)
	data = np.concatenate((x1, x2))
	# Plot initial data 
	ax = fig.add_subplot(1,3,1)
	ax.set_title("Real")
	ax.set_ylim([0,0.25])
	plotData(_K, data, real_theta)
	# Run EM over the incomplete data # 
	theta = EM(data, real_theta, fig, estimate_priors, estimate_means, estimate_sigmas, _K=2)
	# Plot the initial distribution #
	ax = fig.add_subplot(1,3,3)
	ax.set_title("Final")
	ax.set_ylim([0,0.25])
	plotData(_K, data, theta)
	plt.show()

if __name__ == "__main__": 
	print("This is an academic example with the objective of understand the E.M. algorithm. \n" +
		  "In this example we estimate by max-loglikelihood the best gaussian mixtures to explain \n" + 
		  "a set of data generate using two gaussins.")
	inPrior = input("Do you want to estimate the prior probabilities? [Y/n]: ")
	inMeans = input("Do you want to estimate the means? [Y/n]: ")
	inSigmas = input("Do you want to estimate the sigmas? [Y/n]: ")
	estimate_priors = estimate_means = estimate_sigmas = False
	if inPrior.lower() in ['y', 'yes', 'si'] :
		estimate_priors = True
	if inMeans.lower() in ['y', 'yes', 'si'] :
		estimate_means = True
	if inSigmas.lower() in ['y', 'yes', 'si'] :
		estimate_sigmas = True
	run(estimate_priors, estimate_means, estimate_sigmas)
	print("I hope you enjoyed the EM algorithm (-;")
