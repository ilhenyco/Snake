from random import randint
from abc import abstractmethod
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
    """
    базовый класс
    от которого наследуются другие игровые объекты.
    """

    def __init__(self, body_color_value=None, position_value=None):
        if position_value is not None:
            self.position = position_value
        else:
            self.position = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
        self.body_color = body_color_value

    @abstractmethod
    def draw(self):
        """Отрисовка объекта."""
        pass


class Apple(GameObject):
    """
    класс, унаследованный от GameObject
    описывающий змейку и её поведение
    """

    def __init__(self):
        super().__init__(body_color_value=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        new_position = [randint(0, SCREEN_WIDTH - GRID_SIZE),
                        randint(0, SCREEN_HEIGHT - GRID_SIZE)]
        self.position = new_position

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Snake"""

    def __init__(self):
        super().__init__(body_color_value=SNAKE_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT  # Направление по умолчанию - вправо
        self.next_direction = None
        self.last = None  # Для хранения последней позиции (для затирания)

    def update_direction(self):
        """Новое направлние"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки, добавляя новую голову и удаляя хвост"""
        # Сохраняем последнюю позицию для затирания
        self.last = self.positions[-1] if self.positions else None

        # Получаем текущую позицию головы
        head_x, head_y = self.positions[0]

        # Вычисляем новую позицию головы в зависимости от направления
        if self.direction == RIGHT:
            new_head = (head_x + GRID_SIZE, head_y)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + GRID_SIZE)
        elif self.direction == LEFT:
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.direction == UP:
            new_head = (head_x, head_y - GRID_SIZE)
        else:
            new_head = (head_x, head_y)  # На случай неизвестного направления

        # Добавляем новую голову в начало списка
        self.positions.insert(0, new_head)

        # Если длина змейки не увеличилась, удаляем последний элемент
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Draw Snake"""
        for position in self.positions:
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

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0] if self.positions else None

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = pygame.K_RIGHT
        self.next_direction = None
        self.last = None

    def grow(self):
        """Увеличивает длину змейки"""
        self.length += 1

    def check_collision_with_self(self):
        """Проверяет столкновение головы змейки с её телом"""
        if len(self.positions) > 1:
            return self.positions[0] in self.positions[1:]
        return False

    def check_collision_with_apple(self, screen_width, screen_height):
        """Проверяет столкновение змейки со стенами"""
        if not self.positions:
            return False

        head_x, head_y = self.positions[0]
        return (head_x < 0 or head_x >= screen_width
                or head_y < 0 or head_y >= screen_height)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
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
    """Main"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head_rect = pygame.Rect(snake.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
        apple_rect = pygame.Rect(apple.position, (GRID_SIZE, GRID_SIZE))

        if head_rect.colliderect(apple_rect):
            snake.grow()
            apple.randomize_position()

            while apple.position in snake.position:
                apple.randomize_position()

        if snake.check_collision_with_self():
            snake.reset()
            apple.randomize_position()

        screen.fill((255, 255, 255))
        apple.draw()
        snake.draw()

        pygame.display.update()
        clock.tick(SPEED)

    pygame.quit()


if __name__ == '__main__':
    main()
