---
layout: post
title: Low-Density Attack on Subset Sum Problem
category: archived
---

The low-density attack proposed by Lagarias and Odlyzko is a powerful algorithm against the subset sum problem. What is the subset sum problem?

<br>

### Subset Sum Problem

I'll give you the set $$A$$, $$\{-100, -4, 30, 33, 37\}$$. Does there exist a subset of $$A$$ with its sum being 0?

The answer is yes. $$\{-100, 30, 33, 37\}$$ 

This is the part of the subset sum problem. 

In general, **For a given set of positive integers $$A=\{a_{1},\dots,a_{n}\}(a_{i}\neq a_{j})$$ and a given positive integers $$s$$, determining whether there exists a subset of $$A$$ with its sum being $$s$$**, is called the subset sum problem.

<br>

Subset sum problem is known as NP-hard problem. I'll introduce some algorithms to solve subset sum problems, when it has a low density.

The density $$d$$ is defined by

$$
d=n/(\log _{2}\max(a_{i}))
$$

<br>

With LO algorithm, if $$d$$ is smaller than 0.6463, we can solve the problem.
Then CJLOSS algorithm impoved the bound to 0.9408.

<br>


### LO algorithm

Finding a vector $$e = (e_{1},\dots,e_{n})\in \{0,1\}^{n}$$ satisfying $$\sum a_{i}e_{i}=s$$, is also the subset sum problem.

**Theorem 1** Let $$\beta \leq 1/2$$ be a positive rational constant, $$A$$ a positive integer, and $$a_{1},\dots,a_{n}$$ random integers with $$0<a_{i}\leq A$$ for $$1\leq i\leq n$$. Let $$e=(e_{1},\dots,e_{n})\in \{0,1\}^{n}$$ satisfy $$\sum e_{i}\leq \beta n$$ and let $$s=\sum e_{i}a_{i}$$. If density $$d <0.9408$$ , then the subset problem can be solved in polynomial-time with lattice reduction.

<br>

**How to solve** : Make the Lattice and do LLL!

$$
b_{1}=(1,0,\dots,0,Na_{1}),\\
b_{2}=(0,1,\dots,0,Na_{2}),\\
\vdots\\
b_{n}=(0,0,\dots,1,Na_{n}),\\
b_{n+1}=(0,0,\dots,0, Ns)\\
$$

$$N$$ is a positive integer larger than $$\sqrt{n}/2$$. With these vectors, we can construct the lattice.

$$
L=\begin{bmatrix}
1 & 0 & \cdots & 0 & Na_{1}\\
0 & 1 & \cdots & 0 & Na_{2}\\
& &\vdots \\
0 & 0 & \cdots & 1 & Na_{n}\\
0 & 0 & \cdots & 0 & Ns
\end{bmatrix}
$$

**CJLOSS algorithm** uses 

$$
b_{n+1}^{'}=(\beta,\dots,\beta,Ns)
$$

**That's only the difference between LO and CJLOSS.**

<br>

Then the vector $$e = (e_{1},\dots,e_{n},0)$$ is contained in $$L$$. If we make lattice $$L'$$ by CJLOSS algorithm,

$$
(e_{1}-\beta,\dots,e_{n}-\beta,0)\in L'
$$


Just doing LLL and get the answer. 

<br>


### Example

Let's solve the subset sum problem with LO algorithm and Sage.

```python
a = [13690927134943830509, 13876211706406539934, 12513159843013588990, 17967877664635797040, 5848785419645134862, 9540418589697912617, 4053923682838161582, 2164855181189798694, 5910401748741458666, 15313897890081701013, 11521138435324772070, 14135593984214959514, 5522052656667513412, 15892930505438405483, 13072045730860351016, 1936383875374537924, 17543307219144377567, 1371674957251633772, 415015434812167152, 4698213187133497266, 8035934487614551996, 11041324439930660822, 16365515575165927158, 13683880390775221476, 3737671274436834204, 8583295282709393315, 12661448542963540, 10846024688620122060, 16714645054696992400, 13299870714171914680]
n = 30
s = 123339973857697881123
```

Construct the Lattice.

```python
N = ceil(sqrt(n)/2)
B = Matrix(ZZ, n+1, n+1)

for i in range(n):
    B[i,i] = 1
    B[i,n] = N*a[i]
B[n,n] = N*s
```

Do LLL!

```python
B = B.LLL()
```

The first row of $$B$$ is 

```
[-1  0  0  0  0  0  0  0 -1 -1 -1  0 -1  0  0 -1 -1  0  0  0  0 -1  0  0  0  0  0 -1 -1 -1  0]
```

The answer is

```
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1]
```

We have to think the bit flip of answer because it is just a vector!

<br>


**Conclusion: If density is low, we can solve the subset sum problem in polynomial-time!**

<br>


### References

[Low-Density Attack Revisited](https://eprint.iacr.org/2007/066.pdf)

- - -