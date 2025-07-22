from annealing.fitness import calculate_all_distance_fitness_function
from annealing.population import mutation
import random
import math

def simulated_annealing(
        distances, t, factor, count_of_generation, count_of_nested_generation,
        best_path, top_permutation, top_dist, best_distance
    ):
    temperature = []
    generations = []
    best_distances = []
    average_distances = []
    best_paths_history = []
    best_distances_history = []

    while_cycle_index = 0

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
            new_dist = calculate_all_distance_fitness_function(new_permutation_path, distances)

            update = False
            if new_dist < top_dist:
                best_distance = new_dist
                best_path = new_permutation_path.copy()
                top_permutation = best_path.copy()
                top_dist = best_distance
                update = True
                # Save only the best routes
                best_paths_history.append(top_permutation.copy())
                best_distances_history.append(top_dist)

            if not update:
                probability_of_choosing_the_worst_decision = math.exp(-(new_dist - best_distance) / t)
                if random.random() < probability_of_choosing_the_worst_decision:
                    best_path = new_permutation_path.copy()
                    best_distance = new_dist

        if while_cycle_index >= count_of_generation or t < 0.01:
            return (
                top_permutation, top_dist, best_distance, temperature, generations,
                best_distances, average_distances, best_paths_history, best_distances_history
            )