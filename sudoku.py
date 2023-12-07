import pygame, sys
from sudoku_generator import *
from constants1 import *

pygame.init()
pygame.display.set_caption("Sudoku")
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Cell:
    def __init__(self, value, row, col, color, pygame, screen, editable):
        self.value = value
        self.row = row
        self.col = col
        self.color = color
        self.pygame = pygame
        self.screen = screen
        self.sketched_value = 0
        self.editable = editable

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.value = value

    def draw(self):
        top_left = (self.row * 67, self.col * 67)
        top_right = ((self.row + 1) * 67, self.col * 67)
        bottom_left = (self.row * 67, (self.col + 1) * 67)
        bottom_right = ((self.row + 1) * 67, (self.col + 1) * 67)

        # Left
        self.pygame.draw.line(self.screen, self.color, top_left, top_right, 2)
        self.pygame.draw.line(self.screen, self.color, top_right, bottom_right, 2)
        self.pygame.draw.line(self.screen, self.color, bottom_right, bottom_left, 2)
        self.pygame.draw.line(self.screen, self.color, bottom_left, top_left, 2)

        # Value
        if not self.editable:
            font = self.pygame.font.SysFont(None, 45)
            text = font.render(str(self.value), True, BLACK, BG_COLOR)
            text_rec = text.get_rect(center=(self.row * 67 + 33, self.col * 67 + 33))

            self.screen.blit(text, text_rec)

        # Sketched value
        if self.editable:
            if self.value != 0:
                color = (48, 48, 48)
            else:
                color = BG_COLOR
            font = self.pygame.font.SysFont("font", 20)
            text = font.render(str(self.value), True, color, BG_COLOR)
            text_rec = text.get_rect()
            text_rec.center = (self.row * 67 + 10, self.col * 67 + 15)

            self.screen.blit(text, text_rec)


def draw_startup():
    start_title_font = pygame.font.SysFont(None, 70)
    start_subtitle_font = pygame.font.SysFont(None, 50)
    button_font = pygame.font.SysFont(None, 25)
    difficulties = ["Easy", "Medium", "Hard"]

    screen.fill(BG_COLOR)

    # Welcome text
    title_text = start_title_font.render("Welcome to Sudoku", True, BLACK)
    title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_text_rect)

    # Subtitle text
    subtitle_text = start_subtitle_font.render("Select Game Mode:", True, BLACK)
    subtitle_text_rect = subtitle_text.get_rect(
        center=(WIDTH // 2, title_text_rect.bottom + 70))

    screen.blit(subtitle_text, subtitle_text_rect)

    # Difficulty buttons
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


def startup_loop():
    draw_startup()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                print(mouse[0], mouse[1])

                # If Easy difficulty is selected
                if 55 <= mouse[0] <= 205 and 350 <= mouse[1] <= 400:
                    game_mode = 0
                    return game_mode
                # If medium difficulty is selected
                elif 225 <= mouse[0] <= 375 and 350 <= mouse[1] <= 400:
                    game_mode = 1
                    return game_mode
                # If hard difficulty is selected
                elif 400 <= mouse[0] <= 545 and 350 <= mouse[1] <= 400:
                    game_mode = 2
                    return game_mode

        pygame.display.update()


def draw_grid(cells):
    screen.fill(BG_COLOR)

    # Draw cells
    for cell in cells:
        cell.draw()

    # Draw lines

    # draw horizontal
    for i in range(0, 10):
        if i % 3 == 0:
            width = 12
        else:
            width = LINE_WIDTH
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), width)

    # draw vertical
    for j in range(1, 10):
        if j % 3 == 0:
            width = 12
        else:
            width = LINE_WIDTH
        pygame.draw.line(screen, LINE_COLOR, (j * CELL_SIZE, 0), (j * CELL_SIZE, HEIGHT), width)

    pygame.draw.rect(screen, BG_COLOR, (0, HEIGHT - 94, WIDTH, 100), WIDTH)

    # Draw bottom buttons
    button_width = 150
    total_width = 3 * button_width
    start_position = (WIDTH - total_width - 20) // 2 - 10
    button_font = pygame.font.Font(None, 25)
    menu_buttons = ["Reset", "Restart", "Exit"]
    for i, button_text in enumerate(menu_buttons):
        button_position = start_position + i * (button_width + 20)
        button_rect = pygame.Rect(button_position, HEIGHT - 80, button_width, 50)
        pygame.draw.rect(screen, (193, 205, 205), button_rect)

        text = button_font.render(button_text, True, BLACK)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)


def game_loop(sudoku, board, deleted, win_state):
    cells = []
    user_text = ""
    current_cell = None

    # Create cells
    for y, row in enumerate(board):
        for x, value in enumerate(row):
            if value == 0:
                current = Cell(value, x, y, LINE_COLOR, pygame, screen, True)  # Make user-input cells editable
            else:
                current = Cell(value, x, y, LINE_COLOR, pygame, screen, False)  # Mark generated cells as non-editable
            cells.append(current)

    draw_grid(cells)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                x, y = event.pos
                print(x, y)

                # Find which cell was clicked
                if mouse[1] <= 603:
                    x = mouse[0] // 67
                    y = mouse[1] // 67
                    current_cell = cells[9 * y + x]
                    if current_cell.editable:  # Check again for editability

                        current_cell = cells[9 * y + x]
                        if current_cell.value == 0:
                            # Set all other cells' color to LINE_COLOR
                            for cell in cells:
                                cell.color = LINE_COLOR
                                cell.draw()
                            current_cell.color = RED
                            current_cell.draw()

                # Reset button clicked
                if 55 <= mouse[0] <= 205 and 620 <= mouse[1] <= 670:
                    for cell in cells:
                        if cell.editable:
                            cell.value = 0
                            cell.draw()

                # Restart button clicked
                if 225 <= mouse[0] <= 375 and 620 <= mouse[1] <= 670:
                    return main()

                # Exit button clicked
                if 395 <= mouse[0] <= 545 and 620 <= mouse[1] <= 670:
                    return

            if event.type == pygame.KEYDOWN:
                # Set the sketched value if a digit is entered, then reset user input
                if event.unicode.isdigit():
                    user_text += event.unicode
                    current_cell.set_sketched_value(int(user_text))
                    current_cell.draw()
                    user_text = ""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if current_cell and current_cell.editable:
                        current_cell.set_sketched_value(0)
                        current_cell.set_cell_value(0)
                        current_cell.editable = False
                        current_cell.cell_value = current_cell.sketched_value
                        current_cell.draw()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_cell and current_cell.editable:
                        # Set the cell's value to the sketched value
                        temp = current_cell.value
                        current_cell.set_sketched_value(0)
                        current_cell.draw()
                        current_cell.editable = False
                        current_cell.sketched_value = temp
                        current_cell.set_cell_value(current_cell.sketched_value)
                        current_cell.draw()
                        current_cell.editable = True
                        current_cell.set_sketched_value(0)
                        current_cell.draw()

                elif event.key == pygame.K_UP:
                    # Move selection upwards
                    if current_cell:
                        current_cell.color = LINE_COLOR
                        current_cell.draw()
                        if current_cell.col > 0:
                            current_cell = cells[9 * (current_cell.col - 1) + current_cell.row]
                            current_cell.color = RED
                            current_cell.draw()

                elif event.key == pygame.K_DOWN:
                    # Move selection downwards
                    if current_cell:
                        current_cell.color = LINE_COLOR
                        current_cell.draw()
                        if current_cell.col < 8:
                            current_cell = cells[9 * (current_cell.col + 1) + current_cell.row]
                            current_cell.color = RED
                            current_cell.draw()

                elif event.key == pygame.K_LEFT:
                    # Move selection to the left
                    if current_cell:
                        current_cell.color = LINE_COLOR
                        current_cell.draw()
                        if current_cell.row > 0:
                            current_cell = cells[9 * current_cell.col + current_cell.row - 1]
                            current_cell.color = RED
                            current_cell.draw()

                elif event.key == pygame.K_RIGHT:
                    # Move selection to the right
                    if current_cell:
                        current_cell.color = LINE_COLOR
                        current_cell.draw()
                        if current_cell.row < 8:
                            current_cell = cells[9 * current_cell.col + current_cell.row + 1]
                            current_cell.color = RED
                            current_cell.draw()
                current_cell.editable = True
        # Check for game win if all spaces filled
        all_filled = True
        current_board = []
        for i in range(len(board)):
            current_board.append([])
            for j in range(len(board[0])):
                current_board[i].append(cells[i * 9 + j].value)
                if cells[i * 9 + j].value == 0:
                    all_filled = False
                    break

        if all_filled:
            if current_board == win_state:
                return win_loop()

            else:
                # Game lost return loss_loop()
                return loss_loop()

        pygame.display.update()


def draw_loss():
    game_over_font = pygame.font.Font(None, 90)

    screen.fill(BG_COLOR)

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
        game_over_surf = game_over_font.render(text, 0, BLACK)
        game_over_rect = game_over_surf.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 100))

        screen.blit(game_over_surf, game_over_rect)
        pygame.display.update()

def loss_loop():
    draw_loss()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                # Restart button clicked
                if 237 <= mouse[0] <= 365 and 425 <= mouse[1] <= 451:
                    return main()

        pygame.display.update()

def draw_win():
    game_over_font = pygame.font.Font(None, 90)
    screen.fill(BG_COLOR)

    text = "Game Over"

    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, (193, 205, 205), restart_button)
    restart_button_font = pygame.font.Font(None, 36)
    restart_button_text = restart_button_font.render("Restart", True, BLACK)
    restart_button_text_rect = restart_button_text.get_rect(center=restart_button.center)
    screen.blit(restart_button_text, restart_button_text_rect)

    game_over_surf = game_over_font.render(text, 0, BLACK)
    game_over_rect = game_over_surf.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 100))

    screen.blit(game_over_surf, game_over_rect)
    pygame.display.update()

def win_loop():
    draw_win()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                # Exit button clicked
                if 268 <= mouse[0] <= 334 and 425 <= mouse[1] <= 451:
                    return

        pygame.display.update()


def print_board(board):
    for i, row in enumerate(board):
        for element in row:
            print(element, "", end="")
        print()

def main():
    game_mode = startup_loop()

    if game_mode == 0:
        deleted = 30
    elif game_mode == 1:
        deleted = 40
    else:
        deleted = 50

    sudoku = SudokuGenerator(9, deleted)
    sudoku.fill_values()
    board = sudoku.get_board()

    win_state = []
    for i, row in enumerate(board):
        win_state.append([])
        for element in row:
            win_state[i].append(element)

    sudoku.remove_cells()
    board = sudoku.get_board()

    print_board(win_state)

    game_loop(sudoku, board, deleted, win_state)



if __name__ == "__main__":
    main()
