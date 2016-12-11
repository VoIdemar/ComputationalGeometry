import numpy as np

ALLOWED_COMPARISON_ERROR = 10**(-3) 

def ndarrays_almost_equal(arr1, arr2):
    return np.max(np.abs(arr1 - arr2)) <= ALLOWED_COMPARISON_ERROR

def list_contains_ndarray(arrList, arr):
    for array in arrList:
        if ndarrays_almost_equal(array, arr):
            return True
    return False

def remove_ndarray_from_list(arrList, arr):
    return [array for array in arrList if not ndarrays_almost_equal(array, arr)]

def list_index_of(arrList, arr):
    for i in range(0, len(arrList)):
        if ndarrays_almost_equal(arrList[i], arr):
            return i
    return None

def ndarray_lists_equal(arrList1, arrList2):
    if len(arrList1) <> len(arrList2):
        return False
    for (arr1, arr2) in zip(arrList1, arrList2):
        if not ndarrays_almost_equal(arr1, arr2):
            return False
    return True