import pygame
import sys
import thorpy as tp
import tkinter as tk 
from .engine import Box
from .toExcel import saveRecord
from tkinter import Canvas, ttk
import os
from .constants import WIDTH, HEIGHT, BOX_MASS1, SIZEX, SIZEY, FPS
from .globalVars import  mode, carsNumber, friction, boxes, cars, widgets, parameters, selectedBox, readyToMove, inputLocked
from .loader import backgroundImage1, backgroundImage2, backgroundImage3, backgroundImage4, structureImage, carImage, mouseImage, vanImage 



def runGui():
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

    global currentBG


    currentBG = backgroundImage1



    # Створення кнопок у вікні tkinter
    btnEnter = tk.Button(root, text="Run", command=lambda: trigger_event("ENTER"))
    btnEnter.place(x=375, y = 665)

    btnShift = tk.Button(root, text="Reset", command=lambda: trigger_event("SHIFT"))
    btnShift.place(x=420, y = 665)

    btnClear = tk.Button(root, text="Clear", command=lambda: trigger_event("CLEAR"))
    btnClear.place(x=475, y = 665)

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
            currentBG = backgroundImage1

        elif bgVar.get() == 'X-подібний 2':

            currentBG = backgroundImage2

        elif bgVar.get() == 'Т-подібний 1':
            currentBG = backgroundImage3

        elif bgVar.get() == 'Т-подібний 2':
            currentBG = backgroundImage4

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
                boxes[id].sprite = carImage
                inputSize.delete(0, tk.END)
                inputSize.insert(0, "4x2")
            elif typeVar.get() == 'Van':
                boxes[id].sprite = vanImage
                inputSize.delete(0, tk.END)
                inputSize.insert(0, "4x2.1")
            elif typeVar.get() == 'Mouse':
                boxes[id].sprite = mouseImage
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
                    box.updateHitbox()
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
            saveRecord()

            
            
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

    

    def eventHandler():  
        global selectedBox, readyToMove, inputLocked, currentBG, mode, carsNumber
        screen.blit(currentBG, (0, 0))
        
        events = pygame.event.get()
        for event in events:


            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


                
            elif event.type == pygame.MOUSEBUTTONDOWN and not inputLocked and mode == "Cars":
                if event.button == 1 and carsNumber<5:  
                    new_box = Box(event.pos[0], event.pos[1], 8, BOX_MASS1,  -1/600, carImage, SIZEX, SIZEY)
                    boxes.append(new_box)   
                    cars.append(boxes.index(new_box))
                    
                    selectedBox = new_box  
                    createWidget(cars[cars.index(boxes.index(new_box))])
                    carsNumber+=1
                    

                elif event.button == 3 and selectedBox:  
                    selectedBox.setVector(*event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and not inputLocked and mode == "Buildings":
                if event.button == 1:  
                    new_box = Box(event.pos[0], event.pos[1], 0, 999999999999, -1/600, structureImage, 100, 100)
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
        eventHandler()
        root.update_idletasks()
        root.update()

    pygame.quit()
    root.destroy()

