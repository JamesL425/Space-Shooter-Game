#incase this file needs to be run on its own for bug testing (everything between the ###'s are there for this reason)
###
import pygame
import random

#starts engines
pygame.init()
pygame.font.init()
pygame.mixer.init()

#settings
WIDTH, HEIGHT = 900, 600
FPS = 60
WHITE = (250,250,250)

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
###

class Enemy:
    def __init__ (self, rect, n, hp, bullets):
        """Enemy class, stores hitbox, event when hit,
        bullets and hp.
        """
        self.rect = rect
        self.event = pygame.USEREVENT + n #event when hit
        self.hp = hp
        self.bullets = bullets

        #sets initial direction (randomly)
        direction = random.randint(0,1)
        self.direction = not direction


def draw_window(background, player, enemies, ship1, enemyship1, border, player_bullets, hp_font, player_hp, player_bullet, enemy_bullet, level):
    """Draws window. Draws player then text then enemies then bullets.
    """
    WIN.blit(background, (0,0))
    WIN.blit(ship1, (player.x, player.y)) #player ship

    #pygame.draw.rect(WIN,(0,0,0), border) #turn on the see border

    #sums enemy health
    total_enemy_health = 0
    for enemy in enemies:
        total_enemy_health += enemy.hp

    #makes text
    player_hp_text = hp_font.render("HP: " + str(player_hp), 1, WHITE)
    total_enemy_hp_text = hp_font.render("TOTAL HP: " + str(total_enemy_health), 1, WHITE)
    total_enemy_text = hp_font.render("N(ENEMIES): " + str(len(enemies)), 1, WHITE)
    level_text = hp_font.render("LEVEL: " + str(level), 1, WHITE)

    #draws text
    WIN.blit(player_hp_text, (WIDTH //2 -50, HEIGHT-50))
    WIN.blit(total_enemy_hp_text, (50,50))
    WIN.blit(total_enemy_text, (550,50))
    WIN.blit(level_text, (WIDTH //2 -100, 50))

    #each enemy is drawn
    for enemy in enemies:
        WIN.blit(enemyship1, (enemy.rect.x, enemy.rect.y))
    
    #each bullet is drawn
    for bullet in player_bullets:
        WIN.blit(player_bullet, (bullet.x, bullet.y))

    for enemy in enemies:
        for bullet in enemy.bullets:
            WIN.blit(enemy_bullet, (bullet.x, bullet.y))
    
    #updates screen
    pygame.display.flip()

def draw_winner(txt, background, winner_font):
    """Draws winner. Here for convenience. (reused from pvp module)
    """
    WIN.blit(background,(0,0))

    draw_txt = winner_font.render(txt, 1, WHITE)
    WIN.blit(draw_txt, (WIDTH//2 - draw_txt.get_width()//2,HEIGHT //2 - draw_txt.get_height()//2))

    pygame.display.flip()

    pygame.time.delay(1000) #can be changed to reduce waiting time (milliseconds) (a time below 300 milliseconds is not recommended)

def get_enemies(level, ship1width, ship1height):
    """Is done every time pve_game() is started, makes enemies at set intervals.
    """
    #list of enemies
    enemies = []

    #for loop makes 1 enemy each time (can be increased to make more enemies)
    for i in range (1,6):
        #makes hitbox
        enemyrect = pygame.Rect(i*150 - ship1width//2, 30+ship1height//2,ship1width, ship1height)
        #makes enemy object using hitbox
        enemy = Enemy(enemyrect, i+1, level, [])
        #adds to list
        enemies.append(enemy)
    
    return enemies

def player_handle_input(keys_pressed, player, border, vel):
    """Handles player input. Makes sure that the player doesn't go past border or outside screen.
    """
    if keys_pressed[pygame.K_a] and player.x - vel > 0:
        player.x -= vel

    if keys_pressed[pygame.K_d] and player.x + vel + player.width < WIDTH:
        player.x += vel
        
    if keys_pressed[pygame.K_w] and player.y - vel > border.y+ border.height:
        player.y -= vel
        
    if keys_pressed[pygame.K_s] and player.y + vel + player.height < HEIGHT:
        player.y += vel

def enemy_movement(enemies,  vel):
    """Enemy movement is made randomly on initiation of class,
    if enemy touches side of screen, movement is reversed.
    """
    for enemy in enemies:

        if enemy.direction == True:

            if enemy.rect.x - vel > 0:
                enemy.rect.x -= vel

            else:
                enemy.direction = not enemy.direction

        if enemy.direction == False:

            if enemy.rect.x + vel + enemy.rect.width < WIDTH:
                enemy.rect.x += vel

            else:
                enemy.direction = not enemy.direction


def handle_bullets(player_bullets, enemies, player, player_hit, bullet_vel, e_bullet_vel):
    """Handles player and enemy bullets.
    """
    #player bullets
    for bullet in player_bullets:
        
        bullet.y -= bullet_vel

        for enemy in enemies:

            if enemy.rect.colliderect(bullet):

                pygame.event.post(pygame.event.Event(enemy.event))
                player_bullets.remove(bullet)

                break #if one enemy is hit, it stops the loop

        if bullet.y < 0: #top of screen

            player_bullets.remove(bullet)

    #enemy bullets        
    for enemy in enemies:

        for bullet in enemy.bullets:

            bullet.y += e_bullet_vel

            if player.colliderect(bullet):

                pygame.event.post(pygame.event.Event(player_hit))
                enemy.bullets.remove(bullet)

            elif bullet.y > HEIGHT: #bottom of screen

                enemy.bullets.remove(bullet)



            


def pve_game(level , hp , dmg, regen, g = 50):
    """PVE game. Stats are set in parameters. (g is money returned on game end).
    """
    #sets caption
    pygame.display.set_caption("Space Shooter - PVE")
    
    #settings set in function (incase function is run from another file)

    #loads ships and sets hitboxes
    ship1width, ship1height = 64,64
    enemyshipwidth, enemyshipheight = 64 - (2*level) + 5, 64 - (2*level) + 5

    ship1 = pygame.image.load("BLUESHIP 1.png")
    ship1 = pygame.transform.scale(ship1, (ship1width, ship1height))

    enemyship1 = pygame.image.load("REDSHIP 2.png")
    enemyship1 = pygame.transform.rotate(pygame.transform.scale(enemyship1, (enemyshipwidth, enemyshipheight)), 180)
    
    #loads bullets and sets bullet hitboxes
    player_bullet = pygame.image.load("blue_bullet.png")
    player_bullet = pygame.transform.rotate(pygame.transform.scale(player_bullet, (10, 5)), 270)

    player_bullets = []

    enemy_bullet = pygame.transform.rotate(player_bullet, 180)

    #makes sounds
    bullet_sound = pygame.mixer.Sound("SingleShot.wav")
    bullet_sound.set_volume(0.2)
    enemy_bullet_sound = bullet_sound
    enemy_bullet_sound.set_volume(0.02) #sound reduced because there are multiple enemies (to avoid extremely loud volume on later levels)

    #fonts
    winner_font = pygame.font.SysFont("comic sans", 100)
    hp_font = pygame.font.SysFont("comic sans", 50)

    #sets background
    background = pygame.image.load("space5_4-frames.gif")
    background = pygame.transform.scale(background, (WIDTH,HEIGHT))

    #makes border hitbox
    border = pygame.Rect(0, (HEIGHT//2)-5, WIDTH, 10)

    #makes player hitbox
    player = pygame.Rect(WIDTH//2 - ship1width//2, HEIGHT-50-ship1height//2, ship1width, ship1height)

    #makes enemies
    enemies = get_enemies(level, enemyshipwidth, enemyshipheight)

    #game settings
    vel = 5
    e_vel = level//2 + 2

    bullet_vel = 10
    e_bullet_vel = 5 + level 

    max_bullets = 3 + dmg

    player_hit = pygame.USEREVENT + 1 #event when player is hit
    
    player_hp = 10 + hp 

    winner = None #variable to check whether player won or lost

    #variable to end game
    run = True

    #pygame clock
    clock = pygame.time.Clock()

    #main game loop
    while run:

        for event in pygame.event.get():

            #if game is closed, game ends (safety feature)
            if event.type == pygame.QUIT:
                run = False

            #gets keyboard input   
            if event.type == pygame.KEYDOWN:
                
                #player bullet shooting mechanic, controlled by space
                if event.key == pygame.K_SPACE and len(player_bullets) < max_bullets:
                    bullet = pygame.Rect(player.x + player.width//2 - 2, player.y - player.height , 10, 5)
                    
                    player_bullets.append(bullet)
                    bullet_sound.play()
                    pygame.mixer.music.stop()
            
            #if event is event thrown by handle_bullets() (player is hit)
            if event.type == player_hit:
                
                #dmg increases with level
                if level < 5:
                    player_hp -= 1

                elif level < 10:
                    player_hp -= 2

                elif level < 15:
                    player_hp -= 3

                elif level < 20:
                    player_hp -= 4

                else:
                    player_hp -= 5
            
            #checks whether each enemy is hit
            for enemy in enemies:

                if event.type == enemy.event:

                    enemy.hp -= dmg
                    player_hp += regen #regen
        
        #sets player hp to 0 if it is less than 0 to avoid an error
        if player_hp < 0:
            player_hp = 0

        #max bullets (essentially bullet cooldown), changes with level
        max_e_b = level

        if max_e_b > 10:
            max_e_b = 10

        #each enemy checks if it can shoot    
        for enemy in enemies:

            if len(enemy.bullets) < max_e_b:
                bullet = pygame.Rect(enemy.rect.x + enemy.rect.width//2 - 2, enemy.rect.y + enemy.rect.height , 10, 5)

                enemy.bullets.append(bullet)
                enemy_bullet_sound.play()
                pygame.mixer.music.stop() 

        #removes any enemies that have hp < 0          
        for enemy in enemies:

            if enemy.hp <= 0:
                enemies.remove(enemy) 

        #hp cap at 1 million to avoid some errors        
        if player_hp > 1000000:
            player_hp = 1000000   

        #checks if player won or lost   
        if player_hp <= 0:
            winner = "you lose"

        elif len(enemies) <= 0:
            winner = "you win"
       
        clock.tick(FPS) #sets FPS

        #gets input
        keys_pressed = pygame.key.get_pressed()

        #handles input
        player_handle_input(keys_pressed, player, border, vel)
        
        #handles enemy movement
        enemy_movement(enemies,  e_vel)

        #handles bullets
        handle_bullets(player_bullets, enemies, player, player_hit, bullet_vel, e_bullet_vel)

        #draws the window (screen)
        draw_window(background,player, enemies , ship1, enemyship1, border, player_bullets, hp_font, player_hp, player_bullet, enemy_bullet, level)
        
        #if there is a winner (player won or lost) it determines what happens next
        if winner: 
            
            if winner == "you win" and level < 30:
                draw_winner(winner, background, winner_font) #draws winner

                #starts game again with level + 1
                level += 1
                
                #player earns more money with each level completed
                g += 50

                g = pve_game(level, hp, dmg, regen, g)
                
            elif winner == "you win" and level >= 30:
                draw_winner("You beat the game!", background, winner_font) #draws winner
                draw_winner("You got money!", background, winner_font)

                #player gets a lot of money for beating the game (it's very hard)
                return 10000 ** 2
            else:
                draw_winner(winner, background, winner_font) #draws winner
                draw_winner("you got " + str(g), background, winner_font)

                #returns money earned when game is beation
                return g
            
            return g #this is here just incase

    return 0 #incase you press the quit button                
            
            

#only runs when this file is run (for bug testing)
if __name__ == "__main__":
    pve_game(1, 10, 1, 0)

