import pygame

#using video tut
pygame.init()

#setting up the game screen/window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = pygame.Rect(300, 25, 50, 50)

#loop to keep window running and close on condition
run = True
while run:

    screen.fill((0, 0, 0)) #fills rest of the space with black

    pygame.draw.rect(screen, (0, 255, 0), player) #green 'player' rectangle

    #key controls (a,d,w,s) for left, right, up, and down
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-1, 0)
    elif key[pygame.K_d] == True:
        player.move_ip(1, 0)
    if key[pygame.K_w] == True:
        player.move_ip(0, -1)
    if key[pygame.K_s] == True:
        player.move_ip(0, 1)

    #quit screen/window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update() 
    #updates/refreshes the screeen so it does not keep the past frames

pygame.quit()
