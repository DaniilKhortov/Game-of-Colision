import pygame
import sys
import math

# Параметри
WIDTH, HEIGHT = 800, 600              
BOX_SIZE = 100                
INITIAL_SPEED = 5            
FRICTION = 0.99               
BOX_FRICTION = 0.95           
FPS = 60                      
BOX_MASS1 = 1500   
BOX_MASS2 = 1200    
ENERGY_LOSS = 0.8

# Ініціалізація Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Box:
    def __init__(self, x, y, vx, vy, mass):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass  
        self.selected = False
        self.vector_end = None
        self.ready_to_move = False
    
    def update(self):
        if self.ready_to_move:
            # Оновлення позиції
            self.x += self.vx
            self.y += self.vy
            self.vx *= FRICTION
            self.vy *= FRICTION   
            
            # Обмеження в межах екрану
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
        # Малювання прямокутника
        color = (0, 255, 0) if self.selected else (0, 0, 255)
        pygame.draw.rect(screen, color, pygame.Rect(int(self.x - BOX_SIZE / 2), int(self.y - BOX_SIZE / 2), BOX_SIZE, BOX_SIZE))
        
        # Малювання вектора
        if self.vector_end:
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), self.vector_end, 3)
            self._draw_arrowhead(screen, self.vector_end)
    
    def _draw_arrowhead(self, screen, end):
        """Малювання наконечника стрілки."""
        dx, dy = end[0] - self.x, end[1] - self.y
        angle = math.atan2(dy, dx)
        length = 15  # Розмір наконечника
        
        # Вершини наконечника
        left = (end[0] - length * math.cos(angle - math.pi / 6), end[1] - length * math.sin(angle - math.pi / 6))
        right = (end[0] - length * math.cos(angle + math.pi / 6), end[1] - length * math.sin(angle + math.pi / 6))
        
        pygame.draw.polygon(screen, (255, 0, 0), [end, left, right])
    
    def set_vector(self, end_x, end_y):
        # Задати вектор (лише графічно)
        self.vector_end = (end_x, end_y)
        dx, dy = end_x - self.x, end_y - self.y
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.vx = (dx / distance) * INITIAL_SPEED
            self.vy = (dy / distance) * INITIAL_SPEED
    
    def is_clicked(self, pos):
        # Перевірка, чи натиснуто на об'єкт
        return (self.x - BOX_SIZE / 2 <= pos[0] <= self.x + BOX_SIZE / 2 and
                self.y - BOX_SIZE / 2 <= pos[1] <= self.y + BOX_SIZE / 2)
        
    def reset(self):
        """Скидання до початкового стану."""
        self.x = self.start_x
        self.y = self.start_y
        self.vx = 0
        self.vy = 0
        self.vector_end = None
        self.ready_to_move = False
        
    def collide_with(self, other):
        # Перевірка та обробка зіткнення
        if (abs(self.x - other.x) <= BOX_SIZE and abs(self.y - other.y) <= BOX_SIZE):
            total_mass = self.mass + other.mass
            
            new_vx_self = (self.vx * (self.mass - other.mass) + 2 * other.mass * other.vx) / total_mass
            new_vy_self = (self.vy * (self.mass - other.mass) + 2 * other.mass * other.vy) / total_mass
            new_vx_other = (other.vx * (other.mass - self.mass) + 2 * self.mass * self.vx) / total_mass
            new_vy_other = (other.vy * (other.mass - self.mass) + 2 * self.mass * self.vy) / total_mass

            self.vx, self.vy = new_vx_self * ENERGY_LOSS, new_vy_self * ENERGY_LOSS
            other.vx, other.vy = new_vx_other * ENERGY_LOSS, new_vy_other * ENERGY_LOSS        

# Створення об'єктів
box1 = Box(WIDTH // 3, HEIGHT // 2, 0, 0, BOX_MASS1)
box2 = Box(3 * WIDTH // 4, HEIGHT // 2, 0, 0, BOX_MASS2)
boxes = [box1, box2]
selected_box = None
all_ready_to_move = False
input_locked = False  # Заборона вводу після запуску

# Основний цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and not input_locked:
            if event.button == 1:  # Ліва кнопка миші
                # Вибір об'єкта
                for box in boxes:
                    if box.is_clicked(event.pos):
                        selected_box = box
                        box.selected = True
                    else:
                        box.selected = False
            
            elif event.button == 3 and selected_box:  # Права кнопка миші
                # Задання вектора для вибраного об'єкта
                selected_box.set_vector(*event.pos)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not input_locked:  # Клавіша Enter
                input_locked = True  # Заборонити подальший ввід
                all_ready_to_move = True
                for box in boxes:
                    box.ready_to_move = True
            
            elif event.key == pygame.K_LSHIFT:  # Клавіша Shift
                # Перезапуск
                input_locked = False
                all_ready_to_move = False
                for box in boxes:
                    box.reset()
    
    # Оновлення
    if all_ready_to_move:
        for box in boxes:
            box.update()
        box1.collide_with(box2)
    
    # Малювання
    screen.fill((255, 255, 255))
    for box in boxes:
        box.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)