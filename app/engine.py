
import math, pygame
from .constants import SPEED_MEASURE, ROTATION_MEASURE, WIDTH, HEIGHT, ENERGY_LOSS
from .globalVars import friction, damage

class Box:
    def __init__(self, x, y, speed, mass,  acceleration, sprite, sizeX, sizeY):

        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.mass = mass  
        self.selected = False
        self.vectorEnd = None
        self.readyToMove = False
        self.friction = friction+acceleration
        self.acceleration = acceleration
        
        self.speed = speed
        self.angle = 0  # Поточний кут повороту
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.hitbox = pygame.Rect(x - self.sizeX // 2, y - self.sizeY // 2, self.sizeX, self.sizeY)  # Базовий хітбокс
        self.sprite = sprite
        
    def updateHitbox(self):

        rotatedImage = pygame.transform.rotate(self.sprite, self.angle)
        rotatedRect = rotatedImage.get_rect(center=(self.x, self.y))
        self.hitbox = rotatedRect  
    
    def updateImage(self):
        self.sprite = pygame.transform.scale(self.sprite, (self.sizeX, self.sizeY))
        
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
            if self.x < self.sizeX / 2:
                self.x = self.sizeX / 2
                self.vx = -self.vx
            elif self.x > WIDTH - self.sizeX / 2:
                self.x = WIDTH - self.sizeX / 2
                self.vx = -self.vx  

            if self.y < self.sizeY / 2:
                self.y = self.sizeY / 2
                self.vy = -self.vy
            elif self.y > HEIGHT - self.sizeY / 2:
                self.y = HEIGHT - self.sizeY / 2
                self.vy = -self.vy

        # Оновлення хітбокса
        self.updateHitbox()
        
    def draw(self, screen):
        # Малювання оберненого зображення
        rotatedImage = pygame.transform.rotate(self.sprite, self.angle)
        rotatedRect = rotatedImage.get_rect(center=(self.x, self.y))
        screen.blit(rotatedImage, rotatedRect.topleft)

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
        
    def setVector(self, endX, endY):
        self.vectorEnd = (endX, endY)
        dx, dy = endX - self.x, endY - self.y
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.vx = (dx / distance) * self.speed
            self.vy = (dy / distance) * self.speed       
            self.angle = math.degrees(math.atan2(-self.vy, self.vx))
            
    def is_clicked(self, pos):
        # Перевірка кліку по оберненому хітбоксу
        return self.hitbox.collidepoint(pos)
    
    def reset(self):
        self.x = self.startX
        self.y = self.startY
        if self.vectorEnd:  # Якщо вектор заданий
            dx, dy = self.vectorEnd[0] - self.startX, self.vectorEnd[1] - self.startY
            distance = math.hypot(dx, dy)
            if distance > 0:
                self.vx = (dx / distance) * self.speed
                self.vy = (dy / distance) * self.speed
        else:
            self.vx = 0
            self.vy = 0
        self.readyToMove = False
        self.angle = math.degrees(math.atan2(-self.vy, self.vx))    
        
    def collide_with(self, other):
        if (abs(self.x - other.x) <= self.sizeX and abs(self.y - other.y) <= self.sizeY):
            totalMass = self.mass + other.mass
            
            
            initial_energy_self = 0.5 * self.mass * (self.vx**2 + self.vy**2)
            initial_energy_other = 0.5 * other.mass * (other.vx**2 + other.vy**2)
            initial_total_energy = initial_energy_self + initial_energy_other
            
            newVx = (self.vx * (self.mass - other.mass) + 2 * other.mass * other.vx) / totalMass
            newVy = (self.vy * (self.mass - other.mass) + 2 * other.mass * other.vy) / totalMass
            newVxOther = (other.vx * (other.mass - self.mass) + 2 * self.mass * self.vx) / totalMass
            newVyOther = (other.vy * (other.mass - self.mass) + 2 * self.mass * self.vy) / totalMass
            
            # Гасіння дуже малих швидкостей після зіткнення
            if abs(newVx) < SPEED_MEASURE:
                newVx = 0
            if abs(newVy) < SPEED_MEASURE:
                newVy = 0
            if abs(newVxOther) < SPEED_MEASURE:
                newVxOther = 0
            if abs(newVyOther) < SPEED_MEASURE:
                newVyOther = 0
                
            self.vx, self.vy = newVx * ENERGY_LOSS, newVy * ENERGY_LOSS
            other.vx, other.vy = newVxOther * ENERGY_LOSS, newVyOther * ENERGY_LOSS
            
            final_energy_self = 0.5 * self.mass * (self.vx**2 + self.vy**2)
            final_energy_other = 0.5 * other.mass * (other.vx**2 + other.vy**2)
            final_total_energy = final_energy_self + final_energy_other
            
            # Розрахунок втрат енергії
            
            energy_loss = initial_total_energy - final_total_energy
            if len(damage)<10:
                damage.append(energy_loss)

            # print(f"Energy lost in collision: {energy_loss:.2f} J")