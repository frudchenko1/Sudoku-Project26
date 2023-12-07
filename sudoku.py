import pygame, sys
from constants import *
from sudoku_generator import *


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.highlighted = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.value = value

    def set_selected(self, selected):
        self.selected = selected

    def highlight(self):
        self.highlighted = True

    def input_number(self, number):
        if 1 <= number <= 9:  # Ensure input is within the range of a Sudoku cell
            self.value = number

    def clear_highlight(self):
        self.highlighted = False

    def draw(self):
        cell_width = WIDTH // (BOARD_COLS * BOARD_ROWS)
        cell_height = 600 // (BOARD_COLS * BOARD_ROWS)

        x_dimension = self.col * cell_width
        y_dimension = self.row * cell_height

        # Inner lines within 3 x 3
        pygame.draw.rect(self.screen, BLACK, (x_dimension, y_dimension, cell_width, cell_height), 1)

        # Border lines outlining the 3 x 3
        if self.row % 3 == 0:
            pygame.draw.line(self.screen, AZURE4, (x_dimension, y_dimension),
                             (x_dimension + WIDTH // BOARD_ROWS, y_dimension), LINE_WIDTH)
        if self.col % 3 == 0:
            pygame.draw.line(self.screen, AZURE4, (x_dimension, y_dimension),
                             (x_dimension, y_dimension + HEIGHT // BOARD_COLS), LINE_WIDTH)

        # Ensure that the select is within 600 x 600
        while 0 <= x_dimension < 550 and 0 <= y_dimension < 550:
            if self.selected:
                pygame.draw.rect(self.screen, RED, (x_dimension, y_dimension, cell_width, cell_height),
                                 LINE_WIDTH // BOARD_COLS // BOARD_COLS)

            if self.highlighted:
                pygame.draw.rect(self.screen, RED, (x_dimension, y_dimension, cell_width, cell_height), 3)

            break  # Break out of the loop after drawing if conditions are met

        if self.value != 0:
            value_font = pygame.font.Font(None, 60)
            text = value_font.render(str(self.value), True, BLACK)
            text_rect = text.get_rect(center=(x_dimension + cell_width // 2, y_dimension + cell_height // 2))
            self.screen.blit(text, text_rect)


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = [[Cell(0, row, col, screen) for col in range(width)] for row in range(height)]
        self.selected = None
        self.screen = screen
        self.selected_cell = None

    def draw(self):
        self.screen.fill(BG_COLOR)
        sudoku_board = generate_sudoku(9, self.difficulty)

        for row in range(self.width):
            for col in range(self.height):
                cell = self.cells[row][col]
                cell.draw()
        pygame.draw.rect(screen, BG_COLOR, (0, 600, WIDTH, 100))
        button_font = pygame.font.Font(None, 25)
        menu_buttons = ["Reset", "Restart", "Exit"]
        clicked_cell = self.cells[row][col]
        button_width = 150
        total_width = 3 * button_width
        start_position = (WIDTH - total_width - 20) // 2 - 10
        pygame.draw.rect(screen, BG_COLOR, (0, 600, WIDTH, 100))
        button_font = pygame.font.Font(None, 25)
        menu_buttons = ["Reset", "Restart", "Exit"]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Check if any menu button is clicked
                for i, button_text in enumerate(menu_buttons):
                    button_position = start_position + i * (button_width + 20)
                    button_rect = pygame.Rect(button_position, HEIGHT - 80, button_width, 50)


            # Draw menu buttons
            for i, button_text in enumerate(menu_buttons):
                button_position = start_position + i * (button_width + 20)
                button_rect = pygame.Rect(button_position, HEIGHT - 80, button_width, 50)
                pygame.draw.rect(screen, (193, 205, 205), button_rect)

                text = button_font.render(button_text, True, BLACK)
                text_rect = text.get_rect(center=button_rect.center)
                screen.blit(text, text_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row = y // (600 // (BOARD_COLS * BOARD_ROWS))
                    col = x // (WIDTH // (BOARD_COLS * BOARD_ROWS))
                    if self.selected_cell:
                        self.selected_cell.clear_highlight()
                    self.selected_cell = self.cells[row][col]
                    self.selected_cell.highlight()
                    self.draw()
                    if button_rect.collidepoint(x, y):
                        if button_text == "Restart":
                            draw_game_start(screen)
                        elif button_text == "Exit":
                            pygame.quit()
                            sys.exit()

                elif event.type == pygame.KEYDOWN:
                    x, y = pygame.mouse.get_pos()
                    row = y // (600 // (BOARD_COLS * BOARD_ROWS))
                    col = x // (WIDTH // (BOARD_COLS * BOARD_ROWS))
                    clicked_cell = self.cells[row][col]
                    if event.key == pygame.K_1:
                        clicked_cell.input_number(1)
                    elif event.key == pygame.K_2:
                        clicked_cell.input_number(2)
                    elif event.key == pygame.K_3:
                        clicked_cell.input_number(3)
                    elif event.key == pygame.K_4:
                        clicked_cell.input_number(4)
                    elif event.key == pygame.K_5:
                        clicked_cell.input_number(5)
                    elif event.key == pygame.K_6:
                        clicked_cell.input_number(6)
                    elif event.key == pygame.K_7:
                        clicked_cell.input_number(7)
                    elif event.key == pygame.K_8:
                        clicked_cell.input_number(8)
                    elif event.key == pygame.K_9:
                        clicked_cell.input_number(9)
                clicked_cell.draw()



                # Update display
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
        self.value = value

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

    difficulties = ["Easy", "Medium", "Hard"]

    # title text
    title_text = start_title_font.render("Welcome to Sudoku", True, BLACK)
    title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

    # Subtitle text
    subtitle_text = start_subtitle_font.render("Select Game Mode:", True, BLACK)
    subtitle_text_rect = subtitle_text.get_rect(
        center=(WIDTH // 2, title_text_rect.bottom + 70))

    while True:
        screen.fill(BG_COLOR)
        screen.blit(title_text, title_text_rect)
        screen.blit(subtitle_text, subtitle_text_rect)

        button_width = 150
        total_width = 3 * button_width
        start_position = (WIDTH - total_width - 20) // 2 - 10

        for i, difficulty in enumerate(difficulties):
            button_position = start_position + i * (button_width + 20)
            difficulty_button = pygame.Rect(button_position, HEIGHT // 2, button_width, 50)
            pygame.draw.rect(screen, (193, 205, 205), difficulty_button)

            text = button_font.render(difficulty, True, (0, 0, 0))
            text_rect = text.get_rect(center=difficulty_button.center)
            screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // SQUARE_SIZE
                if col == 0:
                    removed_cells = 30
                elif col == 1:
                    removed_cells = 40
                elif col == 2:
                    removed_cells = 50

                sudoku_board = generate_sudoku(9, removed_cells)
                board = Board(WIDTH, HEIGHT - 100, screen, removed_cells)

                for i in range(len(sudoku_board)):
                    for j in range(len(sudoku_board[i])):
                        cell_value = int(sudoku_board[i][j])
                        board.cells[i][j].set_cell_value(cell_value)
                board.draw()

        pygame.display.update()


def game_in_progress(screen, difficulty):
    board = Board(WIDTH, HEIGHT, difficulty)
    board.draw()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


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

        screen.blit(game_over_surf, game_over_rect)
        pygame.display.update()


if __name__ == "__main__":
    game_over = False
    winner = 0

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")

    draw_game_start(screen)

    screen.fill(BG_COLOR)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                if col == 0:
                    difficulty = 30
                elif col == 1:
                    difficulty = 40
                elif col == 2:
                    difficulty = 50
                game_in_progress(screen, difficulty)
        pygame.display.update()
