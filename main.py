import random
import sys

import pygame

pygame.init()
RESOLUTION = (WIDTH, HEIGHT) = (1200, 300)
SCREEN = pygame.display.set_mode(RESOLUTION)
SPRITE = pygame.image.load("assets/sprite.png").convert_alpha()
LOGO = SPRITE.subsurface(2, 2, 72, 64)
CLOUD = SPRITE.subsurface(76, 2, 107, 30)
GROUND = SPRITE.subsurface(2, 98, 1200, 34)
SINKO = SPRITE.subsurface(185, 2, 80, 70)
NUMBERS = (
    SPRITE.subsurface(267, 2, 18, 21),
    SPRITE.subsurface(289, 2, 16, 21),
    SPRITE.subsurface(307, 2, 18, 21),
    SPRITE.subsurface(327, 2, 18, 21),
    SPRITE.subsurface(347, 2, 18, 21),
    SPRITE.subsurface(367, 2, 18, 21),
    SPRITE.subsurface(387, 2, 18, 21),
    SPRITE.subsurface(407, 2, 18, 21),
    SPRITE.subsurface(427, 2, 18, 21),
    SPRITE.subsurface(447, 2, 19, 21),
)
HI = SPRITE.subsurface(467, 2, 38, 21)
GAMEOVER = SPRITE.subsurface(267, 29, 381, 21)
ISKO = (
    SPRITE.subsurface(650, 2, 71, 94),
    SPRITE.subsurface(723, 2, 71, 94),
    SPRITE.subsurface(869, 2, 71, 94),
    SPRITE.subsurface(796, 2, 71, 94),
    SPRITE.subsurface(942, 2, 71, 94),
)
BACKGROUND = (230, 230, 230)
pygame.display.set_icon(LOGO)
pygame.display.set_caption("Isko Runner")


class Isko:
    def __init__(self):
        self.image = ISKO[0]
        self.image_index = 0
        self.running = True
        self.jumping = False
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 186
        self.rect.width -= 15
        self.velocity = self.gravity = 15

    def run(self):
        self.image = ISKO[:4][self.image_index - 1]
        self.image_index += 1

    def jump(self):
        self.image = ISKO[2]
        if self.jumping:
            self.rect.y -= self.velocity
            self.velocity -= 1
        if self.velocity < -self.gravity:
            self.velocity = self.gravity
            self.jumping = False

    def cry(self):
        self.image = ISKO[4]

    def update(self, key):
        if (key[pygame.K_UP] or key[pygame.K_SPACE]) and not self.jumping:
            self.running = False
            self.jumping = True
        elif not self.jumping:
            self.running = True
        if self.running:
            self.run()
        elif self.jumping:
            self.jump()
        if self.image_index >= len(ISKO):
            self.image_index = 0

    def draw(self):
        SCREEN.blit(self.image, self.rect)


class Sinko:
    def __init__(self):
        self.image = SINKO
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = 209
        self.velocity = -10
        self.out = False

    def update(self):
        self.rect.x += self.velocity
        if self.rect.x < -(self.rect.width):
            self.out = True

    def draw(self):
        SCREEN.blit(self.image, self.rect)
        self.update()


class Cloud:
    def __init__(self, x):
        self.image = CLOUD
        self.image.set_alpha(128)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = random.randint(75, 125)
        self.velocity = -3

    def update(self):
        self.rect.x += self.velocity
        if self.rect.x < -(self.rect.width):
            self.rect.x = WIDTH + random.randint(400, 800)
            self.rect.y = random.randint(75, 125)

    def draw(self):
        SCREEN.blit(self.image, self.rect)
        self.update()


class Ground:
    def __init__(self):
        self.image0 = self.image1 = GROUND
        self.rect0 = self.image0.get_rect()
        self.rect1 = self.image1.get_rect()
        self.rect0.bottom = self.rect1.bottom = 300
        self.rect1.left = self.rect0.right
        self.velocity = -10

    def update(self):
        self.rect0.left += self.velocity
        self.rect1.left += self.velocity
        if self.rect0.right < 0:
            self.rect0.left = self.rect1.right
        if self.rect1.right < 0:
            self.rect1.left = self.rect0.right

    def draw(self):
        SCREEN.blit(self.image0, self.rect0)
        SCREEN.blit(self.image1, self.rect1)
        self.update()


class Scoreboard:
    def __init__(self):
        self.score = 0
        self.score_str = str(self.score)
        self.hi_score = "00000"

    def hi(self):
        SCREEN.blit(HI, (870, 20))
        SCREEN.blit(NUMBERS[int(self.hi_score[0])], (934, 20))
        SCREEN.blit(NUMBERS[int(self.hi_score[1])], (956, 20))
        SCREEN.blit(NUMBERS[int(self.hi_score[2])], (978, 20))
        SCREEN.blit(NUMBERS[int(self.hi_score[3])], (1000, 20))
        SCREEN.blit(NUMBERS[int(self.hi_score[4])], (1022, 20))

    def current(self):
        self.score_str = str(int(self.score)).rjust(5, "0")
        SCREEN.blit(NUMBERS[int(self.score_str[0])], (1068, 20))
        SCREEN.blit(NUMBERS[int(self.score_str[1])], (1090, 20))
        SCREEN.blit(NUMBERS[int(self.score_str[2])], (1112, 20))
        SCREEN.blit(NUMBERS[int(self.score_str[3])], (1134, 20))
        SCREEN.blit(NUMBERS[int(self.score_str[4])], (1156, 20))

    def increment(self):
        if self.score < 99999:
            self.score += 0.1

    def update(self):
        self.score_str = str(int(self.score)).rjust(5, "0")
        if self.score_str > self.hi_score:
            self.hi_score = self.score_str

    def draw(self):
        if self.hi_score != "0" * 5:
            self.hi()
        self.current()


def gamestart():
    scoreboard = Scoreboard()
    while True:
        SCREEN.fill(BACKGROUND)
        SCREEN.blit(GROUND, (0, 266))
        SCREEN.blit(ISKO[0], (50, 186))
        scoreboard.draw()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_SPACE,
                pygame.K_UP,
            ]:
                gameplay(scoreboard)
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()


def gameplay(scoreboard):
    player = Isko()
    obstacle = Sinko()
    cloud0 = Cloud(WIDTH)
    cloud1 = Cloud(WIDTH + 600)
    ground = Ground()
    clock = pygame.time.Clock()
    FPS = 30
    scoreboard.score = 0
    while True:
        SCREEN.fill(BACKGROUND)
        cloud0.draw()
        cloud1.draw()
        ground.draw()
        if obstacle.out:
            obstacle = Sinko()
        obstacle.draw()
        if player.rect.colliderect(obstacle.rect):
            scoreboard.update()
            gameover(player, scoreboard)
        else:
            scoreboard.increment()
            scoreboard.draw()
        player.draw()
        player.update(pygame.key.get_pressed())
        clock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()


def gameover(player, scoreboard):
    while True:
        SCREEN.blit(GAMEOVER, ((WIDTH - 381) / 2, 83))
        SCREEN.blit(LOGO, ((WIDTH - 72) / 2, 148))
        player.cry()
        player.draw()
        scoreboard.draw()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_SPACE,
                pygame.K_UP,
            ]:
                gameplay(scoreboard)
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()


def main():
    gamestart()


if __name__ == "__main__":
    main()
