import pygame
import random as R
import math


class Snake:

    display = None
    clock = None
    display_width = 0
    display_height = 0
    square_size = 0
    green = (0, 255, 0)
    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    playing = False
    generation = None

    board_size = 0
    apple_position = []
    snake_position = []
    snake_head = []
    # 0 - up
    # 1 - left
    # 2 - down
    # 3 - right
    snake_direction = 0
    score = 0

    def __init__(self, board_size=8, generation=None):
        self.board_size = board_size
        self.snake_head = [R.randint(1, self.board_size - 2), R.randint(1, self.board_size - 2)]
        self.snake_position = [self.snake_head]
        self.snake_direction = R.randint(0, 3)
        self.generate_apple()
        self.generation = generation
        self.square_size = int(700 / board_size)

        self.display_width = board_size * self.square_size
        self.display_height = (board_size + 1) * self.square_size

    def draw_apple(self):
        pygame.draw.rect(self.display, self.red, pygame.Rect(self.apple_position[0] * self.square_size,
                                                             self.apple_position[1] * self.square_size,
                                                             self.square_size, self.square_size))

    def draw_snake(self):
        for square in self.snake_position:
            pygame.draw.rect(self.display, self.green,
                             pygame.Rect(square[0] * self.square_size, square[1] * self.square_size, self.square_size,
                                         self.square_size))

    def draw_score(self):
        font = pygame.font.SysFont("Arial", int(self.square_size / 2))
        text = font.render("Score : " + str(self.score), True, self.black)
        self.display.blit(text, (
            100 - text.get_width() // 2, (self.board_size + 0.5) * self.square_size - text.get_height() // 2))

    def draw_generation(self):
        font = pygame.font.SysFont("Arial", int(self.square_size / 2))
        text = font.render("Generation : " + str(self.generation), True, self.black)
        self.display.blit(text, (
            350 - text.get_width() // 2, (self.board_size + 0.5) * self.square_size - text.get_height() // 2))

    def return_variables(self):
        return int(self.left_collision()), int(self.right_collision()), int(
            self.front_collision()), self.snake_apple_angle(), self.snake_apple_distance()

    def move(self, direction):
        if direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        elif direction == "forward":
            self.move_forward()

        return self.return_variables()

    def move_forward(self):
        self.snake_head = self.in_front_of_snake(self.snake_direction)
        self.snake_position.insert(0, self.snake_head)
        self.check_collisions()

    def move_left(self):
        self.snake_direction = (self.snake_direction + 1) % 4
        self.snake_head = self.in_front_of_snake(self.snake_direction)
        self.snake_position.insert(0, self.snake_head)
        self.check_collisions()

    def move_right(self):
        self.snake_direction -= 1
        if self.snake_direction < 0:
            self.snake_direction = 3
        self.snake_head = self.in_front_of_snake(self.snake_direction)
        self.snake_position.insert(0, self.snake_head)
        self.check_collisions()

    def generate_apple(self):
        self.apple_position = [R.randint(0, self.board_size - 1), R.randint(0, self.board_size - 1)]
        while self.apple_position in self.snake_position:
            self.apple_position = [R.randint(0, self.board_size - 1), R.randint(0, self.board_size - 1)]

    def in_front_of_snake(self, direction):
        if direction == 0:
            return [self.snake_head[0], self.snake_head[1] - 1]
        if direction == 1:
            return [self.snake_head[0] - 1, self.snake_head[1]]
        if direction == 2:
            return [self.snake_head[0], self.snake_head[1] + 1]
        if direction == 3:
            return [self.snake_head[0] + 1, self.snake_head[1]]

    def check_collisions(self):
        if self.snake_head[0] < 0 or self.snake_head[0] >= self.board_size or self.snake_head[1] < 0 or self.snake_head[
                1] >= self.board_size:
            self.playing = False
        if self.snake_head in self.snake_position[1:]:
            self.playing = False
        if self.snake_head == self.apple_position:
            self.score += 1
            self.generate_apple()
        else:
            self.snake_position.pop()

    def front_collision(self, direction=None):
        if direction is None:
            direction = self.snake_direction
        next_position = self.in_front_of_snake(direction)
        if next_position[0] < 0 or next_position[0] >= self.board_size or next_position[1] < 0 or next_position[
                1] >= self.board_size or next_position in self.snake_position:
            return True
        else:
            return False

    def left_collision(self):
        return self.front_collision((self.snake_direction + 1) % 4)

    def right_collision(self):
        direction = self.snake_direction - 1
        if direction < 0:
            direction = 3
        return self.front_collision(direction)

    def snake_apple_angle(self):
        # 0 - up
        # 1 - left
        # 2 - down
        # 3 - right
        if self.snake_direction == 0:
            head_vector = [0, 1]
        elif self.snake_direction == 1:
            head_vector = [-1, 0]
        elif self.snake_direction == 2:
            head_vector = [0, -1]
        else:
            head_vector = [1, 0]
        head_apple_vector = [self.apple_position[0] - self.snake_head[0], self.snake_head[1] - self.apple_position[1]]
        dot = head_vector[0] * head_apple_vector[0] + head_vector[1] * head_apple_vector[1]
        det = head_vector[0] * head_apple_vector[1] - head_vector[1] * head_apple_vector[0]
        angle = math.atan2(det, dot) / (2 * math.pi)
        return angle

    def snake_apple_distance(self):
        x = self.snake_head[0] - self.apple_position[0]
        y = self.snake_head[1] - self.apple_position[1]
        return math.sqrt(x * x + y * y) / ((self.board_size - 1) * math.sqrt(2))

    def start_game(self):
        self.playing = True

    def init_draw(self):
        pygame.init()
        pygame.display.set_caption('SnakeAI')
        self.display = pygame.display.set_mode((self.display_width, self.display_height))

    @staticmethod
    def quit():
        pygame.quit()

    def draw_game(self):
        if self.playing is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False

            self.display.fill(self.white)

            self.draw_apple()
            self.draw_snake()
            self.draw_score()
            self.draw_generation()

            pygame.display.update()
        else:
            pygame.quit()
            return self.score
