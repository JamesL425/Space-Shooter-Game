#this is here incase this file is run on its own (everything between ### is there for this reason)
###
import pygame

#starts engine
pygame.init()
pygame.font.init()
pygame.mixer.init()

#settings
WIDTH, HEIGHT = 900, 600
FPS = 60
WHITE = (250,250,250)
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

BACKGROUND = pygame.image.load("space3_4-frames.gif")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

#button size
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 100
###

class Button:
    def __init__(self, txt, rect, x, y, func):
        """Assigns text and hitbox (rect)
        x and y and function of button (func).
        """
        self.txt = txt
        self.rect = rect #hitbox
        
        #x and y position here for reference when writing the text
        self.x = x
        self.y = y
        
        #size
        self.width = 60
        self.height = 30

        self.func = func #function of button

    def draw_button(self):
        """Makes button text, then draws it.
        """
        #sets font
        font = pygame.font.SysFont("comic sans", 120)

        #pygame.draw.rect(WIN, (0,0,0), self.rect) #turn on to check the hitbox

        #draws
        draw_txt = font.render(self.txt, 1, WHITE)
        WIN.blit(draw_txt, (self.x, self.y))

def make_buttons():
    """Makes buttons (each button increases stat when clicked, and takes money), x is to go back to main menu.
    """
    buttons = []

    buttons.append(Button("HP", pygame.Rect((WIDTH//2)-BUTTON_WIDTH//2 +50,100-BUTTON_HEIGHT//2,BUTTON_WIDTH//2 + 20,BUTTON_HEIGHT),(WIDTH//2)-BUTTON_WIDTH//2 +50,100-BUTTON_HEIGHT//2,change_hp))
    buttons.append(Button("DMG", pygame.Rect((WIDTH//2)-BUTTON_WIDTH//2,250-BUTTON_HEIGHT//2,BUTTON_WIDTH,BUTTON_HEIGHT),(WIDTH//2)-BUTTON_WIDTH//2,250-BUTTON_HEIGHT//2,change_dmg))
    buttons.append(Button("REGEN", pygame.Rect((WIDTH//2)-BUTTON_WIDTH//2-50,400-BUTTON_HEIGHT//2,BUTTON_WIDTH+100,BUTTON_HEIGHT),(WIDTH//2)-BUTTON_WIDTH//2-50,400-BUTTON_HEIGHT//2,change_regen))
    buttons.append(Button("X", pygame.Rect(WIDTH - 80, 20,BUTTON_WIDTH-140,BUTTON_HEIGHT-20),WIDTH - 80, 20, "q"))

    return buttons

def change_hp(money, hp):
    """Shops for hp when hp button is clicked.
    """
    if hp > 1000:
        return money, hp

    if hp < 20:

        if money >= 10:

            return money - 10, hp + 5

    elif hp >= 20 and hp < 50:

        if money >= 20:

            return money -20, hp + 5
    else:

        if money >= 100:

            return money - 100, hp + 10 

    return money,hp

def change_dmg(money, dmg):
    """Shops for dmg when dmg button is clicked.
    """
    if dmg >= 30:
        return money, dmg

    if dmg < 5:

        if money >= 10:

            return money - 10, dmg + 1

    elif dmg >= 5 and dmg < 15:

        if money >= 20:

            return money -20, dmg + 1

    else:

        if money >= 100:

            return money - 100, dmg + 1 

    return money, dmg

def change_regen(money, regen):
    """Shops for regen when regen button is clicked.
    """
    if regen >= 100:
        return money, regen

    if regen < 20:

        if money >= 10:

            return money - 10, regen + 5

    elif regen >= 20 and regen < 40:

        if money >= 20:

            return money -20, regen + 5

    else:

        if money >= 100:

            return money - 100, regen + 5 

    return money, regen

def draw_shop(buttons, money, hp, dmg, regen):
    """Draws shop. Stats at the bottom.
    """
    font = pygame.font.SysFont("comic sans", 50)

    WIN.blit(BACKGROUND, (0,0))

    #draws each button
    for button in buttons:
        button.draw_button()

    draw_txt = font.render("MONEY: " + str(money) + " HP: " + str(hp) + " DMG: " + str(dmg) + " REGEN: " + str(regen), 1, WHITE)
    WIN.blit(draw_txt, (WIDTH//2 - 350, HEIGHT-50))

    #refreshes screen
    pygame.display.flip()

def ship_shop(money, hp, dmg, regen):
    """Ship Shop. Acts like a shop. When a button is pressed, they take your money: those damn capitalists.
    """
    #sets caption
    pygame.display.set_caption("Space Shooter - Ship Shop")

    #makes buttons on function call
    buttons = make_buttons()

    clock = pygame.time.Clock()
    run = True

    #main loop 
    while run:

        for event in pygame.event.get():

            #if shop is closed, shop closes (safety feature)
            if event.type == pygame.QUIT:
                run = False

            #if mouse is pressed   
            if event.type == pygame.MOUSEBUTTONDOWN:

                #gets mouse location
                pos = pygame.mouse.get_pos()

                #checks whether each button is being pressed (whether mouse.pos == button.pos)
                for button in buttons:

                    if button.rect.collidepoint(pos):

                        if button.func == change_hp:
                            money, hp = button.func(money, hp) #hp shop, changes hp value and money

                        elif button.func == change_dmg:
                            money, dmg = button.func(money, dmg) # dmg shop, changes dmg value and money

                        elif button.func == "q":
                            run = False #ends shop if x is clicked

                        else:
                            money, regen = button.func(money, regen) #regen shop, changes regen value and money

        #draws shop               
        draw_shop(buttons, money, hp, dmg, regen)

        #sets FPS
        clock.tick(60)

    #returns variable changes (from shopping)
    return money, hp, dmg, regen


#only runs when this file is run (for bug testing)        
if __name__ == "__main__":
    ship_shop(50, 10, 1 , 2)  
    
