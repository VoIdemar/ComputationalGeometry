from primitives import get_turn_direction, Direction

def convex_hull(*points):
    """Computes the convex hull of a finite set of 2d-points using Graham scan algorithm
    """
    
    def reorganize_hull(hull):
        """Excludes points which are the vertices of left turn angles on adding 
           new points to the hull
        """            
        while (len(hull) > 2 and get_turn_direction(*hull[-3:]) != Direction.CLOCKWISE):  # @UndefinedVariable
            hull.pop(-2)
    
    p = list(points)
    n = len(points)
    if (n >= 2):
        list.sort(p)                          # Sorting points (x, y) lexicographically
        upperHull = p[0:2]                    # Initiating upper hull: [p0, p1]
        for i in range(2, n):
            upperHull.append(p[i])            
            reorganize_hull(upperHull)        # Modifying upper hull to include more points from the initial set
        lowerHull = [p[n-1], p[n-2]]          # Initiating lower hull: [p[n-1], p[n-2]]
        for i in range(n-3, -1, -1):
            lowerHull.append(p[i])
            reorganize_hull(lowerHull)        # Modifying lower hull to include more points from the initial set
        return upperHull + lowerHull[1:-1]
    else:
        return []