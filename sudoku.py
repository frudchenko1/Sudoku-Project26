import pygame, sys
from constants import *
from sudoku_generator import *


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        pass

    def draw(self):
        pass


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty

    def draw(self):
        pass

    def select(self, row, col):
        pass

    def click(self, x, y):
        pass

    def clear(self):
        pass

    def sketch(self, value):
        pass

    def place_number(self, value):
        pass

    def reset_to_original(self):
        pass

    def is_full(self):
        pass

    def update_board(self):
        pass

    def find_empty(self):
        pass

    def check_board(self):
        pass


def draw_game_start(screen):
    #Initialize title font
    start_title_font = pygame.font.Font(None, 70)
    start_subtitle_font = pygame.font.Font(None, 50)  # Larger subtitle font
    button_font = pygame.font.Font(None, 25)  # Smaller button font

    # Difficulty options variable for referencing via index 
    difficulties = ["Easy", "Medium", "Hard"]

    # Define title and subtitle text
    title_text = start_title_font.render("Welcome to Sudoku", True, BLACK)
    title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

    subtitle_text = start_subtitle_font.render("Select Game Mode:", True, BLACK)
    subtitle_text_rect = subtitle_text.get_rect(
        center=(WIDTH // 2, title_text_rect.bottom + 60)) 
    pass

def draw_game_over(screen):
    while game_over == True:
        game_over_font = pygame.font.Font(None, 90)

        screen.fill(BG_COLOR)
        if winner != 0:
            text = "Game Won!"

            exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
            pygame.draw.rect(screen, (193, 205, 205), exit_button)
            exit_button_font = pygame.font.Font(None, 36)
            exit_button_text = exit_button_font.render("Exit", True, BLACK)
            exit_button_text_rect = exit_button_text.get_rect(center=exit_button.center)
            screen.blit(exit_button_text, exit_button_text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
        else:
            text = "Game Over"

            restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
            pygame.draw.rect(screen, (193, 205, 205), restart_button)
            restart_button_font = pygame.font.Font(None, 36)
            restart_button_text = restart_button_font.render("Restart", True, BLACK)
            restart_button_text_rect = restart_button_text.get_rect(center=restart_button.center)
            screen.blit(restart_button_text, restart_button_text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

        game_over_surf = game_over_font.render(text, 0, BLACK)
        game_over_rect = game_over_surf.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 100))

        # Display title and subtitle text
        screen.blit(game_over_surf, game_over_rect)

        pygame.display.update()


if __name__ == "__main__":
    game_over = False
    winner = 0
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")

    draw_game-start(screen)

    # Color background
    screen.fill(BG_COLOR)
    
    while True:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


