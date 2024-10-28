from random import randint
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


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(320, 240), body_color=None):
        """
        Инициализирует игровой объект с позицией и цветом.

        :param position: начальная позиция объекта
        :param body_color: цвет объекта
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект. Реализация в подклассах."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        """Инициализация яблока с случайной позицией и цветом."""
        super().__init__(body_color=(255, 0, 0))
        self.randomize_position()

    def randomize_position(self):
        """Задает яблоку случайную позицию на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        """Инициализация змейки с начальной длиной, позицией и направлением."""
        super().__init__(body_color=(0, 255, 0))
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку в текущем направлении."""
        x, y = self.get_head_position()
        kx, ky = self.direction
        x = (x + GRID_SIZE * kx) % SCREEN_WIDTH
        y = (y + GRID_SIZE * ky) % SCREEN_HEIGHT

        if len(self.positions) == self.length:
            self.last = self.positions.pop()

        if (x, y) in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, (x, y))

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
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

    def reset(self):
        """Сбрасывает состояние змейки."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.__init__()


def handle_keys(game_object):
    """Обрабатывает события клавиатуры для управления направлением змейки."""
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
    """Основная функция для запуска игры."""
    pygame.init()
    snake_obj = Snake()
    apple_obj = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake_obj)
        snake_obj.update_direction()
        snake_obj.move()

        if snake_obj.get_head_position() == apple_obj.position:
            snake_obj.length += 1
            apple_obj.randomize_position()
        snake_obj.draw()
        apple_obj.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
