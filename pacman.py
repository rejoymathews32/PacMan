# RRM - go over the types of the variables to see what is actually getting assigned

# Import pygame
import pygame

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
    )

# Setup sound effects
pygame.mixer.init()

# Load all sound files
# Sound sources: Jon Fincher
collision_sound = pygame.mixer.Sound("Collision.ogg")

# RRM - need to understand what pygame does under the hood
# Initialize pygame
pygame.init()

# Constants for screen width and screen height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Note Pacman height and width must be the same
# Note pacman height must be divisible by both screen width and height
PACMAN_HEIGHT = 40
PACMAN_WIDTH = PACMAN_HEIGHT

# Total number of food rows and columns
FOOD_COLUMNS = SCREEN_WIDTH//PACMAN_WIDTH
FOOD_ROWS = SCREEN_HEIGHT//PACMAN_HEIGHT

# Define a class for the Pac-man
class Pacman(pygame.sprite.Sprite):
    """
    Pacman class that contains a method to move the Pacman around
    and initialze the pacman
    """

    def __init__(self):
        """ Initialize the Pacman graphical representation """
        super(Pacman, self).__init__() #RRM - need to understand why we pass self to super
        self.picture = pygame.image.load("Pacman_image_HD.png").convert()
        # Reduce the size of the image
        self.surf = pygame.transform.scale(self.picture, (PACMAN_WIDTH,PACMAN_HEIGHT))
        # Color key is set as white. (If image was white, it would have a box around it to avoid blend)
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect()
        #RRM - Add an image and some audio every time it moves

    def update(self, key_pressed):
        """ Method that moves the Pacman around through the game window """
        if(key_pressed[K_UP]):
            self.rect.move_ip(0,-5)
        if(key_pressed[K_DOWN]):
            self.rect.move_ip(0,5)
        if(key_pressed[K_LEFT]):
            self.rect.move_ip(-5,0)
        if(key_pressed[K_RIGHT]):
            self.rect.move_ip(5,0)

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT        

################################################################################

class Food(pygame.sprite.Sprite):
    """ Food the Pacman feeds on """
    # Things to think about:
    # Food should be small white squares
    # Food should be aligned at the center of a Pacman
        # 1 food per Pacman width
        # Food is placed at Pacmans center as a 5x5 object
        # Food top left is (18,18) for a top left Pacman (0,0)
        # In both directions (horizontal and vertical) add pacman_x + pacman_y to get next food

    def __init__(self, food_x_cnt = 0, food_y_cnt = 0):
        """ Initialize the size and position of the food item """
        super(Food, self).__init__()        
        # Size of the food item
        self.surf = pygame.Surface((5,5))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        # Define the position of each food item
        self.rect.left = PACMAN_WIDTH * (food_y_cnt+1)
        self.rect.top = PACMAN_HEIGHT * (food_x_cnt+1)


# Set 2-D game screen
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Instantiate the Pac-Man
pacman = Pacman()

# Creating a sprite group for food collection
food_collection = pygame.sprite.Group()

for x in range(FOOD_ROWS):
    for y in range(FOOD_COLUMNS):
        # Istantiate the food
        food = Food(x,y)
        food_collection.add(food)

# Setup a clock for the fram rate
clock = pygame.time.Clock()

running = True

# Run the code until the user clicks on quit
while running:
     
     # Check for all events via inputs to pygame
    for event in pygame.event.get():
        # If there is a key press
        if event.type == pygame.KEYDOWN:
            #If the key pressed is an escape exit the game
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
            running = False

    # Get all the pressed keys and pass it to the Pacman class
    # to perform an update to move in the specified direction
    keys_pressed = pygame.key.get_pressed()

    #Pass the pressed keys to the Pacman
    pacman.update(keys_pressed)

    # Display all black on the screen
    screen.fill((0,0,0))

    #Blend the Pacman into the screen
    screen.blit(pacman.surf,pacman.rect)

    for food in food_collection:
        #Blend the food into the screen
        screen.blit(food.surf,food.rect)
    
    # Kill all the food items if eaten by Pacman
    if(pygame.sprite.spritecollide(pacman,food_collection,dokill = True)):
        collision_sound.play()

    pygame.display.flip()

    # Game is configured to 30 frames
    clock.tick(60)

pygame.quit()


# 10/04
# Pending activities
# Sound effect when Pacman eats food
# Collision detection leading to killing food
# Steps taken by Pacman and food placement should align