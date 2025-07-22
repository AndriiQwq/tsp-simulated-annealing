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

def generate_permutation(n):
    permutation = list(range(n))  # create list [0, ... n]
    random.shuffle(permutation)   # Shuffle elements in the list
    return permutation

def calculate_all_distance_fitness_function(path, distances_table):
    distance = 0

    for i in range(len(path) - 1):
        distance += distances_table[path[i]][path[i + 1]]
    distance += distances_table[path[0]][path[-1]]

    return distance

def mutation(site):
    index_1, index_2 = sorted(random.sample(range(len(site)), 2))
    site[index_1:index_2 + 1] = reversed(site[index_1:index_2 + 1])
    return site


def simulated_annealing(
        distances, t, factor, count_of_generation, count_of_nested_generation,
        temperature, generations, best_distances, best_path, average_distances,
        top_permutation, top_dist, best_distance
    ):
    while_cycle_index = 0
    best_paths_history = []
    best_distances_history = []

    while True:
        while_cycle_index += 1
        temperature.append(t)
        generations.append(while_cycle_index)
        best_distances.append(top_dist)

        average_distance = best_distance / count_of_nested_generation
        average_distances.append(average_distance)

        print(top_permutation, ': ', t)

        t = t * factor
        for _ in range(count_of_nested_generation):

            new_permutation_path = mutation(best_path.copy())
            new_dist = calculate_all_distance_fitness_function(new_permutation_path,  distances)

            best_paths_history.append(top_permutation.copy())
            best_distances_history.append(top_dist)

            update = 0
            if new_dist < top_dist:
                update = 1
                best_distance = new_dist
                best_path = new_permutation_path.copy()

                top_permutation = best_path.copy()
                top_dist = best_distance

            if update == 0:
                probability_of_choosing_the_worst_decision = math.exp(-(new_dist - best_distance) / t)
                if random.random() < probability_of_choosing_the_worst_decision:
                    best_path = new_permutation_path.copy()
                    best_distance = new_dist

        if while_cycle_index >= count_of_generation or t < 0.01:
            return (
                top_permutation, top_dist, best_distance, temperature, generations,
                best_distances, average_distances, best_paths_history, best_distances_history
            )