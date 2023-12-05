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
        self.value = value

    def draw(self):

        pygame.draw.rect(self.screen, BLACK, (self.col * SQUARE_SIZE, self.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

        if self.value != 0:
            value_font = pygame.font.Font(None, 35)
            value = value_font.render(str(self.value), True, BLACK)
            value_rect = value.get_rect(center=(self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2))
            self.screen.blit(value, value_rect)


class Board:
    def __init__(self, width, height, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = [[Cell(0, row, col, screen) for col in range(width)] for row in range(height)]

    def draw(self):
        self.screen.fill(BG_COLOR)
        for row in range(self.width):
            for col in range(self.height):
                cell = self.cells[row][col]
                cell.draw()
        pygame.display.update()

    def select(self, row, col):
        return self.cells[row][col]

    def click(self, x, y):
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return self.cells[row][col]

    def clear(self):
        self.value = 0

    def sketch(self, value):
        pass

    def place_number(self, value):
        pass

    def reset_to_original(self):
        pass

    def is_full(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].is_empty():
                    return False
        return True

    def update_board(self):
        pass

    def find_empty(self):
        pass

    def check_board(self):
        pass


def draw_game_start(screen):
    # Initialize title font
    start_title_font = pygame.font.Font(None, 70)
    start_subtitle_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 25)
    board = None

    # Define button colors
    difficulties = ["Easy", "Medium", "Hard"]

    # Define title text
    title_text = start_title_font.render("Welcome to Sudoku", True, BLACK)
    title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

    # Define subtitle text
    subtitle_text = start_subtitle_font.render("Select Game Mode:", True, BLACK)
    subtitle_text_rect = subtitle_text.get_rect(
        center=(WIDTH // 2, title_text_rect.bottom + 60))

    while True:
        screen.fill(BG_COLOR)
        # Display title and subtitle text
        screen.blit(title_text, title_text_rect)
        screen.blit(subtitle_text, subtitle_text_rect)

        button_width = 150
        total_width = 3 * button_width
        start_position = (WIDTH - total_width - 20) // 2

        for i, difficulty in enumerate(difficulties):
            button_position = start_position + i * (button_width + 20)  # Displaying buttons side by side
            difficulty_button = pygame.Rect(button_position, HEIGHT // 2 + 50, button_width, 50)
            pygame.draw.rect(screen, (193, 205, 205), difficulty_button)

            text = button_font.render(difficulty, True, (0, 0, 0))
            text_rect = text.get_rect(center=difficulty_button.center)
            screen.blit(text, text_rect)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // SQUARE_SIZE
                if col == 0:
                    difficulty = 'Easy'
                elif col == 1:
                    difficulty = 'Medium'
                elif col == 2:
                    difficulty = 'Hard'
                board = Board(WIDTH, HEIGHT, difficulty)
        if board:
            board.draw()
        pygame.display.update()


def game_in_progress(screen):
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
                    if restart_button.collidepoint(mouse_pos):
                        draw_game_start(screen)
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

    draw_game_start(screen)

    # Color background
    screen.fill(BG_COLOR)

    while True:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                if col == 0:
                    difficulty = 'Easy'
                elif col == 1:
                    difficulty = 'Medium'
                elif col == 2:
                    difficulty = 'Hard'
                board = Board(WIDTH, HEIGHT, difficulty)
                board.draw()
        pygame.display.update()

