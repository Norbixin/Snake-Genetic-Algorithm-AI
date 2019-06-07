# Snake-Genetic-Algorithm-AI
### AI that trains snake using genetic algorithm and neural network

## Python-version 3.7

## Usage

- `python main.py`

## Flags
- `-h` help
- `-d` draw run for best chromosome
- `-L` save every chromosome with its score to log file
- `-g` `--generation` number of generations
- `-p` `--population` population size
- `-c` `--crossover` crossover probability
- `-m` `--mutation` mutation probability
- `-l` `--layers` number of hidden layers in neural network
- `-n` `--nodes` number of nodes in hidden layer
- `-b` `--board` board size

## Dependencies
- `pygame`

## Files
- `main.py` main file that runs genetic algorithm
- `snake_game.py` contains game logic, uses pygame for drawing
- `run_game.py` plays snake game using neural network for predicting next move, used by fitness function in genetic algorithm
- `genetic_algorithm.py` contains genetic algorithm functions
- `neural_network.py` contains neural network
