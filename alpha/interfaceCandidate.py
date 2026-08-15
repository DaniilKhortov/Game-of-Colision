import tkinter as tk
from tkinter import *
import pygame
import os

# Створення вікна tkinter з більшими розмірами
root = tk.Tk()
root.title("Pygame в Tkinter")
root.geometry("800x600")  # Задання розмірів вікна

# Створення Canvas в tkinter з меншими розмірами
canvas = Canvas(root, width=640, height=480)
canvas.pack()

# Ініціалізація Pygame
os.environ['SDL_WINDOWID'] = str(canvas.winfo_id())
pygame.init()

# Створення Pygame екрану
screen = pygame.display.set_mode((640, 480))

# Основний цикл для відображення Pygame в tkinter
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Чорний фон
    pygame.draw.circle(screen, (255, 0, 0), (320, 240), 50)  # Малювання червоного кола
    pygame.display.update()

    root.update_idletasks()
    root.update()

pygame.quit()
root.destroy()
