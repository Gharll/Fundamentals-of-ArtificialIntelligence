import random
import math
import itertools
import numpy as np
import copy

class Point:
    maxRange = 100

    def __init__(self, x=None, y=None):
        if x is None:
            self.x = random.randint(0, self.maxRange)
        else:
            self.x = x

        if y is None:
            self.y = random.randint(0, self.maxRange)
        else:
            self.y = y

    def __str__(self):
        return 'Point: [{self.x}, {self.y}]'.format(self=self)


class Node:
    id = 0

    def __init__(self, point=None):
        self.id = Node.id
        Node.id = Node.id + 1
        if point is None:
            self.point = Point()
        else:
            self.point = point

    def __str__(self):
        return 'City: [id: {self.id}, {self.point}]'.format(self=self)


class Relation:
    def __init__(self, start: Node, destination: Node):
        self.start: Node = start
        self.destination: Node = destination
        self.distance = self.calculate_distance(start.point, destination.point)

    @staticmethod
    def calculate_distance(p1: Point, p2: Point):
        len_x = p1.x - p2.x
        len_y = p1.y - p1.y
        return math.sqrt(math.pow(len_x, 2) + math.pow(len_y, 2))

    def __str__(self):
        return 'Start: [{self.start}] Destination [{self.destination}] distance: {self.distance}'.format(self=self)


class Path:

    def __init__(self):
        self.relations = []
        self.total_distance = 0

    def add(self, relation: Relation):
        self.relations.append(relation)
        self.total_distance += relation.distance


class Area:
    def __init__(self, size: int):
        self.nodes = []
        self.generate_nodes(size)
        self.relations = []

    def generate_nodes(self, size: int):
        for i in range(0, size):
            self.nodes.append(Node())

    def generate_one_to_all_relations(self):
        size = len(self.nodes)
        for const_id in range(0, size - 1):
            for next_id in range(const_id + 1, size):
                start = self.nodes[const_id]
                destination = self.nodes[next_id]
                relation = Relation(start, destination)
                self.relations.append(relation)

    def nodes_str(self):
        s = "\n"
        for node in self.nodes:
            s += str(node) + "\n"
        return s

    def relations_str(self):
        s = "\n"
        for relation in self.relations:
            s += str(relation) + "\n"
        return s

    def __str__(self):
        return self.nodes_str() + self.relations_str()


class BruteForce:
    def __init__(self, area: Area):
        self.area = area
        self.paths = []
        self.min_path: Path = None
        self.max_path: Path = None

    def run(self):
        area_size = len(self.area.nodes)
        id_list = np.arange(area_size)
        permutations = itertools.permutations(id_list)
        for permutation in permutations:
            path = Path()
            for i in range(0, len(permutation) - 1):
                start = self.area.nodes[permutation[i]]
                destination = self.area.nodes[permutation[i+1]]
                relation = Relation(start, destination)
                path.add(relation)
            self.paths.append(path)
        self.generate_info()

    def generate_info(self):
        self.min_path = min(self.paths, key=lambda path: path.total_distance)
        self.max_path = max(self.paths, key=lambda path: path.total_distance)

    def __str__(self):
        return "Brtutforce method: \n Min: " + str(self.min_path.total_distance) \
               + "\n Max: " + str(self.max_path.total_distance)

class SmallestCost:

    def __init__(self, area: Area):
        self.area = area
        self.path = Path()

    def run(self):
        id_list = list(np.arange(len(self.area.nodes)))

        for i in range(0, len(id_list) - 1):
            relations = []
            for j in range(1, len(id_list)):
                relation = Relation(self.area.nodes[id_list[0]], self.area.nodes[id_list[j]])
                relations.append(relation)
            min_relation = min(relations, key=lambda relation: relation.distance)
            self.path.add(min_relation)

            min_id = None
            if min_relation.destination.id != id_list[0]:
                min_id = min_relation.destination.id
            elif min_relation.start.id != id_list[0]:
                min_id = min_relation.start.id

            id_list.pop(0)
            id_list.remove(min_id)
            id_list.insert(0, min_id)

    def __str__(self):
        return "Smallest cost method: \n min distance: " + str(sc.path.total_distance)



a = Area(5)
bf = BruteForce(a)
bf.run()
print(bf)

print()
sc = SmallestCost(a)
sc.run()
print(sc)


