import random as r
from run_game import run


class GeneticAlgorithm:

    # Variables for genetic algorithm
    population_size = 0
    number_of_generations = 0
    crossover_probability = 0
    mutation_probability = 0
    population = []

    # Variables for neutral network
    number_of_hidden_layers = 0
    node_for_hidden_layer = 0
    node_for_first_layer = 5
    node_for_last_layer = 3

    # Variables for snake game
    board_size = 0
    draw = None

    log = False
    log_file = None

    def __init__(self, population_size, number_of_generations, crossover_probability, mutation_probability, board_size,
                 draw, log):
        self.population_size = population_size
        self.number_of_generations = number_of_generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

        self.draw = draw
        self.board_size = board_size

        if log:
            self.log = log
            self.log_file = open("log.txt", "w")

    @staticmethod
    def create_node(edges):
        node = []
        for edge_num in range(edges):
            node.append(r.uniform(-1, 1))
        return node

    def create_layer(self, nodes, edges_for_node):
        layer = []
        for node_num in range(nodes):
            layer.append(self.create_node(edges_for_node))
        return layer

    def init_population(self):
        for chromosome_num in range(self.population_size):
            chromosome = [self.create_layer(self.node_for_first_layer, self.node_for_hidden_layer)]
            for layer_num in range(1, self.number_of_hidden_layers):
                chromosome.append(self.create_layer(self.node_for_hidden_layer, self.node_for_hidden_layer))
            chromosome.append(self.create_layer(self.node_for_hidden_layer, self.node_for_last_layer))
            self.population.append(chromosome)

    def fitness(self, chromosome):
        return run(chromosome, self.number_of_hidden_layers, self.node_for_first_layer, self.node_for_hidden_layer,
                   self.node_for_last_layer, self.board_size * self.board_size, self.board_size)

    def draw_run(self, chromosome, generation):
        return run(chromosome, self.number_of_hidden_layers, self.node_for_first_layer, self.node_for_hidden_layer,
                   self.node_for_last_layer, self.board_size * self.board_size, self.board_size, True,
                   generation=generation)

    def generate_scores(self):
        scores = []
        score_sum = 0
        for chromosome_num, chromosome in enumerate(self.population):
            score = self.fitness(chromosome)
            scores.append([score, chromosome])
            score_sum += score
            if self.log:
                self.log_file.write(
                "Chromosome [" + str(chromosome_num + 1) + "] score: " + str(score) + ", genes: " + str(
                    chromosome) + "\n")
        print("Average score: ", str(score_sum / self.population_size))
        if self.log:
            self.log_file.write("Average score: " + str(score_sum / self.population_size) + "\n")
        return scores

    def evolve(self):
        for generation_num in range(1, self.number_of_generations + 1):
            print("Generation: ", generation_num)
            if self.log:
                self.log_file.write("Generation: " + str(generation_num) + "\n")
            scores = self.generate_scores()
            scores.sort(reverse=True)
            parents = []
            score_sum = 0
            for score, chromosome in scores[:int(len(scores)/10)]:
                if score > 0:
                    parents.append([score, chromosome])
                    score_sum += score
            if len(parents) < 2:
                print("Population is too weak")
                return None
            if self.log:
                self.log_file.write("Best score: " + str(parents[0][0]) + "\n\n")

            print("Score for best chromosome: ", parents[0][0])

            if self.draw:
                self.draw_run(scores[0][1], generation_num)

            self.population = self.generate_offspring(parents, score_sum)
        if self.log:
            self.log_file.close()

    @staticmethod
    def roulette(population, score_sum, last_chromosome=None):
        result = []
        random = r.randint(0, score_sum)
        cur = 0
        for chromosome in population:
            cur += chromosome[0]
            if cur >= random:
                result = chromosome[1]
                if last_chromosome != result:
                    break
        return result

    def generate_offspring(self, parents, score_sum):
        offspring = []
        while len(offspring) < self.population_size:
            parent1 = parent2 = self.roulette(parents, score_sum)
            while parent2 == parent1:
                parent2 = self.roulette(parents, score_sum, parent1)

            if r.uniform(0, 1) <= self.crossover_probability:
                child = self.crossover(parent1, parent2)
                if child not in offspring:
                    offspring.append(child)
            else:
                child = r.choice([parent1, parent2])
                if child not in offspring:
                    offspring.append(child)

            if r.uniform(0, 1) <= self.mutation_probability:
                offspring[-1] = self.mutate(offspring[-1])

        return offspring

    def mutate(self, chromosome):
        for layer_num in range(self.number_of_hidden_layers + 1):
            for node_num in range(len(chromosome[layer_num])):
                for edge_num in range(len(chromosome[layer_num][node_num])):
                    if r.uniform(0, 1) < 0.05:
                        chromosome[layer_num][node_num][edge_num] = r.uniform(-1, 1)
        return chromosome

    def crossover(self, parent1, parent2):
        child = []
        for layer_num in range(self.number_of_hidden_layers + 1):
            layer_child = []
            for node_num in range(len(parent1[layer_num])):
                layer_node = []
                for edge_num in range(len(parent1[layer_num][node_num])):
                    layer_node.append(
                        (parent1[layer_num][node_num][edge_num] + parent2[layer_num][node_num][edge_num]) / 2)
                layer_child.append(layer_node)
            child.append(layer_child)
        return child
