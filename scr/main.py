from config_manager import ConfigManager
import os
from annealing.simulated_annealing import simulated_annealing
from visualizer import plot_cities, plot, animate_path
from annealing.cities import generate_cities, callculate_distances
from annealing.fitness import calculate_all_distance_fitness_function
from annealing.population import generate_permutation
from logger import Logger

def main():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini'))
    config = ConfigManager()
    config.load_config(config_path)

    logging_enabled = config.get('logging_enabled')
    count_of_cities = config.get('count_of_cities')
    size_of_map = config.get('size_of_map')
    count_of_generation = config.get('count_of_generation')
    count_of_nested_generation = config.get('count_of_nested_generation')
    cities = config.get('cities', [])

    logger = Logger(logging_enabled)

    # Generate cities
    cities = generate_cities(count_of_cities, size_of_map)
    logger.log('Generation of cities:')
    logger.log(f'Sites: {str(cities)}\nCount of sites: {str(count_of_cities)}')

    distances = callculate_distances(len(cities), len(cities), cities)
    permutation = generate_permutation(count_of_cities)

    best_distance = calculate_all_distance_fitness_function(permutation, distances)  # new_path
    best_path = permutation.copy()
    top_dist = best_distance
    top_permutation = permutation.copy()
    t = 1600 # High temperature values allow for the acceptance of worse solutions, aiding the transition from one minimum to another.
    factor = 0.99 # determines how fast the temperature decreases

    logger.log('Initial permutation: ' + str(top_permutation))

    result = simulated_annealing(
        distances, t, factor, count_of_generation, count_of_nested_generation,
        best_path, top_permutation, top_dist, best_distance
    )
    top_permutation, top_dist, best_distance, temperature, generations, best_distances, average_distances, best_paths_history, best_distances_history = result

    logger.log(f'\nBest permutations and distances: {top_permutation}\nPath: {top_dist}')
    logger.close()
    print(f'Current results:\nBest permutations and distances: {top_dist}\nPath: {top_permutation}')

    plot_cities(cities, best_path, top_permutation)
    plot(generations, temperature, best_distances, average_distances)
    animate_path(cities, best_paths_history, best_distances_history)

if __name__ == "__main__":
    main()