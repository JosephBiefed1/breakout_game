
import pygame
from pygame.locals import *

pygame.init()

#define game variables
screen_width = 600
screen_height = 600
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

#define font
font = pygame.font.SysFont('Constantia', 30)

#define colors

bg = (234, 218, 184)
#block colors
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)
paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)

#text colour
text_colour = (78, 81, 139)


#define game cariables
cols = 6
rows = 6

#function for outputting text onto the screen
def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img,(x, y))

#brick wall class
class wall():
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50

    def create_wall(self):
        self.block = []
        #define an empty list for an individual block
        block_individual = []
        #iterate through each column in that row, basically, putting the x axis down
        for row in range(rows):
            #reset the block row list
            block_row = []
            #iterate through each column in that row
            for col in range(cols):
                #generate the x and y positions for each blocks and create a rectangle from that
                block_x = col * self.width #0, 1 screen_width, 2 screen_width
                block_y = row * self.height #0,0, 0, 0,
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                #assign block strength according to row
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row <6:
                    strength = 1
                #create a list at this point to store the rect and colour data
                block_individual = [rect, strength]
                #append that individual block to the vlock row
                block_row.append(block_individual)


            self.block.append(block_row) #so that you can call this block attribute


#[rect, stength], [rect, stength], [rect, stength], [rect, stength], [rect, stength], [rect, stength], added into self.block, then block row resets,
# [ [[],[], [],[],[],[],[]],[[

    def draw_wall(self):
        for row in self.block: #each block_row
            for block in row: #each block_individual
                #assign a color based on block strength:
                if block[1] == 3: #strengtj
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0]) #rect
                pygame.draw.rect(screen, bg, (block[0]), 2) #rect
                # the '2'is used to signify the line-thickness of the block


wall = wall() #instantiate
wall.create_wall() #one-time


class paddle():
    def __init__(self):
        # define paddle variables
        self.height = 20
        self.width = int(screen_width / cols)
        self.x = int((screen_width / 2)) - (self.width / 2)  # since the startv position must be half from the center x position of the screen
        self.y = screen_height - (self.height * 2)
        self.speed = 8
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0



    def move(self):
        #reset the movement direction

        self.direction = 0
        key = pygame.key.get_pressed() #gets a sequence of boolean values
        if key[pygame.K_LEFT] and self.rect.left > 0: #allow for movement based on keyboard, and the paddle dont touch the sides of the container
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

        #when the keyboard button is pressed once, speed adds or reduces from the value of self.x, and also changes the self.direction

    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect)


class game_ball():
    def __init__(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4  # control this for the speed
        self.speed_y = -4
        self.game_over = 0
        self.max_speed = 5

    def move(self):
        collision_thresh = 5
        #look for collision with paddle

        #start off with the assumption that the wall has been destroyed
        wall_destroyed = 1
        row_count = 0 #tell which row your are in
        for row in wall.block:
            item_counter = 0

            for item in row:
                #check collision
                if self.rect.colliderect(item[0]):
                    #check if collision is from above
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    #check if collision is from below
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    #check if collision is from left
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                    #check if collision is from right
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                    #reduce the block strength by doing damage to it
                    if wall.block[row_count][item_counter][1] > 1:
                        wall.block[row_count][item_counter][1] -= 1
                    else:
                        wall.block[row_count][item_counter][0] = (0, 0, 0, 0) #save the rectangle to a rectangle with left, top, width, height = 0

                #check if block still exists, in which the case the wall is not destroyed
                if wall.block[row_count][item_counter][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                #increase item counter
                item_counter += 1 # increase item in row
            #increase row count
            row_count += 1 # increase row
        #after iterating through all the blocks, check if the wall is destroyed
        if wall_destroyed == 1: #check if there are still any walls
            self.game_over = 1 #player won




        if self.rect.colliderect(player_paddle):
            #check if colliding from top
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction #1 or -1
                if self.speed_x > self.max_speed:
                    self.speed_x = self.max_speed
                if self.speed_x < 0 and self.speed_x < -self.max_speed:
                    self.speed_x = -self.max_speed
            else:
                pass


        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        #check for collision with the wall
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1 #flips direction but speed continues the same
        if self.rect.top < 0:
            self.speed_y *= -1 #flips direction
        if self.rect.bottom > screen_height:
            self.game_over = -1

        return self.game_over





    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)

player_paddle = paddle()
#create ball
ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)



run = True
while run:
    clock.tick(fps)
    screen.fill(bg)

    #draw all objects
    wall.draw_wall()
    player_paddle.draw()
    ball.draw()

    if live_ball:
        player_paddle.move()
        game_over = ball.move() #move within game_ball class returns a self.game_over, which is either a 1, -1 or 0(from the global varibale)
                                #saves into the global variable game_over
        if game_over != 0:
            live_ball = False
    if not live_ball:
        if game_over == 0:
            draw_text("CLICK ANYWHERE TO START", font, text_colour, 100, screen_height // 2 + 100)
        elif game_over == 1:
            draw_text("YOU WON", font, text_colour, 240, screen_height // 2 + 50)
        elif game_over == -1:
            draw_text("YOU LOST!", font, text_colour, 240, screen_height // 2 + 50)
            draw_text("CLICK ANYWHERE TO START", font, text_colour, 100, screen_height // 2 + 100)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.__init__(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.__init__()
            wall.create_wall() #reset using block = []



    pygame.display.update()
pygame.quit()