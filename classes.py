import numpy as np
import random


class Ant:
    def __init__(self, city_list):
        self.city = random.sample(city_list, 1)[0]
        self.visited_cities = [self.city]

    def visited(self, city):
        if city not in self.visited_cities:
            self.visited_cities.append(city)

    def next_iteration(self, city_list):
        self.city = random.sample(city_list, 1)[0]
        self.visited_cities = [self.city]

    def route_distance(self):
        distance = 0
        for i in range(len(self.visited_cities) - 1):
            distance += City.distance(self.visited_cities[i], self.visited_cities[i + 1])
        if (len(self.visited_cities) - 1) > 0:
            distance += City.distance(self.visited_cities[0], self.visited_cities[-1])
        return distance


# Class defining cities coordinates

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        xd = abs(self.x - city.x)
        yd = abs(self.y - city.y)
        dist = np.sqrt((xd ** 2) + (yd ** 2))
        return dist

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
