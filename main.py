from frog import Frog
from street import Street
from log import Log
from river import River
import pygame, sys, random

pygame.init()
pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT])

SCREEN_DIM = WIDTH, HEIGHT = 600, 500
SCREEN = pygame.display.set_mode(SCREEN_DIM)

CLOCK = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (28, 128, 28)
YELLOW = (100, 85, 0)
BROWN = (118, 92, 72)
GRAY = (175, 175, 175)
BLUE = (0, 0, 175)

FONT = pygame.font.Font('resources/joystix monospace.ttf', 20)
MENU_BIG = pygame.font.Font('resources/joystix monospace.ttf', 60)
MENU_MED = pygame.font.Font('resources/joystix monospace.ttf', 25)
MENU_SMALL = pygame.font.Font('resources/joystix monospace.ttf', 15)

# Images
MENU_IMAGE = pygame.image.load('resources/menu_image.png')

START_MENU = True
END_MENU = False

frog = Frog()

# Create Street objects
streets = []
number_of_buses = 3
street_height = 400
for _ in range(2):
    streets.append(Street(street_height, 'Left', random.randint(1, number_of_buses)))
    streets.append(Street(street_height - 40, 'Right', random.randint(1, number_of_buses)))
    street_height -= 80

# Create River objects
rivers = []
number_of_logs = 3
river_height = 200
for _ in range(2):
    rivers.append(River(river_height, 'Left', random.randint(1, number_of_logs)))
    rivers.append(River(river_height - 30, 'Right', random.randint(1, number_of_logs)))
    river_height -= 60

score = 0
high_score = 0
current_best = 0

while True:

    while START_MENU:
        # Tick forward at 15 frames per second
        CLOCK.tick(15)

        SCREEN.fill(GREEN)

        # Show text on menu screen
        name = MENU_BIG.render('FISH ROAD', True, WHITE)
        instructions = MENU_SMALL.render('Press Space To Start', True, WHITE)
        SCREEN.blit(name, (75, 130))
        SCREEN.blit(instructions, (180, 210))
        SCREEN.blit(MENU_IMAGE, (145, 260))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    START_MENU = False

        pygame.display.update()

    while END_MENU:
        # Tick forward at 15 frames per second
        CLOCK.tick(15)

        SCREEN.fill(GREEN)

        # Show text on menu screen
        thx = MENU_MED.render('Thanks for Playing!', True, WHITE)
        scores = MENU_MED.render('Your Final Score: %d' % (score + current_best), True, WHITE)
        instructions = MENU_SMALL.render('Press \'Space\' To Play Again', True, WHITE)
        SCREEN.blit(thx, (85, 120))
        SCREEN.blit(scores, (70, 180))
        SCREEN.blit(instructions, (130, 240))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    END_MENU = False
                    # Reset all stats
                    current_best = 0
                    score = 0
                    frog.lives = 3

        pygame.display.update()

    CLOCK.tick(FPS)
    SCREEN.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  # W
                frog.move_up()
            if event.key == pygame.K_a:  # A
                frog.move_left()
            if event.key == pygame.K_s:  # S
                frog.move_down()
            if event.key == pygame.K_d:  # D
                frog.move_right()

    for street in streets:
        SCREEN.fill(BLUE, street.rect)
        for bus in street.buses:
            SCREEN.blit(bus.image, bus.rect)
            bus.move()
            if frog.rect.colliderect(bus.rect):
                frog.reset_position()

    # Act on rivers and logs
    frog_on_log = False  # new
    for river in rivers:
        # Draw River
        SCREEN.fill(YELLOW, river.rect)

        # Log
        for log in river.logs:
            SCREEN.blit(log.image, log.rect)
            log.move()
            if frog.rect.colliderect(log.rect):
                frog.move_on_log(log)
                frog_on_log = True  # new

        # Collided with River and not a Log - new
        if not frog_on_log and frog.rect.colliderect(river.rect):
            frog.reset_position()

    SCREEN.blit(log.image, log.rect)
    SCREEN.blit(frog.image, frog.rect)

    # Update the score only if the score is increasing
    if 475 - frog.rect.top > current_best:
        current_best = 475 - frog.rect.top

    # Frog reached end
    if frog.rect.top <= 60:
        frog.reset_position()
        frog.lives += 1
        score += 1000 + current_best
        current_best = 0

    # Update high score
    if score + current_best >= high_score:
        high_score = score + current_best

    print("Score: " + str(score + current_best))
    print("High Score: " + str(high_score))
    print("Lives: " + str(frog.lives))

    score_text = FONT.render("Score: " + str(score + current_best), True, WHITE)
    high_score_text = FONT.render("High Score: " + str(high_score), True, WHITE)
    lives_text = FONT.render("Lives: " + str(frog.lives), True, WHITE)

    SCREEN.blit(score_text, (5, 0))
    SCREEN.blit(high_score_text, (5, 20))
    SCREEN.blit(lives_text, (5, 40))

    if frog.lives == 0:
        END_MENU = True

    pygame.display.flip()