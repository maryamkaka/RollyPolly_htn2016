import pygame, sys
import serial
from pygame.locals import *
from itertools import cycle
import time
import struct

#Some colors, for simplicity
BLACK = 0, 0, 0 #aka the color black
WHITE = 255, 255, 255 #aka the color white
YELLOW = 255, 255, 0 #here are your basic primary colors
RED = 255, 0, 0
GREEN = 0, 255, 0

WIDTH = 1024
HEIGHT = 600
running = 1 #just to make the while loop look cool 

BLINK_EVENT = pygame.USEREVENT + 0 #For the blinking "insert credits"

#Keeping track of highscores 
scores = [46,23,6,87,9,7,57,87,20]

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

def gameplay():
    print("at gameplay!")
    scoreValue = 0
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Setting the screen parameters 
    screen_rect = screen.get_rect()

    background = pygame.Surface(screen.get_size()) #Filling up the background 
    background = background.convert()
    background.fill(BLACK)
    
    #Text Display
    title = pygame.font.Font(None, 70)
    gameover = pygame.font.Font(None, 100)
    text1 = title.render('GAME TIME!', 1, RED)

    background = pygame.Surface(screen.get_size()) #Filling up the background 

    textpos1 = text1.get_rect(center=(0, 70))
    textpos1.centerx = background.get_rect().centerx

    score = pygame.font.Font(None, 200)
    scoreNum = score.render(str(scoreValue), 1, WHITE)
    scorepos = scoreNum.get_rect(center=(0, (HEIGHT/2)))
    scorepos.centerx = background.get_rect().centerx

    #circle_rect = Rect(410, 200, 200, 200)
    #pygame.draw.ellipse(background, WHITE, circle_rect)
    #Blit everything, i.e. makes everything appear
    background.blit(text1, textpos1)
    background.blit(scoreNum, scorepos)
    screen.blit(background, (0,0))

    gameOver = False
    while not(gameOver): #as of now, score updates because of time, implementation of scoring to come
        pygame.display.flip()
        screen.fill(BLACK) #"Erases" old score every time to make way for the new one
        text1 = title.render('GAME TIME!', 1, RED)
        scoreNum = score.render(str(scoreValue), 1, WHITE)
        scorepos = scoreNum.get_rect(center=(0, (HEIGHT/2)))
        scorepos.centerx = background.get_rect().centerx
        screen.blit(text1, textpos1)
        screen.blit(scoreNum, scorepos)
        scoreValue+=1
        time.sleep(.1)
        
        #Find a condition for ending the game, for now we'll use this 
        if scoreValue >= 10:
            gameOver = True
            pygame.display.flip()
            screen.fill(BLACK)
            text2 = gameover.render('GAME OVER', 1, RED)
            textpos2 = text2.get_rect(center=(0, (HEIGHT/2)))
            textpos2.centerx = background.get_rect().centerx
            maxscore = title.render('Your score: ' + str(scoreValue), 1, WHITE)
            maxscorepos = maxscore.get_rect(center=(0, (HEIGHT/2 + 70)))
            maxscorepos.centerx = background.get_rect().centerx
            screen.blit(text2, textpos2)
            screen.blit(maxscore, maxscorepos)
        
    #What will be written here is how the program will deal with the raspberry pi
    #i.e. how points will be assigned based on sensor values and whatnot
    #store the point stuff in a variable and increment it once in a while
    #perhaps implement another method in order to keep track of points and stuff and loop
    #dunno about  stopping  condition....lol
    #how long does gameplay last? how to determine how to get back to the main page?
    #End condition: NO MORE BALLS, add score to highscore list 

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Setting the screen parameters 
    screen_rect = screen.get_rect()
    pygame.display.set_caption('Pinball 4 lyfe') 

    background = pygame.Surface(screen.get_size()) #Filling up the background 
    background = background.convert()
    background.fill(BLACK)

    waitingForAOne = True  
    
    #Text Display
    title = pygame.font.Font(None, 50)
    subtitle = pygame.font.Font(None, 36)
    font = pygame.font.Font(None, 36)
    text1 = title.render('PINBALL!', 1, YELLOW)
    text2 = subtitle.render('Insert an AMERICAN quarter to begin', 1, WHITE)

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

    pygame.display.flip()

    credit=0
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)
    while waitingForAOne: #Until we get a 1 value from the arduino, we stay here 5ever
        time.sleep(0.1)
        arduinoRead = arduino.readline()[:-2] #the last bit gets rid of the new-line chars 
        try:
            credit = int(struct.unpack('s', arduinoRead)[0]) #converting serial value from arduino to int
            print('AAANNNDDD the value is ' + str(credit)) #if the value is zero, error occurs so we cop out to the exception at this point
            if credit==1:
                print("thank you for inserting a coin!") #FOR DEBUGGING PURPOSES
                waitingForAOne = False
                #arduino.close() #closing the port
        except:
            pass #can't think of anything better
    
    while running: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP: #this is all for shits and giggles 
                screen.fill(pygame.Color("black"))
                on_text_surface = font.render('Thanks for paying up, CHUMP!', 1, pygame.Color("black"))
                changeBlink() #By clicking multiple times, one can toggle blinking on and off
                gameplay() #this should start the actual game
            if event.type == BLINK_EVENT:
                if getBlink():
                    blink_surface = next(blink_surfaces)
                    screen.blit(blink_surface, blink_rect)
                else:
                    pass
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
