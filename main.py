import pygame
import random
import math
#initializing the pygame
pygame.init()

#create the scrren
screen=pygame.display.set_mode((800,600))

#background
background=pygame.image.load('Background1.jpg')

#Title and Icon modification
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('001-ufo.png')
pygame.display.set_icon(icon)

#player
playerimg=pygame.image.load('001-space-invaders.png')
#values assigned to make player appear at the middle
playerX=370
playerY=480
playerX_change=0

enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range (num_of_enemies):
    enemyimg.append(pygame.image.load('001-enemy.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(40)

#Bullet
#Ready-you cant see the bullet on the screen
#Fire-the bullet is currently moving
bulletimg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480  #because playerY is at 480
bulletX_change=0 # it is of no use because we wont move bullets horizantally
bulletY_change=5  #bullet speed
bullet_state="ready"

#SCORE
score_val=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

#Game Over Text
over_font=pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score=font.render("score:"+str(score_val),True,(255,255,255))   #first render text and then blit on the screen
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text,(200,250))
def player(x,y):
    #blit used to draw img of player on to screen
    screen.blit(playerimg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y,))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(x+16,y+10))  #x+16 and y+10 because to move the bullet from the centre of spaceship

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False
#game loop
running=True
while running:

    # adding bg color
    screen.fill((0, 0, 0))

    # backgound image
    screen.blit(background,(0,0))

    #moving the spaceship object
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    #if keystroke is pressed check wheteher its right or left
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-4
            if event.key==pygame.K_RIGHT:
                playerX_change=4
            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    #current X coordinate of spaceship
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
        if event.type==pygame.KEYUP: #this is releasing a pressed button
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
    #checking for boundaries pf spaceship so that it doesnt go out of bound
    playerX+=playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=736:  #736 because 64px is given to spaceship
        playerX=736

    #controlling enemy movements
    for i in range (num_of_enemies):
        #Game Over
        if enemyY[i] >= 440:
            for j in range (num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=3
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-3
            enemyY[i] += enemyY_change[i]

            # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_val += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
#bullet movement
    if bulletY <=0 :
        bulletY=480
        bullet_state="ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change

    #we add player after scrren fill
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
