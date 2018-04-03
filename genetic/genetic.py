import random
import copy

class config:
    POPULATION_SIZE = 8
    CHROMOSOME_MAX_LEN = 7
    CROSSOVER_PROBABILITY = 0.9
    MUTATION_PROBABILITY = 0.2

class Chromosome:
    MAX_LEN = config.CHROMOSOME_MAX_LEN;
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
        locus = random.randint(1, Chromosome.MAX_LEN - 1)
        return locus;

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

    def __init__(self, size: int):
        self.size = size
        self.stored_chromosome = []
        for i in range(0, size):
            self.stored_chromosome.append(Chromosome())

        self.stored_chromosome.sort(key=lambda x: x.adaptation, reverse=True)

    def add(self, chromosome: Chromosome):
        self.size += 1
        self.stored_chromosome.append(chromosome)

    def __str__(self):
        s = ""
        for i in range(0, self.size):
            s += str(self.stored_chromosome[i]) + "\n"
        return s

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

    def calculate_adaptation_sum(self):
        for chromosome in self.population.stored_chromosome:
            self.adaptation_sum += chromosome.adaptation

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

class Crossover:

    def __init__(self, population:Population):
        self.population = population
        self.crossed_population = Population(config.POPULATION_SIZE)

        stored_id = list(range(Chromosome.start_id, self.population.size))
        for i in range(0, population.size):
            random_number = random.uniform(0, 1)
            locus = Chromosome.rand_locus();

            if len(stored_id) < 2:
                break

            first_chromosome_id = stored_id[random.randint(0, len(stored_id)-1)]
            stored_id.remove(first_chromosome_id)
            second_chromosome_id = stored_id[random.randint(0, len(stored_id)-1)]
            stored_id.remove(second_chromosome_id)

            if random_number < config.CROSSOVER_PROBABILITY:
                first_chromosome = self.population.stored_chromosome[first_chromosome_id]
                second_chromosome = self.population.stored_chromosome[second_chromosome_id]
                self.crossing(first_chromosome, second_chromosome)
                self.crossed_population.stored_chromosome.append(first_chromosome)
                self.crossed_population.stored_chromosome.append(second_chromosome)

            random_number = random.uniform(0,1)
            if random_number < config.MUTATION_PROBABILITY:
                self.mutation(first_chromosome)

            random_number = random.uniform(0, 1)
            if random_number < config.MUTATION_PROBABILITY:
                self.mutation(second_chromosome)


    def crossing(self, first_chromosome: Chromosome, second_chromosome: Chromosome):
        tmp = copy.deepcopy(first_chromosome);
        locus = Chromosome.rand_locus()
        for i in range(locus, Chromosome.MAX_LEN):
            first_chromosome.alleles[i] = second_chromosome.alleles[i]
            second_chromosome.alleles[i] = tmp.alleles[i]

    def mutation(self, chromosome: Chromosome):
        index = random.randint(0, Chromosome.MAX_LEN - 1)
        value = chromosome.alleles[index]
        if value == 1:
            value = 0
        else:
            value = 1
        chromosome.alleles[index] = value

p = Population(config.POPULATION_SIZE)
print(p)
r = Roulette(p)
c = Crossover(p)
print("after")
print(c.crossed_population)

""" print()
r.rand()
print(r.posterity) """
