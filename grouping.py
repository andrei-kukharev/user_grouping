# -*- coding: utf-8 -*-

""" The grouping of user matrices with Networkx
"""

from __future__ import division  # can be run on python2

import sys
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from mytools import *
from genmatrices import gen_matrices


def is_similar(arr, i1, i2, maxdist = 0.2, percent = 0.7):
	""" Comparing two matrices.
	
	Parameters
	----------
	arr : np.array - Array of "matrices"
	i1, i2 : int	- Rows of the array where our matrices is located
		arr[i1,:] is the first matrix 
		arr[i2,:] is the second matrix 
	
	Returns
	-------
	issimilar : bool - True if the matrices is similar to each other

	>>> arr = np.array([[1.0, 1.0, 1.0, 1.0], [1.3, 1.3, 1.1, 1.1]])
	>>> is_similar(arr, 0, 1, maxdist = 0.2, percent = 0.7)
	False
	>>> is_similar(arr, 0, 1, maxdist = 0.2, percent = 0.3)
	True
	>>> is_similar(arr, 0, 1, maxdist = 0.4, percent = 0.7)
	True
	"""
	
	count = np.count_nonzero(abs(arr[i1,:] - arr[i2,:]) <= maxdist)		
	issimilar = count/arr.shape[1] > percent
		
	#if i1==813 and i2==952:
	#	print('arr1 = \n{0}'.format(arr[i1,:]))
	#	print('arr2 = \n{0}'.format(arr[i2,:]))
	#	print('count = {0}'.format(count))
	#	print('maxdist = {0}'.format(maxdist))
	#	print('percent = {0}'.format(percent))
	#	print('arr.shape[1] = {0}'.format(arr.shape[1]))
		
	#	diff = abs(arr[i1,:] - arr[i2,:])
	#	sim = list(map(lambda b: '+' if b else '', diff <= 0.2))
		
	#	for i in range(arr.shape[1]):
	#		print("{0}: {1:5.2f} : {2:5.2f} : {3} : {4}".format(i, arr[i1,i], arr[i2,i], diff[i], sim[i] ))			
	#	sys.exit(0)
	
	return issimilar


def similarity(arr):
	"""
	Parameters
	----------
	arr : np.array - Array of "matrices"
	
	Returns: 
	-------
	adj_matrix, number_edges : np.array, int
		adj_matrix is the adjacency matrix of corresponded graph
		number_edges is the number of connections	
	"""
	
	dim = arr.shape[0]
	adj_matrix = np.zeros(shape=(dim,dim), dtype=np.int8)
	number_edges = 0	

	for i1 in range(dim):
		for i2 in range(i1+1, dim):
			if is_similar(arr, i1, i2):
				adj_matrix[i1,i2] = 1
				adj_matrix[i2,i1] = 1
				number_edges += 1	

	return adj_matrix, number_edges


def analysis_with_networkx():
	
	timer('Load data')
	
	array_matrices = load_matrices(filename='matrices.csv', size=100)
	total_number = array_matrices.shape[0]  # total number of matrices
	
	### or generate it right here:
	#number = 1001
	#array_matrices = gen_matrices(number=number, size=100, deviation=0.195)
		
	timer('grouping of matrices')
	
	adj_matrix, number_edges = similarity(array_matrices)
		
	timer('create a graph')
		
	G = nx.from_numpy_matrix(adj_matrix)

	timer('find connected components')

	#nontrivial_components = filter(lambda x: len(x)>1, nx.connected_component_subgraphs(G))
	components = nx.connected_component_subgraphs(G)

	# OUTPUT
	timer('draw graph')
		
	plt.rcParams["figure.figsize"] = (12, 9)	

	try:
		pos = nx.graphviz_layout(G, prog="neato")		
		# if it doesn't work, try this: sudo apt-get install -y python-pygraphviz
	except:
		print('graphviz is not installed')
		pos = nx.random_layout(G)

	number_isolated = 0
	total_num_components = 0
		
	print('\nConnected components which content more than one vertex:')
	for i, comp in enumerate(components):
		total_num_components += 1
		if len(comp) > 1:
			print('- component #{0} ({1:.2f}%): {2}'.format(i, len(comp)* 100.0/total_number, comp ))
			nx.draw(comp, pos=pos, node_size=35, with_labels = True)
		else:
			number_isolated += 1
	
	#nx.draw(G, pos=pos, node_size=35, with_labels = True) # with_labels = True
	
	plt.savefig("graph_networkx.png")
	#plt.show()
	
	#number_isolated = sum([len(c)==1 for c in components])
	percent_isolated = number_isolated * 100.0 / total_number 
	percent_grouped = 100 - percent_isolated
	print('Total number of vertices = {0}'.format(total_number))
	print('Number of isolated vertices = {0}'.format(number_isolated))
	print('Number of connections (edges) = {0}'.format(number_edges))
	print('Number of connected components (groups) = {0}'.format(total_num_components))
	print('The percentage of isolated vertices = {0:.2f}%'.format(percent_isolated))
	print('The percentage of grouped vertices = {0:.2f}%'.format(percent_grouped))
	
	if percent_grouped < 5.0:
		print('Very few grouped vertices')
	
	timer()

	
if __name__ == '__main__':
	
	import doctest
	doctest.testmod()
	
	analysis_with_networkx()  


	
"""
OUTPUT

$ python grouping.py 
START TIMER 
TIME: 0.0465 sec. (Load data)
TIME: 19.4709 sec. (grouping of matrices)
TIME: 0.0284 sec. (create a graph)
Total number of vertices = 1001
Number of isolated vertices = 720
Number of connections (edges) = 241
Number of connected components (groups) = 765
The percentage of isolated vertices = 71.93%
The percentage of grouped vertices = 28.07%

Connected components which content more than one vertex:
- component #0 (0.30%): [0, 149, 791]
- component #3 (0.60%): [482, 3, 842, 738, 117, 29]
- component #6 (13.59%): [513, 342, 6, 521, 15, 530, 21, 539, 35, 37, 38, 552, 554, 43, 563, 52, 53, 571, 60, 67, 69, 583, 72, 77, 78, 596, 600, 601, 91, 92, 605, 608, 609, 610, 615, 18, 632, 122, 639, 642, 644, 139, 140, 653, 658, 661, 150, 161, 283, 678, 172, 815, 178, 179, 693, 698, 189, 191, 707, 233, 460, 206, 774, 215, 216, 229, 744, 745, 234, 750, 246, 258, 262, 898, 279, 795, 804, 809, 812, 302, 303, 307, 310, 311, 829, 319, 833, 823, 844, 850, 854, 856, 347, 348, 861, 868, 874, 365, 878, 373, 375, 381, 166, 384, 897, 386, 387, 903, 396, 404, 917, 407, 411, 929, 934, 423, 937, 428, 430, 437, 954, 444, 961, 965, 966, 332, 971, 972, 469, 985, 988, 989, 485, 935, 338, 498]
- component #16 (0.60%): [419, 998, 17, 274, 766, 671]
- component #31 (0.50%): [904, 841, 674, 36, 255]
- component #40 (0.20%): [48, 176]
- component #43 (0.80%): [66, 517, 391, 275, 684, 467, 721, 51]
- component #44 (1.20%): [164, 901, 939, 781, 336, 626, 54, 695, 570, 507, 380, 794]
- component #54 (0.40%): [120, 65, 787, 646]
- component #58 (0.20%): [73, 126]
- component #73 (0.30%): [568, 944, 90]
- component #74 (0.20%): [747, 93]
- component #77 (0.20%): [96, 432]
- component #83 (0.20%): [728, 102]
- component #84 (0.20%): [711, 103]
- component #89 (0.30%): [772, 907, 108]
- component #92 (1.00%): [225, 324, 581, 111, 115, 885, 759, 472, 516, 219]
- component #97 (0.40%): [353, 980, 118, 127]
- component #101 (0.30%): [824, 124, 982]
- component #105 (0.20%): [641, 130]
- component #106 (0.20%): [656, 131]
- component #110 (0.20%): [637, 135]
- component #119 (0.20%): [146, 652]
- component #130 (0.30%): [969, 962, 159]
- component #134 (0.20%): [273, 165]
- component #151 (0.30%): [187, 484, 230]
- component #153 (0.40%): [777, 284, 190, 873]
- component #169 (0.20%): [208, 660]
- component #198 (0.20%): [245, 567]
- component #218 (0.70%): [813, 269, 531, 663, 952, 858, 623]
- component #227 (0.40%): [282, 299, 572, 629]
- component #247 (0.20%): [905, 308]
- component #274 (0.50%): [834, 420, 378, 662, 343]
- component #307 (0.20%): [945, 388]
- component #320 (0.20%): [403, 677]
- component #321 (0.20%): [405, 773]
- component #354 (0.20%): [448, 584]
- component #385 (0.20%): [957, 486]
- component #388 (0.20%): [489, 692]
- component #417 (0.20%): [561, 524]
- component #437 (0.20%): [547, 964]
- component #456 (0.20%): [996, 575]
- component #477 (0.20%): [602, 758]
- component #519 (0.20%): [667, 942]
- component #620 (0.20%): [875, 798]
TIME: 0.0135 sec. (find connected components)
TIME: 20.3301 sec. (draw graph)
"""
