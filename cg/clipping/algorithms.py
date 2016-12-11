import numpy as np

from cg.polygons.polygon import Polygon
from cg.utils.misc import sign

def sutherland_hodgman(polygon, window):
    """
    Performs polygon clipping with the specified window using Sutherland-Hodgman algorithm 
    """
    np = len(polygon.points)
    window_points = window.points + [window.points[0]]
    nw = len(window_points)
    
    def intersect_custom_observity(polygon, check_observity):
        intersection_points = []
        s = None
        f = None
        for i in range(0, nw - 1):
            intersection_points = []
            j = 0
            wi, wi1 = window_points[i:i+2]
            np = len(polygon.points)
            while j < np:
                if j == 0:
                    f = polygon.points[j]
                elif _actual_intersection_exists(s, polygon.points[j], wi, wi1):                
                    intersection_points.append(find_intersection_point(s, polygon.points[j], wi, wi1))
                s = polygon.points[j]
                observity = _get_observity(s, wi, wi1)
                if check_observity(observity):
                    intersection_points.append(s)
                j += 1
                if j == np:
                    # Handling the last point
                    if len(intersection_points) == 0:
                        return Polygon()
                    elif _actual_intersection_exists(s, f, wi, wi1):
                        intersection_points.append(find_intersection_point(s, f, wi, wi1))
                    polygon = Polygon(intersection_points)
        return Polygon(intersection_points)
    
    # Calculate intersection checking the condition: observity >= 0
    intersection = intersect_custom_observity(polygon, lambda observity: observity >= 0)
    if len(intersection.points) == 0:
        # If intersection is not found (<==> is empty) then it is calculated with the condition:
        # observity <= 0
        intersection = intersect_custom_observity(polygon, lambda observity: observity <= 0)
    return intersection

def find_intersection_point(p1, p2, w1, w2):
    """
    Gets intersection point of the segments [p1, p2], [w1, w2]
    """
    (p1x, p1y), (p2x, p2y), (w1x, w1y), (w2x, w2y) = p1, p2, w1, w2
    coef = np.linalg.inv(np.array([[p2x-p1x, w1x-w2x],
                                   [p2y-p1y, w1y-w2y]]))
    right = np.array([w1x-p1x, w1y-p1y])    
    param = np.dot(coef, right)
    t, _ = param
    return p1 + (p2-p1)*t
            
def _get_observity(p, p1, p2):
    """
    Checks whether the p point is observed with respect to the segment [p1, p2]
    """
    (x, y), (x1, y1), (x2, y2) = p, p1, p2
    return sign((x-x1)*(y2-y1) - (y-y1)*(x2-x1))
    
def _actual_intersection_exists(start, end, w1, w2):
    observ_start = _get_observity(start, w1, w2)
    observ_end = _get_observity(end, w1, w2)
    return observ_start*observ_end < 0   