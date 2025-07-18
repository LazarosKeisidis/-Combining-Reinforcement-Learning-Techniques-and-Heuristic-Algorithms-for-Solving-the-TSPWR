import math
import numpy as np

# Distances
def haversine(city_dataA , city_dataB):
    lat1 = city_dataA[1]
    lat2 = city_dataB[1]
    lon1 = city_dataA[2]
    lon2 = city_dataB[2]
    # Earth's radius in kilometers
    R = 6371

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

#Distance matrix
def get_distance_matrix (city_data , number_of_cities) :
    distance_matrix = np.zeros((number_of_cities,number_of_cities))
    for i in range(number_of_cities):
        for j in range(number_of_cities):
            distance = haversine(city_data[i],city_data[j])
            distance_matrix[i][j] = distance    
    return distance_matrix