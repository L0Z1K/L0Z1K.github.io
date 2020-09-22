#!/usr/bin/sage

from Crypto.Util.number import getPrime
from random import getrandbits

p, q = getPrime(512), getPrime(512)
N = p*q
e = 3

plaintext = getrandbits(512)
ans = plaintext % 2**170
a = plaintext - ans

c = pow(plaintext, e, N)

P.<x> = PolynomialRing(ZZ)
f = (x+a)^3-c
f = f.change_ring(ZZ) # default ring is Zmod(N)

X = 2^170
delta = f.degree()
epsilon = 0.167
m = ceil(1/(delta*epsilon))

g=[]
for i in range(1,m+1):
    j = delta-1
    while j >= 0:
        g.append((x*X)**j * N**i * f(x*X)**(m-i))
        j -= 1

rank = m*delta
M = Matrix(ZZ, rank)
for i in range(rank):
    for j in range(rank):
        M[i, rank-1-j] = g[i][j]

M = M.LLL()
f_new = 0
for i in range(rank):
    f_new += M[0][i] * x**(rank-1-i) / X**(rank-1-i)

print(f_new.roots()[0][0])

if f_new.roots()[0][0] == ans:
    print("SUCCESS")
else:
    print("FAIL")