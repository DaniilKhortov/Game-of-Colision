import pygame
import sys

WIDTH, HEIGHT = 800, 600              
BOX_SIZE = 100                
INITIAL_SPEED = 5            
FRICTION = 0.99               
BOX_FRICTION = 0.95           
        
FPS = 60                      
BOX_MASS1 = 1500   
BOX_MASS2 = 1200    
ENERGY_LOSS = 0.8


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Box:
    def __init__(self, x, y, vx, vy, mass):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass  
        
    def update(self):

        self.x += self.vx
        self.y += self.vy
        
        self.vx *= FRICTION
        self.vy *= FRICTION   
        
        
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
    
    def collide_with(self, other):

        if (abs(self.x - other.x) <= BOX_SIZE and abs(self.y - other.y) <= BOX_SIZE):

            total_mass = self.mass + other.mass
            
            new_vx_self = (self.vx * (self.mass - other.mass) + 2 * other.mass * other.vx) / total_mass
            new_vy_self = (self.vy * (self.mass - other.mass) + 2 * other.mass * other.vy) / total_mass
            new_vx_other = (other.vx * (other.mass - self.mass) + 2 * self.mass * self.vx) / total_mass
            new_vy_other = (other.vy * (other.mass - self.mass) + 2 * self.mass * self.vy) / total_mass


            self.vx, self.vy = new_vx_self * ENERGY_LOSS, new_vy_self * ENERGY_LOSS
            other.vx, other.vy = new_vx_other * ENERGY_LOSS, new_vy_other * ENERGY_LOSS        
            
box1 = Box(WIDTH // 3, HEIGHT // 2, INITIAL_SPEED, INITIAL_SPEED, BOX_MASS1)
box2 = Box(3 * WIDTH // 3, HEIGHT // 2, 0, 0, BOX_MASS2)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    screen.fill((255, 255, 255))
    

    box1.update()
    box2.update()
    box1.collide_with(box2)  

    box1.draw(screen)
    box2.draw(screen)
    

    pygame.display.flip()
    

    clock.tick(FPS)
            