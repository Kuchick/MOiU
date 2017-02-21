import numpy
#=================================================
#=================start data======================
#=================================================

# A = numpy.matrix([[0,1,4,1,0,-3,5,0],
# 				  [1,-1,0,1,0,0,1,0],
# 				  [0,7,-1,0,-1,3,8,0],
# 				  [1,1,1,1,0,3,-3,1]])

# b = numpy.matrix([6, 10, -2, 15])

# c = numpy.matrix([-5, -2, 3, -4, -6, 0, -1, -5])

# x_begin =  numpy.matrix([4, 0, 0, 6, 2, 0, 0, 5])

# Jb = [1, 4, 5, 8]

#+++++++++++++++++++++++++++++++++++++++++++++++++
# A = numpy.matrix([[0,1,4,1,0,-3,1,0],
# 				  [1,-1,0,1,0,0,0,0],
# 				  [0,7,-1,0,-1,3,-1,0],
# 				  [1,1,1,1,0,3,-1,1]])

# b = numpy.matrix([6, 10, -2, 15])

# c = numpy.matrix([-5, -2, 3, -4, -6, 0, 1, -5])

# x_begin =  numpy.matrix([10, 0, 1.5, 0, 0.5, 0, 0, 3.5])

# Jb = [1, 3, 5, 8]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++
A = numpy.matrix([[5,9,1,0,0],
				  [3,3,0,1,0],
				  [2,1,0,0,1]])

b = numpy.matrix([45, 19, 10])

c = numpy.matrix([5, 6, 0, 0, 0])

x_begin =  numpy.matrix([0, 0, 45, 19, 10])

Jb = [3, 4, 5]


#=================================================
#================help functions===================
#=================================================
infinity = float("inf")

def theta_helper(z_i, x_base_i):
	if z_i > 0:
		return x_base_i / z_i
	else:
		return infinity 

def get_new_x_and_Jb(x, theta_0, z, Jb, j_s, j0):
	x[j0-1] = theta_0
	for i in xrange(len(z)):
		x[Jb[i]-1] = x[Jb[i]-1] - theta_0*z[i]
	Jb.remove(j_s)
	Jb.append(j0)
	Jb.sort()
	return numpy.matrix(x), Jb

def iteration(x_begin, Jb, A, b, c):
	x_base_list = [x_begin.item(i - 1) for i in Jb]
	Jn = [i+1 for i in xrange(c.size) if i+1 not in Jb]
	A_transpose = A.transpose()
	Ab = numpy.matrix([A_transpose[j-1].tolist()[0] for j in Jb ]).transpose()
	B =  numpy.linalg.inv(Ab)
	cb = numpy.matrix([c.item(i-1) for i in Jb])
	u = cb * B
	delta = u * A - c
	delta_n = numpy.matrix([delta.item(i-1) for i in Jn])
	if all ((i >= 0) for i in delta_n.tolist()[0]):
		print "Optimal plan"
		return x_begin.tolist()[0]

	for i in xrange(delta.size):
		if delta.item(i) < 0 and i+1 in Jn:
			j0 = i + 1
			break
	z = B * A_transpose[j0 - 1].transpose()
	if all ((component <= 0) for component in z):
		print "Infinity solves"
		return

	theta = [theta_helper(z[i].item(0), x_base_list[i]) for i in xrange(z.size) ]

	theta_0 = min(theta)
	s = theta.index(theta_0) + 1
	j_s = Jb[s - 1]

	x_new, Jb_new = get_new_x_and_Jb(x_begin.tolist()[0], theta_0, z.transpose().tolist()[0], Jb, j_s, j0)
	return iteration(x_new, Jb_new, A, b, c)

x_solve = iteration(x_begin, Jb, A, b, c)
c_list = [c.item(i) for i in xrange(c.size)]
answer = sum([a*b for a,b in zip(x_solve,c_list)])
print x_solve
print answer