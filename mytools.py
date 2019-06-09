# -*- coding: utf-8 -*-

""" Some functions.
"""

from __future__ import division  # it's nesessary if you use python2
import numpy as np
import pandas as pd
from time import time


def load_matrices(filename, size):
	""" Load matrices from file.
	Return array of matrices.
	"""
	try:
		arr = pd.read_csv(filename, header=None, index_col=0).values
	except:
		print('Can not read file {}'.format(filename))
		raise
	return arr


def timer(msg='', ls = [0,'']):
	""" Timer
	"""
	if ls[0]:
		print('TIME: {0:.4f} sec. ({1})'.format(time() - ls[0], ls[1]))
	else:
		print('START TIMER {0}'.format(ls[1]))
	ls[0] = time()
	ls[1] = msg
		
	
if __name__ == '__main__':
	""" Testing
	"""
	timer("Test timer")
	timer()
	
	
