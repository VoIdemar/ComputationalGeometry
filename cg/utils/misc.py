from math import copysign, pi

def to_rad(degr):
    return degr * pi / 180.0

def sgn(x):
    """
    Version of the standard sgn(x) function which uses copysign() function
    """
    return copysign(1, x)

def sign(x):
    """
    Version of the standard sgn(x) function which uses branching
    """
    return ( 1 if x > 0.0 else
            -1 if x < 0.0 else
             0 )