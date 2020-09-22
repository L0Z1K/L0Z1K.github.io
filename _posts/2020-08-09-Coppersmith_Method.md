---
layout: post
title: Finding small roots of modular equations in univariate case
category: research
---

In this article, we present the Coppersmith method to find small roots of a monic univariate polynomial. I recommend to read [The Basic Concepts of LLL](/research/2020/08/07/The_basic_concepts_of_LLL/) first.

We want to efficiently find all the solutions $$x_0$$ satisfying,

$$
f(x_0)=0\mod{N}\hspace{0.2cm}with \hspace{0.1cm}|x_0|\leq X
$$

<br>
**Howgrave-Graham** : Let $$g(x)$$ be an univariate polynomial of degree $$\delta$$. Further, let $$m$$ be a positive integer. Suppose that

$$
g(x_0)=0\mod N^{m}\hspace{0.2cm}where\hspace{0.1cm}|x_0|\leq X\\
\|g(xX)\|<\frac{N^m}{\sqrt{\delta+1}}
$$

Then $$g(x_0)=0$$ holds over the integers.

This theorem simply saids that if coefficients of polynomial is small enough, we can solve the polynomial with the exception of modular. Therefore, **using the LLL learned before to make the coefficient smaller, you can find the roots of polynomial more efficiently.**


<br>
**Coppersmith** : Let $$f(x)$$ be a univariate monic polynomial of degree $$\delta$$. Let $$N$$ be an integer of unknow factorization. And let $$\epsilon>0$$. Then we can find all soultions $$x_0$$ for the equation,

$$
f(x)=0\mod N \hspace{0.2cm}with\hspace{0.1cm}|x_0|\leq\frac{1}{2}N^{\frac{1}{\delta}-\epsilon}
$$

<br>

$$Proof.$$ If we set $$m=\left \lceil\frac{1}{\delta\epsilon} \right\rceil$$ and $$X=\frac{1}{2}{N}^{\frac{1}{\delta}-\epsilon}$$, we can prove Coppersmith method by using Howgrave-Graham.

First, for using LLL, we have to construct a lattice with a collection of polynomials, where each polynomial has a root $$x_0$$ modulo $$N^m$$.

$$
g_{i,j}(x)=x^{j}N^{i}f^{m-i}(x)\hspace{0.2cm}for\hspace{0.2cm}i=1,...,m\hspace{0.2cm}and\hspace{0.2cm}j=0,...,\delta-1
$$

<br>

Then we construct the lattice $$\Lambda$$ that is spanned by the coefficient vectors of $$g_{i,j}(xX)$$ :

$$
\Lambda =\begin{bmatrix}
NX^{\delta m-1} & - & - & \dots & \dots & \dots& \dots& \dots & - \\
0 & \ddots \\
0 & \dots & NX^{\delta m-\delta +1} & - & \dots& \dots& \dots & \dots & - \\
0 & \dots & 0 & NX^{\delta m-\delta} & - & \dots& \dots& \dots & - \\
 & & & &\ddots & \ddots \\
0 & \dots & \dots &\dots & \dots & N^{m}X^{\delta -1} & 0 &\dots & 0 \\
& & & & &  & \ddots & &  \\
0 & \dots& \dots& \dots& \dots& \dots& 0&N^mX&0\\
0 & \dots& \dots& \dots& \dots& \dots& \dots&0&N^m\\
\end{bmatrix}
$$

<br>

Of course, you can't understand this lattce easily. I'll give you example below the article.

<br>

The rank of the lattice is $$\delta m$$. We can easily compute the determinant because this lattice is triangular.

$$
\det \Lambda = N^{\frac{1}{2}\delta m(m+1)}X^{\frac{1}{2}\delta m(\delta m-1)}
$$

<br>

Then make 2-reduced basis($$c=2$$) with LLL. We can get new polynomial $$g(x)$$ with the first vector of the basis $$\bf{b_1}$$ and it satisfies Howgrave-Graham theorem because of LLL properties.

$$
\|g(xX)\|=\|{\bf b_1}\|<\frac{N^m}{\sqrt{\delta m}}<\frac{N^m}{\sqrt{\delta+1}}
$$

<br>

## Applications

We can use the coppersmith method to solve the Relaxed RSA problem where e is small and we have an approximation $$M'$$ of $$M$$ such that $$M=M'+x_0$$ for some unknown part $$\lvert x_0\rvert \leq N^{\frac{1}{e}}$$ .

$$
\begin{align*}
c &=M^e \mod N\\
  &=(M'+x_0)^e \mod N\\
\end{align*}
$$

$$
f(x)=(M'+x_0)^e-c \mod N
$$

<br>

Let's find the roots of $$f(x)$$. I make the problem and solved it with [sage](https://www.sagemath.org). 

<br>

First, we should make the keys for RSA.

```python
from Crypto.Util.number import getPrime
from random import getrandbits

p, q = getPrime(512), getPrime(512)
N = p*q
e = 3
```

e should be small.

<br>

Make $$M$$ and we can get the $$M$$ except for 170 bits($$a$$).

```python
plaintext = getrandbits(512)
ans = plaintext % 2**170
a = plaintext - ans
```

We should solve the $$ans$$. 

<br>

Encryption.

```python
c = pow(plaintext, e, N)
```

<br>

$$X$$ is the upper bound of $$x$$. Therefore,

$$
X = 2^{170}
$$

<br>

Check the $$f(x)$$.

$$
\begin{align*}
f(x)&=(a+x)^3-c\\
&=x^3+3ax^2+3a^2x+a^3-c
\end{align*}
$$

$$f(x)$$ is a monic univariate polynomial, degree of $$f(x)$$ is 3.

$$
\delta=3
$$

<br>

Solve the $$\epsilon$$. If $$\epsilon$$ is big, LLL can be computed faster.

$$
X\leq \frac{1}{2}N^{\frac{1}{\delta}-\epsilon}\\
\begin{align*}
\Rightarrow \epsilon &\leq \frac{1}{\delta}-\log_{N}{2X}\\
&\simeq 0.167
\end{align*}
$$

<br>

Solve the $$m$$.

$$
\begin{align*}
m&=\left \lceil \frac{1}{\delta\epsilon}\right\rceil\\
&=2
\end{align*}
$$

<br>

Construct the lattice.

```python
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
```

<br>

Do LLL and make new polynomials and GET THE ROOT!

```python
M = M.LLL()
f_new = 0
for i in range(rank):
    f_new += M[0][i] * x**(rank-1-i) / X**(rank-1-i)

print(f_new.roots()[0][0])
```

<br>

SUCCESS!!

```python
if f_new.roots()[0][0] == ans:
    print("SUCCESS")
else:
    print("FAIL")
```

<br>

Result is

```bash
$ sage ex.sage
558434381386214027963442801767805533534639529673598
SUCCESS
```

<br>

I uploaded the whole sage file below this article.


<a class = "btn" href="/docs/2020-08-09-solve.sage" download>Download file</a>






<br>

### References

[LLL lattice basis reduction algorithm - Helfer Etienne](https://algo.epfl.ch/_media/en/projects/bachelor_semester/rapportetiennehelfer.pdf)

- - -