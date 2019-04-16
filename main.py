import matplotlib.pyplot as plt
from classes import Ant, City
import numpy as np
import operator
import random
import copy


alpha = 1
beta = 5
ph_evaporation_rate = 0.5
ph_t0 = 0.1
t = 0
t_max = 200
ant_nr = 10
bestAntDist = np.inf
bestAnt = 0

# cityList = [City(x=1, y=1), City(x=1, y=5), City(x=1, y=10), City(x=2, y=3), City(x=2, y=7)]
cityList = [City(x=0, y=1),
            City(x=3, y=4),
            City(x=6, y=5),
            City(x=7, y=3),
            City(x=15, y=0),
            City(x=12, y=4),
            City(x=14, y=10),
            City(x=9, y=6),
            City(x=7, y=9),
            City(x=0, y=10)]

nr_of_cities = len(cityList)

ph_on = np.zeros((nr_of_cities, nr_of_cities))
distances = np.zeros((nr_of_cities, nr_of_cities))
dec_matrix = np.zeros((nr_of_cities, nr_of_cities))
ants = []
tau_eta = np.zeros((nr_of_cities, nr_of_cities))

for i in range(nr_of_cities):
    for j in range(nr_of_cities):
        if j != i:
            dec_matrix[i, j] = 0
            distances[i, j] = cityList[i].distance(cityList[j])
        else:
            distances[i, j] = np.inf
            dec_matrix[i, j] = np.inf


def init(ant_nr, ph_t0):

    for i in range(nr_of_cities):
        for j in range(nr_of_cities):
            if i != j:
                ph_on[i, j] = ph_t0
            else:
                ph_on[i, j] = 0

    for i in range(ant_nr):
        ants.append(Ant(cityList))


def move_ants():
    for i in range(nr_of_cities):
        for j in range(nr_of_cities):
            if j != i:
                tau_eta[i, j] = (ph_on[i, j] ** alpha) * ((1/distances[i, j]) ** beta)

    for ant in ants:
        nonvisited = [city for city in cityList if city not in ant.visited_cities]
        i = cityList.index(ant.city)
        nbr_dec = 0
        for nv_city in nonvisited:
            j = cityList.index(nv_city)
            nbr_dec += tau_eta[i, j]

        dec_list = []
        sum_dec_m = 0
        for nv_city in nonvisited:
            j = cityList.index(nv_city)
            val = ((ph_on[i, j] ** alpha) * ((1/distances[i, j]) ** beta)) / nbr_dec
            # print(str(val) + " : " + str(ph_on[i, j]) + " : " + str(1/distances[i, j]) + " : " + str(nbr_dec))
            dec_list.append((j, val))
            sum_dec_m += val

        r = random.uniform(0, 1)
        x = 0
        while r > 0:
            next_city = cityList[dec_list[x][0]]
            r -= dec_list[x][1] / sum_dec_m
            x += 1

        ant.visited(next_city)


def update_pheromones(bestAnt, bestAntDist):
    new_ph = np.zeros((nr_of_cities, nr_of_cities))
    for ant in ants:
        if ant.route_distance() < bestAntDist:
            bestAntDist = ant.route_distance()
            bestAnt = copy.copy(ant)

        dist = 1 / (ant.route_distance())
        i = cityList.index(ant.visited_cities[0])
        j = cityList.index(ant.visited_cities[-1])
        new_ph[i, j] += dist
        new_ph[j, i] += dist
        for x in range(1, len(ant.visited_cities)):
            j = cityList.index(ant.visited_cities[x])
            new_ph[i, j] += dist
            new_ph[j, i] += dist
            i = j
        ant.next_iteration(cityList)
    return new_ph, bestAnt, bestAntDist


init(ant_nr, ph_t0)

while t < t_max:
    for moves in range(len(cityList)-1):
        move_ants()
    new_ph, bestAnt, bestAntDist = update_pheromones(bestAnt, bestAntDist)
    ph_on = np.multiply(ph_on, 0.5)
    ph_on = np.add(ph_on, new_ph)
    t += 1

the_route = []
for vc in bestAnt.visited_cities:
    the_route.append([vc.x, vc.y])
the_route.append([bestAnt.visited_cities[0].x, bestAnt.visited_cities[0].y])
np_route = np.array(the_route)
plt.title("Final Route")
print(bestAnt.visited_cities)
plt.plot(*np_route.T, alpha=0.5)
plt.scatter(np_route[:, 0], np_route[:, 1], color='b')
plt.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
plt.xticks(range(0, 16, 1))
plt.yticks(range(0, 16, 1))
plt.show()


# np_cl = np.array([(city.x, city.y) for city in cityList])
#
# for i in range(len(cityList)):
#     for j in range(len(cityList)):
#         sub = np.array([(cityList[i].x, cityList[i].y), (cityList[j].x, cityList[j].y)])
#         plt.plot(*sub.T, alpha=ph_on[i, j], color='b')
# plt.scatter(np_cl[:, 0], np_cl[:, 1], color='b')
# plt.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
# plt.xticks(range(0, 5, 1))
# plt.yticks(range(0, 11, 1))
# plt.show()
#
# print(ph_on)
