from eventpoint import EventPoint
from queueentry import EventQueueEntry
from utils.rbtree import RBTree 


def find_intersections(segments):       
    eventQueue = RBTree()
    T = RBTree()
    for segm in segments:
        endpoints = [EventPoint(*point) for point in segm]
        upper = EventQueueEntry()
        upper.eventpoint = min(endpoints)
        pos = eventQueue.search(upper)
        if pos <> RBTree.NIL:
            eventQueue.get_value(pos).append(segm)
        else:
            upper.segments.append(segm)
            eventQueue.insert(upper)
        lower = EventQueueEntry()
        lower.eventpoint = max(endpoints)
        pos = eventQueue.search(lower)
        if pos == RBTree.NIL:
            eventQueue.insert(lower)
    while not eventQueue.is_empty():
        min_pos = eventQueue.min()
        p = eventQueue.get_value(min_pos)
        eventQueue.delete(min_pos)
        handle_event_point(p, T)
            
def handle_event_point(p, segments):
    u = p.segments
    l = [segm for segm in segments if min()]
    
            
            
        