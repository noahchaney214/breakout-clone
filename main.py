import pygame as pg
from pathlib import Path
from sprites import Ball, Brick, Timer

""" Breakout

    Clear all of the blocks to win!

    Player gets 3 lives, displayed as hearts at the top right of the screen. Slightly advanced collision on the paddle to give variety to the ball direction.
    After each 1/4 of the bricks are destroyed the speed of the ball increases by 0.25 to add difficulty. 

    Author: Noah Chaney
"""

WIDTH = 650
HEIGHT = 700

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('PONG')
pg.display.set_icon(pg.image.load('assets/images/257357-200.png'))
clock = pg.time.Clock()
running = True

# ball variables
ball_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
RADIUS = 10
ball = Ball(RADIUS, ball_pos.x, ball_pos.y)
ball_group = pg.sprite.GroupSingle()
ball_group.add(ball)

# paddle variables
wall_marg = 30
paddle_w = 75
paddle_h = 10
paddl1_pos = pg.Vector2(screen.get_width()/2 - paddle_w/2, screen.get_height() - wall_marg - paddle_h/2)

# Declare Font
path = Path('C:\\').joinpath('Users').joinpath('Noah').joinpath('Desktop').joinpath('Stuff').joinpath('Portfolio Projects') \
    .joinpath('Breakout').joinpath('assets').joinpath('fonts').joinpath('Grand9K Pixel.ttf')
font = pg.font.Font(path, 16)
lg_font = pg.font.Font(path, 30)
huge_font = pg.font.Font(path, 50)

# player 1 score
score, score_text = 0, '0'

# countdown timer
countdown, text = 3, '3'
pg.time.set_timer(pg.USEREVENT, 1000)

# lives variables
lives = 3
life_w = 30
life_h = 32
life_buffer = 10
life_pos_x = screen.get_width() - (life_w + life_buffer)*3 - 15
life_pos_y = 25
heart = pg.image.load('assets/images/pixelheart.png')
heart = pg.transform.scale(heart, (life_w, life_h))

# bricks
brick_marg = 5
brick_w = (screen.get_width()-(brick_marg*9)) / 8
brick_h = paddle_h
brick_rows = 8
brick_cols = 8
brick_colors = [pg.Color("red"), pg.Color(230, 62, 21), pg.Color("orange"), pg.Color("yellow"), pg.Color(130, 204, 2), pg.Color("green"), pg.Color("blue"), pg.Color(93, 2, 204)]
brick_pos = pg.Vector2(brick_marg, screen.get_height() / 6)
num_bricks = brick_rows * brick_cols

# calculate brick positions and colors and save to list
brick_x = brick_pos.x
brick_y = brick_pos.y
bricks = pg.sprite.Group()
for i in range(brick_rows):
    for j in range(brick_cols):
        brick_x = brick_pos.x + (brick_w + brick_marg)*j
        brick_y = brick_pos.y + (brick_h + brick_marg)*i
        brick = Brick(brick_w, brick_h, brick_x, brick_y, brick_colors[i])
        bricks.add(brick)

dt = 0

# Countdown timer
timer = Timer(lg_font, 3)
timer_group = pg.sprite.GroupSingle()
timer_group.add(timer)

while running:
    # poll for events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.USEREVENT and timer_group:
            timer.down()
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    if lives > 0 and not len(bricks.sprites()) == 0 :
        keys = pg.key.get_pressed()

        timer_group.draw(screen)

        if not timer_group:
            ball.update(dt, screen)

        # draw paddle 1
        pg.draw.rect(screen, "white", pg.Rect((paddl1_pos.x, paddl1_pos.y),(paddle_w, paddle_h)))


        bricks.draw(screen)        
        ball_group.draw(screen)

        # paddle movements
        if keys[pg.K_LEFT]:
            if paddl1_pos.x > 0:
                paddl1_pos.x -= 0.4 * dt
        if keys[pg.K_RIGHT]:
            if paddl1_pos.x + paddle_w < screen.get_width():
                paddl1_pos.x += 0.4 * dt

        for i in range(lives):
            life = heart.convert()
            life_rect = life.get_rect()
            life_rect.x = life_pos_x + i*(life_w + life_buffer)
            life_rect.y = life_pos_y
            screen.blit(life, life_rect)
    else:
        win_text = ""
        if len(bricks.sprites()) == 0:
            win_text = "You Win!"
        elif lives <= 0:
            countdown = -10
            win_text = "You Lose!"
        fin_text = huge_font.render(win_text, True, (0,255,0) if len(bricks.sprites()) == 0 else (255,0,0))
        fin_text_rect = fin_text.get_rect()

        screen.blit(fin_text, (screen.get_width()/2 - fin_text_rect.width/2, screen.get_height() / 2 - fin_text_rect.height/2))

    pg.display.flip()
    dt = clock.tick(60)
    
pg.quit()