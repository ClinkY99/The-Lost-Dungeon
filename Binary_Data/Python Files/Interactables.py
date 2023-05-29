import pygame, Functions


class Button():

# declaring the variable necessary for this class like the font,color, hovering color and position
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, sound = './SFX/menu_button.mp3', disabled = False):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.sound = pygame.mixer.Sound(sound)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.disabled = disabled

# updating the screen so we can keep up with what us currently displayed on the screen
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

# A function used to see if the button on the screen has been clicked.
    def checkForInput(self, position):
        if not self.disabled:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                self.sound.play()
                return True
        return False

# The function used to change the color if you are hovering above it, and it base coloring if you are not.
    def changeColor(self, position):
        if not self.disabled:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                self.text = self.font.render(self.text_input, True, self.hovering_color)

            else:
                self.text = self.font.render(self.text_input, True, self.base_color)
    def ForceColor(self, color):
        self.text = self.font.render(self.text_input, True, color)

class ImageButton():
    def __init__(self, image, pos, Hoverimage, stayclicked = False, Sound = './SFX/button.mp3'):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.regularimage = image
        self.Hoverimage = Hoverimage
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.stayclicked = stayclicked
        self.clicked = False
        self.Sound = pygame.mixer.Sound(Sound)

    # updating the screen so we can keep up with what us currently displayed on the screen
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)

    # A function used to see if the button on the screen has been clicked.
    def checkForInput(self, position):
        if not self.stayclicked:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom):
                self.Sound.play()
                return True
            return False
        else:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom) and self.clicked:
                self.image = self.regularimage
                self.clicked = False
                self.Sound.play()
                return 0
            elif position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom):
                self.image = self.Hoverimage
                self.clicked = True
                self.Sound.play()
                return 1
            return None
    # The function used to change the color if you are hovering above it, and it base coloring if you are not.
    def changeColor(self, position):
        if not self.stayclicked:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom):
                self.image = self.Hoverimage
            else:
                self.image = self.regularimage


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font, outline, backcolor = None, highlightcolor = None):
        super().__init__()
        self.color = outline
        self.backcolor = backcolor
        self.highlightcolor = highlightcolor
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
        if self.highlightcolor and self.active:
            self.image.fill(self.highlightcolor)
        elif self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(center = self.pos)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pass
                else:
                    self.text += event.unicode
        self.render_text()
