"""Модуль с игрой 'Змейка'."""
from random import randint

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self, position=(0, 0), body_color=None):
        """Инициализация игрового объекта.

        Аргументы:
            position (tuple): Кортеж координат объекта.
            body_color (tuple): Цвет игрового объекта.
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка игрового объекта."""
        pass

    def draw_cell(self, position, color=None):
        """Отрисовка одной ячейки."""
        if color is None:
            color = self.body_color
        rect = pygame.Rect((position), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)


class Apple(GameObject):
    """Класс для представления яблока."""

    def __init__(self, occupied_positions=[], body_color=APPLE_COLOR):
        """Инициализация яблока.

        Аргументы:
            occupied_positions (list): Занятые позиции в игре.
            body_color (tuple): Цвет яблока.
        """
        super().__init__()
        self.GRID_SIZE = 20
        self.position = self.randomize_position(occupied_positions)
        self.body_color = body_color

    def randomize_position(self, occupied_positions):
        """Установка случайной позиции яблока в игровом окне."""
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * self.GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * self.GRID_SIZE)
            if new_position not in occupied_positions:
                self.position = new_position
                break
        return self.position

    def draw(self):
        """Отрисовка яблока."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс для представления змейки."""

    def __init__(self, position=(0, 0), body_color=SNAKE_COLOR):
        """Инициализация змейки.

        Аргументы:
            position (tuple): Кортеж координат головы змейки (head_x, head_y).
            body_color (tuple): Цвет змейки.
        """
        super().__init__(position, body_color)
        self.last = None
        self.reset()

    def update_direction(self, direction):
        """Обновление направления движения змейки."""
        self.direction = direction

    def move(self):
        """Обновление позиции змейки в связи с выбранным направлением."""
        head_x, head_y = self.position
        point_x, point_y = self.direction
        head_x = (head_x + point_x * GRID_SIZE) % SCREEN_WIDTH
        head_y = (head_y + point_y * GRID_SIZE) % SCREEN_HEIGHT

        self.last = self.positions[-1]
        self.position = (head_x, head_y)
        self.positions.insert(0, self.position)
        if len(self.positions) > self.length:
            tail = self.positions.pop()
            self.draw_cell(tail, BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Отрисовка змейки."""
        self.draw_cell(self.positions[0], self.body_color)
        if len(self.positions) > self.length:
            self.draw_cell(self.positions[-1], BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возврат позиции головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки к начальному состоянию."""
        self.positions = [self.position]
        self.direction = RIGHT
        self.length = 1
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))


def handle_keys(game_object):
    """Обработка направления игрового объекта по нажатию клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple(snake.positions)

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        handle_keys(snake)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.position = apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
