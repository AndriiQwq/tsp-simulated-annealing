import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def plot_cities(sites, best_path, top_permutation):
    connections = []
    for i in range(len(top_permutation) - 1):
        connections.append([top_permutation[i], top_permutation[i + 1]])
    connections.append([top_permutation[-1], top_permutation[0]])

    plt.figure(figsize=(8, 8))
    plt.xlim(0, 200)
    plt.ylim(0, 200)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().add_patch(plt.Rectangle((0, 0), 200, 200, fill=None, edgecolor='black'))

    for i in range(len(sites)):
        if i == best_path[0]:
            plt.plot(sites[i][0], sites[i][1], 'go', markersize=15)
        else:
            plt.plot(sites[i][0], sites[i][1], 'ro')
        plt.text(sites[i][0], sites[i][1], f'({sites[i][0]}, {sites[i][1]})', fontsize=9, ha='right')

    plt.title('Map')
    plt.grid()

    for i, connection in enumerate(connections):
        plt.plot(
            [sites[connection[0]][0], sites[connection[1]][0]],
            [sites[connection[0]][1], sites[connection[1]][1]],
            'b-'
        )

        mid_x = (sites[connection[0]][0] + sites[connection[1]][0]) / 2
        mid_y = (sites[connection[0]][1] + sites[connection[1]][1]) / 2
        plt.text(mid_x, mid_y, str(i + 1), fontsize=10, ha='center', va='bottom')

    plt.show()

def plot(generations, temperature, best_distances, average_distances):
    plt.plot(generations, temperature, label='Temperature')
    plt.xlabel('Generation')
    plt.ylabel('Temperature')
    plt.title('Investigation of Temperature per Generation')
    plt.legend()
    plt.show()

    plt.plot(generations, best_distances, label='Best Distances')
    plt.xlabel('Generation')
    plt.ylabel('Distance')
    plt.title('Best Distances Over Generations')
    plt.legend()
    plt.show()

    plt.plot(generations, average_distances, label='Average Distances', color='orange')
    plt.xlabel('Generation')
    plt.ylabel('Distance')
    plt.title('Average Distances Over Generations')
    plt.legend()
    plt.show()

def animate_path(cities, best_paths, best_distances):
    """
    Animates the change of the best route and distance at each step.
    :param cities: list of cities coordinates
    :param best_paths: history of best permutations (routes)
    :param best_distances: history of best distances
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 200)
    ax.set_aspect('equal', adjustable='box')
    ax.add_patch(plt.Rectangle((0, 0), 200, 200, fill=None, edgecolor='black'))

    ax.scatter([c[0] for c in cities], [c[1] for c in cities], c='red')
    lines, = ax.plot([], [], 'b-', lw=2)
    text_dist = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=12, verticalalignment='top')

    max_frames = 100
    slow_tail = 20
    if len(best_paths) > max_frames:
        step = len(best_paths) // max_frames
        frames = list(range(0, len(best_paths), step))
        if len(best_paths) > slow_tail:
            frames += list(range(len(best_paths) - slow_tail, len(best_paths)))
    else:
        frames = list(range(len(best_paths)))

    def update(frame):
        path = best_paths[frame]
        x = [cities[i][0] for i in path] + [cities[path[0]][0]]
        y = [cities[i][1] for i in path] + [cities[path[0]][1]]
        lines.set_data(x, y)
        text_dist.set_text(f"Best Distance: {best_distances[frame]:.2f}")
        return lines, text_dist

    def gen_intervals():
        for idx, frame in enumerate(frames):
            if frame >= len(best_paths) - slow_tail:
                yield 100  
            else:
                yield 10 

    ani = FuncAnimation(
        fig, update, frames=frames, interval=10, blit=True, repeat=False
    )
    plt.title('TSP Simulated Annealing Best Path Progress')
    plt.show()