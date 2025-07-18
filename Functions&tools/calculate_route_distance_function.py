import numpy as np

# route distance
def route_distance(route: np.ndarray, distance_matrix: np.ndarray):
    distance_of_route = 0
    for i in range(1, len(route)):
        distance_of_route += distance_matrix[int(route[i - 1]), int(route[i])]
    distance_of_route += distance_matrix[int(route[-1]), int(route[0])]
    return distance_of_route