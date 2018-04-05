import random
import copy

class Config:
    POPULATION_SIZE = 50
    MAX_GENERATION = 50
    CHROMOSOME_MAX_LEN = 8
    CROSSOVER_PROBABILITY = 0.4
    MUTATION_PROBABILITY = 0.05


class Chromosome:
    MAX_LEN = Config.CHROMOSOME_MAX_LEN
    start_id = 1
    id = start_id

    def __init__(self):
        self.alleles = [None] * Chromosome.MAX_LEN
        self.id = Chromosome.id
        Chromosome.id += 1
        self.adaptation = 0
        for i in range(0, Chromosome.MAX_LEN):
            self.alleles[i] = random.randint(0, 1)
        self.adaptation_assessment()

    @staticmethod
    def rand_locus():
        locus = random.randint(1, Chromosome.MAX_LEN - 2)
        return locus

    def allelles_to_str(self):
        s = ""
        for i in range(0, Chromosome.MAX_LEN):
            s += str(self.alleles[i])
        return s

    def adaptation_assessment(self):
        value = int(self.allelles_to_str(), 2)
        self.adaptation = (value * value + 1) * 2

    def __str__(self):
        return 'Chromosome id {self.id} {self.alleles} Adaptation: {self.adaptation}'.format(self=self)


class Population:

    def __init__(self, size: int = 0):
        self.size = size
        self.stored_chromosome = []
        for i in range(0, size):
            self.stored_chromosome.append(Chromosome())
        self.sort()

    def add(self, chromosome: Chromosome):
        self.size += 1
        self.stored_chromosome.append(chromosome)

    def get(self, index: int):
        return self.stored_chromosome[index]

    def __str__(self):
        s = ""
        for i in range(0, self.size):
            s += str(self.stored_chromosome[i]) + "\n"
        return s

    def sort(self):
        self.stored_chromosome.sort(key=lambda x: x.adaptation, reverse=True)

class Roulette:

    def __init__(self, population: Population):
        self.population = population
        self.posterity = Population(0)
        self.adaptation_sum = 0
        self.calculate_adaptation_sum()
        self.chance_table = [None] * population.size
        self.scope = [None] * (population.size + 1)
        self.max_scope = 0
        self.calculate_scope()
        self.rand()
        self.posterity.sort()

    def calculate_adaptation_sum(self):
        for chromosome in self.population.stored_chromosome:
            self.adaptation_sum += chromosome.adaptation

    """
    Scope is calculating for given chromosome to specify how 
    much 'space' takes in the roulette
    """
    def calculate_scope(self):
        itr = 0
        sum = 0
        for chromosome in self.population.stored_chromosome:
            self.scope[itr] = sum
            chance = chromosome.adaptation / self.adaptation_sum * 100
            sum += chance
            self.chance_table[itr] = chance
            itr += 1

        self.scope[itr] = sum
        self.max_scope = sum

    def calculate_roulete_range_table(self):
        for i in range(self.population.size, 0, -1):
            pass

    def rand(self):
        for i in range(0, self.population.size):
            self.rand_next()

    def rand_next(self):
        roulette_position = random.uniform(0.0, self.max_scope)
        for x in range(0, self.population.size):
            i = self.population.size - x - 1
            if roulette_position > self.scope[i]:
                self.posterity.add(self.population.stored_chromosome[i])
                break


class Genetic:

    def __init__(self, population:Population):
        self.population = population
        self.crossed_population = Population()
        self.crossed_pair_list = []
        self.mutated_chromosome_list = []
        self.stored_id = list(range(0, self.population.size))
        self.run_algorithm()

    def run_algorithm(self):
        max_step = int(len(self.stored_id)/2)
        for i in range(0, max_step):
            first_chromosome = self.get_random_chromosome()
            second_chromosome = self.get_random_chromosome()

            self.check_cross(first_chromosome, second_chromosome)
            self.check_mutation(first_chromosome)
            self.check_mutation(second_chromosome)

            if len(self.stored_id) == 1:
                chromosome = self.population.get(0)
                self.crossed_population.add(chromosome)
                self.check_mutation(chromosome)
                self.crossed_population.sort()
                break

        self.crossed_population.sort()

    def get_random_chromosome(self):
        max_index = len(self.stored_id) - 1
        random_index = random.randint(0, max_index)
        chromosome_index = self.stored_id[random_index]
        self.stored_id.remove(chromosome_index)

        return self.population.get(chromosome_index)

    def check_cross(self, first_chromosome: Chromosome, second_chromosome: Chromosome):
        random_number = random.uniform(0, 1)
        if random_number < Config.CROSSOVER_PROBABILITY:
            crossed_pair = CrossedPair(first_chromosome, second_chromosome)
            first_chromosome = crossed_pair.first_chromosome_result
            second_chromosome = crossed_pair.second_chromosome_result
            self.crossed_pair_list.append(crossed_pair)

        self.crossed_population.add(first_chromosome)
        self.crossed_population.add(second_chromosome)

    def check_mutation(self, chromosome: Chromosome):
        random_number = random.uniform(0, 1)
        if random_number < Config.MUTATION_PROBABILITY:
            mutated_chromosome = MutatedChromosome(chromosome)
            self.mutated_chromosome_list.append(mutated_chromosome)


class CrossedPair:

    def __init__(self, first_chromosome: Chromosome, second_chromosome: Chromosome):
        self.locus = Chromosome.rand_locus()
        self.first_chromosome: Chromosome = first_chromosome
        self.second_chromosome: Chromosome = second_chromosome
        self.first_chromosome_result: Chromosome = None
        self.second_chromosome_result: Chromosome = None
        self.crossing(first_chromosome, second_chromosome)

    def crossing(self, first_chromosome: Chromosome, second_chromosome: Chromosome):
        self.first_chromosome_result = copy.deepcopy(first_chromosome)
        self.second_chromosome_result = copy.deepcopy(second_chromosome)

        tmp = copy.deepcopy(self.first_chromosome_result)
        for i in range(self.locus, Chromosome.MAX_LEN):
            self.first_chromosome_result.alleles[i] = self.second_chromosome_result.alleles[i]
            self.second_chromosome_result.alleles[i] = tmp.alleles[i]
        self.first_chromosome_result.adaptation_assessment()
        self.second_chromosome_result.adaptation_assessment()

    def chromosome_with_locus_str(self, chromosome):
        alleles_with_locus_str = ""
        for i in range(0, Chromosome.MAX_LEN):
            alleles_with_locus_str += str(chromosome.alleles[i])
            if i == self.locus:
                alleles_with_locus_str += "|"

        return 'Chromosome id {chromosome.id} {alleles_with_locus_str} Adaptation: {chromosome.adaptation}'\
            .format(chromosome=chromosome, alleles_with_locus_str=alleles_with_locus_str)

    def __str__(self):
        s = "\nLocus: {self.locus}\n".format(self=self)
        s += self.chromosome_with_locus_str(self.first_chromosome) + "\n"
        s += self.chromosome_with_locus_str(self.second_chromosome) + "\n"
        s += "Result: \n"
        s += self.chromosome_with_locus_str(self.first_chromosome_result) + "\n"
        s += self.chromosome_with_locus_str(self.second_chromosome_result) + "\n"
        return s


class MutatedChromosome:

    def __init__(self, chromosome: Chromosome):
        self.chromosome_before = copy.deepcopy(chromosome)
        self.mutation_index = 0
        self.chromosome_mutated = self.mutation(chromosome)

    def mutation(self, chromosome: Chromosome):
        self.mutation_index = random.randint(0, Chromosome.MAX_LEN - 1)
        value = chromosome.alleles[self.mutation_index]
        if value == 0:
            value = 1
        else:
            value = 0

        chromosome.alleles[self.mutation_index] = value
        chromosome.adaptation_assessment()
        return chromosome

    def chromosome_show_mutation(self, chromosome: Chromosome):
        alleles_with_mutation_str = ""
        for i in range(0, len(chromosome.alleles)):
            if i == self.mutation_index:
                alleles_with_mutation_str += "[" + str(chromosome.alleles[i]) + "]"
            else :
                alleles_with_mutation_str += str(chromosome.alleles[i])

        return 'Chromosome id {chromosome.id} {alleles_with_mutation_str} Adaptation: {chromosome.adaptation}'\
            .format(chromosome=chromosome, alleles_with_mutation_str=alleles_with_mutation_str)

    def __str__(self):
        return "Mutation index = {self.mutation_index}\n".format(self=self) \
                + self.chromosome_show_mutation(self.chromosome_before) + "\n" \
                + self.chromosome_show_mutation(self.chromosome_mutated) + "\n"


p = Population(Config.POPULATION_SIZE)

for i in range(0, Config.MAX_GENERATION):
    if i != 0:
        p = copy.deepcopy(g.crossed_population)

    print("Generation number: " + str(i))
    print(p)
    r = Roulette(p)
    print("Population after roulette:")
    print(r.posterity)
    g = Genetic(r.posterity)

    print("Crossing step by step:")
    for pair in g.crossed_pair_list:
        print(pair)

    print("Show mutation:")
    for mutated_chromosome in g.mutated_chromosome_list:
        print(mutated_chromosome)

    print("Population after crossing and mutation")
    print(g.crossed_population)

    print("=========")