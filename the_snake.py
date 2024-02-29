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

    def __init__(self, position=0, body_color=0):
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


class Apple(GameObject):
    """Класс для представления яблока."""

    def __init__(self,
                 position=(randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                           randint(0, GRID_HEIGHT - 1) * GRID_SIZE),
                 body_color=APPLE_COLOR):
        """Инициализация яблока.

        Аргументы:
            position (tuple): Кортеж координат яблока.
            body_color (tuple): Цвет яблока.
        """
        super().__init__(position, body_color)

    def randomize_position(self):
        """Установка случайной позиции яблока в игровом окне."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE, 
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        """Отрисовка яблока на поверхности.

        Аргумент:
            surface (pygame.Surface): Поверхность для отрисовки яблока.
        """
        rect = pygame.Rect(
                          (self.position[0], self.position[1]),
                          (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для представления змейки."""

    def __init__(self, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                 body_color=SNAKE_COLOR):
        """Инициализация змейки.

        Аргументы:
            position (tuple): Кортеж координат головы змейки (head_x, head_y).
            body_color (tuple): Цвет змейки.
        """
        super().__init__(position, body_color)
        self.length = 2
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновление позиции змейки в связи с выбранным направлением."""
        head_x, head_y = self.position
        if self.direction == UP:
            head_y -= GRID_SIZE
        elif self.direction == DOWN:
            head_y += GRID_SIZE
        elif self.direction == LEFT:
            head_x -= GRID_SIZE
        elif self.direction == RIGHT:
            head_x += GRID_SIZE

        head_x = head_x % SCREEN_WIDTH
        head_y = head_y % SCREEN_HEIGHT

        self.last = self.positions[-1]
        self.position = (head_x, head_y)
        self.positions.insert(0, self.position)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовка змейки на поверхность.

        Аргумент:
            surface (pygame.Surface): Поверхность для отрисовки змейки.
        """
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )  
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возврат позиции головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки к начальному состоянию."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Обработка направления игрового объекта по нажатию клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры."""
    snake = Snake(((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)), SNAKE_COLOR)
    apple = Apple((randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                   randint(0, GRID_HEIGHT - 1) * GRID_SIZE), APPLE_COLOR)

    running = True
    while running:
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)

        snake.update_direction()

        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position() 

        if snake.get_head_position() in snake.positions[1:]:
            running = False

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
