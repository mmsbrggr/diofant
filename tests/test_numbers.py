import sys
sys.path.append(".")

import sym as g

def testRational():
    n1=g.Rational(1,4)
    n2=g.Rational(1,3)
    n3=g.Rational(2,4)
    n4=g.Rational(2,-4)
    n5=g.Rational(0)
    n6=g.Rational(1)
    n7=g.Rational(3)
    n8=g.Rational(-3)
    assert str(n1.mul(n2)) == "1/12"
    assert str(n1.mul(n2)) == "1/12"
    assert str(n3) == "1/2"
    assert str(n1.mul(n3)) == "1/8"
    assert str(n1.add(n3)) == "3/4"
    assert str(n1.add(n2)) == "7/12"
    assert str(n1.add(n4)) == "(-1/4)"
    assert str(n4.mul(n4)) == "1/4"
    assert str(n4.add(n2)) == "(-1/6)"
    assert str(n4.add(n5)) == "(-1/2)"
    assert str(n4.mul(n5)) == "0"
    assert str(n3.add(n4)) == "0"
    assert str(n1.pow(n7)) == "1/64"
    assert str(n2.pow(n7)) == "1/27"
    assert str(n2.pow(n8)) == "27"
    assert str(n7.pow(n8)) == "1/27"

def testRational_comparisons():
    n1=g.Rational(1,4)
    n2=g.Rational(1,3)
    n3=g.Rational(2,4)
    n4=g.Rational(2,-4)
    n5=g.Rational(0)
    n6=g.Rational(1)
    n7=g.Rational(3)
    n8=g.Rational(-3)

    assert n8<n5
    assert n5<n6
    assert n6<n7
    assert n8<n7
    assert n7>n8

    assert n4<n3
    assert n2<n3
    assert n1<n2
    assert n3>n1
    assert not n3<n1

def test_inf():
    assert g.infty==g.infty
    assert g.infty!=1
    assert 1!=g.infty
    assert g.infty!=g.Symbol("x")**3

def test_powers():
    assert 64**(g.Rational(1)/3)==4
    assert 64**(g.Rational(2)/3)==16
    assert 24*64**(-g.Rational(1)/2)==3

def test_realbug():
    x=g.Symbol("x")
    assert str(2.0*x*x)=="(2.0*x)*x"
    assert str(2.1*x*x)!="(2.0*x)*x"

def test_acceptint():
    g.Real(4)