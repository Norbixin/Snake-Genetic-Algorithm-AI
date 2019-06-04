from snake_game import Snake
from neural_network import Network
import time


def run(weights, number_of_hidden_layers, node_for_first_layer, node_for_hidden_layer, node_for_last_layer, max_steps,
        board_size=None, draw=False, generation=None):
    snake = Snake(board_size=board_size, generation=generation)
    score = 0
    game_score = 0
    direction = 0
    same_direction = 0

    left_collision, right_collision, front_collision, angle, distance = snake.return_variables()

    network = Network(number_of_hidden_layers, node_for_first_layer,
                      node_for_hidden_layer, node_for_last_layer, weights)

    if draw:
        snake.init_draw()

    snake.start_game()

    steps = 0

    while steps < max_steps:
        if not snake.playing:
            break

        # last_distance = distance
        last_score = game_score
        last_direction = direction

        network.set_first_layer([left_collision, right_collision, front_collision, angle, distance])
        output = network.calculate_output()
        if output[0] >= output[1]:
            if output[0] >= output[2]:
                left_collision, right_collision, front_collision, angle, distance = snake.move("left")
                direction = 0
            else:
                left_collision, right_collision, front_collision, angle, distance = snake.move("forward")
                direction = 2
        elif output[1] >= output[2]:
            left_collision, right_collision, front_collision, angle, distance = snake.move("right")
            direction = 1
        else:
            left_collision, right_collision, front_collision, angle, distance = snake.move("forward")
            direction = 2

        game_score = snake.score

        if game_score > last_score:
            score += 1
            steps = 0
        if last_direction == direction:
            same_direction += 1
        else:
            same_direction = 0
        if same_direction > board_size:
            score = 0
            snake.playing = False

        if draw:
            snake.draw_game()
            time.sleep(0.02)
        steps += 1

    return score
