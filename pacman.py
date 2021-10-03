# 10/02/2021
# Tasks
# Create black screen
# Create Pacman
# Allow Pacman to move in bounded box
# When he tries to fo beyond bounded box stop him
# Food is everywhere
# As pacman moves on the food, food is eaten


# Import pygame
import pygame

# RRM - need to understand what pygame does under the hood
# Initialize pygame
pygame.init()

# Define a class for the Pac-man
class Pacman(pygame.sprite.Sprite):

    def __init__(self):
        super(Pacman, self).__init__() #RRM - need to understand why we pass self to super
        self.surf = pygame.Surface((50,50))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
#Notes - Add an image and some audio every time it moves


# Constants for screen width and screen height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

# Set 2-D game screen
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Instantiate the Pac-Man
pacman = Pacman()


running = True

# Run the code until the user clicks on quit
while running:
     
     # Check for all events via inputs to pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display all black on the screen
    screen.fill((0,0,0))

    #Blend the Pacman into the screeb
    screen.blit(pacman.surf,(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    pygame.display.flip()

pygame.quit()
