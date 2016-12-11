from math import sin, cos, pi
from random import random

import numpy as np

from cg.basic.primitives import point2d, Intersection, find_intersection_point, angle
from cg.utils.ndarrays import list_contains_ndarray, ndarrays_almost_equal, ALLOWED_COMPARISON_ERROR
from cg.utils.misc import to_rad, sgn

class Polygon(object):
    
    UNCYCLED_SEGMENTS_ERROR = u'Segments do not represent polygon sides (segments chaining failed)'
    
    def __init__(self, points=None):
        self.__points = points if not (points is None) else []
        
    @property
    def points(self):
        return self.__points
    
    def is_empty(self):
        return len(self.points) == 0
    
    @staticmethod
    def create_random_polygon(origin, a, b, theta):
        points = []
        phi = 0
        x, y = origin
        while phi < 360:
            r = a + (b - a)*random()
            points.append( point2d(x + r*cos(to_rad(phi)), y + r*sin(to_rad(phi))) )
            phi = phi + theta*random()
        if random() > 0.5:
            points = points[::-1]
        return Polygon(points)
    
    def find_point_orientation(self, point):
        points = self.points + [self.points[0]]
        r = l = e = 0
        for i in range(0, len(points) - 1):
            f = np.linalg.det(np.array([point - points[i], points[i+1] - points[i]]))
            if f == 0:
                e = 1
            elif f < 0:
                l = 1
            else:
                r = 1
            if l*r <> 0:
                return l
        return e - 1
    
    def find_point_orientation_rad(self, point):
        s = delta = 0
        w = None
        for i in range(0, len(self.points)):
            v = self.points[i] - point
            if np.abs(np.linalg.norm(v)) <= ALLOWED_COMPARISON_ERROR:
                return 0
            if i == 0:
                w = v
                continue
            delta = angle(v, w)
            deltaNorm = np.linalg.norm(delta)
            if deltaNorm < pi:
                w = v
                s = s + delta
            elif deltaNorm == pi:
                return 0
        return sgn(pi - np.abs(s))
                
    def find_intersection_with_polygon_orient(self, segment, radTest=True):
        get_orientation = self.find_point_orientation_rad if radTest else self.find_point_orientation
        a, b = segment
        intersectCount = 0
        V = b - a
        L = [0, 1]
        if len(self.points) >= 2:
            points = self.points + [self.points[0]]
            for i in range(0, len(points) - 1):
                intersectFlag, t, _, _ = find_intersection_point(segment, points[i:i+2])
                if intersectFlag == Intersection.INTERSECT:
                    intersectCount = intersectCount + 1
                    L.append(t)
            L.sort()
            segments = []
            for k in range(0, len(L) - 1):
                m = a + 0.5*(L[k] + L[k+1])*V                
                orientation = get_orientation(m)
                if orientation < 0:
                    segments.append([a + L[k]*V, a + L[k+1]*V])
            return segments
        return []
    
    def find_intersection(self, polygon, radTest=True):
        return Polygon.find_polygons_intersection(self, polygon, radTest)
    
    @staticmethod
    def find_polygons_intersection(polygon1, polygon2, radTest=True):
        if polygon1.is_empty() or polygon2.is_empty():
            return [Polygon()]
        segments = Polygon.__find_intersection_segments(polygon1, polygon2, radTest)
        segments = segments + Polygon.__find_intersection_segments(polygon2, polygon1, radTest)
        if len(segments) > 0:
            return [Polygon(chain) for chain in Polygon.get_sorted_points_from_segments_list(segments)]
        return [Polygon()]
    
    @staticmethod
    def get_sorted_points_from_segments_list(segments):
        intersection = []
        while len(segments) > 0:
            p1, p2 = segments[0]
            current = [p1, p2]
            segments = segments[1:]
            chainCompleted = False        
            while len(segments) > 0 and not chainCompleted:
                pLast = current[-1]
                nextFound = False     
                for i in range(0, len(segments)):
                    pStart, pEnd = segments[i]
                    matchedPoint = (pEnd if ndarrays_almost_equal(pLast, pStart) else
                                    pStart if ndarrays_almost_equal(pLast, pEnd) else 
                                    None)
                    if not (matchedPoint is None):
                        current.append(matchedPoint)
                        nextFound = True
                        del segments[i]
                        if ndarrays_almost_equal(current[0], current[-1]):                   
                            intersection.append(current[:-1])
                            chainCompleted = True
                        break
                if not nextFound:
                    raise ValueError(Polygon.UNCYCLED_SEGMENTS_ERROR)
        return intersection
    
    @staticmethod
    def __find_intersection_segments(polygon, intersectingPolygon, radTest=True):
        segments = []
        points = intersectingPolygon.points + [intersectingPolygon.points[0]] 
        for i in range(0, len(points) - 1):
            segment = points[i:i+2]
            result = polygon.find_intersection_with_polygon_orient(segment, radTest)
            if len(result) <> 0:
                for segm in result:
                    if not list_contains_ndarray(segments, np.array(segm)):
                        segments.append(segm)
        return segments
    
    def __str__(self):
        return 'Polygon:\n' + self.__points.__str__()