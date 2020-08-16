#!/usr/bin/env python3

import random 
from secret import p, flag 

def transpose(x):
	result = [[x[j][i] for j in range(len(x))] for i in range(len(x[0]))]
	return result

def multiply(A, B):
	if len(A[0]) != len(B):
		return None
	result = []
	for i in range(len(A)):
		r = []
		for j in range(len(B[0])):
			r.append(0)
		result.append(r)
	for i in range(len(A)): 
		for j in range(len(B[0])): 
			for k in range(len(B)): 
				result[i][j] += A[i][k] * B[k][j] 	
	return result

def sum_matrix(A, B):
	result = []
	for i in range(len(A)):
		r = []
		for j in range(len(A[0])):
			r.append(A[i][j]+B[i][j])
		result.append(r)
	return result

def keygen(p):
	d = random.randint(1, 2**64)
	if p % 4 == 1:
		Q = []
		for i in range(p):
			q = []
			for j in range(p):
				if i == j:
					q.append(0)
				elif pow((i-j), int ((p-1) // 2), p) == 1:
					q.append(1)
				else:
					q.append(-1)
			Q.append(q)
		Q_t = transpose(Q)
		H = []
		r = []
		r.append(0)
		r.extend([1 for i in range(p)])
		H.append(r)
		for i in range(1, p + 1):
			r = []
			for j in range(p + 1):
				if j == 0: 
					r.append(1)
				else:
					r.append(Q[i-1][j-1])
			H.append(r)

		H2 = [[0 for j in range(2*(p+1))] for i in range(2*(p+1))]
		for i in range(0, p+1):
			for j in range(0, p+1):
				if H[i][j] == 0:
					H2[i*2][j*2] = 1
					H2[i*2][j*2+1] = -1
					H2[i*2+1][j*2] = -1
					H2[i*2+1][j*2+1] = -1
				elif H[i][j] == 1:
					H2[i*2][j*2] = 1
					H2[i*2][j*2+1] = 1
					H2[i*2+1][j*2] = 1
					H2[i*2+1][j*2+1] = -1
				else:
					H2[i*2][j*2] = -1
					H2[i*2][j*2+1] = -1
					H2[i*2+1][j*2] = -1
					H2[i*2+1][j*2+1] = +1
		ID = [[(-1)**d if i == j else 0 for i in range(len(H2))] for j in range(len(H2))]
		H2 = multiply(ID, H2)
		return(H2, d)	
	else: 
		Q = []
		for i in range(p):
			q = []
			for j in range(p):
				if i == j:
					q.append(0)
				elif pow( (i-j), int ((p-1) // 2), p) == 1:
					q.append(1)
				else:
					q.append(-1)
			Q.append(q)
		Q_t = transpose(Q)
		Q_Q_t = multiply(Q, Q_t)
		H1 = []
		H1.append([1 for i in range(p+1)])
		for i in range(1, p +1):
			r = []
			for j in range(p +1):
				if j == 0: 
					r.append(-1)
				elif i == j:
					r.append(1 + Q[i-1][j-1])
				else:
					r.append(Q[i-1][j-1])
			H1.append(r)
		ID = [[(-1)**d if i == j else 0 for i in range(len(H1))] for j in range(len(H1))]
		H1 = multiply(ID, H1)
		return(H1, d)

def encrypt(msg, key): 
	matrix = key[0]
	d = key[1]
	m = [[ord(char) for char in msg ]]
	de = [[-d for i in range(len(msg))]]
	C = multiply(m, matrix)
	cipher = sum_matrix(C, de)
	return cipher

key = keygen(p)
flag = flag + (len(key[0][0]) - len(flag)) * flag[-1]
cipher = encrypt(flag, key)
print('cipher =', cipher)