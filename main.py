import sys
import getopt
from genetic_algorithm import GeneticAlgorithm


def main(argv):
    # Variables for genetic algorithm
    number_of_generations = 30
    population_size = 100
    crossover_probability = 0.7
    mutation_probability = 0.1

    # Variables for neutral network
    number_of_hidden_layers = 3
    node_for_hidden_layer = 6

    # Variables for snake game
    draw = False
    board_size = 10

    log = False

    try:
        opts, args = getopt.getopt(argv, "hdLg:p:c:m:l:n:b:",
                                   ["generations=", "population=", "crossover=", "mutation=", "layers=",
                                    "nodes=", "board="])
    except getopt.GetoptError:
        print(
            'main.py -d (draw best run) -L (save every chromosome with its score to log file) -g <number_of_generations> -p <population_size> -c <crossover_probability>\
 -m <mutation_probability> -l <number_of_hidden_layers> -n <nodes_for_hidden_layer> -b <board_size>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                'main.py -d (draw best run) -L (save every chromosome with its score to log file) -g <number_of_generations> -p <population_size> -c <crossover_probability>\
 -m <mutation_probability> -l <number_of_hidden_layers> -n <nodes_for_hidden_layer> -b <board_size>')
            sys.exit()
        elif opt == '-d':
            draw = True
        elif opt == '-L':
            log = True
        elif opt in ("-g", "--generations"):
            number_of_generations = int(arg)
        elif opt in ("-p", "--population"):
            population_size = int(arg)
        elif opt in ("-c", "--crossover"):
            crossover_probability = float(arg)
        elif opt in ("-m", "--mutation"):
            mutation_probability = float(arg)
        elif opt in ("-l", "--layers"):
            number_of_hidden_layers = int(arg)
        elif opt in ("-n", "--nodes"):
            node_for_hidden_layer = int(arg)
        elif opt in ("-b", "--board"):
            board_size = int(arg)

    print(number_of_generations, population_size, crossover_probability, mutation_probability, number_of_hidden_layers,
          node_for_hidden_layer, board_size)

    genetic_algorithm = GeneticAlgorithm(population_size, number_of_generations, crossover_probability,
                                         mutation_probability, board_size, draw, log)
    genetic_algorithm.number_of_hidden_layers = number_of_hidden_layers
    genetic_algorithm.node_for_hidden_layer = node_for_hidden_layer
    genetic_algorithm.init_population()
    genetic_algorithm.evolve()


if __name__ == "__main__":
    main(sys.argv[1:])
