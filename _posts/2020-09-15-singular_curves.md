---
layout: post
title: Don't Use Singular Curves in ECC
category: archived
---

In mathematics, an elliptic curve is a plane algebraic curve defined by an equation of the form

$$
y^{2}=x^{3}+ax+b
$$

which is **non-singular**.

<br>

If curve is singular, it means that the discriminant is zero.

$$
\Delta=4a^{3}+27b^{2}=0
$$

**We must not use singular curve in ECC.** If we use singular curve, it enables to solve ECDLP faster. Because that curve is isomorphic to multiplicative group.

<br>

There is a multiple root in $$x^{3}+ax+b=0$$ when the discriminant is zero. It can be divided into two cases.

First, it has triple root. In this case, we can substitute the polynomial to $$x^{3}$$.

Second, it does not. In this case, we can substitute the polynomial to $$x^{2}(x+a)$$.

<br>

#### When $$y^{2}=x^{3}$$,

We can substitute elliptic curve points to multiplicative group,

$$
(x,y) \mapsto \frac{x}{y}
$$


#### When $$y^{2}=x^{2}(x+a)$$,

If there exists $$\alpha$$ such that $$\alpha^{2}=a$$, we can substitute samely.

$$
(x,y) \mapsto \frac{y+\alpha x}{y-\alpha x}
$$


### Example

We begin with the singular curve

$$
y^{2}=x^{3}+17230x+22699
$$

```python
sage: p = 23981
sage: P.<x,y> = PolynomialRing(GF(p))
sage: f = y^2 - (x^3 + 17230*x + 22699)
```

You can recognize that discriminant is zero.

```python
sage: (4*17230^3+27*22699^2) % p
0
```

It has singular point and we can find that point with sage.

```python
sage: g = x^3 + 17230*x + 22699
sage: g.factor()
(x - 370) * (x + 185)^2
```

$$(-185, 0)$$ is a singular point! So Let's translate the curve by changing variables

$$
(x, y)\mapsto(x-(-185), y)
$$

```python
sage: f = f(x+(-185), y)
sage: f
-x^3 + 555*x^2 + y^2
```

$$
y^2=x^2(x-555)
$$

Let's find the square root of $$-555$$.

```python
sage: t = GF(p)(-555).square_root()
sage: t
7020
```

Now we can maps curve to the multiplicative group $$\mathbb{F}^{*}_{p}$$. The map is

$$
(x,y)\mapsto \frac{y+7020x}{y-7020x}
$$


$$P=(1451, 1362)$$, $$Q=(3141, 12767)$$. Find the $$d$$. 

```python
sage: P = (1451, 1362)
sage: Q = (3141, 12767)
sage: u = (P[1]+t*P[0])/(P[1]-t*P[0]) % p
sage: v = (Q[1]+t*Q[0])/(Q[1]-t*Q[0]) % p
sage: v.log(u)
8279
```

$$
\therefore d=8279
$$


**Conclusion : Using the singular curve in ECC is vulnerable!**



### References

[Singular curves](https://ecc.danil.co/tasks/singular/)

[How to solve this ECDLP?](https://crypto.stackexchange.com/questions/61302/how-to-solve-this-ecdlp)

- - -

