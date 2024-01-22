import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue=(6,4,210)

# Creating window
screen_width = 950
screen_height = 700
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#Background Image
background = pygame.image.load("Background.jpeg")
background = pygame.transform.scale(background, (screen_width, screen_height)).convert_alpha()
bg = pygame.image.load("Overscreen.jpg")
bg = pygame.transform.scale(bg, (screen_width, screen_height)).convert_alpha()
backimg = pygame.image.load("backimg.jpg")
backimg = pygame.transform.scale(backimg, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((255, 0, 0))
        gameWindow.blit(backimg, (0, 0))
        text_screen("Press Space To Play", black, 285, 650)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('Gamemusic.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(30)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    # Check if highscore file exists
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 30
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            gameWindow.blit(bg, (0, 0))
            text_screen("Game Over! ", red, 285, 250)
            text_screen("Press Enter To Continue...", red, 165, 290)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score +=10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<10 and abs(snake_y - food_y)<10:
                score +=10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length +=5
                if score>int(highscore):
                    highscore = score

            gameWindow.fill(white)
            gameWindow.blit(background, (0, 0))
            text_screen("Score: " + str(score) + "  Highscore: "+str(highscore), blue, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('Gameover.mp3')
                pygame.mixer.music.play()
                
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('Gameover.mp3')
                pygame.mixer.music.play()
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
