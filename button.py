import pygame


class Button():

# declaring the variable necessary for this class like the font,color, hovering color and position
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, sound = './SFX/button.mp3'):
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

# updating the screen so we can keep up with what us currently displayed on the screen
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

# A function used to see if the button on the screen has been clicked.
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.sound.play()
            return True
        return False

# The function used to change the color if you are hovering above it, and it base coloring if you are not.
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)

        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
    def ForceColor(self, color):
        self.text = self.font.render(self.text_input, True, color)

class ImageButton():
    def __init__(self, image, pos, Hoverimage):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.regularimage = image
        self.Hoverimage = Hoverimage
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    # updating the screen so we can keep up with what us currently displayed on the screen
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)

    # A function used to see if the button on the screen has been clicked.
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    # The function used to change the color if you are hovering above it, and it base coloring if you are not.
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.image = self.Hoverimage
        else:
            self.image = self.regularimage
