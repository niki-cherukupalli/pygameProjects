import random
import pygame

pygame.init()

#set up window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trying Drap and Drop")


activeSprite = None #what sprite has been clicked on

#create a bunch of boxes/rectangles and put in a list
boxes = []
for i in range(10):
    x = random.randint(50, 700)
    y = random.randint(50, 350)
    w = random.randint(35, 65)
    h = random.randint(35, 65)
    box = pygame.Rect(x, y, w, h)
    boxes.append(box)



#main while loop
run = True
while run:

    screen.fill("#F8C8DC")

    for box in boxes:
        pygame.draw.rect(screen, "#FF69B4", box)
        
  
    #for drap and drop capabilities
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, box in enumerate(boxes):
                    if box.collidepoint(event.pos):
                        activeSprite = num

        #check that the mouse was released
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                activeSprite = None

        #move the sprite with the mouse
        if event.type == pygame.MOUSEMOTION:
            if activeSprite != None:
                boxes[activeSprite].move_ip(event.rel)
        
        #if user quits the game
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.flip()

pygame.quit()