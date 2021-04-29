# Intro to GameDev - main game file
import pgzrun
import random

WIDTH = 1000
HEIGHT = 600

BACKGROUND_TITLE = "aaspace_shooters_bg"
BACKGROUND_LEVEL1 = "aspace_shooters_bg"
BACKGROUND_LEVEL2 = "bspace_shooters_bg"
BACKGROUND_LEVEL3 = "cspace_shooters_bg"
BACKGROUND_INS = "dspace_shooters_bg"

BACKGROUND_IMG = BACKGROUND_TITLE
PLAYER_IMG = "spaceship4game"
JUNK_IMG = "space_junk"
SATELLITE_IMG = "satellite_adv"
DEBRIS_IMG = "space_debris2"
LASER_IMG = "laser_red"

START_IMG = "start_button"
INSTRUCTIONS_IMG = "instructions_button"

start_button = Actor(START_IMG)
start_button.center = (WIDTH/2, 455)

instructions_button = Actor(INSTRUCTIONS_IMG)
instructions_button.center = (WIDTH/2, 530)

SCOREBOX_HEIGHT = 60

score = 0
level = 0
level_screen = 0

junk_collect = 0
lvl2_LIMIT = 5
lvl3_LIMIT = 20
lvl4_LIMIT = 30

JUNK_SPEED = 7
SATELLITE_SPEED = 6
DEBRIS_SPEED = 3
LASER_SPEED = -5


def init():
    global player, junks, junk, satellite, debris, lasers
    player = Actor (PLAYER_IMG)
    player.midright = (WIDTH - 15, HEIGHT/2)

    junk = Actor (JUNK_IMG)
    junk.pos = (0, HEIGHT/2)

    junks = []
    for i in range (5):
        junk= Actor(JUNK_IMG)
        x_pos = random.randint(-500,-50)
        y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
        junk.topright = (x_pos, y_pos)
        junks.append (junk)

    satellite = Actor(SATELLITE_IMG)
    x_sat = random.randint (-500,-50)
    y_sat = random.randint (SCOREBOX_HEIGHT, HEIGHT - satellite.height)
    satellite.topright = (x_sat,y_sat)

    debris= Actor(DEBRIS_IMG)
    x_deb = random.randint(-500,-50)
    y_deb = random.randint (SCOREBOX_HEIGHT, HEIGHT - debris.height)
    debris.topright = (x_deb,y_deb)

    lasers = []
    player.laserActive = 1

init ()
def update ():
    global level, level_screen, BACKGROUND_IMG, junk_collect, score, junks
    if junk_collect == lvl2_LIMIT:
        level = 2
    if junk_collect >= lvl3_LIMIT:
        level = 3
    if junk_collect >= lvl4_LIMIT:
        level = 4
        level_screen = 8
        updateJunk()
        updateSatellite()

    if level_screen == 8:
        BACKGROUND_IMG = BACKGROUND_INS
        if keyboard.RETURN == 1:
            level = 0
            level_screen = 0
            BACKGROUND_IMG = BACKGROUND_TITLE
            score = 0
            junk_collect = 0
            updateJunk()
            updateSatellite()
            updateDebris()
        
    if level == -1:
        BACKGROUND_IMG = BACKGROUND_INS

    #if score >= 0 and level >=1:
    if level_screen == 1:
        BACKGROUND_IMG = BACKGROUND_LEVEL1
        if keyboard.RETURN == 1:
            level_screen = 2
    if level_screen ==2:
        updatePlayer()
        updateJunk()
    if level == 2 and level_screen <=3:
        level_screen = 3
        updateJunk()
        BACKGROUND_IMG = BACKGROUND_LEVEL2
        if keyboard.RETURN == 1:
            level_screen = 4
    if level_screen == 4:
        updatePlayer()
        updateJunk()
        updateSatellite()
    if level == 3 and level_screen <=5:
        level_screen = 5
        updateJunk()
        updateSatellite()
        BACKGROUND_IMG = BACKGROUND_LEVEL3
        if keyboard.RETURN == 1:
            level_screen = 6
    if level_screen == 6:
        updatePlayer()
        updateJunk()
        updateSatellite()
        updateDebris()
        updateLasers()
    if score < 0:
        level_screen = 7
    if level_screen == 7:
        BACKGROUND_IMG = BACKGROUND_IMG
        updateJunk()
        updateSatellite()
        updateDebris()
        if keyboard.RETURN == 1:
            level = 0
            level_screen = 0
            BACKGROUND_IMG = BACKGROUND_TITLE
            score = 0
            junk_collect = 0
            updateJunk()
            updateSatellite()
            updateDebris()

def updatePlayer():
    if (keyboard.up == 1):
        player.y += (-5)
    elif (keyboard.down == 1):
        player.y += 5

    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
    if player.top < 60:
        player.top = 60

    if keyboard.space == 1:
        laser= Actor(LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)

def updateJunk():
    global score, JUNK_SPEED, junk_collect, level_screen
    for junk in junks:
        junk.x += JUNK_SPEED
        collision = player.colliderect (junk)
        if junk.left > WIDTH or collision == 1:
            JUNK_SPEED = random.randint (2,10)
            x_pos = -50
            y_pos = random.randint (SCOREBOX_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)
        if level_screen == 0 or level_screen == 3 or level_screen== 5 or level_screen == 7 or level_screen == 8:
            x_pos = random.randint (-500, -50)
            y_pos = random.randint (SCOREBOX_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)
        if (collision == 1):
            score +=1
            junk_collect +=1

def updateSatellite():
    global score, SATELLITE_SPEED
    satellite.x += SATELLITE_SPEED

    collision = player.colliderect (satellite)
    if satellite.left > WIDTH or collision ==1 or level_screen == 5 or level_screen == 7 or level_screen==8:
        x_sat = random.randint (-500,-50)
        y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)
    if collision ==1:
        score += -10

def updateDebris():
    global score, DEBRIS_SPEED
    debris.x += DEBRIS_SPEED
    DEBRIS_SPEED = random.randint (3,5)
    collision = player.colliderect (debris)
    if debris.left >WIDTH or collision == 1 or level_screen == 7 or level_screen==8:
        x_deb = random.randint (-500,-50)
        y_deb = random.randint (SCOREBOX_HEIGHT, HEIGHT- debris.height)
        debris.topright = (x_deb, y_deb)
    if collision == 1:
        score += -10

def draw():
    screen.clear()
    screen.blit(BACKGROUND_IMG, (0,0))
    if level == 0:
        start_button.draw()
        instructions_button.draw()
    if level == -1:
        start_button.draw()
        show_instructions = "Use UP and DOWN arrow keys to move your player\n\npress SPACEBAR to shoot\nplayers are only allowed to shoot lasers in level 3\n\n\nThe objective of the game is to clean up space and get the highest score\nthis is done by collecting space debris and shooting destroyed satellites"

        screen.draw.text(show_instructions,midtop= (WIDTH/2, 150), fontsize = 35, color="white")

    if level_screen ==1 or level_screen == 3 or level_screen ==5:
        show_restart_text = "Press ENTER to start game"
        screen.draw.text(show_restart_text,midtop= (WIDTH/2, 125), fontsize = 45, color="white")

        show_level_title = "LEVEL" +str(level)
        screen.draw.text(show_level_title, center= (WIDTH/2, HEIGHT/2), fontsize= 70, color="white")

    if level_screen == 1:
        show_rule_a = "collect the junks with your ship\n\nyou must collect 5 junks to reach level 2"
        screen.draw.text (show_rule_a, center = (WIDTH/2,450), fontsize = 35, color = "white")

    if level_screen== 3 :
        show_rule_b = "collect junks like in level 1\n\nyou must avoid the satellites or else you will lose 10 points\n\nyou must collect 20 junks to reach the final level"
        screen.draw.text (show_rule_b, center = (WIDTH/2,450), fontsize = 35, color = "white")
    
    if level_screen == 5:
        show_rule_c = "shoot the dead debris by pressing the SPACEBAR\n\nyou will earn 5 points\n\nif you shoot the satellites you will lose 5 points\n\nthe game will end when you have collected 30 junks"
        screen.draw.text (show_rule_c, center = (WIDTH/2,450), fontsize = 35, color = "white")

    if level >=1: 
        player.draw()
        for junk in junks:
            junk.draw()

    if level >= 2:
        satellite.draw()

    if level == 3:
        debris.draw()
        for laser in lasers:
            laser.draw()
      
    if level_screen >= 2:
        show_score = "Score:" + str (score)
        screen.draw.text (show_score, topleft = (650,30), fontsize = 35, color = "white")

        show_collect_value = "Junk:" +str(junk_collect)
        screen.draw.text (show_collect_value, topleft= (450,30), fontsize = 35, color = "white")

    if level_screen == 7:
        show_over = "GAME OVER\n\npress ENTER to play again\n\nscore:" + str (score)
        screen.draw.text (show_over, center = (WIDTH/2, HEIGHT/2), fontsize = 70, color = "white")

    if level_screen == 8:
        show_win = "YOU WIN\n\npress ENTER to play again\n\nscore:" +str (score)
        screen.draw.text (show_win, center = (WIDTH/2, HEIGHT/2), fontsize = 70, color = "white")
        show_creator = "Made by :Shamaica S"
        screen.draw.text (show_creator, center = (650,500), fontsize = 35, color = "white")

def updateLasers():
    global score
    for laser in lasers:
        laser.x += LASER_SPEED
        if laser.right<0:
            lasers.remove(laser)
        if satellite.colliderect (laser)==1:
            lasers.remove(laser)
            x_sat = random.randint(-500,-50)
            y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score += -5
        if debris.colliderect(laser)==1:
            lasers.remove(laser)
            x_deb = random.randint(-500,-50)
            y_deb = random.randint (SCOREBOX_HEIGHT, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score += 5

def on_mouse_down(pos):
    global level, level_screen
    if start_button.collidepoint(pos):
        level=1
        level_screen=1
        print ("start button pressed!")
    if instructions_button.collidepoint(pos):
        level = -1
        print("instructions button pressed!")

player.laserActive = 1  # add laserActive status to the player

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list

    
pgzrun.go()
