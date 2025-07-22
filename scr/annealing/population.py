import random

def generate_permutation(n):
    permutation = list(range(n))  # create list [0, ... n]
    random.shuffle(permutation)   # Shuffle elements in the list
    return permutation

def mutation(site):
    index_1, index_2 = sorted(random.sample(range(len(site)), 2))
    site[index_1:index_2 + 1] = reversed(site[index_1:index_2 + 1])
    return site
