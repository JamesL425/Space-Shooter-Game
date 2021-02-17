#importing modules and other files (for pvp, pve and shop)
import pygame
import pvp
import pve
import shop

#starting up engines
pygame.init()
pygame.font.init()
pygame.mixer.init()

#settings (can be changed)
WIDTH, HEIGHT = 900, 600
FPS = 60
WHITE = (250,250,250)

#makes screen and caption
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Shooter - Main Menu")

#pygame settings
BACKGROUND = pygame.image.load("space1_4-frames.gif")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
FONT = pygame.font.SysFont("comic sans", 150)

#button size
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 100

#button class (makes buttons (obviously))
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
        #pygame.draw.rect(WIN, (0,0,0), self.rect) #turn on to check the hitbox
        draw_txt = FONT.render(self.txt, 1, WHITE)
        WIN.blit(draw_txt, (self.x, self.y))
        


def make_buttons():
    """Makes a list with buttons (button name and attributes set)
    there's probably a more efficient way to do this, but this was the way I did it.
    """
    buttons = []
    buttons.append(Button("PVP", pygame.Rect((WIDTH//2)-BUTTON_WIDTH//2,100-BUTTON_HEIGHT//2,BUTTON_WIDTH,BUTTON_HEIGHT),(WIDTH//2)-BUTTON_WIDTH//2,100-BUTTON_HEIGHT//2,pvp.pvp_game))
    buttons.append(Button("PVE", pygame.Rect((WIDTH//2)-BUTTON_WIDTH//2,300-BUTTON_HEIGHT//2,BUTTON_WIDTH,BUTTON_HEIGHT),(WIDTH//2)-BUTTON_WIDTH//2,300-BUTTON_HEIGHT//2,pve.pve_game))
    buttons.append(Button("SHOP", pygame.Rect((WIDTH//2)-BUTTON_WIDTH//2-50,500-BUTTON_HEIGHT//2,BUTTON_WIDTH+100,BUTTON_HEIGHT),(WIDTH//2)-BUTTON_WIDTH//2-50,500-BUTTON_HEIGHT//2,shop.ship_shop))
    
    return buttons

def draw_menu(buttons):
    """Draws background then draws all buttons on top (using button.draw_button()).
    """
    WIN.blit(BACKGROUND, (0,0))
    
    #draws each button
    for button in buttons:
        button.draw_button()

    #refreshes display
    pygame.display.flip()


def main_menu():
    """Main function (everything runs from this function)
    when mousebutton1 is pressed, it gets pos (mouse position)
    and runs the button's function. 
    """
    #when run is false, the game ends
    run = True

    #makes buttons
    buttons = make_buttons()
    
    #assigns clock for later
    clock = pygame.time.Clock()

    #settings for PVE
    level = 1
    money = 0
    hp = 10
    dmg = 1
    regen = 0

    #main game loop
    while run:
        for event in pygame.event.get():
            
            #if tab is closed, game ends (a safety feature)
            if event.type == pygame.QUIT:
                run = False

            #if mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:

                #gets mouse position
                pos = pygame.mouse.get_pos()

                #iterating through buttons, then if one is where mouse position is, it does button.func
                for button in buttons:

                    if button.rect.collidepoint(pos):

                        if button.func == pve.pve_game:
                            money += button.func(level, hp, dmg, regen) #money can be gained through pve game, (pve game returns an int)

                        elif button.func == shop.ship_shop:
                            money, hp, dmg, regen = button.func(money, hp, dmg, regen)

                        else:
                            button.func()

                        #resets the window caption
                        pygame.display.set_caption("Space Shooter - Main Menu")
        
        #draws the menu every frame
        draw_menu(buttons)

        #sets fps
        clock.tick(FPS)

        

    #closes the pygame engine    
    pygame.quit()








#safety feature: only runs if this is the file that is being run
if __name__ == "__main__":
    main_menu()