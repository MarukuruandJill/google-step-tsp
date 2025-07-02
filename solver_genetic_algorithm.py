import sys
import math
import random

from common import print_tour, read_input

def distance(city1, city2):
    return math.hypot(city1[0] - city2[0], city1[1] - city2[1])


def total_distance(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[i + 1]]) for i in range(len(tour) - 1)) + distance(cities[tour[-1]], cities[tour[0]])  # 戻る距離


########################################################################
# 遺伝的アルゴリズムの実装
#
#  step1: 初期集団の生成
#  step2: 評価　解とみなせるならば終了
#  step3: 選択
#  step4: 交叉
#  step5: 突然変異
#  step6: step2に戻る
#
########################################################################

#pop_size: 生成する数　#num_cities: 都市の数
#cityの訪問順をランダムに並べた配列を作る(cityのインデックスが入る)
def create_initial_population(pop_size, num_cities): 
    return [random.sample(range(num_cities), num_cities) for _ in range(pop_size)]

# トーナメント選択法
# 距離が短いルートを選び出す
def select(population, cities, k=5):
    selected = random.sample(population, k)
    selected.sort(key=lambda route: total_distance(route, cities))
    return selected[0]

#交叉
# 2つの親ルートから都市の順序を受け継いだ子ルートを生成
def crossover(parent1, parent2):
    # 交叉範囲をランダムに決める
    a, b = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)
    #交叉範囲にparent1を入れる
    child[a:b] = parent1[a:b]
    #まだchildに含まれていないparent2のcityを取り出す
    fill = [city for city in parent2 if city not in child]
    j = 0
    #parent2の要素を入れる
    for i in range(len(parent1)):
        if child[i] is None:
            child[i] = fill[j]
            j += 1
    return child

# 突然変異
# 確率的に2つの都市の位置を入れ替えて解の多様性を確保する
def mutate(route, mutation_rate=0.02):
    for i in range(len(route)):
        # mutation_rateの確率でランダムに交換
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]
    return route

# メインの処理
# citiee: 都市の座標のリスト
# generations: 世代数
# pop_size: 1世代あたりの個体数
# mutation_rate: 突然変異を起こす確率
def genetic_algorithm(cities, generations=500, pop_size=100, mutation_rate=0.02):
    num_cities = len(cities)  #都市数
    population = create_initial_population(pop_size, num_cities) #初期配列 ランダムに並べたもの
    best_route = min(population, key=lambda r: total_distance(r, cities)) #初期配列の中から、距離が一番短いルートの要素を返す

    for gen in range(generations):
        new_population = []
        for _ in range(pop_size):
            #親になるルートを2つ選ぶ
            p1 = select(population, cities)
            p2 = select(population, cities)
            #交叉、突然変異を行う
            child = crossover(p1, p2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population
        current_best = min(population, key=lambda r: total_distance(r, cities))
        if total_distance(current_best, cities) < total_distance(best_route, cities):
            best_route = current_best

        if gen % 50 == 0:
            print(f"Generation {gen}: distance = {total_distance(best_route, cities):.2f}")
    print(f"final distance = {total_distance(best_route, cities):.2f}")

    return best_route

if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = genetic_algorithm(cities)
    print_tour(tour)