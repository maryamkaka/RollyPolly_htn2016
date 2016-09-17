import pygame
from pygame.locals import *

WIDTH = 640
HEIGHT = 480
running = 1
bgcolor = 0, 0, 0
fontcolor = 255, 255, 255

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pinball 4 lyfe')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(bgcolor)

    #Text Display
    title = pygame.font.Font(None, 50)
    font = pygame.font.Font(None, 36)
    text1 = title.render('Pinball!', 1, fontcolor)
    text = font.render('Insert quarters', 1, fontcolor)

    #Setting the title at the top of the page
    textpos1 = text1.get_rect()
    textpos1.centerx = background.get_rect().centerx

    #Setting the "insert quarters" near the bottom of the screen
    textpos = text.get_rect(center=(0, 400))
    textpos.centerx = background.get_rect().centerx

    

    #Blit errythang
    background.blit(text1, textpos1)
    background.blit(text, textpos)
    screen.blit(background, (0,0))
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        screen.blit(background, (0, 0))
        pygame.display.flip()


#Start
if __name__ == '__main__':
    main()







