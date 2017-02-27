import numpy
#=================================================
#=================start data======================
#=================================================
# inverse 
# A = numpy.matrix([[-2,-1,1,-7,0,0,0,2],
# 				  [4,2,1,0,1,5,-1,-5],
# 				  [1,1,0,-1,0,3,-1,1]])

# b = numpy.matrix([-2, 4, 3])

# c = numpy.matrix([2, 2, 1, -10, 1, 4, -2, -3])

# y_begin =  numpy.matrix([1, 1, 1])

# Jb = [2, 5, 7]

# delta_koplan = y_begin * A - c

#+++++++++++++++++++++++++++++++++++++++++++++++++
# inverse 
# A = numpy.matrix([[-2,-1,1,-7,0,0,0,2],
# 				  [4,2,1,0,1,5,-1,-5],
# 				  [1,1,0,1,0,3,1,1]])

# b = numpy.matrix([-2, 4, 3])

# c = numpy.matrix([2,2,1,-10,1,4,0,-3])

# y_begin =  numpy.matrix([1,1,1])

# Jb = [2, 5, 7]

# delta_koplan = y_begin * A - c

#+++++++++++++++++++++++++++++++++++++++++++++++++++++
# inverse 
# A = numpy.matrix([[-2,-1,1,-7,1,0,0,2],
# 				  [-4,2,1,0,5,1,-1,5],
# 				  [1,1,0,1,4,3,1,1]])

# b = numpy.matrix([-2, 8, -2])

# c = numpy.matrix([12,-2,-6,20,-18,-5,-7,-20])

# y_begin =  numpy.matrix([-3, -2, -1])

# Jb = [2, 4, 6]

# delta_koplan = y_begin * A - c
#++++++++++++++++++++++++++++++++++++++++++++++++++++++
inverse = True

A = numpy.matrix([[0,-1,-1,1,0,0],
				  [-2,-1,-2,0,1,0],
 				  [-2,1,-2,0,0,1]])

b = numpy.matrix([-4,-6,-2])

c = numpy.matrix([-3, -2, -1, 0, 0, 0])

y_begin =  numpy.matrix([0.5,0.25,0.25])

Jb = [4, 5, 6]

delta_koplan = y_begin * A - c

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
# inverse = 
# A = numpy.matrix([[-2,-1,1,-7,0,0,0,2],
# 				  [4,2,1,0,1,5,-1,-5],
#  				  [1,1,0,-1,0,3,-1,1]])

# b = numpy.matrix([-2,-4,-2])

# c = numpy.matrix([5, 2, 3, -16, 1, 3, -3, -12])

# y_begin =  numpy.matrix([1,2,-1])

# Jb = [1,2,3]

# delta_koplan = y_begin * A - c

#=================================================
#================help functions===================
#=================================================
infinity = float("inf")

def sigma_helper(u_j, delta_j):
	if u_j < 0:
		return  -delta_j / u_j
	else:
		return infinity 

def iteration(y_begin, Jb, A, b, c, delta_koplan):
	Jn = [i+1 for i in xrange(c.size) if i+1 not in Jb]
	A_transpose = A.transpose()
	Ab = numpy.matrix([A_transpose[j-1].tolist()[0] for j in Jb ]).transpose()
	B =  numpy.linalg.inv(Ab)
	print Ab
	print B

	chi = (B * b.transpose()).transpose()
	chi_list = chi.tolist()[0]
	print chi_list
	if all ((i >= 0) for i in chi_list):
		print "Optimal plan"
		answer = [0 for i in xrange(c.size)]
		chi_list.reverse()
		for index in Jb:
			answer[index - 1] = chi_list.pop()
		return answer

	for i in xrange(chi.size):
		if chi.item(i) < 0:
			k = i + 1
			break
	j_k = Jb[k - 1]
	u = B[k - 1] * A


	sigma = [sigma_helper(u.item(i - 1), delta_koplan.item(i - 1)) for i in Jn ]
	sigma_0 = min(sigma)

	if sigma_0 == infinity:
		print "No root, because restrictions are incompatible"
		return
		
	s = sigma.index(sigma_0) + 1
	j_0 = Jn[s - 1]

	y_new = y_begin + sigma_0 * B[k - 1]
	delta_koplan = delta_koplan + sigma_0 * u
	Jb[k - 1] = j_0
	#delta_koplan =  y_new * A - c
	return iteration(y_new, Jb, A, b, c, delta_koplan)

x_solve = iteration(y_begin, Jb, A, b, c, delta_koplan)
if x_solve:
	c_list = [c.item(i) for i in xrange(c.size)]
	if inverse:
		answer = sum([a*-b for a,b in zip(x_solve,c_list)])
	else:
		answer = sum([a*-b for a,b in zip(x_solve,c_list)])
	print x_solve
	print answer