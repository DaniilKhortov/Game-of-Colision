import pygame
import sys
import math
import thorpy as tp
import tkinter as tk 

from tkinter import Canvas, ttk, PhotoImage
import os

WIDTH, HEIGHT = 800, 600              
SIZEX = 160               
SIZEY = 85         
           
ROTATION_MEASURE = 1  
SPEED_MEASURE = 0.1 
FPS = 60                      
BOX_MASS1 = 1500   
BOX_MASS2 = 1200    
ENERGY_LOSS = 0.8



try:
    background_image1 = pygame.image.load("assets/crossroad1.png")
    background_image1 = pygame.transform.scale(background_image1, (810, 610))
    background_image2 = pygame.image.load("assets/crossroad3.png")
    background_image2 = pygame.transform.scale(background_image2, (810, 610))
    background_image3 = pygame.image.load("assets/crossroad2.png")
    background_image3 = pygame.transform.scale(background_image3, (810, 610))
    background_image4 = pygame.image.load("assets/crossroad4.png")
    background_image4 = pygame.transform.scale(background_image4, (810, 610))   
    structureImage = pygame.image.load("assets/structure.png")
    structureImage = pygame.transform.scale(structureImage, (40, 40))   
     
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()

try:
    car_image = pygame.image.load("assets/car.png")
    car_image = pygame.transform.scale(car_image, (4*28, 2*28))
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()

try:
    mouse_image = pygame.image.load("assets/mouse.png")
    mouse_image = pygame.transform.scale(mouse_image, (10*28, 3.6*28))
    
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()



try:
    van_image = pygame.image.load("assets/van.png")
    van_image = pygame.transform.scale(van_image, (4*28, 2.1*28))
    
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()

root = tk.Tk()
root.title("Pygame в Tkinter")
root.geometry("1200x720")



canvas = Canvas(root, width=WIDTH, height=HEIGHT)
canvas.place(x=375, y=50)



os.environ['SDL_WINDOWID'] = str(canvas.winfo_id())

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
tp.init(screen, tp.theme_human)
clock = pygame.time.Clock()




mm = tp.gametools.MovementManager() #this data structures handles smooth movements

global currentBG, mode, carsNumber, friction, currentWeather
carsNumber = 0
friction = 0.95

currentBG = background_image1
mode = "Cars"


# Створення кнопок у вікні tkinter
btn_enter = tk.Button(root, text="Run", command=lambda: trigger_event("ENTER"))
btn_enter.place(x=375, y = 665)

btn_shift = tk.Button(root, text="Reset", command=lambda: trigger_event("SHIFT"))
btn_shift.place(x=420, y = 665)

btn_Clear = tk.Button(root, text="Clear", command=lambda: trigger_event("CLEAR"))
btn_Clear.place(x=475, y = 665)

labelBG = tk.Label(root, text="Місцевість:")
labelBG.place(x=540, y = 670)  

bgVar = tk.StringVar()

inputBG = ttk.Combobox(root, textvariable=bgVar)
inputBG['values'] = ('X-подібний 1', 'X-подібний 2', 'Т-подібний 1', 'Т-подібний 2')
inputBG.current(0)

inputBG.place(x=620, y = 670)


labelWeather = tk.Label(root, text="Погода:")
labelWeather.place(x=780, y = 670)  


weatherVar = tk.StringVar()

inputWeather = ttk.Combobox(root, textvariable=weatherVar)
inputWeather['values'] = ('Сухо', 'Волого', 'Дощ')
inputWeather.current(0)

inputWeather.place(x=840, y = 670)



def updateWeather(event):
    global friction
    if weatherVar.get() == 'Сухо':
        friction =  0.95
        

    elif weatherVar.get() == 'Волого':

        friction = 0.97

    elif weatherVar.get() == 'Дощ':
        friction = 0.98



inputWeather.bind("<<ComboboxSelected>>", updateWeather)

def updateBG(event):
    global currentBG
    if bgVar.get() == 'X-подібний 1':
        currentBG = background_image1

    elif bgVar.get() == 'X-подібний 2':
        print(bgVar.get())
        currentBG = background_image2

    elif bgVar.get() == 'Т-подібний 1':
        currentBG = background_image3

    elif bgVar.get() == 'Т-подібний 2':
        currentBG = background_image4

def toggle_button_text():
    global mode
    if buttonMode["text"] == "Транспорт":
        buttonMode.config(text="Будівлі")
        mode = "Buildings"
    else:
        buttonMode.config(text="Транспорт")
        mode = "Cars"
                    
inputBG.bind("<<ComboboxSelected>>", updateBG)

buttonMode = tk.Button(root, text="Транспорт", command=toggle_button_text)
buttonMode.place(x=1050, y = 665)

class Box:
    def __init__(self, x, y, speed, mass,  acceleration, sprite, sizeX, sizeY):

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
        self.friction = friction+acceleration
        self.acceleration = acceleration
        
        self.speed = speed
        self.angle = 0  # Поточний кут повороту
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.hitbox = pygame.Rect(x - self.sizeX // 2, y - self.sizeY // 2, self.sizeX, self.sizeY)  # Базовий хітбокс
        self.sprite = sprite
        
    def update_hitbox(self):

        rotated_image = pygame.transform.rotate(self.sprite, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        self.hitbox = rotated_rect  
    
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
            print(self.friction)
            print(self.vx)
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
        self.update_hitbox()
        
    def draw(self, screen):
        # Малювання оберненого зображення
        rotated_image = pygame.transform.rotate(self.sprite, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect.topleft)

        # Малювання хітбокса (для тестування)
        pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)

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
            self.angle = math.degrees(math.atan2(-self.vy, self.vx))
            
    def is_clicked(self, pos):
        # Перевірка кліку по оберненому хітбоксу
        return self.hitbox.collidepoint(pos)
    
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        if self.vectorEnd:  # Якщо вектор заданий
            dx, dy = self.vectorEnd[0] - self.start_x, self.vectorEnd[1] - self.start_y
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
      
      
            

boxes = []
cars = []
widgets = []
parameters = []

selectedBox = None
readyToMove = False
inputLocked = False  


def createWidget(id):

    global widgets, parameters
    
    labelHeader = tk.Label(root, text=f"Авто {len(widgets)+1}")
    labelHeader.place(x=30, y=50+120*(len(widgets)))
    
    
    
    labelSpeed = tk.Label(root, text="Швидкість")
    labelSpeed.place(x=30, y=70+120*(len(widgets)))  
    
    speed = tk.StringVar()
    
    inputSpeed = tk.Entry(root, textvariable = speed)
    inputSpeed.place(x=30, y=95+120*(len(widgets)), width=80)  

    inputSpeed.insert(0, 80)
      
    labelAcceleration = tk.Label(root, text="Прискорення")
    labelAcceleration.place(x=120, y=70+120*(len(widgets)))       
    
    
    acceleration = tk.StringVar()
    
    inputAcceleration = tk.Entry(root, textvariable = acceleration)
    inputAcceleration.place(x=120, y=95+120*(len(widgets)), width=80)     
     
    inputAcceleration.insert(0, -1)
    
    labelType = tk.Label(root, text="Тип")
    labelType.place(x=30, y=120+120*(len(widgets)))  
      

    
    
      
    labelSize = tk.Label(root, text="Розміри")
    labelSize.place(x=120, y=120+120*(len(widgets)))   
    
    
    
    size = tk.StringVar()
    
    inputSize = tk.Entry(root, textvariable = size)
    inputSize.place(x=120, y=145+120*(len(widgets)), width=80)  
         
    inputSize.insert(0, "4x2")
    
       
    
    labelMass = tk.Label(root, text="Вага")
    labelMass.place(x=210, y=120+120*(len(widgets)))      
      
    
    
    
    
    typeVar = tk.StringVar()
    inputType = ttk.Combobox(root, textvariable=typeVar)
    inputType['values'] = ('Sedan', 'Van', 'Mouse')
    inputType.current(0)
    inputType.place(x=30, y=145 + 120 * (len(widgets)), width=80)
    
    def update_sprite(event):

        if typeVar.get() == 'Sedan':
            boxes[id].sprite = car_image
            inputSize.delete(0, tk.END)
            inputSize.insert(0, "4x2")
        elif typeVar.get() == 'Van':
            boxes[id].sprite = van_image
            inputSize.delete(0, tk.END)
            inputSize.insert(0, "4x2.1")
        elif typeVar.get() == 'Mouse':
            boxes[id].sprite = mouse_image
            inputSize.delete(0, tk.END)
            inputSize.insert(0, "10x3.6")
            
    inputType.bind("<<ComboboxSelected>>", update_sprite)
    
    
    
    mass = tk.StringVar()
    
    inputMass = tk.Entry(root, textvariable = mass)
    inputMass.place(x=210, y=145+120*(len(widgets)), width=80)       
    
    inputMass.insert(0, 3.5)
    
    widgets.append([labelHeader, labelSpeed, labelAcceleration, labelType, labelSize, labelMass, inputAcceleration, inputSpeed, inputMass, inputSize, inputType])
    parameters.append([speed, acceleration, size, mass, typeVar])
    

    
    

def trigger_event(event_type):
    global inputLocked, readyToMove, carsNumber
    if event_type == "ENTER" and not inputLocked:
        
        
        

        for box in boxes:
            if boxes.index(box) in cars:
                id = cars.index(boxes.index(box))
                mass = parameters[id][3].get() 
                speed = parameters[id][0].get() 
                acceleration = parameters[id][1].get()
                size = parameters[id][2].get()
                x, y = size.split("x")
                x = float(x)
                y = float(y)
                box.sizeX = x*28
                box.sizeY = y*28
                box.update_hitbox()
                box.updateImage()
                box.friction = friction+box.acceleration

                
                box.mass = float(mass)
                box.speed = float(speed)/10
                box.acceleration = float(acceleration)/600
            
        inputLocked = True
        readyToMove = True
        for box in boxes:
            box.reset()
            
        for box in boxes:
            box.readyToMove = True
            
    elif event_type == "SHIFT":
        inputLocked = False
        readyToMove = False


        
        
        for box in boxes:
            box.reset()
    elif event_type == "CLEAR":
        inputLocked = False
        readyToMove = False
        boxes.clear()
        for widget in widgets:
            for element in widget:
                element.destroy()
                
        cars.clear()
        parameters.clear()
        carsNumber=0        
        widgets.clear()        

   

def pygame_event_handler():  
    global selectedBox, readyToMove, inputLocked, currentBG, mode, carsNumber
    screen.blit(currentBG, (0, 0))
    
    events = pygame.event.get()
    for event in events:


        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


            
        elif event.type == pygame.MOUSEBUTTONDOWN and not inputLocked and mode == "Cars":
            if event.button == 1 and carsNumber<5:  
                new_box = Box(event.pos[0], event.pos[1], 8, BOX_MASS1,  -1/600, car_image, SIZEX, SIZEY)
                boxes.append(new_box)   
                cars.append(boxes.index(new_box))
                
                selectedBox = new_box  
                createWidget(cars[cars.index(boxes.index(new_box))])
                carsNumber+=1
                

            elif event.button == 3 and selectedBox:  
                selectedBox.set_vector(*event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and not inputLocked and mode == "Buildings":
            if event.button == 1:  
                new_box = Box(event.pos[0], event.pos[1], 0, 999999999999, -1/600, structureImage, 40, 40)
                boxes.append(new_box)
                



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
    mm.update()


    if readyToMove:
        for box in boxes:
            box.update()

        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                boxes[i].collide_with(boxes[j])

    
    
    for box in boxes:
        box.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)



running = True
while running:
    pygame_event_handler()
    root.update_idletasks()
    root.update()

pygame.quit()
root.destroy()

