import pygame
from pygame.locals import *

pygame.init()

screen_height = 300
screen_width = 300
line_width = 6
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tic Tac Toe')


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
background_color = (186, 198, 224)  # bac6e0
border_color = (0, 0, 0)


font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 80)

# Game variables
clicked = False
player_turn = 1
pos = (0, 0)
markers = []
game_over = False
winner = 0
player_1_marker = None
player_2_marker = None

# "Play Again" Option
again_rect = pygame.Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)
quit_rect = pygame.Rect(screen_width // 2 - 80, screen_height // 2 + 60, 160, 50)

# Empty 3 x 3 list for grid
for x in range(3):
    row = [0] * 3
    markers.append(row)

def draw_board():
    bg = background_color
    grid = (50, 0, 50)
    screen.fill(bg)
    for x in range(1, 3):
        pygame.draw.line(screen, grid, (0, 100 * x), (screen_width, 100 * x), line_width)
        pygame.draw.line(screen, grid, (100 * x, 0), (100 * x, screen_height), line_width)

def draw_markers():
    x_pos = 0
    for x in markers:
        y_pos = 0
        for y in x:
            if y == player_1_marker:
                if player_1_marker == 1:
                    pygame.draw.line(screen, red, (x_pos * 100 + 15, y_pos * 100 + 15), (x_pos * 100 + 85, y_pos * 100 + 85), line_width)
                    pygame.draw.line(screen, red, (x_pos * 100 + 85, y_pos * 100 + 15), (x_pos * 100 + 15, y_pos * 100 + 85), line_width)
                else:
                    pygame.draw.circle(screen, green, (x_pos * 100 + 50, y_pos * 100 + 50), 38, line_width)
            elif y == player_2_marker:
                if player_2_marker == 1:
                    pygame.draw.line(screen, red, (x_pos * 100 + 15, y_pos * 100 + 15), (x_pos * 100 + 85, y_pos * 100 + 85), line_width)
                    pygame.draw.line(screen, red, (x_pos * 100 + 85, y_pos * 100 + 15), (x_pos * 100 + 15, y_pos * 100 + 85), line_width)
                else:
                    pygame.draw.circle(screen, green, (x_pos * 100 + 50, y_pos * 100 + 50), 38, line_width)
            y_pos += 1
        x_pos += 1

def check_game_over():
    global game_over
    global winner

    x_pos = 0
    for x in markers:
        # Check columns
        if sum(x) == 3 * player_1_marker:
            winner = 1
            game_over = True
        elif sum(x) == 3 * player_2_marker:
            winner = 2
            game_over = True
        # Check rows
        if markers[0][x_pos] + markers[1][x_pos] + markers[2][x_pos] == 3 * player_1_marker:
            winner = 1
            game_over = True
        elif markers[0][x_pos] + markers[1][x_pos] + markers[2][x_pos] == 3 * player_2_marker:
            winner = 2
            game_over = True
        x_pos += 1

    # Check cross
    if markers[0][0] + markers[1][1] + markers[2][2] == 3 * player_1_marker or markers[2][0] + markers[1][1] + markers[0][2] == 3 * player_1_marker:
        winner = 1
        game_over = True
    elif markers[0][0] + markers[1][1] + markers[2][2] == 3 * player_2_marker or markers[2][0] + markers[1][1] + markers[0][2] == 3 * player_2_marker:
        winner = 2
        game_over = True

    # Check for tie
    if not game_over:
        tie = True
        for row in markers:
            for i in row:
                if i == 0:
                    tie = False
        # If it is a tie, then call game over and set winner to 0 (no one)
        if tie:
            game_over = True
            winner = 0

def draw_game_over(winner):
    if winner != 0:
        end_text = "Player " + str(winner) + " wins!"
    else:
        end_text = "You have tied!"

    
    end_box_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 60, 200, 50)
    pygame.draw.rect(screen, background_color, end_box_rect)
    pygame.draw.rect(screen, border_color, end_box_rect, 2)

    end_img = font.render(end_text, True, blue)
    end_img_rect = end_img.get_rect(center=end_box_rect.center)
    screen.blit(end_img, end_img_rect)

    
    pygame.draw.rect(screen, background_color, again_rect)
    pygame.draw.rect(screen, border_color, again_rect, 2)

    again_text = 'Play Again?'
    again_img = font.render(again_text, True, blue)
    again_img_rect = again_img.get_rect(center=again_rect.center)
    screen.blit(again_img, again_img_rect)

    
    pygame.draw.rect(screen, background_color, quit_rect)
    pygame.draw.rect(screen, border_color, quit_rect, 2)

    quit_text = 'Quit'
    quit_img = font.render(quit_text, True, blue)
    quit_img_rect = quit_img.get_rect(center=quit_rect.center)
    screen.blit(quit_img, quit_img_rect)

def player_choice():
    global player_1_marker, player_2_marker
    choosing = True
    while choosing:
        screen.fill(background_color)
        choice_text = "Player 1, choose X or O"
        choice_img = font.render(choice_text, True, blue)
        screen.blit(choice_img, (screen_width // 2 - 120, screen_height // 2 - 100))

        x_text = "X"
        o_text = "O"
        x_img = large_font.render(x_text, True, red)
        o_img = large_font.render(o_text, True, green)

        x_rect = pygame.Rect(screen_width // 2 - 80, screen_height // 2 - 20, 50, 50)
        o_rect = pygame.Rect(screen_width // 2 + 30, screen_height // 2 - 20, 50, 50)

        pygame.draw.rect(screen, background_color, x_rect)
        pygame.draw.rect(screen, background_color, o_rect)

        screen.blit(x_img, (screen_width // 2 - 75, screen_height // 2 - 35))
        screen.blit(o_img, (screen_width // 2 + 35, screen_height // 2 - 35))

        
        pygame.draw.rect(screen, background_color, quit_rect)
        pygame.draw.rect(screen, border_color, quit_rect, 2)

        quit_text = 'Quit'
        quit_img = font.render(quit_text, True, blue)
        quit_img_rect = quit_img.get_rect(center=quit_rect.center)
        screen.blit(quit_img, quit_img_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if x_rect.collidepoint(pos):
                    player_1_marker = 1  # X for Player 1
                    player_2_marker = -1  # O for Player 2
                    choosing = False
                elif o_rect.collidepoint(pos):
                    player_1_marker = -1  # O for Player 1
                    player_2_marker = 1  # X for Player 2
                    choosing = False
                elif quit_rect.collidepoint(pos):
                    pygame.quit()
                    exit()

# Main loop
run = True
first_run = True
while run:
    if first_run:
        player_choice()
        first_run = False

    draw_board()
    draw_markers()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Run new game
        if not game_over:
            # Check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and not clicked:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked:
                clicked = False
                pos = pygame.mouse.get_pos()
                cell_x = pos[0] // 100
                cell_y = pos[1] // 100
                if markers[cell_x][cell_y] == 0:
                    if player_turn == 1:
                        markers[cell_x][cell_y] = player_1_marker
                        player_turn = 2
                    else:
                        markers[cell_x][cell_y] = player_2_marker
                        player_turn = 1
                    check_game_over()

    # Check if game has been won
    if game_over:
        draw_game_over(winner)
        # Check mouse click for "Play Again" or "Quit"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not clicked:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked:
                clicked = False
                pos = pygame.mouse.get_pos()
                if again_rect.collidepoint(pos):
                    game_over = False
                    player_turn = 1
                    pos = (0, 0)
                    markers = []
                    winner = 0
                    for x in range(3):
                        row = [0] * 3
                        markers.append(row)
                    player_choice()
                elif quit_rect.collidepoint(pos):
                    pygame.quit()
                    exit()

    pygame.display.update()

pygame.quit()
