from pygame import * 
from pygame import mixer
import json
from pygame.locals import *
from datetime import datetime

# Initializing the game
pygame.init()
clock = pygame.time.Clock()
# Variables to show the game-end time and write it to json file
now = datetime.now()
game_started = now.strftime("%H:%M:%S")

# Game screen
screen_width = 920
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
background_image = pygame.image.load("background.jpg")

# Screen caption
pygame.display.set_caption('Breakout')
icon = pygame.image.load('Ball.png')
pygame.display.set_icon(icon)

# Colors
back_ground_color = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
player_color = (100, 50, 255)
player_border = (100, 50, 180)

# The blocks row and columns
rows = 6
cols = 8

# The Game variables

# Variables to define game end
live_ball = False
game_over = 0

# Score text
font = pygame.font.SysFont('Constantia', 30)
score_screen = "Score:"
game_font = pygame.font.SysFont('Constantia', 30)

# Player score text
player_score = 0
game_font = pygame.font.SysFont('Constantia', 30)


class Player():
    """
    This class define the paddle that player will control.
    the paddle will go either right or left
    """

    def __init__(self):
        """
        This function will make player-paddle surface
        """
        self.height = 20
        self.width = int(screen_width / cols)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 7
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

    def move(self):
        """
        To make player-paddle move right when key right arrow pressed
        and left when key left arrow pressed
        """
        # Reset movement direction
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        """
        To show player-paddle surface in main game screen
        """
        pygame.draw.rect(screen, player_color, self.rect)
        pygame.draw.rect(screen, player_border, self.rect, 3)


# Brick wall class
class Wall():
    """
    This class creates a wall of paddles
    these paddles will be destroyed by a ball
    """

    def __init__(self):
        """
        Make wall-surface of paddles that player will try to destroy
        """
        self.width = screen_width // cols
        self.height = 35

    def create_wall(self):
        """
        This function will make wall-paddle
        """
        self.blocks = []
        # Define an empty list for an individual block
        block_individual = []
        for row in range(rows):
            # Reset the block row list
            block_row = []
            # Iterate through each column in that row
            for col in range(cols):
                # Generate x, y position for each block and create a rectangle from that
                block_x = col * self.width
                block_y = row * self.height + 50
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                # Assign block strength based on row
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                # Create a list at this point to store rect color data
                block_individual = [rect, strength]
                # Append that individual block to the block row
                block_row.append(block_individual)
            # Append the row to the full list of blocks
            self.blocks.append(block_row)

    def draw_wall(self):
        """
        To show wall-paddle to the main game screen
        """
        for row in self.blocks:
            for block in row:
                if block[1] == 3:
                    block_color = blue
                if block[1] == 2:
                    block_color = green
                if block[1] == 1:
                    block_color = red
                pygame.draw.rect(screen, block_color, block[0])
                pygame.draw.rect(screen, back_ground_color, (block[0]), 2)


# Ball
class Ball():
    """
    This class make the game ball and define the mechanism to how ball will act in the game
    """

    def __init__(self, x, y):
        """
        Create the ball
        :param x: Horizontal axis
        :param y:Vertical axis
        """
        self.ball_radius = 10
        self.x = x - self.ball_radius
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_radius * 2, self.ball_radius * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.max_speed = 5
        self.game_over = 0

    def move(self):
        """
        Define all the movement conditions to the game ball
        and the relationship between the ball, player-paddle and the paddle-wall
        """
        global player_score
        collision_thresh = 5
        # start of with assumption that the wall has been destroyed
        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                # Check
                if self.rect.colliderect(item[0]):
                    player_score += 1
                    # Check if colliding from the top
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                        mixer.music.load('pong.ogg')
                        mixer.music.play()
                    # Check if colliding from the bottom
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                        mixer.music.load('pong.ogg')
                        mixer.music.play()
                    # Check if colliding from the left
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                        mixer.music.load('pong.ogg')
                        mixer.music.play()
                    # Check if colliding from the right
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                        mixer.music.load('pong.ogg')
                        mixer.music.play()

                    # Reduce the block's strength by doing damage to it
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)

                # Check if the wall still here
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                # Increase item counter
                item_count += 1
            # increase row counter
            row_count += 1
        # After iterating through all the blocks, check if the wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1
        # Check if ball collide to the screen edge
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            mixer.music.load('score.ogg')
            mixer.music.play()
            self.game_over = 1

        # The ball bouncing when hitting the player
        if self.rect.colliderect(player_paddle):
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.max_speed:
                    self.speed_x = self.max_speed
                elif self.speed_x < 0 and self.speed_x < -self.max_speed:
                    self.speed_x = -self.max_speed
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, green, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius),
                           self.ball_radius)
        pygame.draw.circle(screen, back_ground_color, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius),
                           self.ball_radius, 3)


# Create the player paddle
player_paddle = Player()

# Create a wall
wall = Wall()
wall.create_wall()

# Create a ball
ball = Ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not live_ball:
            live_ball = True

    # visuals
    screen.fill(back_ground_color)
    screen.blit(background_image, [0, 0])
    # draw_text('Score:', font, white, 5, 5)
    player_text = game_font.render(f'{player_score}', False, white)
    screen.blit(player_text, (90, 4))
    score_text = game_font.render(f'{score_screen}', False, white)
    screen.blit(score_text, (5, 5))

    date_save = {
        'Your score': player_score,
        'Game started at': game_started
    }
    # Draw Game
    wall.draw_wall()
    ball.draw()
    player_paddle.draw()

    # Game over
    if live_ball:
        game_over = ball.move()
        if game_over != 0:
            live_ball = False
            with open("score.json", "w") as file:
                json.dump(date_save, file)

    player_paddle.move()

    # Updating the window
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
