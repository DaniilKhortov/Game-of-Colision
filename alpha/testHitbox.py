import pygame
import sys
import math

WIDTH, HEIGHT = 800, 600              
SIZEX = 160               
SIZEY = 85         
           
ROTATION_MEASURE = 1  # Поріг зміни кута
SPEED_MEASURE = 0.1  # Поріг для швидкості (для уникнення вібрацій)
FPS = 60                      
BOX_MASS1 = 1500   
BOX_MASS2 = 1200    
ENERGY_LOSS = 0.8

try:
    car_image = pygame.image.load("assets/car.png")
    car_image = pygame.transform.scale(car_image, (SIZEX, SIZEY))
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Box:
    def __init__(self, x, y, speed, mass, friction, acceleration):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.mass = mass  
        self.selected = False
        self.vectorEnd = None
        self.readyToMove = False
        self.friction = friction + acceleration
        self.speed = speed
        self.angle = 0  # Поточний кут повороту
        self.hitbox = pygame.Rect(x - SIZEX // 2, y - SIZEY // 2, SIZEX, SIZEY)  # Базовий хітбокс
        
    def update_hitbox(self):

        rotated_image = pygame.transform.rotate(car_image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        self.hitbox = rotated_rect  
        
    def update(self):
        if self.readyToMove:
            # Оновлення позиції
            self.x += self.vx
            self.y += self.vy

            # Гасіння швидкості, якщо вона дуже мала
            if abs(self.vx) < SPEED_MEASURE:
                self.vx = 0
            if abs(self.vy) < SPEED_MEASURE:
                self.vy = 0

            self.vx *= self.friction
            self.vy *= self.friction

            # Визначення цільового кута
            if self.vx != 0 or self.vy != 0:
                target_angle = math.degrees(math.atan2(-self.vy, self.vx))
                angle_diff = (target_angle - self.angle + 180) % 360 - 180

                # Поворот тільки якщо різниця кута більше порогу
                if abs(angle_diff) > ROTATION_MEASURE:
                    self.angle += 1 * math.copysign(1, angle_diff)
                else:
                    self.angle = target_angle

            # Відбивання від меж
            if self.x < SIZEX / 2:
                self.x = SIZEX / 2
                self.vx = -self.vx
            elif self.x > WIDTH - SIZEX / 2:
                self.x = WIDTH - SIZEX / 2
                self.vx = -self.vx  

            if self.y < SIZEY / 2:
                self.y = SIZEY / 2
                self.vy = -self.vy
            elif self.y > HEIGHT - SIZEY / 2:
                self.y = HEIGHT - SIZEY / 2
                self.vy = -self.vy

        # Оновлення хітбокса
        self.update_hitbox()
        
    def draw(self, screen):
        # Малювання оберненого зображення
        rotated_image = pygame.transform.rotate(car_image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect.topleft)

        # Малювання хітбокса (для тестування)
        # pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)

        # Малювання вектора
        if self.vectorEnd:
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), self.vectorEnd, 3)
            self.drawArrow(screen, self.vectorEnd)
    
    def drawArrow(self, screen, end):

        dx, dy = end[0] - self.x, end[1] - self.y
        angle = math.atan2(dy, dx)
        length = 15  
        

        left = (end[0] - length * math.cos(angle - math.pi / 6), end[1] - length * math.sin(angle - math.pi / 6))
        right = (end[0] - length * math.cos(angle + math.pi / 6), end[1] - length * math.sin(angle + math.pi / 6))
        
        pygame.draw.polygon(screen, (255, 0, 0), [end, left, right])                           
        
    def set_vector(self, end_x, end_y):
        self.vectorEnd = (end_x, end_y)
        dx, dy = end_x - self.x, end_y - self.y
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.vx = (dx / distance) * self.speed
            self.vy = (dy / distance) * self.speed       
            
    def is_clicked(self, pos):
        # Перевірка кліку по оберненому хітбоксу
        return self.hitbox.collidepoint(pos)
    
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.vx = 0
        self.vy = 0
        self.vectorEnd = None
        self.readyToMove = False   
        self.angle = 0      
        
    def collide_with(self, other):
        if (abs(self.x - other.x) <= SIZEX and abs(self.y - other.y) <= SIZEY):
            total_mass = self.mass + other.mass
            
            new_vx_self = (self.vx * (self.mass - other.mass) + 2 * other.mass * other.vx) / total_mass
            new_vy_self = (self.vy * (self.mass - other.mass) + 2 * other.mass * other.vy) / total_mass
            new_vx_other = (other.vx * (other.mass - self.mass) + 2 * self.mass * self.vx) / total_mass
            new_vy_other = (other.vy * (other.mass - self.mass) + 2 * self.mass * self.vy) / total_mass
            
            # Гасіння дуже малих швидкостей після зіткнення
            if abs(new_vx_self) < SPEED_MEASURE:
                new_vx_self = 0
            if abs(new_vy_self) < SPEED_MEASURE:
                new_vy_self = 0
            if abs(new_vx_other) < SPEED_MEASURE:
                new_vx_other = 0
            if abs(new_vy_other) < SPEED_MEASURE:
                new_vy_other = 0
                
            self.vx, self.vy = new_vx_self * ENERGY_LOSS, new_vy_self * ENERGY_LOSS
            other.vx, other.vy = new_vx_other * ENERGY_LOSS, new_vy_other * ENERGY_LOSS      
            
box1 = Box(WIDTH // 3, HEIGHT // 2, 5, BOX_MASS1, 0.99, -0.01)
box2 = Box(3 * WIDTH // 4, HEIGHT // 2, 7, BOX_MASS2, 0.99, 0)
box3 = Box(5 * WIDTH // 5, HEIGHT // 3, 7, BOX_MASS2, 0.99, 0)
boxes = [box1, box2, box3]
selectedBox = None
readyToMove = False
inputLocked = False  

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and not inputLocked :
            if event.button == 1:  

                for box in boxes:
                    if box.is_clicked(event.pos):
                        selectedBox = box
                        box.selected = True
                    else:
                        box.selected = False
            
            elif event.button == 3 and selectedBox:  # Права кнопка миші

                selectedBox.set_vector(*event.pos)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not inputLocked:  
                inputLocked = True  
                readyToMove = True
                for box in boxes:
                    box.readyToMove = True
            
            elif event.key == pygame.K_LSHIFT:  

                inputLocked = False
                readyToMove = False
                for box in boxes:
                    box.reset()
    
    # Оновлення
    if readyToMove:
        for box in boxes:
            box.update()
        box1.collide_with(box2)
        box1.collide_with(box3)
        box2.collide_with(box3)
    
    # Малювання
    screen.fill((255, 255, 255))
    for box in boxes:
        box.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)          