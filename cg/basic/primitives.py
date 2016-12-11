import math

import numpy as np

from cg.utils.enumeration import enum
from cg.utils.misc import sgn

COLLINEARITY_PRECISION = 0.000001

Direction = enum('Direction', CLOCKWISE = 0, COUNTERCLOCKWISE = 1, COLLINEAR = 2)
Intersection = enum('Intersection', NONE = 0, PARALLEL = -1, INTERSECT = 1)

def point2d(x, y):
    return np.array([x, y])

def are_noncollinear(points):
    for i in range(0, len(points) - 1):
        for j in range(i + 1, len(points)):
            (x1, y1), (x2, y2) = points[i], points[j]
            for k in range(j + 1, len(points)):
                (x, y) = points[k]
                if abs((y1 - y2)*x + (x2 - x1)*y + (x1*y2 - x2*y1)) <= COLLINEARITY_PRECISION:
                    return False
    return True

def triangle_exists(a, b, c):
    return (a + b) > c and (b + c) > a and (a + c) > b

def triangle_exists2(point1, point2, point3):
    return are_noncollinear([point1, point2, point3])

def heron_triangle_area_sides(a, b, c):
    """Numerically stable variant of Heron's formula"""
    if triangle_exists(a, b, c):
        return 0.25*math.sqrt((a + (b + c))*(c - (a - b))*(c + (a - b))*(a + (b - c)))
    else:
        return 0

def heron_triangle_area(point1, point2, point3):
    (x1, y1), (x2, y2), (x3, y3) = point1, point2, point3    
    a = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    b = math.sqrt((x3 - x2)**2 + (y3 - y2)**2)
    c = math.sqrt((x3 - x1)**2 + (y3 - y1)**2)
    return heron_triangle_area_sides(a, b, c)

def cross_product(p0, p1, p2):
    """Computes cross product of vectors p[0]p[1] and p[0]p[2]"""
    (x0, y0), (x1, y1), (x2, y2) = p0, p1, p2
    return (x1 - x0)*(y2 - y0) - (x2 - x0)*(y1 - y0)

def triangle_area(p0, p1, p2):
    return 0.5*abs(cross_product(p0, p1, p2))

def get_turn_direction(p1, p2, p3):
    cproduct = cross_product(p1, p2, p3)
    return (Direction.CLOCKWISE if cproduct < 0 else
            Direction.COUNTERCLOCKWISE if cproduct > 0 else 
            Direction.COLLINEAR)

def on_segment(segment, p):
    (x1, y1), (x2, y2), (x, y) = segment, p
    return (min(x1, x2) <= x <= max(x1, x2)) and (min(y1, y2) <= y <= max(y1, y2) and
            get_turn_direction((x1, y1), (x2, y2), p) == Direction.COLLINEAR) 

def are_successive_segments(segment1, segment2):
    p1, p2, p3, p4 = segment1, segment2
    return ((on_segment(p3, p4, p1)) or (on_segment(p3, p4, p2)) or
            (on_segment(p1, p2, p3)) or (on_segment(p1, p2, p4)))

def are_mismatched_segments(segment1, segment2):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = segment1, segment2   
    return (x1 <> x3 or x1 <> x4 or x2 <> x3 or x2 <> x4 or
            y1 <> y3 or y1 <> y4 or y2 <> y3 or y2 <> y4)


def segments_intersect(segment1, segment2):
    """Checks whether segments [p1, p2] and [p3, p4] intersect or not"""
    (p1, p2), (p3, p4) = segment1, segment2    
    d1 = get_turn_direction(p3, p4, p1)
    d2 = get_turn_direction(p3, p4, p2)
    d3 = get_turn_direction(p1, p2, p3)
    d4 = get_turn_direction(p1, p2, p4)
    return (((d1 == Direction.CLOCKWISE and d2 == Direction.COUNTERCLOCKWISE) or
             (d2 == Direction.CLOCKWISE and d1 == Direction.COUNTERCLOCKWISE)) and
            ((d3 == Direction.CLOCKWISE and d4 == Direction.COUNTERCLOCKWISE) or
             (d4 == Direction.CLOCKWISE and d3 == Direction.COUNTERCLOCKWISE)) or
            on_segment(p3, p4, p1) or
            on_segment(p3, p4, p2) or
            on_segment(p1, p2, p3) or
            on_segment(p1, p2, p4))
    
def find_intersection_point(segment1, segment2):
    a, b = segment1 
    c, d = segment2
    V = b - a
    M = np.array([V, c - d])
    if np.linalg.det(M) == 0:
        return (Intersection.PARALLEL, None, None, None)
    t, tau = np.dot(c - a, np.linalg.inv(M))
    q = a + V*t
    return (Intersection.INTERSECT if 0 <= t <= 1 and 0 <= tau <= 1 else Intersection.NONE,
            t, tau, q)

def angle(v, w):
    d = np.linalg.det(np.array([v, w]))
    sign = 1 if d == 0 else sgn(d)
    return sign*math.acos(np.dot(v, w) / (np.linalg.norm(v)*np.linalg.norm(w)))