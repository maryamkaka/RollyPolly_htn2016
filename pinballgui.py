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
CREDITS_EVENT = pygame.USEREVENT + 1 #doesn't really serve a purpose atm...

#The following is to disable and enable blinking after a click (or whatever action)
keepBlinking = True
def changeBlink():
    global keepBlinking
    if keepBlinking:
        keepBlinking = False
    else:
        keepBlinking = True
def getBlink():
    global keepBlinking
    return keepBlinking


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Setting the screen parameters 
    screen_rect = screen.get_rect()
    pygame.display.set_caption('Pinball 4 lyfe') 

    background = pygame.Surface(screen.get_size()) #Filling up the background 
    background = background.convert()
    background.fill(bgcolor)

    waitingForAOne = True  
    
    #Text Display
    title = pygame.font.Font(None, 50)
    subtitle = pygame.font.Font(None, 36)
    font = pygame.font.Font(None, 36)
    text1 = title.render('PINBALL!', 1, YELLOW)
    text2 = subtitle.render('Insert an AMERICAN quarter to begin', 1, fontcolor)

    #Setting the title at the top of the page
    textpos1 = text1.get_rect(center=(0, 100))
    textpos1.centerx = background.get_rect().centerx
    textpos2 = text2.get_rect(center=(0,150))
    textpos2.centerx = background.get_rect().centerx

    #This only shows up once the user has inserted a USA quarter 
    on_text_surface = font.render('Thanks for paying up, CHUMP!', 1, RED)

    #This does the blinking action (i.e. switches between the message being written and blank space) 
    clock = pygame.time.Clock()
    blink_rect = on_text_surface.get_rect(center=(0, HEIGHT-100))
    blink_rect.centerx = screen_rect.centerx
    off_text_surface = pygame.Surface(blink_rect.size)
    blink_surfaces = cycle([on_text_surface, off_text_surface])
    blink_surface = next(blink_surfaces)
    pygame.time.set_timer(BLINK_EVENT, 500)
        
        
    #Blit everything, i.e. makes everything appear
    background.blit(text1, textpos1)
    background.blit(text2, textpos2)
    screen.blit(background, (0,0))

    #If you want to have a circle in the middle of the screen
    #circle_rect = Rect(410, 200, 200, 200)
    #pygame.draw.ellipse(screen, fontcolor, circle_rect)
    pygame.display.flip()


    credit=0
    arduino = serial.Serial('COM3', 9600, timeout=.1)
    while waitingForAOne: #Until we get a 1 value from the arduino, we stay here 5ever
        time.sleep(0.1)
        arduinoRead = arduino.readline()[:-2] #the last bit gets rid of the new-line chars 
        try:
            credit = int(struct.unpack('s', arduinoRead)[0]) #converting serial value from arduino to int
            print('AAANNNDDD the value is ' + str(credit)) #if the value is zero, error occurs so we cop out to the exception at this point
            if credit==1:
                print("thank you for inserting a coin!") #FOR DEBUGGING PURPOSES
                waitingForAOne = False
                my_event = pygame.event.Event(CREDITS_EVENT, message="credits inserted")
                pygame.event.post(my_event)
        except:
            pass #can't think of anything better, ayy lmao
            #my_event = pygame.event.Event(BLINK_EVENT, message="idk!")
            #pygame.event.post(my_event) #is this even necessary...nobody knowsss


    
    while running: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP: #this is all for shits and giggles 
                screen.fill(pygame.Color("black"))
                on_text_surface = font.render('Thanks for paying up, CHUMP!', 1, pygame.Color("black"))
                changeBlink() #By clicking multiple times, one can toggle blinking on and off
                #gamePlay(), this should start the actual game
            if event.type == BLINK_EVENT:
                if getBlink():
                    blink_surface = next(blink_surfaces)
                    screen.blit(blink_surface, blink_rect)
                else:
                    pass
                
            if event.type == CREDITS_EVENT: #dont think we rlly need this
                print("yay credits")
            #if event.type == GAMEOVER_EVENT:
                #pass #Game over, display high scores?
            #if event.type == RESTART_EVENT:
            if event.type == pygame.KEYDOWN: #pressing R restarts the process
                if event.key == pygame.K_r: #Can change to whatever condition
                    if getBlink() == False:
                        changeBlink()
                    main()
        pygame.display.update()
        clock.tick(60)


#Start
if __name__ == '__main__':
    main()
