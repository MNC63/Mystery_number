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

# Clock
clock = pygame.time.Clock()

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
        self.check_btn = Button("Play Again", 200, 320,
                                200, 40, FONT, base_color=BLUE)
        self.playagain_btn = Button(
            "Play Again", 200, 320, 200, 40, FONT, base_color=BLUE)

        # Menu Buttons
        self.menu_buttons = []
        start_y = 180
        for i, diff in enumerate(DIFFICULTY.keys()):
            btn = Button(diff, 200, start_y + i * 60, 200, 48, FONT)
            self.menu_buttons.append((diff, btn))

        # Game State Variables
        self.target = None
        self.attempts = 0
        self.max_attempts = 7
        self.max_range = 100
        self.message = "Choose difficulty and start"
        self.best_score = None

    def start_game(self, diff_name):
        cfg = DIFFICULTY[diff_name]
        self.difficulty = diff_name
        self.max_range = cfg["range"]
        self.max_attempts = cfg["attempts"]
        self.target = random.randint(1, self.max_range)
        self.attempts = 0
        self.message = f"Guess a number between 1 and {self.max_range}"
        self.input_box.text = ''
        self.input_box.txt_surface = FONT.render('', True, BLACK)
        self.state = "playing"

    def check_guess(self, guess_str):
        if not guess_str:
            self.message = "⚠️ Enter a number"
            return
        try:
            g = int(guess_str)
        except ValueError:
            self.message = "⚠️ Invalid number!"
            return

        if g < 1 or g > self.max_range:
            self.message = f"⚠️ Number must be 1 - {self.max_range}"
            return

        self.attempts += 1

        if g == self.target:
            self.message = f"Correct! You won in {self.attempts} attempts!"
            self.state = "end"
            if self.best_score is None or self.attempts < self.best_score:
                self.best_score = self.attempts

        elif g < self.target:
            self.message = "Higher"
        else:
            self.message = "Lower"
        if self.attempts > self.max_attempts and self.state != "end":
            self.message = f"Out of attempts! The number was {self.target}"
            self.state = "end"

    def handle_event(self, event):
        if self.state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for diff_name, btn in self.menu_buttons:
                    if btn.is_clicked(event.pos):
                        self.start_game(diff_name)
        elif self.state == "playing":
            submitted = self.input_box.handle_event(event)
            if submitted is not None:
                self.check_guess(submitted)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.check_btn.is_clicked(event.pos):
                    self.check_guess(self.input_box.text)
        elif self.state == "end":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.playagain_btn.is_clicked(event.pos):
                    self.state = "menu"

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill(WHITE)
        if self.state == "menu":
            title = BIG_FONT.render("Mystery Number", True, BLACK)
            self.screen.blit(title, ((WIDTH - title.get_width()) // 2, 80))
            subtitle = FONT.render("Choose difficulty:", True, BLACK)
            self.screen.blit(subtitle, (220, 140))
            for _, btn in self.menu_buttons:
                btn.draw(self.screen)
        elif self.state == "playing":
            header = FONT.render(
                f"Difficulty: {self.difficulty} Attempts: {self.attempts}/{self.max_attempts}", True, BLACK)
            self.screen.blit(header, (20, 30))
            self.input_box.draw(self.screen)
            self.check_btn.draw(self.screen)

            # Message
            msg_color = RED if "⚠️" in self.message or "Out of" in self.message else BLACK
            msg = FONT.render(self.message, True, msg_color)
            self.screen.blit(msg, (50, 200))
        elif self.state == "end":
            end_msg = BIG_FONT.render(self.message, True, BLACK)
            self.screen.blit(
                end_msg, ((WIDTH - end_msg.get_width()) // 2, 180))
            self.playagain_btn.draw(self.screen)
            if self.best_score is not None:
                best = FONT.render(
                    f"Best: {self.best_score} tries", True, BLACK)
                self.screen.blit(best, (20, 20))


# Main Loop
game = MysteryNumberGame(screen)

while True:
    dt = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.handle_event(event)

    # Draw
    game.update(dt)
    game.draw()
    pygame.display.flip()
