import sys
sys.path.append(".")

import sym as g
import sym as s

def testfunc():
    a=g.Symbol("a")
    b=g.Symbol("b")
    c=g.Symbol("c")
    p=g.Rational(5)
    e=a*b+g.sin(b**p)
    assert e == a*b+g.sin(b**5)
    assert e.diff(a) == b
    assert e.diff(b) == a+5*b**4*g.cos(b**5)
    e=g.tan(c)
    assert e == g.tan(c)
    assert e.diff(c) == g.cos(c)**(-2)
    e=c*g.log(c)-c
    assert e == -c+c*g.log(c)
    assert e.diff(c) == g.log(c)
    e=g.log(g.sin(c))
    assert e == g.log(g.sin(c))
    assert e.diff(c) == g.sin(c)**(-1)*g.cos(c)
    assert e.diff(c) != g.cos(c)**(-1)*g.sin(c)
    assert e.diff(c) != g.sin(c)**(-2)*g.cos(c)
    assert e.diff(c) != g.sin(c)**(-3)*g.cos(c)
    t=g.Rational(2)
    e=(t**a/g.log(t))
    assert e == 2**a*g.log(g.Rational(2))**(-1)
    assert e.diff(a) == 2**a

def testexplog():
    x=g.Symbol("x")
    assert g.log(g.exp(x))==x
    assert g.exp(g.log(x))==x

def testlogexpansion():
    x=g.Symbol("x")
    y=g.Symbol("y")
    assert g.log(x*y)==g.log(x)+g.log(y)
    assert g.log(x**2)==2*g.log(x)

def testloghashingbug():
    x=s.Symbol("y")
    assert x!=s.log(s.log(x))
    assert s.log(x)!=s.log(s.log(s.log(x)))

    e=1/s.log(s.log(x)+s.log(s.log(x)))
    e=e.eval()
    assert isinstance(e.base,s.log)
    e=1/s.log(s.log(x)+s.log(s.log(s.log(x))))
    e=e.eval()
    assert isinstance(e.base,s.log)

def testexpbug():
    x=s.Symbol("x")
    assert s.exp(1*s.log(x))==x

def testexpexpand():
    x=s.Symbol("x")
    e=s.exp(s.log(s.Rational(2))*(1+x)-s.log(s.Rational(2))*x)
    assert e.expand()==2