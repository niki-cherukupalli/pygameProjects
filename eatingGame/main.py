# game where you have to feed the hungry monster the correct 
# food in a time limit, or it will die <3

import random
import pygame

pygame.init()

#font and text init
pygame.font.init()
theFont = pygame.font.SysFont("Comic Sans MS", 30)

#set up window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Eating Game")

activeSprite = None #what sprite has been clicked on

#create a bunch of good food sprites and put in a list
foodItems = []
for i in range(10):
    x = random.randint(50, 600)
    y = random.randint(50, 350)
    w = random.randint(35, 65)
    h = random.randint(35, 65)
    food = pygame.Rect(x, y, w, h)
    foodItems.append(food)

#create mouth
#change to image later
mouth = pygame.Rect(300, 400, 200, 100)

#main while loop
run = True
while run:

    screen.fill("#F8C8DC")

    #draw good food
    #figure out way to randomize what color drawn
    for food in foodItems:
        pygame.draw.rect(screen, "GREEN", food)
    
    #draw the mouth
    pygame.draw.rect(screen, (0, 0, 0), mouth, 4) #clear rect


    #for drap and drop capabilities
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, box in enumerate(foodItems):
                    if box.collidepoint(event.pos):
                        activeSprite = num

        #check that the mouse was released
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                activeSprite = None

        #move the sprite with the mouse
        if event.type == pygame.MOUSEMOTION:
            if activeSprite != None:
                foodItems[activeSprite].move_ip(event.rel)
        
        #if user quits the game
        if event.type == pygame.QUIT:
            run = False
    
    #check if box in touching the goal
    for food in foodItems:
        if box.colliderect(mouth):
            # text shows up when they touch

            #if food
                text_surface = theFont.render("yummy!", False, "GREEN")
                screen.blit(text_surface, (0, 0))
                #increment point counter here

            #if not food
                text_surface = theFont.render("uh oh...", False, "RED")
                screen.blit(text_surface, (0, 0))

        #find a way to make the box sprites disappear
        

    
    pygame.display.flip()

pygame.quit()

