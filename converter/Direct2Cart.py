#!/usr/bin/python
import string
import numpy as np
import sys

if '--h' in sys.argv or '--help' in sys.argv or len(sys.argv) != 4:
	print 'usage: Direct2Cart.py data_in lattice_in data_out'
	print 
	exit(1)


def str2list(rawstr):
	rawlist = rawstr.strip(string.whitespace).split(' ')
	#remove space elements in list
	cleanlist = [x for x in rawlist if x !=' ' and x != '']
	return cleanlist

def array2str(raw_array):
	"""
	convert 2d array -> string
	"""
	array_str = ''
	for array_1d in raw_array:
		array_str += '%-22.16f %-22.16f %-22.16f\n' % (tuple(array_1d))

	return array_str

def get_data_array(filename):
	"return a 2d array of list of absolute coordinates."
	file_obj = open(filename, 'rU')
	content_list = []
	for line_str in file_obj:
		line_list = str2list(line_str)
		content_list.append(line_list)
	file_obj.close()

	return np.float64(np.array(content_list))

def get_axes(filename):
	"return a (3, 3) array of axes"
	axes_array = get_data_array(filename)
	if axes_array.shape != (3, 3):
		raise ValueError('3*3 matrix is expected')
	else:
		return np.float64(axes_array)

def get_abs_coord(abs_array, axes_array):
	"Use Ax = b to get absolute coordinates array"
	abs_matrix = np.matrix(abs_array)
	axes_matrix = np.matrix(axes_array)

	return np.array(abs_matrix * axes_matrix)

#get filenames
data_file = sys.argv[1]
axes_file = sys.argv[2]
out_file = sys.argv[3]
abs_array = get_data_array(data_file)
axes_array = get_axes(axes_file)
rel_array = get_abs_coord(abs_array, axes_array)
#create relative coordinate file
f = open(out_file, 'w')
content_str = array2str(rel_array)
f.write(content_str)
f.close()
