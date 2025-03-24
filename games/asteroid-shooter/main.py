# import packages
import sys
sys.path.append('/')


import pygame
import pygame.locals
from asteroid import *
from player import *
from cursor import *
from bullet import *
import time



################################
# initializing imported module #
################################

pygame.init()




#######################
# Variables partagées #
#######################

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

SCREEN_WIDTH = window.get_width()
SCREEN_HEIGHT = window.get_height()
PLAYER_WIDTH = 45
PLAYER_HEIGHT = 45
PAUSE_TICKING = 15
POLICE = 'comicsansms'
MENU_PAUSE_BUTTONS_COLOR = 'white'
MENU_PAUSE_ON_HOVER_BUTTONS_COLOR = 'grey41'

clock = pygame.time.Clock()
pause = False
start_time = time.time()
SCREEN_CENTER_X = SCREEN_WIDTH/2
SCREEN_CENTER_Y = SCREEN_HEIGHT/2

player = Player(SCREEN_CENTER_X, SCREEN_CENTER_Y, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
cursor = Cursor(SCREEN_CENTER_X, SCREEN_CENTER_Y)

bullets = []
asteroids = []

all_player_sprites = None
all_cursor_sprites = None
all_asteroids_sprites_list = None


##################################
# Utilitaire pour le menu pause  #
##################################

def quit_game():
    pygame.quit()
    sys.exit()

def text_objects(text, font, color='black'):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(label, posX, posY, width, height, backgroundColor, onHoverBackgroundColor, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if posX+width > mouse[0] > posX and posY+height > mouse[1] > posY:
        pygame.draw.rect(window, onHoverBackgroundColor,(posX, posY, width, height))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(window, backgroundColor,(posX, posY, width, height))

    smallText = pygame.font.SysFont(POLICE, 20)
    textSurf, textRect = text_objects(label, smallText)
    textRect.center = ( (posX+(width/2)), (posY+(height/2)) )
    window.blit(textSurf, textRect)

def unpause():
    newevent = pygame.event.Event(pygame.locals.KEYDOWN, unicode="esc", key=pygame.locals.K_ESCAPE, mod=pygame.locals.KMOD_NONE)
    pygame.event.post(newevent)
    clock.tick(PAUSE_TICKING)

def paused():
    pause = True
    pygame.mouse.set_visible(True)
    largeText = pygame.font.SysFont(POLICE, 115)
    TextSurf, TextRect = text_objects("Paused", largeText, MENU_PAUSE_BUTTONS_COLOR)
    TextRect.center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))
    window.blit(TextSurf, TextRect)
    
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False

        button("Continue", (SCREEN_WIDTH/2)-175, (SCREEN_HEIGHT/2)-300, 150, 50, MENU_PAUSE_BUTTONS_COLOR, MENU_PAUSE_ON_HOVER_BUTTONS_COLOR, unpause)
        button("Quit", (SCREEN_WIDTH/2)+25, (SCREEN_HEIGHT/2)-300, 150, 50, MENU_PAUSE_BUTTONS_COLOR, MENU_PAUSE_ON_HOVER_BUTTONS_COLOR, quit_game)

        pygame.display.update()
        clock.tick(PAUSE_TICKING)
        
    pygame.mouse.set_visible(False)




#####################################
# Utilitaire pour le menu game over #
#####################################

def restart():
    player = Player(SCREEN_CENTER_X, SCREEN_CENTER_Y, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    bullets = []
    asteroids = []
    start_time = time.time()
    counter = 0
    all_player_sprites = pygame.sprite.Group(player)
    all_cursor_sprites = pygame.sprite.Group(cursor)
    all_asteroids_sprites_list = []
    newevent = pygame.event.Event(pygame.locals.KEYDOWN, unicode="esc", key=pygame.locals.K_ESCAPE, mod=pygame.locals.KMOD_NONE)
    pygame.event.post(newevent)
    clock.tick(PAUSE_TICKING)

def game_over():
    pause = True
    pygame.mouse.set_visible(True)
    largeText = pygame.font.SysFont(POLICE, 115)
    mediumText = pygame.font.SysFont(POLICE, 50)
    
    TextSurf, TextRect = text_objects("Game over", largeText, MENU_PAUSE_BUTTONS_COLOR)
    TextRect.center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))
    window.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("Final score : " + str(player.score), mediumText, MENU_PAUSE_BUTTONS_COLOR)
    TextRect.center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2) + 200)
    window.blit(TextSurf, TextRect)
    
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False

        button("Restart", (SCREEN_WIDTH/2)-175, (SCREEN_HEIGHT/2)-300, 150, 50, MENU_PAUSE_BUTTONS_COLOR, MENU_PAUSE_ON_HOVER_BUTTONS_COLOR, restart)
        button("Quit", (SCREEN_WIDTH/2)+25, (SCREEN_HEIGHT/2)-300, 150, 50, MENU_PAUSE_BUTTONS_COLOR, MENU_PAUSE_ON_HOVER_BUTTONS_COLOR, quit_game)

        pygame.display.update()
        clock.tick(PAUSE_TICKING)
        
    pygame.mouse.set_visible(False)




##############################
# Affichage des informations #
##############################

def show_timer():
    counting_string = ""
    
    total = int(time.time() - start_time)
    seconds = total % 60
    minutes = (total // 60) % 60
    heures = minutes // 60

    if (heures < 10):
        counting_string = counting_string + "0" + str(heures) + ":"
    else :
        counting_string = counting_string + str(heures) + ":"

    if (minutes < 10):
        counting_string = counting_string + "0" + str(minutes) + ":"
    else :
        counting_string = counting_string + str(minutes) + ":"

    if (seconds < 10):
        counting_string = counting_string + "0" + str(seconds)
    else :
        counting_string = counting_string + str(seconds)

    smallText = pygame.font.SysFont(POLICE, 14)
    TextSurf, TextRect = text_objects(counting_string, smallText, 'white')
    TextRect.center = (SCREEN_WIDTH-100, 30)
    window.blit(TextSurf, TextRect)

def show_player_life():
    xStart = SCREEN_WIDTH-400
    heartWidth = 18

    for i in range(0, player.pv):
        rect = player.pv_img.get_rect(center = (xStart + heartWidth*i, 30))
        window.blit(player.pv_img, rect)

def show_player_score():
    smallText = pygame.font.SysFont(POLICE, 14)
    TextSurf, TextRect = text_objects("Score : " + str(player.score), smallText, 'white')
    TextRect.center = (100, 30)
    window.blit(TextSurf, TextRect)
    
def show_top_informations():
    show_timer()
    show_player_life()
    show_player_score()


###########################
# Variable initialisation #
###########################

running = True

all_player_sprites = pygame.sprite.Group(player)
all_cursor_sprites = pygame.sprite.Group(cursor)
all_asteroids_sprites_list = []

pygame.mouse.set_visible(False)
counter = 0
count_before_next_asteroid = 200




##########################################
# keep game running till running is true #
##########################################

while running:

    player.point_at(*pygame.mouse.get_pos())

    bullets = [bullet for bullet in bullets if bullet.isOutOfRange(SCREEN_WIDTH, SCREEN_HEIGHT)]
    
    # Check for event if user has pushed 
    # any event in queue
    for event in pygame.event.get():
         
        # if event is of type quit then set 
        # running bool to false
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused()

        if event.type == pygame.MOUSEBUTTONDOWN:
            bullets.append(Bullet(player.rect[0]+(PLAYER_WIDTH/2), player.rect[1]+(PLAYER_HEIGHT/2), *pygame.mouse.get_pos()))

    keys = pygame.key.get_pressed()
    player.move(keys[pygame.K_RIGHT]-keys[pygame.K_LEFT], keys[pygame.K_DOWN]-keys[pygame.K_UP])
    cursor.move(*pygame.mouse.get_pos())

    if (counter % count_before_next_asteroid == 0):
        newAsteroid = Asteroid(player.rect[0], player.rect[1], SCREEN_WIDTH, SCREEN_HEIGHT)
        asteroids.append(newAsteroid)
        all_asteroids_sprites_list.append(pygame.sprite.Group(newAsteroid))

    # Dessiner les objets
    window.fill('black')
    
    for bullet in bullets :
        bullet.draw(window)
        bullet.updatePos()

    for asteroid in asteroids :
        asteroid.move()

    collisionsWithPlayer = player.rect.collidelistall([asteroid.rect for asteroid in asteroids])
    collisionsWithBullets = []
    bulletsToDelete = []
    for i, bullet in enumerate(bullets) :
        newCollisions = bullet.rect.collidelistall([asteroid.rect for asteroid in asteroids])
        if (len(newCollisions) > 0):
            collisionsWithBullets += bullet.rect.collidelistall([asteroid.rect for asteroid in asteroids])
            bulletsToDelete.append(i)

    if (bulletsToDelete) :
        bulletsToDelete.reverse()
        for bullet in bulletsToDelete :
            bullets.pop(bullet)

    if len(collisionsWithPlayer) > 0 :
        collisionsWithPlayer.reverse()
        for collision in collisionsWithPlayer :
            player.pv -= 1
            if (player.pv <= 0):
                game_over()
            asteroids.pop(collision)
            all_asteroids_sprites_list.pop(collision)

    if len(collisionsWithBullets) > 0 :
        collisionsWithBullets.reverse()
        for collision in collisionsWithBullets :
            player.score += 10
            asteroids.pop(collision)
            all_asteroids_sprites_list.pop(collision)

        
    all_player_sprites.draw(window)
    all_cursor_sprites.draw(window)
    for sprites in all_asteroids_sprites_list :
        sprites.draw(window)
    
    show_top_informations()
    
    pygame.display.update()

    counter += 1
    



###########################
# Fin de la boucle de jeu #
###########################

pygame.quit()
sys.exit()
