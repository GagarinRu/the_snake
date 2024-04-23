from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """это базовый класс, от которого наследуются другие игровые объекты."""

    position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
    body_color = (0, 0, 0)

    def __init__(self):
        pass

    def draw(self):
        """Метод, отрисовывающий объекты"""


class Apple(GameObject):
    """Класс,описывающий яблоко."""

    body_color = APPLE_COLOR
    randomize_position = ''

    def __init__(self):
        self.body_color = Apple.body_color
        Apple.position = self.generate_position()

    def generate_position(self):
        """Метод,генерирующий позицию яблока."""
        return ((randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                (randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
                )

    def draw(self):
        """Метод draw класса Apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    body_color = SNAKE_COLOR
    length = 1
    positions = [GameObject.position]
    last = None
    next_direction = None

    def __init__(self):
        self.length = Snake.length
        self.direction = 'RIGHT'
        self.positions = Snake.positions
        self.body_color = Snake.body_color
        self.last = Snake.last
        self.next_direction = Snake.next_direction

    def draw(self):
        """Метод draw класса Snake."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод,обновляющий атрибут направления движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def handle_keys(self):
        """Функция обработки действий пользователя"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = 'UP'
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = 'DOWN'
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = 'RIGHT'

    def move(self):
        """Модуль,описывающий движение змейки."""
        head_snake = self.get_head_position()
        dx, dy = {'UP': UP,
                  'DOWN': DOWN,
                  'LEFT': LEFT,
                  'RIGHT': RIGHT
                  }[self.direction]
        new_head_snake = (head_snake[0] + (dx * GRID_SIZE),
                          head_snake[1] + (dy * GRID_SIZE)
                          )
        new_head_snake = self.boarder_out(new_head_snake)
        if new_head_snake in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_snake)
            if new_head_snake == Apple.position:
                Apple.position = Apple.generate_position(Apple)
                self.positions.append(self.positions[-1])
                self.length += 1
            elif len(self.positions) > self.length:
                self.positions.pop()

    def boarder_out(self, coord):
        """Модуль, отвечаюищий за перемещение на границы экрана"""
        x, y = coord
        if x < 0:
            coord = (SCREEN_WIDTH, y)
        elif x > SCREEN_WIDTH:
            coord = (0, y)
        elif y < 0:
            coord = (x, SCREEN_HEIGHT)
        elif y > SCREEN_HEIGHT:
            coord = (x, 0)
        return coord

    def get_head_position(self):
        """Модуль, создающий координаты головы"""
        return self.positions[0]

    def reset(self):
        """Модуль, сбрасывающий параметры змейки"""
        self.length = 1
        self.positions = [GameObject.position]
        self.direction = choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])


def main():
    """Инициализация PyGame:"""
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.handle_keys()
        snake.update_direction()
        snake.move()
        apple.draw()
        snake.draw()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
