import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.hypot(city1[0] - city2[0], city1[1] - city2[1])


def total_distance(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[i + 1]]) for i in range(len(tour) - 1)) + distance(cities[tour[-1]], cities[tour[0]])  # 戻る距離


def two_opt(tour, cities):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour)):
                if j - i == 1:  # 連続した辺はスキップ
                    continue
                new_tour = tour[:]
                new_tour[i:j] = reversed(tour[i:j])
                if total_distance(new_tour, cities) < total_distance(tour, cities):
                    tour = new_tour
                    improved = True
                    break
            if improved:
                break
    return tour


def solve(cities):
    N = len(cities)

    # まず貪欲法でtourを出す
    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities, key=lambda city: distance(cities[current_city], cities[city]))
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city

    # 2-opt で改善
    tour = two_opt(tour, cities)
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = solve(cities)
    print_tour(tour)
