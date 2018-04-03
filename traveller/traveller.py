import random
import math
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


class City:
    def __init__(self, id, point=None):
        self.id = id
        if point is None:
            self.point = Point()
        else:
            self.point = point

    def __str__(self):
        return 'City: [id: {self.id}, {self.point}]'.format(self=self)


class Cities:
    def __init__(self):
        self.cityList: City = list()
        self.id: int = 0

    def generate_next_city(self, how: int = 1):
        for i in range(0, how):
            self.cityList.append(City(self.id))
            self.id += 1


class Node:
    pass


class Relation:
    def __init__(self, start: Node, destination: Node):
        self.start:Node = start
        self.destination:Node = destination
        self.distance = self.calculate_distance(start.data.point, destination.data.point)

    @staticmethod
    def calculate_distance(p1: Point, p2: Point):
        len_x = p1.x - p2.x
        len_y = p1.y - p1.y
        return math.sqrt(math.pow(len_x, 2) + math.pow(len_y, 2))

    def is_visited(self) -> bool:
        return self.start.is_visited == True and self.destination.is_visited == True

    def mark_as_visited(self, is_visited:bool):
        self.start.is_visited = is_visited
        self.destination.is_visited = is_visited

    def __str__(self):
        return 'Start: [{self.start}] Destination [{self.destination}] distance: {self.distance}'.format(self=self)


class Node:
    def __init__(self, data):
        self.data:City = data
        self.connections: list = list()
        self.is_visited: bool = False

    def add_relation(self, *children: Relation):
        for c in children:
            self.connections.append(c)

    def __str__(self):
        return 'Node: [{self.data}, is_visited: {self.is_visited}]'.format(self=self)


class Nodes:
    nodeList:Node = list()

    def __init__(self, cities = None):
        if(cities != None):
            for city in cities.cityList:
                self.nodeList.append(Node(city))

    def clear_is_visited(self):
        for node in self.nodeList:
            node.is_visited = False


class Relations:

    def __init__(self, nodes: Nodes = None):
        if (nodes != None):
            self.relationList = list()
            self.generate(copy.copy(nodes.nodeList))
        else:
            self.relationList = list()

    def generate(self, nodes):
        while len(nodes) > 1:
            start_node = nodes[0]
            del (nodes[0])
            for i in range(0, len(nodes)):
                relation = Relation(start_node, nodes[i])
                self.relationList.append(relation)

    def get_min_distance(self, id:int = None) -> Relation:
        if id is None:
            searchingList = self.relationList
        else:
            searchingList = self.get_relations_with_city(id)

        if len(searchingList) == 0:
            return None

        min_relation: Relation = searchingList[0]

        for relation in searchingList:
            if relation.distance < min_relation.distance:
                min_relation = relation
        return min_relation

    def get_available_relation_from(self, id):
        available_relations = Relations()
        for relation in self.relationList:
            if (relation.destination.data.id == id or relation.start.data.id == id) and not relation.is_visited():
                available_relations.relationList.append(relation)
        return available_relations

    # mark as dangerous
    def get_relations_without_city(self, id, is_visited = False):
        relations = list();
        for relation in self.relationList:
            if relation.destination.data.id != id and relation.start.data.id != id:
                relations.append(relation)
        return relations

    # mark as dangerous
    def get_relations_with_city(self, id):
        relations = list()
        for relation in self.relationList:
            if relation.destination.data.id == id or relation.start.data.id == id:
                relations.append(relation)
        return relations

    def mark_all_visited(self, is_visited:bool):
        for relation in relations.relationList:
            relation.mark_as_visited(False)


class Path:
    relations = list()

    def get_distance(self):
        distance = 0
        print(len(relations.relationList))
        for relation in self.relations:
            distance += relation.distance
        return distance


class SmallestCost:
    path:Path = Path()

    def __init__(self, relations:Relations):
        self.relations = copy.copy(relations)
        self.caluclate()

    def caluclate(self):
        relations.mark_all_visited(False)
        self.path.relations.clear()

        shortest_relation = relations.get_min_distance()
        self.path.relations.append(shortest_relation)
        shortest_relation.mark_as_visited(True)
        next_id = shortest_relation.destination.data.id

        while True:
            relations_from_node = relations.get_available_relation_from(next_id)

            if relations_from_node is None or len(relations_from_node.relationList) is 0:
                break

            shortest_relation = relations_from_node.get_min_distance()
            self.path.relations.append(shortest_relation)

            if shortest_relation.destination.is_visited is False:
                next_id = shortest_relation.destination.data.id
            elif shortest_relation.start.is_visited is False:
                next_id = shortest_relation.start.data.id

            shortest_relation.mark_as_visited(True)

    def __str__(self):
        s = ""
        for relation in self.path.relations:
            s += str(relation) + "\n"
        s += "Total distance: " + str(self.path.get_distance()) + "\n"
        return s


class BruteForce:

    def __init__(self, relations):
        self.relations = copy.copy(relations)
        self.nodes_id = list()
        self.generate_id()
        self.permutation_pare_index = 0

    def generate_id(self):
        for relation in self.relations.relationList:
            is_already_id_in_list = [False, False]
            for id in self.nodes_id:
                if relation.start.data.id is id:
                    is_already_id_in_list[0] = True
                if relation.destination.data.id is id:
                    is_already_id_in_list[1] = True
                if is_already_id_in_list[0] is True and is_already_id_in_list[1] is True:
                    break

            if is_already_id_in_list[0] is False:
                self.nodes_id.append(relation.start.data.id)
            if is_already_id_in_list[1] is False:
                self.nodes_id.append(relation.destination.data.id)

        self.nodes_id = sorted(self.nodes_id)

    def next_permutation(self):
        tmp = self.nodes_id[self.permutation_pare_index]
        self.nodes_id[self.permutation_pare_index] = self.nodes_id[self.permutation_pare_index+1]
        self.nodes_id[self.permutation_pare_index+1] = tmp
        self.permutation_pare_index += 1
        if self.permutation_pare_index < len(self.nodes_id):
            self.permutation_pare_index = 0

cities = Cities()
cities.generate_next_city(3)
nodes = Nodes(cities)
relations = Relations(nodes)

bf = BruteForce(relations)
bf.permutate()

'''
for x in bf.nodes_id:
    print(x)
'''

'''
for x in relations.relationList:
    print(x)
'''


'''
smallestCost = SmallestCost(relations)
smallestCost.caluclate()

print(smallestCost)
'''