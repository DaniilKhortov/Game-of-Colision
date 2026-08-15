import pygame
import sys

# Налаштування параметрів
WIDTH, HEIGHT = 800, 600      # Розмір екрану
BALL_RADIUS = 20              # Радіус м'яча
BOX_SIZE = 100                # Збільшений розмір коробки
INITIAL_SPEED = 10            # Початкова швидкість м'яча
FRICTION = 0.99               # Коєфіцієнт тертя для м'яча
BOX_FRICTION = 0.95           # Коєфіцієнт тертя для коробки
SPEED_TRANSFER = 0.3          # Частка швидкості, що передається від м'яча коробці
FPS = 60                      # Частота оновлення екрану
BALL_MASS = 1    # Маса м'яча
BOX_MASS = 5     # Маса коробки

# Ініціалізація Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Ball:
    def __init__(self, x, y, vx, vy, mass):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass  # Маса м'яча
        
    
    def update(self):
        # Оновлення позиції м'яча
        self.x += self.vx
        self.y += self.vy
        
        # Втрата швидкості через тертя
        self.vx *= FRICTION
        self.vy *= FRICTION
        
        # Відбивання від стін
        if self.x - BALL_RADIUS <= 0 or self.x + BALL_RADIUS >= WIDTH:
            self.vx = -self.vx
        if self.y - BALL_RADIUS <= 0 or self.y + BALL_RADIUS >= HEIGHT:
            self.vy = -self.vy
            
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), BALL_RADIUS)
    
    
    def collide_with_box(self, box):
        # Перевірка зіткнення з коробкою
        if (box.x - BOX_SIZE / 2 <= self.x <= box.x + BOX_SIZE / 2 and
            box.y - BOX_SIZE / 2 <= self.y <= box.y + BOX_SIZE / 2):
            
            # Розрахунок нових швидкостей після зіткнення
            total_mass = self.mass + box.mass
            
            # Збереження імпульсу
            new_vx_ball = (self.vx * (self.mass - box.mass) + 2 * box.mass * box.vx) / total_mass
            new_vy_ball = (self.vy * (self.mass - box.mass) + 2 * box.mass * box.vy) / total_mass
            new_vx_box = (box.vx * (box.mass - self.mass) + 2 * self.mass * self.vx) / total_mass
            new_vy_box = (box.vy * (box.mass - self.mass) + 2 * self.mass * self.vy) / total_mass

            # Оновлення швидкостей
            self.vx, self.vy = new_vx_ball, new_vy_ball
            box.vx, box.vy = new_vx_box, new_vy_box

class Box:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.mass = mass  # Маса коробки
    
    def update(self):
        # Оновлення позиції коробки з урахуванням швидкості
        self.x += self.vx
        self.y += self.vy
        
        # Втрата швидкості через тертя
        self.vx *= BOX_FRICTION
        self.vy *= BOX_FRICTION

        # Обмеження руху коробки в межах екрану
        if self.x < BOX_SIZE / 2:
            self.x = BOX_SIZE / 2
            self.vx = -self.vx
        elif self.x > WIDTH - BOX_SIZE / 2:
            self.x = WIDTH - BOX_SIZE / 2
            self.vx = -self.vx

        if self.y < BOX_SIZE / 2:
            self.y = BOX_SIZE / 2
            self.vy = -self.vy
        elif self.y > HEIGHT - BOX_SIZE / 2:
            self.y = HEIGHT - BOX_SIZE / 2
            self.vy = -self.vy
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(int(self.x - BOX_SIZE / 2), int(self.y - BOX_SIZE / 2), BOX_SIZE, BOX_SIZE))


# Створення об'єктів м'яча та коробки з початковими параметрами
ball = Ball(WIDTH // 3, HEIGHT // 2, INITIAL_SPEED, INITIAL_SPEED, BALL_MASS)
box = Box(3 * WIDTH // 3, HEIGHT // 2, BOX_MASS)

# Основний цикл
while True:
    # Перевірка на закриття вікна
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Очищення екрану
    screen.fill((255, 255, 255))
    
    # Оновлення та малювання м'яча і коробки
    ball.update()
    box.update()
    ball.collide_with_box(box)  # Перевірка на зіткнення м'яча з коробкою

    ball.draw(screen)
    box.draw(screen)
    
    # Оновлення дисплею
    pygame.display.flip()
    
    # Затримка для регулювання FPS
    clock.tick(FPS)
