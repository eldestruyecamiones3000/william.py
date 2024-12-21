#PONG

import pygame
import sys
import random
#from pygame import *

# initializacion de pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Configuraciones básicas and crear ventana
ANCHO, ALTO = 1000, 600
FPS = 30
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ponk!")
clock = pygame.time.Clock()
sfont=pygame.font.Font(None,100)

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Variables 
p1s,p2s= 0,0

#Definir players
Pad_zise=((ANCHO//70),(ALTO//2)-100)
D_Pad_poz=[ANCHO-Pad_zise[0],(ALTO//2-Pad_zise[1]//2)]
I_Pad_poz=[0,(ALTO//2-Pad_zise[1]//2)]
p1=pygame.Rect(D_Pad_poz[0],D_Pad_poz[1],Pad_zise[0],Pad_zise[1])
p2=pygame.Rect(I_Pad_poz[0],I_Pad_poz[1],Pad_zise[0],Pad_zise[1])
ball=pygame.Rect((ANCHO//2)-15,(ALTO//2)-15,30,30)
ball_speed=10*random.choice((1,-1))
ball_speedy=10*random.choice((1,-1))
b,a=0,0
# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    # Update
    # Check for keys
    keys=pygame.key.get_pressed()

    if keys[pygame.K_s]:
        p2[1]+=5
    if keys[pygame.K_w]:
        p2[1]-=5
    if keys[pygame.K_UP]:
        p1[1]-=5
    if keys[pygame.K_DOWN]:
        p1[1]+=5
    
    
    ball.x+=ball_speed
    ball.y+=ball_speedy
    

    if p1.top<=0:
        p1.top=0
    elif p1.bottom>=ALTO:
        p1.bottom=ALTO
    if p2.top<=0:
        p2.top=0
    elif p2.bottom>=ALTO:
        p2.bottom=ALTO
    if (a:=ball.left>=ANCHO) or (b:=ball.right<=0):
        p2s+=1 if a else 0
        p1s+=1 if b else 0
        ball.x=ANCHO//2-15
        ball.y=ALTO//2-15
        #ps+= 1 if a 
    if ball.top<=0 or ball.bottom>=ALTO:
        ball_speedy*=-1
    if (bp1:=ball.colliderect(p1)) or (bp2:= ball.colliderect(p2)):
        ball_speed*=-1
        ball.x-=30 if bp1 else 0
        ball.x+=30 if bp2 else 0
    # Draw / render
    screen.fill(BLACK)
    score1=sfont.render(str(p1s),True,WHITE)
    score2=sfont.render(str(p2s),True,WHITE)
    screen.blit(score2,(ANCHO//4,20))
    screen.blit(score1,(3*ANCHO//4,20))
    pygame.draw.line(screen, WHITE, (ANCHO//2-0.5,0),(ANCHO//2-0.5,ALTO))
    pygame.draw.rect(screen,RED,p1)
    pygame.draw.rect(screen,RED,p2)
    pygame.draw.ellipse(screen,WHITE,ball)
    # after drawing everything, flip the display
    pygame.display.flip()
pygame.quit()
