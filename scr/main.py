from config_manager import ConfigManager
import os
from datetime import datetime
from utiles import generate_cities, callculate_distances, generate_permutation, calculate_all_distance_fitness_function, simulated_annealing
from visualizer import plot_cities, plot, animate_path

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

    if logging_enabled:
        logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
        os.makedirs(logs_dir, exist_ok=True)
        log_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
        log_path = os.path.join(logs_dir, log_name)
        log = open(log_path, 'w')

    # Generate cities
    cities = generate_cities(count_of_cities, size_of_map)
    if logging_enabled:
        log.write('Generation of cities:\n')
        log.write(f'Sites: {str(cities)}\nCount of sites: {str(count_of_cities)}\n')

    rows = len(cities)
    cols = len(cities)
    distances = callculate_distances(rows, cols, cities)

    # We create lists for analytics: temperature, generations, best_distances, average_distances 
    temperature = []
    generations = []
    best_distances = []
    average_distances = []

    permutation = generate_permutation(count_of_cities)

    best_distance = calculate_all_distance_fitness_function(permutation, distances)  # new_path
    best_path = permutation.copy()

    top_dist = best_distance
    top_permutation = permutation.copy()

    t = 1600 # High temperature values allow for the acceptance of worse solutions, aiding the transition from one minimum to another.
    factor = 0.99 # determines how fast the temperature decreases

    if logging_enabled:
        log.write('Initial permutation: ' + str(top_permutation))

    top_permutation, top_dist, best_distance, temperature, generations, best_distances, average_distances, best_paths_history, best_distances_history = simulated_annealing(
        distances, t, factor, count_of_generation, count_of_nested_generation,
        temperature, generations, best_distances, best_path, average_distances,
        top_permutation, top_dist, best_distance
    )

    if logging_enabled:
        print("Current results:\n")
        print(f'Best permutations and distances: {top_dist}\nPath: {top_permutation}')

    plot_cities(cities, best_path, top_permutation)
    plot(generations, temperature, best_distances, average_distances)
    animate_path(cities, best_paths_history, best_distances_history)

    if logging_enabled:
        log.write(f'\nBest permutations and distances: {top_permutation}\nPath: {top_dist}')
        log.close()

if __name__ == "__main__":
    main()