import pygame
import sys
from pygame.math import Vector2
import random

class SNAKE:
    
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up = pygame.image.load('snakeimages/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('snakeimages/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('snakeimages/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('snakeimages/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('snakeimages/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('snakeimages/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('snakeimages/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('snakeimages/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('snakeimages/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('snakeimages/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('snakeimages/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('snakeimages/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('snakeimages/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('snakeimages/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('crunch.wav')


    def draw_snake(self):

        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                    next_block = self.body[index - 1] - block
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)


                # pygame.draw.rect(screen,(150,100,100), block_rect)
    
    def update_head_graphics(self):
        head_pos = self.body[1] - self.body[0]
        if head_pos == Vector2(1,0):self.head = self.head_left
        elif head_pos == Vector2(-1,0):self.head = self.head_right
        elif head_pos == Vector2(0,1):self.head = self.head_up
        elif head_pos == Vector2(0,-1):self.head = self.head_down
    
    def update_tail_graphics(self):
        tail_pos = self.body[-2] - self.body[-1]
        if tail_pos == Vector2(1,0):self.tail = self.tail_left
        elif tail_pos == Vector2(-1,0):self.tail = self.tail_right
        elif tail_pos == Vector2(0,1):self.tail = self.tail_up
        elif tail_pos == Vector2(0,-1):self.tail = self.tail_down
    

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False

        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True
    
    def play_crunch_sound(self):
        self.crunch_sound.play()

class FRUIT:
    def __init__(self, fruit_type='apple'):
        self.fruit_type = fruit_type
        self.randomize()
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        if self.fruit_type == 'apple':
            screen.blit(apple, fruit_rect)
        elif self.fruit_type == 'mango':
            screen.blit(mango, fruit_rect)
    
    def randomize(self):
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        
        self.snake = SNAKE()
        self.fruit = FRUIT('apple')
        self.mango = None
        self.highest_score = 0
        self.mango_appeared_time = None
        self.score = 0
        self.game_over_sound = pygame.mixer.Sound('game_over.wav')
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fails()
        self.handle_mango()
    
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        if self.mango:
            self.mango.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
    
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.score += 1
            self.snake.play_crunch_sound()
        
        if self.mango and self.mango.pos == self.snake.body[0]:
            self.snake.add_block()
            self.mango = None
            self.mango_appeared_time = pygame.time.get_ticks()
            self.score += 5
            self.snake.play_crunch_sound()
        
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    
    def handle_mango(self):
        current_time = pygame.time.get_ticks()
        
        if not self.mango:
            if current_time - (self.mango_appeared_time or 0) >= 10000:
                self.mango = FRUIT('mango')
                self.mango_appeared_time = current_time
        else:
            if current_time - self.mango_appeared_time >= 5000:
                self.mango = None
                self.mango_appeared_time = current_time
            if self.mango and current_time - self.mango_appeared_time >= 10000:
                self.mango = FRUIT('mango')
                self.mango_appeared_time = current_time

    
    def check_fails(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def game_over(self):
        score = self.score
        if score > self.highest_score:
            self.highest_score = score
        self.game_over_sound.play()
        self.show_game_over_screen(score)
    
    def draw_grass(self):
        grass_color = (78,210,70)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color,  grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color,  grass_rect)

    def draw_score(self):
        
        high_score_text = "High Score: " + str(self.highest_score)
        high_score_surface = game_font.render(high_score_text, True, (56, 74, 12))
        high_score_x = int(cell_size * cell_number - 90)
        high_score_y = int(cell_size * cell_number - 80)
        high_score_rect = high_score_surface.get_rect(center=(high_score_x, high_score_y))
        screen.blit(high_score_surface, high_score_rect)

        
        score_text = "Score: " + str(self.score)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)
    
    def show_game_over_screen(self, score):
        screen.fill((75, 215, 70))
        
        self.draw_grass()
        
        game_over_font = pygame.font.Font(None, 75)
        small_font = pygame.font.Font(None, 35)

        game_over_surface = game_over_font.render('GAME OVER', True, (255, 0, 0))
        score_surface = small_font.render(f'Your Score: {score}', True, (255, 255, 255))
        high_score_surface = small_font.render(f'Highest Score: {self.highest_score}', True, (255, 255, 255))
        restart_surface = small_font.render('Press R to Replay or Q to Quit', True, (255, 255, 255))

        game_over_rect = game_over_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2 - 50))
        score_rect = score_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
        high_score_rect = high_score_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2 + 40))
        restart_rect = restart_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2 + 80))

        screen.blit(game_over_surface, game_over_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(high_score_surface, high_score_rect)
        screen.blit(restart_surface, restart_rect)
        pygame.display.flip()

        self.wait_for_input()


    def wait_for_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
    
    def reset(self):
        self.game_over_sound.stop()
        self.snake = SNAKE()
        self.fruit = FRUIT('apple')
        self.mango = None
        self.mango_appeared_time = pygame.time.get_ticks()
        self.score = 0
        pygame.time.set_timer(SCREEN_UPDATE, 150)


pygame.mixer.pre_init(44100,-16,2,512)

pygame.init()

pygame.display.set_caption('Snake Game')

cell_size = 40
cell_number = 20

screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('apple.png').convert_alpha()
mango = pygame.image.load('mango_optimized.png').convert_alpha()
game_font = pygame.font.Font('PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            
    screen.fill((75,215,70))
    main_game.draw_elements()
    pygame.display.update() 
    clock.tick(60)