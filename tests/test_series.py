import sys
sys.path.append(".")

import py

import sym as g

def testseries():
    n3=g.Rational(3)
    n2=g.Rational(2)
    n6=g.Rational(6)
    x=g.Symbol("x")
    c=g.Symbol("c")
    e=g.sin(x)
    assert str(e) == "sin(x)"
    assert str(e.series(x,0)) == "0"
    assert str(e.series(x,1)) == "x"
    assert str(e.series(x,2)) == "x"
    assert e.series(x,3) == x+(-g.Rational(1)/6)*x**3
    assert e.series(x,4) == x+(-g.Rational(1)/6)*x**3

    e=((g.exp(x)-1)/x)
    assert e.series(x,1) == g.Rational(1)
    py.test.raises(g.pole_error, g.Basic.series, e,x,0)

    #e=2*g.sin(x)*g.cos(x)
    #print
    #print e.series(x,5)
    #e=g.sin(2*x)
    #e=g.tan(2*x)
    #e=1/g.cos(x)
    #print e.series(x,8)

def testseriesbug1():
    x=g.Symbol("x")
    assert (1/x).series(x,3)==1/x
    assert (x+1/x).series(x,3)==x+1/x

def testseries2():
    x=g.Symbol("x")
    assert ((x+1)**(-2)).series(x,3)==1-2*x+3*x**2-4*x**3
    assert ((x+1)**(-1)).series(x,3)==1-x+x**2-x**3
    assert ((x+1)**0).series(x,3)==1
    assert ((x+1)**1).series(x,3)==1+x
    assert ((x+1)**2).series(x,3)==1+2*x+x**2
    assert ((x+1)**3).series(x,3)==1+3*x+3*x**2+x**3

    assert (1/(1+x)).series(x,3)==1-x+x**2-x**3
    assert (x+3/(1+2*x)).series(x,3)==3-5*x+12*x**2-24*x**3

    assert ((1/x+1)**3).series(x,3)== x**(-3)+3*x**(-2)+3*x**(-1)
    assert (1/(1+1/x)).series(x,3)==x-x**2+x**3
    assert (1/(1+1/x**2)).series(x,6)==x**2-x**4+x**6-x**8+x**10-x**12

def xtestfind(self):
    a=g.Symbol("a")
    b=g.Symbol("b")
    c=g.Symbol("c")
    p=g.Rational(5)
    e=a*b+b**p
    assert e.find(b)
    assert not e.find(c)

def xtest_log():
    "too difficult"
    x=g.Symbol("x")
    ec=g.exp(g.Rational(1))
    e=(g.log(1/x+ec)-ec)/(x*g.log(1/x+1))
    print
    print e.eval()
    d= e.diff(x)

def test_bug2():
    w=g.Symbol("w")
    log=g.log
    e=(w**(-1)+w**(-log(3)*log(2)**(-1)))**(-1)*(3*w**(-log(3)*log(2)**(-1))+2*w**(-1))
    e=e.eval().expand()
    #should be 3, but is 2
#    print e.series(w,4)

def test_exp():
    x=g.Symbol("x")
    e=(1+x)**(1/x)
    assert e.eval().series(x,1)==g.exp(1)

def test_exp2():
    x=g.Symbol("x")
    w=g.Symbol("w")
    log=g.log
    e=w**(1-log(x)/(log(2)+log(x)))
    assert e.eval().series(w,1)!=0

def test_generalexponent():
    x=g.Symbol("x")
    log=g.log
    p=2
    e=(2/x+3/x**p)/(1/x+1/x**p)
    assert e.eval().series(x,1).leadterm(x)==(3,0)
    p=g.Rational(1,2)
    e=(2/x+3/x**p)/(1/x+1/x**p)
    assert e.eval().series(x,1).leadterm(x)==(2,0)
    p=g.Rational(3,2)
    e=(2/x+3/x**p)/(1/x+1/x**p)
    assert e.eval().series(x,1).leadterm(x)==(3,0)

    e=1+x**g.Rational(1,2)
    assert e.eval().series(x,4)==1+x**g.Rational(1,2)
    e=1/(1+x**g.Rational(1,2))
    assert e.eval().series(x,2)==1-x**g.Rational(1,2)

def test_subsbug1():
    x=g.Symbol("x")
    e=1+x**g.Rational(1,2)
    e=e.diff(x)
    py.test.raises(g.pole_error,e.subs,x,g.Rational(0))