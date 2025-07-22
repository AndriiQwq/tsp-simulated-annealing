import random
import math

def generate_cities(count_of_cities, size_of_map):
    """
    Generates a list of cities with random coordinates.
    """
    cities = []
    for _ in range(count_of_cities):
        random_x = random.randint(0, size_of_map[0])
        random_y = random.randint(0, size_of_map[1])
        cities.append([random_x, random_y])

    return cities

def callculate_distances(rows, cols, cities):
    """
    Calculates the distances between each pair of cities.
    Returns a 2D list of distances.
    """
    distances = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            first_city = cities[i]
            second_city = cities[j]
            distance = math.sqrt((first_city[0] - second_city[0]) ** 2 + (first_city[1] - second_city[1]) ** 2)
            distances[i][j] = distance
            distances[j][i] = distance

    return distances
