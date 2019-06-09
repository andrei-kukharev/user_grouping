# -*- coding: utf-8 -*-

""" Generation of the csv-file with user matrices
"""

import numpy as np
import pandas as pd		
	

def gen_matrices(number, size, deviation):
	"""	Create array of matrices:
	
	Parameters
	----------
	number : int  - number of matrices
	size : int - number of coefficients (features), default = 100 = 10*10
	deviation : float - standard deviation
	
	Returns
	-------
	arr : np.array - array where each row is a matrix
	"""
	arr = np.empty(shape=(number,size), dtype=np.float16)
	
	for i in range(0, number):
		mat = np.random.normal(size=size, scale=deviation)
		mat = mat.astype(np.float16)
		mat = np.where( ( mat >= -1) & ( mat <= 1 ), mat, 0)
		arr[i] = mat

	return arr


def save_matrices_to_csv(filename, arr):	
	"""
	Save given array in csv file
	"""
	df = pd.DataFrame(arr)
	df.to_csv(filename, sep=',', header=False, float_format='%.2f')
	
	
if __name__ == '__main__':
		
	# Generate array of matrices
	number = 1001
	arr = gen_matrices(number=number, size=100, deviation=0.195)
	save_matrices_to_csv('matrices.csv', arr)
	
	
	
	