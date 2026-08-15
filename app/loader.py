import sys, pygame

try:
    backgroundImage1 = pygame.image.load("assets/crossroad1.png")
    backgroundImage1 = pygame.transform.scale(backgroundImage1, (810, 610))
    backgroundImage2 = pygame.image.load("assets/crossroad3.png")
    backgroundImage2 = pygame.transform.scale(backgroundImage2, (810, 610))
    backgroundImage3 = pygame.image.load("assets/crossroad2.png")
    backgroundImage3 = pygame.transform.scale(backgroundImage3, (810, 610))
    backgroundImage4 = pygame.image.load("assets/crossroad4.png")
    backgroundImage4 = pygame.transform.scale(backgroundImage4, (810, 610))   
    structureImage = pygame.image.load("assets/structure.png")
    structureImage = pygame.transform.scale(structureImage, (100, 100))   
    carImage = pygame.image.load("assets/car.png")
    carImage = pygame.transform.scale(carImage, (4*28, 2*28))
    mouseImage = pygame.image.load("assets/mouse.png")
    mouseImage = pygame.transform.scale(mouseImage, (10*28, 3.6*28))
    vanImage = pygame.image.load("assets/van.png")
    vanImage = pygame.transform.scale(vanImage, (4*28, 2.1*28))
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()

