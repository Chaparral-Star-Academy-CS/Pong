'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
#####
Ismail A Ahmed
Paddle
Version 2.0
'''

import pygame
import sys
import random

global sped
sped = 4

background = (0, 0, 0)
entity_color = (255, 255, 255)

def doRectsOverlap(rect1, rect2): #checks to see if the first rect collides coordinates with the second
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        # Check if a's corners are inside b
        if ((isPointInsideRect(a.left, a.top, b)) or
            (isPointInsideRect(a.left, a.bottom, b)) or
            (isPointInsideRect(a.right, a.top, b)) or
            (isPointInsideRect(a.right, a.bottom, b))):
            return True

    return False

def isPointInsideRect(x, y, rect): #checks to see if the point is inside the rect
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
        return True
    else:
        return False


class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Paddle(Entity):
    """
    Player controlled or AI controlled, main interaction with
    the game
    """

    def __init__(self, x, y, width, height):
        try:
            super(Paddle, self).__init__(x, y, width, height)

            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(entity_color)
        except:
            pass


class Player(Paddle):
    """The player controlled Paddle"""

    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height)

        # How many pixels the Player Paddle should move on a given frame.
        self.y_change = 0
        # How many pixels the paddle should move each frame a key is pressed.
        self.y_dist = 5
        self.newy=250

    def getheight(self):
        return self.height

    def MoveKeyDown(self, key):
        """Responds to a key-down event and moves accordingly"""
        if (key == pygame.K_UP):
            self.y_change += -self.y_dist
            self.newy+= -self.y_dist

        elif (key == pygame.K_DOWN):
            self.y_change += self.y_dist
            self.newy += self.y_dist

    def MoveKeyUp(self, key):
        """Responds to a key-up event and stops movement accordingly"""
        if (key == pygame.K_UP):
            self.y_change += self.y_dist
            self.newy += self.y_dist

        elif (key == pygame.K_DOWN):
            self.y_change += -self.y_dist
            self.newy += -self.y_dist

    def update(self):
        """
        Moves the paddle while ensuring it stays in bounds
        """
        # Moves it relative to its current location.
        self.rect.move_ip(0, self.y_change)
        # If the paddle moves off the screen, put it back on.
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > window_height - self.height:
            self.rect.y = window_height - self.height
    def heightupdate(self,height2):
        self.height=height2
        super(Player, self).__init__(self.x, self.rect.y, self.width, self.height)


class Enemy(Paddle):
    """
    AI controlled paddle, simply moves towards the ball
    and nothing else.
    """

    def __init__(self, x, y, width, height):
        super(Enemy, self).__init__(x, y, width, height)

        self.y_change = 4

    def update(self):
        """
        Moves the Paddle while ensuring it stays in bounds
        """
        # Moves the Paddle up if the ball is above,
        # and down if below.
        if ball.rect.y < self.rect.y:
            self.rect.y -= self.y_change
        elif ball.rect.y > self.rect.y:
            self.rect.y += self.y_change

        # The paddle can never go above the window since it follows
        # the ball, but this keeps it from going under.
        if self.rect.y + self.height > window_height:
            self.rect.y = window_height - self.height


class Ball(Entity):
    """
    The ball!  Moves around the screen.
    """

    def __init__(self, x, y, width, height):
        super(Ball, self).__init__(x, y, width, height)

        self.image = pygame.Surface([width, height])
        self.image.fill(entity_color)

        directions = [1,-1] #makes it go other ways
        self.x_direction = random.choice(directions)
        # Positive = down, negative = up
        self.y_direction = random.choice(directions)
        # Current speed.
        self.speed = 4

    def update(self):
        # Move the ball!
        global Pcount
        global Ecount

        self.rect.move_ip(self.speed * self.x_direction,
                          self.speed * self.y_direction)
        # Keep the ball in bounds, and make it bounce off the sides.
        directions = [1, -1]

        if self.rect.y < 0:
            self.y_direction *= -1

        elif self.rect.y > window_height - 20:
            self.y_direction *= -1

        if self.rect.x < 0:
            self.x_direction *= -1 #makes go opposite direction
            Ecount += 1 #if it hits player wall, enemy gets point for making past paddle
            self.speed = 4 #restarts speed back to original
            self.rect.x = 350 #x center of grid
            self.rect.y = 200 #y center of grid
            self.x_direction = random.choice(directions)
            # Positive = down, negative = up
            self.y_direction = random.choice(directions)
            player.heightupdate(50) #resets height back to original of 50

        elif self.rect.x > window_width - 20:
            self.x_direction *= -1
            Pcount += 1 #if it hits enemy wall, player gets point for making past paddle
            self.speed = 4
            self.rect.x = 350
            self.rect.y = 200
            self.x_direction = random.choice(directions)
            # Positive = down, negative = up
            self.y_direction = random.choice(directions)


pygame.init()

#scores
global Pcount
Pcount = 0
global Ecount
Ecount = 0

window_width = 700
window_height = 400
screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

global firsthalf
firsthalf = 0

ball = Ball(window_width / 2, window_height / 2, 20, 20)
player = Player(10, window_height / 2, 20, 50)
enemy = Enemy(window_width - 30, window_height / 2, 20, 50)

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(ball)
all_sprites_list.add(player)
all_sprites_list.add(enemy)

basicfont = pygame.font.SysFont(None, 35)  # 35 is font size, no font type
basicfont2 = pygame.font.SysFont(None, 35)  # 35 is font size, no font type
highscore = pygame.font.SysFont(None, 25)  # 35 is font size, no font type

while True:
    # Event processing here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            player.MoveKeyDown(event.key)
        elif event.type == pygame.KEYUP:
            player.MoveKeyUp(event.key)

    for ent in all_sprites_list:
        ent.update()

    #replaces the rect1 and rect2 with ball and player so that it can be checked if they collide
    if doRectsOverlap(ball.rect, player.rect):
        if ball.rect.y < (player.rect.y+(player.getheight()/2)): #if it is the top part of the paddle
            print("<25")
            ball.x_direction *= -1
            ball.y_direction *= -1
            heightvalue = player.getheight()  # current height
            if heightvalue >= 15: #makes sure the paddle doesnt shrink till nothing is left
                player.heightupdate(heightvalue - 5) #reduces the height

        elif ball.rect.y >= (player.rect.y+(player.getheight()/2)): #if it is the bottom of the paddle
            print(">=25")
            ball.x_direction *= -1
            ball.y_direction *= -1
            heightvalue = player.getheight()  # current height
            if heightvalue >= 15: #makes sure the paddle doesnt shrink till nothing is left
                player.heightupdate(heightvalue - 5) #reduces the height
        if ball.speed < 9: #increases speed if hits player paddle
            ball.speed += 1
    # replaces the rect1 and rect2 with ball and player so that it can be checked if they collide
    if doRectsOverlap(ball.rect, enemy.rect):
        if ball.rect.y < (enemy.rect.y+25): #if it is the top part of the paddle
            print("<25")
            ball.x_direction *= -1
            ball.y_direction *= -1

        elif ball.rect.y >= (enemy.rect.y + 25):  # if it is the bottom of the paddle
            print(">=25")
            ball.x_direction *= -1
            ball.y_direction *= -1
        if ball.speed < 9: #increases speed if hits enemy paddle
            ball.speed += 1

    screen.fill(background)
    #prints the scores to the GUI
    text = basicfont.render("Player: "+str(Pcount), True, entity_color, background)  # first set of parenthesis is the font color, second set is the background of the words
    screen.blit(text, (50, 10))
    text2 = basicfont2.render("Enemy: "+str(Ecount), True, entity_color, background)  # first set of parenthesis is the font color, second set is the background of the words
    screen.blit(text2, (540, 10))

    if Ecount > 2: #check to see if if player lost 3 times
        outfile = open('highscore.txt', 'a')
        outfile.write(str(Pcount) + '\n') #stores player's high score in
        outfile.close
        infile = open('highscore.txt', 'r')
        column = []
        for line in infile: #goes through each line of the file
            if line == "\n":
                this = "doesnothing" #ignores the new line
            else:
                column.append(int(line)) #adds the high score value to list
        high = sorted(column, reverse=True) #orders the list, biggest to smallest
        z = []
        for x in high[:10]:
            z.append(x)

        text = basicfont.render("High Scores: "+str(z), True, entity_color, background)  # first set of parenthesis is the font color, second set is the background of the words
        screen.blit(text, (190, 150))
        infile.close()

    all_sprites_list.draw(screen)

    pygame.display.flip()

    if Ecount > 2: #so can show high score, pause, and remove high score
        pygame.time.wait(1000)
        Pcount = 0 #restarts score back to zero
        Ecount = 0

    clock.tick(60)