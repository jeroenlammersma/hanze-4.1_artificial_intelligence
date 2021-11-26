import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)

def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # note: cities is a set, sets don't support indexing
    start = next(iter(cities)) 
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]

def nearest_neighbour(cities):
    start = next(iter(cities))
    tour = [start]

    current_city = start
    while len(cities) != 1:
        cities -= {current_city}
        nearest = find_nn(current_city, cities)
        tour.append(nearest)
        current_city = nearest

    return tour

def find_nn(city, cities):
    return min(cities, key=lambda c: distance(c, city))
    # nearest = None
    # nearest_distance = 0
    # for c in cities:
    #     distance_between = distance(city, c)
    #     if nearest == None or distance_between < nearest_distance:
    #         nearest = c
    #         nearest_distance = distance_between

    # return nearest

# https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def two_opt(cities):
    tour = nearest_neighbour(cities)

    for _ in range(len(tour) * 10):
        cities_ab = tour[:2]
        rest = tour[2:]
        
        for idx in range(len(rest) - 1):
            left_side = rest[:idx]
            cities_cd = rest[idx: idx + 2]
            right_side = rest[idx + 2:]

            if intersect(cities_ab[0], cities_ab[1], cities_cd[0], cities_cd[1]):
                alt_tour = [cities_ab[0]] + [cities_cd[0]] + left_side[::-1] + [cities_ab[1]] + [cities_cd[1]] + right_side
            
                if tour_length(alt_tour) < tour_length(tour):
                    tour = alt_tour

        tour = tour[1:] + tour[:1]

    return tour

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed(3) # the current system time is used as a seed
                  # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))

def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-') # blue circle markers, solid line style
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

# give a demo with 10 cities using brute force
# plot_tsp(try_all_tours, make_cities(10))
# plot_tsp(nearest_neighbour, make_cities(500))
plot_tsp(two_opt, make_cities(500))