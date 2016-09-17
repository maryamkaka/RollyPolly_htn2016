import pygame, sys
import serial
from pygame.locals import *
from itertools import cycle
import time
import struct

WIDTH = 1024
HEIGHT = 600
running = 1
bgcolor = 0, 0, 0
fontcolor = 255, 255, 255
YELLOW = 255, 255, 0
RED = 255, 0, 0
BLINK_EVENT = pygame.USEREVENT + 0 #For the blinking "insert credits"
CREDITS_EVENT = pygame.USEREVENT + 1 #For the initialization of the game
creditsInserted = False

def creditIsInserted():
    global creditsInserted
    creditsInserted = True

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen_rect = screen.get_rect()
    pygame.display.set_caption('Pinball 4 lyfe')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(bgcolor)

    waitingForAOne = 1  
    
    #Text Display
    title = pygame.font.Font(None, 50)
    font = pygame.font.Font(None, 36)
    text1 = title.render('PINBALL!', 1, YELLOW)

    #don't think we need this but use it if .read() doesn't work
    
    #Setting the title at the top of the page
    textpos1 = text1.get_rect(center=(0, 100))
    textpos1.centerx = background.get_rect().centerx

    global creditsInserted 
    if not(creditsInserted): #if no quarters have been inserted 
        on_text_surface = font.render('Insert quarter(s)', 1, RED)
    else:
        s = '1 credit inserted'
        on_text_surface = font.render(s, 1, RED)
        #so we can check if another quarter is inserted
        #my_event = pygame.event.Event(CREDITS_EVENT, creditsInserted=1)
        #pygame.event.post(my_event)

    
    #Setting the "insert quarters" near the bottom of the screen
    clock = pygame.time.Clock()
    blink_rect = on_text_surface.get_rect(center=(0, HEIGHT-100))
    blink_rect.centerx = screen_rect.centerx
    off_text_surface = pygame.Surface(blink_rect.size)
    blink_surfaces = cycle([on_text_surface, off_text_surface])
    blink_surface = next(blink_surfaces)
    pygame.time.set_timer(BLINK_EVENT, 1000)
        
        
    #Blit everything
    background.blit(text1, textpos1)
    #background.blit(text, textpos)
    screen.blit(background, (0,0))

    #If you want to have a circle in the middle of the screen
    #circle_rect = Rect(410, 200, 200, 200)
    #pygame.draw.ellipse(screen, fontcolor, circle_rect)
    pygame.display.flip()

    credit=0
    arduino = serial.Serial('COM3', 9600, timeout=.1)
    while waitingForAOne:
        time.sleep(0.1)
        arduinoRead = arduino.readline()[:-2] #the last bit gets rid of the new-line chars 
        try:
            credit = int(struct.unpack('s', arduinoRead)[0]) #converting serial value from arduino to int
            print('AAANNNDDD the value is ' + str(credit))
            if credit==1:
                print("thank you for inserting a coin!") #FOR DEBUGGING PURPOSES
                waitingForAOne = False
                creditsInserted = True
                my_event = pygame.event.Event(CREDITS_EVENT, creditsInserted=1)
                pygame.event.post(my_event)
        except:
            print('it is zero')

        
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                screen.blit(off_text_surface, blink_rect)
                print("Your mouse position is " + str(pos))
            if event.type == BLINK_EVENT:
                 blink_surface = next(blink_surfaces)
                 screen.blit(blink_surface, blink_rect)
            if event.type == CREDITS_EVENT:
                creditIsInserted()
            #if event.type == GAMEOVER_EVENT:
                #pass #Game over, display high scores?
            #if event.type == RESTART_EVENT:
                #pass #Somehow loop back to the start screen
        pygame.display.update()
        clock.tick(60)


#Start
if __name__ == '__main__':
    main()
