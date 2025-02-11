# game where you have to feed the hungry monster the correct 
# food in a time limit, or it will die <3

import random
import pygame
import time  # Add this import

pygame.init()

#font and text init
pygame.font.init()
theFont = pygame.font.SysFont("Comic Sans MS", 30)

#set up window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

# Add UI variables
MAX_HEALTH = 100
health = MAX_HEALTH
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20
UI_PADDING = 20  # Space between UI elements
UI_X = SCREEN_WIDTH - HEALTH_BAR_WIDTH - UI_PADDING
UI_Y = UI_PADDING

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Eating Game")

activeSprite = None #what sprite has been clicked on

# Add score variable at the top of the game
score = 0

# Add timer and spawn variables
GAME_DURATION = 30  # Changed from 60 to 30 seconds
start_time = time.time()
last_spawn_time = time.time()
SPAWN_INTERVAL = 2  # Spawn new food every 2 seconds
MIN_FOOD_ITEMS = 5  # Minimum number of food items on screen

#create a food class
class foodItem: 
    def __init__(self, color, width, height, start_pos):
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = pygame.Rect(start_pos, (width, height))
        self.color = color
        self.velocity = [0, 0]  # Add velocity for explosion effect
    
    def get_color(self):
        return self.color

    def update(self):  # Add update method for explosion movement
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


#create a bunch of good food sprites and put in a list
foodItems = []

for i in range(10):
    color = random.choice(["RED", "GREEN"])

    x = random.randint(50, 600)
    y = random.randint(50, 350)

    w = random.randint(35, 65)
    h = random.randint(35, 65)
    food = foodItem(color, w, h, (x, y))
    foodItems.append(food)

#create mouth
#change to image later
mouth = pygame.Rect(300, 400, 200, 100)

#main while loop
run = True
while run:
    current_time = time.time()
    time_left = max(0, GAME_DURATION - (current_time - start_time))
    
    screen.fill("#F8C8DC")

    # Spawn new food items periodically
    if current_time - last_spawn_time >= SPAWN_INTERVAL and time_left > 0:
        if len(foodItems) < 15:  # Cap maximum items
            # Add 1-3 new food items
            for _ in range(random.randint(1, 3)):
                color = random.choice(["RED", "GREEN"])
                x = random.randint(50, SCREEN_WIDTH - 100)
                y = random.randint(50, SCREEN_HEIGHT - 150)
                w = random.randint(35, 65)
                h = random.randint(35, 65)
                food = foodItem(color, w, h, (x, y))
                foodItems.append(food)
        last_spawn_time = current_time

    # Ensure minimum number of food items
    if len(foodItems) < MIN_FOOD_ITEMS and time_left > 0:
        color = random.choice(["RED", "GREEN"])
        x = random.randint(50, SCREEN_WIDTH - 100)
        y = random.randint(50, SCREEN_HEIGHT - 150)
        w = random.randint(35, 65)
        h = random.randint(35, 65)
        food = foodItem(color, w, h, (x, y))
        foodItems.append(food)

    #draw all rectangles randomly green or red
    for food in foodItems:
        pygame.draw.rect(screen, food.color, food)

    #draw the mouth
    pygame.draw.rect(screen, (0, 0, 0), mouth, 4) #clear rect


    #for drap and drop capabilities
    for event in pygame.event.get():
        
        #if user quits the game
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, food in enumerate(foodItems):
                    if food.rect.collidepoint(event.pos):
                        activeSprite = num

        #check that the mouse was released
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                activeSprite = None

        #move the sprite with the mouse
        if event.type == pygame.MOUSEMOTION:
            if activeSprite != None:
                foodItems[activeSprite].rect.move_ip(event.rel)
        

    
    #check if box in touching the goal
    for food in foodItems[:]:
        if food.rect.colliderect(mouth):
            # text shows up when they touch
            if food.get_color() == "GREEN":
                text_surface = theFont.render(f"yummy! +10 points", False, "GREEN")
                screen.blit(text_surface, (0, 0))
                score += 10
                # If the active sprite is being removed, reset it
                if activeSprite is not None and food == foodItems[activeSprite]:
                    activeSprite = None
                foodItems.remove(food)

            if food.get_color() == "RED":
                text_surface = theFont.render("uh oh... -15 points!", False, "RED")
                screen.blit(text_surface, (0, 0))
                score -= 15
                health = max(0, health - 20)  # Decrease health but don't go below 0
                
                # Create explosion pieces
                original_pos = food.rect.center
                original_size = (food.rect.width, food.rect.height)
                
                # Create 4-6 smaller pieces
                for _ in range(random.randint(4, 6)):
                    # Create smaller pieces (1/2 to 1/3 of original size)
                    new_width = original_size[0] // random.randint(2, 3)
                    new_height = original_size[1] // random.randint(2, 3)
                    
                    # Position pieces near the original position
                    new_x = original_pos[0] - new_width // 2
                    new_y = original_pos[1] - new_height // 2
                    
                    # Create new piece
                    piece = foodItem("RED", new_width, new_height, (new_x, new_y))
                    piece.velocity = [random.randint(-5, 5), random.randint(-8, -2)]
                    foodItems.append(piece)
                
                # Remove the original food item
                if activeSprite is not None and food == foodItems[activeSprite]:
                    activeSprite = None
                foodItems.remove(food)

    # Update positions of exploding food items and remove if off screen
    for food in foodItems[:]:
        food.update()
        # Remove if off screen or if it's red and has moved a bit
        if (food.rect.y > SCREEN_HEIGHT or food.rect.y < -50 or 
            food.rect.x > SCREEN_WIDTH or food.rect.x < -50 or
            (food.get_color() == "RED" and food.velocity != [0, 0] and 
             abs(food.rect.y - mouth.y) > 100)):  # Remove red items after they've moved away
            if activeSprite is not None and food == foodItems[activeSprite]:
                activeSprite = None
            foodItems.remove(food)

    # Draw UI (timer, score and health bar)
    # Timer display
    timer_text = f"Time: {int(time_left)}s"
    timer_surface = theFont.render(timer_text, True, (0, 0, 0))
    timer_rect = timer_surface.get_rect(topright=(UI_X - UI_PADDING, UI_Y + 40))
    screen.blit(timer_surface, timer_rect)
    
    # Score display with background
    score_text = f"Score: {score}"
    score_surface = theFont.render(score_text, True, (0, 0, 0))
    score_rect = score_surface.get_rect(topright=(UI_X - UI_PADDING, UI_Y))
    
    # Health bar background
    health_bar_bg = pygame.Rect(UI_X, UI_Y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
    pygame.draw.rect(screen, (100, 100, 100), health_bar_bg)
    
    # Health bar fill
    health_width = (health / MAX_HEALTH) * HEALTH_BAR_WIDTH
    health_bar = pygame.Rect(UI_X, UI_Y, health_width, HEALTH_BAR_HEIGHT)
    health_color = (
        max(0, min(255, 510 * (1 - health/MAX_HEALTH))),  # Red increases as health decreases
        max(0, min(255, 510 * (health/MAX_HEALTH))),      # Green decreases as health decreases
        0
    )
    pygame.draw.rect(screen, health_color, health_bar)
    
    # Health bar border
    pygame.draw.rect(screen, (0, 0, 0), health_bar_bg, 2)
    
    # Draw score
    screen.blit(score_surface, score_rect)
    
    # Draw UI and check game over conditions
    if health <= 0:
        # Game over due to health loss
        game_over_text = f"Game Over - You ran out of health! Final Score: {score}"
        game_over_surface = theFont.render(game_over_text, True, (0, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(game_over_surface, game_over_rect)
        
        pygame.display.flip()
        pygame.time.wait(3000)
        run = False
    elif time_left <= 0:
        # Game over due to time
        game_over_text = f"Time's up! Final Score: {score}"
        game_over_surface = theFont.render(game_over_text, True, (0, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(game_over_surface, game_over_rect)
        
        pygame.display.flip()
        pygame.time.wait(3000)
        run = False

    pygame.display.flip()

pygame.quit()

