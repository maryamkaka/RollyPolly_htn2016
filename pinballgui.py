import pygame
from pygame.locals import *
from itertools import cycle

#For the screen size:
WIDTH = 1024 
HEIGHT = 600

running = 1
bgcolor = 0, 0, 0
fontcolor = 255, 255, 255
BLINK_EVENT = pygame.USEREVENT + 0


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen_rect = screen.get_rect()
    pygame.display.set_caption('Pinball 4 lyfe')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(bgcolor)

    #Text Display
    title = pygame.font.Font(None, 50)
    font = pygame.font.Font(None, 36)
    text1 = title.render('Pinball!', 1, fontcolor)
    on_text_surface = font.render('Insert quarters', 1, fontcolor)

    #Setting the title at the top of the page
    textpos1 = text1.get_rect()
    textpos1.centerx = background.get_rect().centerx

    #Setting the "insert quarters" near the bottom of the screen
    clock = pygame.time.Clock()
    #Create a "blinking" effect by drawing and erasing the font 
    blink_rect = on_text_surface.get_rect(center=(0, 400))
    blink_rect.centerx = screen_rect.centerx
    off_text_surface = pygame.Surface(blink_rect.size)
    blink_surfaces = cycle([on_text_surface, off_text_surface]) 
    blink_surface = next(blink_surfaces)
    pygame.time.set_timer(BLINK_EVENT, 1000)
    
    

    #Blit errythang
    background.blit(text1, textpos1)
    #background.blit(text, textpos)
    screen.blit(background, (0,0))
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == BLINK_EVENT:
                blink_surface = next(blink_surfaces) #blinking the text
        screen.blit(blink_surface, blink_rect)
        pygame.display.update()
        clock.tick(60)


#Start
if __name__ == '__main__':
    main()
