import pygame
import random
import sys

pygame.init()


# Config
WIDTH, HEIGHT = 600, 600
FONT = pygame.font.SysFont("Arial", 32)
BIG_FONT = pygame.font.SysFont("Arial", 40)


# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 150, 255)
RED = (255, 70, 70)
GREEN = (50, 200, 50)

# Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mystery Number Game")


# UI Class

class InputBox:
    def __init__(self, x, y, w, h, font, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = text
        self.txt_surface = self.font.render(text, True, BLACK)
        self.active = False
        self.color_inactive = GRAY
        self.color_active = BLUE
        self.color = self.color_inactive

    def handle_event(self, event):
        # return a submitted string when Enter pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                submitted = self.text
                self.text = ''
                self.txt_surface = self.font.render(self.text, True, BLACK)
                return submitted
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # Accept only digits
                if event.unicode.isdigit():
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, BLACK)
        return None

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, 2)  # Draw Rect
        surf.blit(self.txt_surface, (self.rect.x + 6, self.rect.y +
                  (self.rect.h - self.txt_surface.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Button:
    def __init__(self, text, x, y, w, h, font, base_color=GRAY, hover_color=BLUE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color

    def draw(self, surf):
        mouse = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(
            mouse) else self.base_color
        pygame.draw.rect(surf, color, self.rect)
        txt = self.font.render(self.text, True, BLACK)
        surf.blit(
            txt,
            (
                self.rect.x + (self.rect.w - txt.get_width()) // 2,
                self.rect.y + (self.rect.h - txt.get_height()) // 2
            )
        )

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Difficulty table
DIFFICULTY = {
    "Easy": {"range": 50, "attempts": 10},
    "Normal": {"range": 100, "attempts": 7},
    "Hard": {"range": 500, "attempts": 5}
}


class MysteryNumberGame:
    def __init__(self, screen):
        self.screen = screen
        self.state = "menu"
        self.difficulty = "Normal"
        self.input_box = InputBox(200, 260, 200, 40, FONT)


# Main Loop
clock = pygame.time.Clock()
input_box = InputBox(200, 250, 200, 50, FONT)
button = Button("PLAY", 220, 400, 160, 60, FONT)
# game = MysteryNumberGame()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.is_clicked(event.pos):
                print("Button clicked!")

        # Event InputBox
        submitted = input_box.handle_event(event)
        if submitted is not None:
            print("You Entered: ", submitted)

        # Draw
        screen.fill(BLACK)
        input_box.draw(screen)
        button.draw(screen)

    pygame.display.flip()
    clock.tick(30)
