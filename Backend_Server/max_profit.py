# from math import *; 
# def drange(start, stop, step):
#     r = start
#     while r < stop:
#         yield r
#         r += step

# def maxResult(n, a, b, c) : 
# 	maxVal = 0; 
# 	for i in drange(0.0001, n + 1, a) : 

# 		for j in drange(0.0001, n - i + 1, b) : 
# 			z = (n - (i + j)) / c; 
# 			if (1) : 
# 				x = i // a
# 				y = j // b 
# 				maxVal = max(maxVal, (0.15*x) + (0.07*y) + (0.02*int(z)))
# 				maxVal2 = max(maxVal, x + y + int(z))
# 				print(x)
# 				print(y)
# 				print(int(z))
# 				if(x == 0 or y == 0 or z == 0):
# 				    maxResult(n, a, b, c)                
# 	return maxVal2; 

# if __name__ == "__main__" : 
	
# 	n = 3000
# 	a = 0.15
# 	b = 0.23
# 	c = 0.4
	
# 	print(maxResult(n, a, b, c)); 

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import nnls 

A = np.array([[60, 90, 120],[60, 90, 120]])

b = np.array([67.5, 67.5])

x, rnorm = nnls(A,b)

print (x)
#[ 0.          0.17857143  0.42857143]
print (rnorm)
#0.0