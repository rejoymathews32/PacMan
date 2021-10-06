# RRM - go over the types of the variables to see what is actually getting assigned

# Import pygame
import pygame
import random
import time

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
death_sound = pygame.mixer.Sound("Pacman-death-sound.mp3")

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

# Note Pacman height and width must be the same
# Note pacman height must be divisible by both screen width and height
GHOST_HEIGHT = PACMAN_HEIGHT
GHOST_WIDTH = GHOST_HEIGHT

# Total number of food rows and columns
FOOD_COLUMNS = SCREEN_WIDTH//PACMAN_WIDTH
FOOD_ROWS = SCREEN_HEIGHT//PACMAN_HEIGHT

# Total number of ghost per game
GHOSTS_PER_GAME = 5

################################################################################
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
# Define the ghosts roaming around

class Ghost(pygame.sprite.Sprite):
    """
    Ghost class that contains an initialization method and a 
    method to move the ghost around randomly
    """

    def __init__(self):
        """ Initialize the Ghost graphical representation """
        super(Ghost, self).__init__()
        self.picture = pygame.image.load("Ghost.jpg").convert()
        # Reduce the size of the image
        self.surf = pygame.transform.scale(self.picture, (PACMAN_WIDTH,PACMAN_HEIGHT))
        # Color key is set as white. (If image was white, it would have a box around it to avoid blend)
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect()
        # Ghosts start from the centre of the screen
        self.rect.left = SCREEN_WIDTH//2
        self.rect.top = SCREEN_HEIGHT//2

        # A counter variable is used to slow down direction change for the ghost
        self.counter = 0
        self.random_direction = 0

        # Slow down the ghost
        # Let the ghost move in one direction for multiple frames
        # before it changes direction


    def update(self):
        """ Method that moves the Ghost around through the game window """
        if (self.counter == 40):
            self.counter = 0
        else:
            self.counter+=1

        if(self.counter == 0):
            self.random_direction = random.randrange(0,4)

        # Update direction of the ghost randomly
        if(self.random_direction == 0):
            self.rect.move_ip(0,-5)
        if(self.random_direction == 1):
            self.rect.move_ip(0,5)
        if(self.random_direction == 2):
            self.rect.move_ip(-5,0)
        if(self.random_direction == 3):
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
        self.rect.left = (PACMAN_WIDTH*food_y_cnt) + PACMAN_WIDTH//2
        self.rect.top = (PACMAN_HEIGHT*food_x_cnt) + PACMAN_HEIGHT//2

################################################################################
# Main code

# Set 2-D game screen
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Instantiate the Pac-Man
pacman = Pacman()

# Creating a sprite group for ghosts
ghost_group = pygame.sprite.Group()

# Creating a sprite group for food collection
food_collection = pygame.sprite.Group()

# Creating an all sprites group
all_sprites = pygame.sprite.Group()

all_sprites.add(pacman)

for x in range(FOOD_ROWS):
    for y in range(FOOD_COLUMNS):
        # Istantiate the food
        food = Food(x,y)
        food_collection.add(food)
        all_sprites.add(food)

for _ in range(GHOSTS_PER_GAME):
    # Instantiate ghosts
    ghost = Ghost()
    ghost_group.add(ghost)
    all_sprites.add(ghost)

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

    # Render all sprites
    for entity in all_sprites:
        #Blend the entity into the screen
        screen.blit(entity.surf,entity.rect)

    for ghost in ghost_group:
        #Blend the ghost into the screen
        ghost.update()
    
    # Kill all the food items if eaten by Pacman
    if(pygame.sprite.spritecollide(pacman,food_collection,dokill = True)):
        collision_sound.play()

    # Kill pacman if it comes in contact with any of the ghosts
    if(pygame.sprite.spritecollideany(pacman,ghost_group)):
        pacman.kill()
        death_sound.play()
        # Let the sound-effect play for a couple of seconds before ending game
        time.sleep(2)
        running = False

    pygame.display.flip()

    # Game is configured to 30 frames
    clock.tick(60)

pygame.quit()


# 10/05
# Add walls 
# Pacman cant cross walls
