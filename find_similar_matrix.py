# -*- coding: utf-8 -*-

import math
import numpy as np
import pandas as pd
from mytools import *

def distance(arr, i, j, metric='part', percent=70.0):
	"""	Find the distance between two matrices i and j in given metric ('quad' or 'user'):
	'full' - standard deviation (all features is accounted);
	'part' - we take to account not all features (only given percent);
	
	>>> arr = np.array([[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]])
	>>> distance(arr, 0, 1, metric='full')
	1.0
	>>> distance(arr, 0, 1, metric='part', percent=70.0)
	1.0
	>>> arr = np.array([[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 50.0]])
	>>> distance(arr, 0, 1, metric='part', percent=70.0)
	1.0
	"""
	number_features = arr.shape[1] # total number of feature
	
	if metric == 'full':		
		dist = sum(np.square(arr[i,:] - arr[j,:])) / number_features
		
	elif metric == 'part':
		diff = abs(arr[i,:] - arr[j,:])
		diff.sort()		
		slice_len = int(math.ceil(percent / 100.0 * number_features))
		dist = sum(np.square(diff[0:slice_len])) / slice_len
	
	else:
		dist = 0
		
	return dist


def find_the_most_similar_matrix(arr, index, metric='part'):
	"""
	Find the most similar matrix to a matrix given by index.	
	Returns:
	index_similar_matrix, min_dist : int, float
	"""
	dist_to_i = [ distance(arr, index, j, metric=metric) for j in range(arr.shape[0]) if j != index ]
	min_dist = min(dist_to_i)
	index_similar_matrix = np.argmin(dist_to_i)			 
	return index_similar_matrix, min_dist


def run():
	
	array_matrices = load_matrices(filename='matrices.csv', size=100)
	number = array_matrices.shape[0]  # number of matrices
	
	index_given_matrix = 875
	
	index_similar_matrix, min_dist = find_the_most_similar_matrix(array_matrices, index=index_given_matrix, metric='part')
		
	print('Given matrix: {0}'.format(index_given_matrix))
	print('Similar matrix: {0}'.format(index_similar_matrix))
		
	diff = abs(array_matrices[index_given_matrix]- array_matrices[index_similar_matrix])
	s = ''.join(['{0:5.2f} : {1:5.2f} : {2:5.2f} : {3}\n'.format(x1,x2,d,b) for (x1,x2,d,b) in 
		zip(array_matrices[index_given_matrix], 
			array_matrices[index_similar_matrix], 
			diff,
			map(lambda b: '+' if b else '', diff <= 0.2)
			)
		]) 
	print('\nGiven :Similar:  Diff : d<0.2')
	print('-----------------------------')
	print(s)		
	
	count_similar_features = np.count_nonzero(diff <= 0.2)
	print('Count_similar_features = {0}'.format(count_similar_features))
	
	
if __name__ == '__main__':
	
	import doctest
	doctest.testmod()
	
	run()


"""
OUTPUT

$ python find_similar_matrix.py
Given matrix: 875
Similar matrix: 798

Given :Similar:  Diff : d<0.2
-----------------------------
-0.19 : -0.01 :  0.18 : +
-0.13 : -0.14 :  0.01 : +
 0.23 :  0.15 :  0.08 : +
 0.43 : -0.37 :  0.80 : 
-0.11 : -0.15 :  0.04 : +
-0.26 : -0.08 :  0.18 : +
-0.04 :  0.19 :  0.23 : 
-0.20 :  0.05 :  0.25 : 
-0.11 : -0.10 :  0.01 : +
 0.24 :  0.06 :  0.18 : +
-0.25 : -0.08 :  0.17 : +
-0.18 : -0.35 :  0.17 : +
-0.04 :  0.01 :  0.05 : +
 0.05 : -0.02 :  0.07 : +
-0.12 : -0.12 :  0.00 : +
-0.07 :  0.13 :  0.20 : +
-0.20 :  0.04 :  0.24 : 
 0.18 : -0.13 :  0.31 : 
 0.00 : -0.09 :  0.09 : +
-0.11 :  0.36 :  0.47 : 
 0.07 :  0.18 :  0.11 : +
 0.29 :  0.29 :  0.00 : +
-0.01 :  0.32 :  0.33 : 
 0.10 :  0.22 :  0.12 : +
-0.31 :  0.07 :  0.38 : 
-0.06 : -0.12 :  0.06 : +
-0.10 : -0.05 :  0.05 : +
 0.12 : -0.42 :  0.54 : 
 0.11 :  0.14 :  0.03 : +
-0.01 :  0.03 :  0.04 : +
 0.36 :  0.13 :  0.23 : 
 0.18 :  0.12 :  0.06 : +
 0.46 :  0.10 :  0.36 : 
 0.13 :  0.15 :  0.02 : +
-0.19 : -0.02 :  0.17 : +
 0.11 :  0.01 :  0.10 : +
-0.22 :  0.02 :  0.24 : 
-0.10 : -0.26 :  0.16 : +
-0.19 :  0.18 :  0.37 : 
-0.20 : -0.01 :  0.19 : +
-0.21 : -0.14 :  0.07 : +
-0.03 :  0.06 :  0.09 : +
-0.34 : -0.22 :  0.12 : +
-0.21 : -0.06 :  0.15 : +
-0.00 :  0.13 :  0.13 : +
 0.09 :  0.05 :  0.04 : +
-0.24 :  0.02 :  0.26 : 
 0.12 : -0.08 :  0.20 : +
-0.06 : -0.05 :  0.01 : +
-0.12 :  0.03 :  0.15 : +
 0.09 :  0.06 :  0.03 : +
 0.11 : -0.33 :  0.44 : 
 0.38 : -0.18 :  0.56 : 
-0.17 : -0.01 :  0.16 : +
-0.34 :  0.08 :  0.42 : 
 0.09 : -0.17 :  0.26 : 
 0.01 : -0.11 :  0.12 : +
-0.04 : -0.15 :  0.11 : +
 0.38 : -0.22 :  0.60 : 
 0.01 :  0.08 :  0.07 : +
-0.07 :  0.28 :  0.35 : 
 0.04 : -0.11 :  0.15 : +
 0.10 :  0.05 :  0.05 : +
-0.06 : -0.18 :  0.12 : +
 0.11 :  0.03 :  0.08 : +
 0.26 :  0.32 :  0.06 : +
-0.37 : -0.20 :  0.17 : +
-0.43 : -0.14 :  0.29 : 
-0.21 : -0.10 :  0.11 : +
 0.19 :  0.07 :  0.12 : +
 0.00 : -0.21 :  0.21 : 
-0.14 : -0.24 :  0.10 : +
 0.14 :  0.16 :  0.02 : +
-0.08 : -0.11 :  0.03 : +
-0.28 : -0.59 :  0.31 : 
-0.30 :  0.14 :  0.44 : 
 0.11 :  0.19 :  0.08 : +
-0.05 : -0.13 :  0.08 : +
 0.05 : -0.09 :  0.14 : +
 0.39 :  0.40 :  0.01 : +
-0.19 : -0.14 :  0.05 : +
 0.05 : -0.11 :  0.16 : +
-0.07 :  0.23 :  0.30 : 
 0.17 : -0.05 :  0.22 : 
-0.55 : -0.17 :  0.38 : 
 0.13 :  0.23 :  0.10 : +
-0.04 : -0.05 :  0.01 : +
 0.08 :  0.21 :  0.13 : +
 0.13 :  0.26 :  0.13 : +
 0.12 : -0.25 :  0.37 : 
-0.05 : -0.20 :  0.15 : +
 0.13 :  0.31 :  0.18 : +
 0.14 :  0.09 :  0.05 : +
 0.15 :  0.25 :  0.10 : +
-0.12 : -0.11 :  0.01 : +
 0.21 :  0.18 :  0.03 : +
-0.12 : -0.10 :  0.02 : +
-0.29 : -0.22 :  0.07 : +
 0.06 :  0.26 :  0.20 : +
 0.27 :  0.09 :  0.18 : +

Count_similar_features = 72



"""
