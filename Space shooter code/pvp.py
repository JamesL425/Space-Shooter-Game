#incase this file needs to be run on its own for bug testing (all the stuff in between the ### is there for this reason)
###
import pygame

#starts engines
pygame.init()
pygame.font.init()
pygame.mixer.init()

#settings
WIDTH, HEIGHT = 900, 600
FPS = 60
WHITE = (250,250,250)

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Shooter - PVP")
###    

def draw_window(background, blue, red, blue_bullets, red_bullets, blue_hp, red_hp, hp_font, blueship1, redship1, blue_bullet, red_bullet):
    """Draws window. Background then text then ships then bullets.
    """

    WIN.blit(background,(0,0)) #background

    #pygame.draw.rect(WIN, (0,0,0), BORDER) this is the border (can be turned on)

    #makes hp text
    blue_hp_text = hp_font.render("HP: " + str(blue_hp), 1, WHITE)
    red_hp_text = hp_font.render("HP: " + str(red_hp), 1, WHITE)
    
    #blits text onto WIN (the screen)
    WIN.blit(blue_hp_text, (10, 10))    
    WIN.blit(red_hp_text,(WIDTH - red_hp_text.get_width() - 10, 10))   

    #blits ships onto the screen at the screen's hitbox (x and y of rect (blue and red))
    WIN.blit(blueship1, (blue.x,blue.y))
    WIN.blit(redship1, (red.x,red.y))

    #draws blue bullets
    for bullet in blue_bullets:
        WIN.blit(blue_bullet, (bullet.x, bullet.y))

    #draws red bullets
    for bullet in red_bullets:
        WIN.blit(red_bullet, (bullet.x, bullet.y))

    #refreshes screen    
    pygame.display.flip()

def draw_winner(txt, background, winner_font):
    """Draws the text of the winner on screen (this function is here for convenience)
    """
    WIN.blit(background,(0,0))

    #makes text and draws it
    draw_txt = winner_font.render(txt, 1, WHITE)
    WIN.blit(draw_txt, (WIDTH//2 - draw_txt.get_width()//2,HEIGHT //2 - draw_txt.get_height()//2))

    #updates screen and waits to let user see it
    pygame.display.flip()
    pygame.time.delay(1500) #amount of time can be changed here (in milliseconds)


def blue_handle_input(keys_pressed, blue, border, vel):
    """Takes input and determines whether input is legal (in borders)
    if input is legal, it executes it (by adding velocity).
    """
    #each if statement is separate to allow for multiple buttons to be pressed to prevent some pygame errors
    if keys_pressed[pygame.K_a] and blue.x - vel > 0:
        blue.x -= vel

    if keys_pressed[pygame.K_d] and blue.x + vel + blue.width < border.x:
        blue.x += vel

    if keys_pressed[pygame.K_w] and blue.y - vel > 0:
        blue.y -= vel

    if keys_pressed[pygame.K_s] and blue.y + vel + blue.height < HEIGHT:
        blue.y += vel

def red_handle_input(keys_pressed, red, border, vel):
    """Takes input and determines whether input is legal (in borders)
    if input is legal, it executes it (by adding velocity).
    """
    #each if statement is separate to allow for multiple buttons to be pressed to prevent some pygame errors
    if keys_pressed[pygame.K_LEFT] and red.x - vel > border.x + border.width:
        red.x -= vel

    if keys_pressed[pygame.K_RIGHT] and red.x + vel + red.width < WIDTH:
        red.x += vel

    if keys_pressed[pygame.K_UP] and red.y - vel > 0:
        red.y -= vel

    if keys_pressed[pygame.K_DOWN] and red.y + vel + red.height < HEIGHT:
        red.y += vel

def handle_bullets(blue_bullets, red_bullets, blue, red, blue_hit, red_hit, bullet_vel):
    """Takes bullets and checks if they touch the enemy's hitbox or the border of screen. 
    """
    #blue bullets
    for bullet in blue_bullets:
        bullet.x += bullet_vel #moves bullet

        if red.colliderect(bullet): #collision with player
            pygame.event.post(pygame.event.Event(red_hit))
            blue_bullets.remove(bullet)

        #elif so there is no risk of it removing 2 bullets instead of 1    

        elif bullet.x > WIDTH: #collision with border
            blue_bullets.remove(bullet)
    
    #red bullets
    for bullet in red_bullets:
        bullet.x -= bullet_vel #moves bullet

        if blue.colliderect(bullet): #collision with player
            pygame.event.post(pygame.event.Event(blue_hit))
            red_bullets.remove(bullet)

        #elif so there is no risk of it removing 2 bullets instead of 1

        elif bullet.x < 0: #collision with border
            red_bullets.remove(bullet)




def pvp_game():
    """Main game loop, settings are set for when this function is called from a different file
    launches PVP game.
    """
    #settings
    pygame.display.set_caption("Space Shooter - PVP") # sets caption

    background = pygame.image.load("space2_4-frames.gif")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    border = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT) #border hitbox (rectangle)

    bullet_sound = pygame.mixer.Sound("SingleShot.wav") #loads sound and lowers its volume (because it's extremely loud)
    bullet_sound.set_volume(0.1)

    #events to flag when player is hit
    blue_hit = pygame.USEREVENT + 1 
    red_hit = pygame.USEREVENT + 2

    run = True
    
    #fonts
    winner_font = pygame.font.SysFont("comic sans", 100)
    hp_font = pygame.font.SysFont("comic sans", 50)

    #game settings
    vel = 5 
    spaceshipwidth, spaceshipheight = 128,128 
    max_bullets = 3 #max bullets on screen (essentially acts as a cooldown for shooting)
    bullet_vel = 10
    blue_hp = 10
    red_hp = 10

    #loads player ships and rotates and resizes them
    blueship1 = pygame.image.load("BLUESHIP 1.png")
    blueship1 = pygame.transform.rotate(pygame.transform.scale(blueship1, (spaceshipwidth, spaceshipheight)),270)

    redship1 = pygame.image.load("REDSHIP 1.png")
    redship1 = pygame.transform.rotate(pygame.transform.scale(redship1, (spaceshipwidth, spaceshipheight)),90)

    #loads player bullets and rotates and reiszes them
    blue_bullet = pygame.image.load("blue_bullet.png")
    blue_bullet = pygame.transform.scale(blue_bullet, (10, 5))

    red_bullet = pygame.transform.rotate(blue_bullet, 180)

    

    #hitboxes
    blue = pygame.Rect(100 - spaceshipwidth//2, HEIGHT//2 - spaceshipheight//2, spaceshipwidth, spaceshipheight)
    red = pygame.Rect(WIDTH-100 - spaceshipwidth//2, HEIGHT//2 - spaceshipheight//2, spaceshipwidth, spaceshipheight)
    
    #list of bullet objects
    blue_bullets = []
    red_bullets = []

    #variable to check if someone won
    winner = None

    #game clock
    clock = pygame.time.Clock()

    #game loop
    while run:
        
        for event in pygame.event.get():
            
            #if game is closed, game ends (safety feature)
            if event.type == pygame.QUIT:
                run = False
            
            #if a keyboard input is pressed
            if event.type == pygame.KEYDOWN:
                
                #blue bullet (controlled by left control)
                if event.key == pygame.K_LCTRL and len(blue_bullets) < max_bullets:
                    bullet = pygame.Rect(blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5) #hitbox
                    
                    blue_bullets.append(bullet)

                    #sound
                    bullet_sound.play()
                    pygame.mixer.music.stop()

                #red bullet (controlled by right control)
                if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 - 2, 10, 5) #hitbox

                    red_bullets.append(bullet)

                    #sound
                    bullet_sound.play()
                    pygame.mixer.music.stop()
            
            #handles event thrown when bullet collides with player hitbox (in handle_bullets())
            if event.type == blue_hit:
                blue_hp -= 1
                
            if event.type ==  red_hit:
                red_hp -= 1
                
            
            #when someone's hp falls below 0, game ends (winner is shown)
            if blue_hp <= 0:
                winner = "Red won"
            elif red_hp <= 0:
                winner = "Blue won"
        
        #gets inputs
        keys_pressed = pygame.key.get_pressed()

        #handles inputs
        blue_handle_input(keys_pressed, blue, border, vel)
        red_handle_input(keys_pressed, red, border, vel)

        #handles bullets
        handle_bullets(blue_bullets, red_bullets, blue, red, blue_hit, red_hit, bullet_vel)

        #draws screen    
        draw_window(background, blue, red, blue_bullets, red_bullets, blue_hp, red_hp, hp_font, blueship1, redship1, blue_bullet, red_bullet)
        
        #sets FPS
        clock.tick(FPS)
        
        #if there is a winner, game ends and winner is shown
        if winner:
            draw_winner(winner, background, winner_font)
            run = False
       
#only runs when running this file (for bug testing)          
if __name__ == "__main__":
    pvp_game() 
    


