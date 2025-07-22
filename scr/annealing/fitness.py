def calculate_all_distance_fitness_function(path, distances_table):
    distance = 0
    for i in range(len(path) - 1):
        distance += distances_table[path[i]][path[i + 1]]
    distance += distances_table[path[0]][path[-1]]
    return distance


