import pygame
from random import uniform, randint

num = int()

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)
# Declaring the image and screen so that it has variables and boundaries
class Pause:
    def __init__(self, x, y):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False
        pygame.display.set_caption("Highscore Menu")

# This is the logic for whether someone has clicked on to the button

    def response(self):
        global num
        position=pygame.mouse.get_pos()
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                num += 1
                self.clicked=True
                display_circle()
            if not pygame.mouse.get_pressed()[0]:
                self.clicked=False
        screen.blit(self.img, (self.rect.x, self.rect.y))


# A function that creates random circles, with their own shape, and color that can spawn in particular boundaries
def display_circle():
    global num, score
    position_y = uniform(100, 500)
    position_x = uniform(100, 900)
    hue=(randint(0, 255), randint(0, 255), randint(0, 255))
    pygame.draw.circle(screen, hue, (position_x, position_y), uniform(10, 50))
pygame.init()

# Variables for the screen, like color, and height / width
time=pygame.time.Clock()
FPS=30
color=(155, 155, 255)
thickness=1000
tallness=600
screen = pygame.display.set_mode((1280, 720))

# Variables for the button image and scaling it to fit into the menu properly
img=pygame.image.load("assets/Pause.png")
img=pygame.transform.scale(img, (100, 100))
Savetext = get_font(45).render("This is the HIGHSCORE screen:", True, "White")

Saverect = Savetext.get_rect(center=(640, 260))


B=Pause(585, 100)
run=True


# the logic for quiting the PauseScreen
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

# Using the previous displayed variables to manipulate the game screen.
    screen.fill(color)
    B.response()
    Savetext1 = get_font(65).render(str(num), True, "White")
    Saverect1 = Savetext1.get_rect(center=(640, 360))
    screen.blit(Savetext, Saverect)
    screen.blit(Savetext1, Saverect1)
    pygame.display.flip()
    time.tick(FPS)
pygame.quit()