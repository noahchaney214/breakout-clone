import pygame as pg 


# simple class to contain brick sprite for ease of use in collision
class Brick(pg.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, color):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.color = "white"
        self.rect = self.image.get_rect()
        self.rect.left = pos_x
        self.rect.top = pos_y


# ball sprite class for enhanced collision detection and reduction of code in game loop
class Ball(pg.sprite.Sprite):
    def __init__(self, rad, pos_x, pos_y):
        super().__init__()
        self.speed = 1
        self.dir = pg.Vector2(0, 0.25) * self.speed
        self.dir_range = 0.5
        self.radius = rad
        self.image = pg.Surface((rad*2, rad*2))
        self.rect = self.image.get_rect()
        self.rect.center = pg.Vector2(pos_x, pos_y)
        pg.draw.circle(self.image, pg.Color("white"), (self.rect.width//2, self.rect.height//2), self.radius)

    def update(self, dt, screen):
        self.move(dt, screen)
        self.check_collisions()

    # simple collision detection for walls along with code to keep ball in motion
    def move(self, dt, screen):
        import main
        # collision detection for ball
        if self.rect.centery + self.radius >= screen.get_height():
            self.rect.center = pg.Vector2(screen.get_width() / 2, 2*(screen.get_height() / 3))
            main.lives -= 1
            main.timer = Timer(main.lg_font, 3)
            main.timer_group.add(main.timer)

        if self.rect.centery - self.radius <= 0:
            self.dir.y *= -1 
        if self.rect.centery + self.radius >= main.paddl1_pos.y - main.paddle_h/2 and main.paddl1_pos.x + main.paddle_w >= self.rect.centerx >= main.paddl1_pos.x : 
            self.dir.y *= -1
            # this line adds more advanced bouncing physics on the paddle so the ball isn't going a constant direction each time
            self.dir.x = -0.25 + (((self.dir_range * (1-(((main.paddl1_pos.x+main.paddle_w)-(self.rect.centerx))/main.paddle_w)))))
            print(self.dir.x)
        if self.rect.centerx + self.radius >= screen.get_width():
            self.dir.x *= -1
        if self.rect.centerx - self.radius <= 0:
            self.dir.x *= -1

        self.rect.y += self.dir.y * dt * self.speed
        self.rect.x += self.dir.x * dt * self.speed

    # checks for collision on all sides of bricks to have accurate bouncing
    def check_collisions(self):
        import main

        collided_bricks = pg.sprite.spritecollide(self, main.bricks, True)

        for brick in collided_bricks:
            # Check collision on each side of the brick
            if self.rect.colliderect(brick.rect):
                if self.rect.bottom >= brick.rect.top and self.rect.top <= brick.rect.top:
                    # Ball hit from bottom side of brick
                    self.dir.y *= -1
                elif self.rect.top <= brick.rect.bottom and self.rect.bottom >= brick.rect.bottom:
                    # Ball hit from top side of brick
                    self.dir.y *= -1
                elif self.rect.right >= brick.rect.left and self.rect.left <= brick.rect.left:
                    # Ball hit from right side of brick
                    self.dir.x *= -1
                elif self.rect.left <= brick.rect.right and self.rect.right >= brick.rect.right:
                    # Ball hit from left side of brick
                    self.dir.x *= -1
                
                break

        if len(collided_bricks) >= 1:
            main.score += 1
            main.score_text = str(main.score)
            main.num_bricks -= 1

        # I want to add the directional collision detection here

class Timer(pg.sprite.Sprite):
    def __init__(self, font, time):
        super().__init__()
        import main
        self.time = time
        self.font = font
        self.time_text = "{}".format(self.time)
        self.txt = font.render(self.time_text, True, (255, 255, 255))
        self.rect = self.txt.get_rect()
        self.rect.center = (main.screen.get_width()/2, main.screen.get_height()/2 - self.rect.height*1.5)
        self.image = pg.Surface((self.rect.width, self.rect.height))
        self.image.blit(self.txt, (0, 0))

    def down(self):
        self.time -= 1
        self.update()

    def update(self):
        import main
        if self.time <= 0:
            self.kill()
        self.time_text = "{}".format(self.time)
        self.txt = self.font.render(self.time_text, True, (255, 255, 255))
        self.rect = self.txt.get_rect()
        self.rect.center = (main.screen.get_width()/2, main.screen.get_height()/2 - self.rect.height*1.5)
        self.image.fill((0,0,0))
        self.image.blit(self.txt, (0, 0))
