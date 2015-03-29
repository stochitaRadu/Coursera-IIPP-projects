# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [0,0]
ball_vel = [0,0]

paddle1_pos = [[HALF_PAD_WIDTH,HEIGHT/2-HALF_PAD_HEIGHT],
              [HALF_PAD_WIDTH,HEIGHT/2+HALF_PAD_HEIGHT]]
paddle2_pos = [[WIDTH-HALF_PAD_WIDTH,HEIGHT/2 - HALF_PAD_HEIGHT],
              [WIDTH-HALF_PAD_WIDTH,HEIGHT/2 + HALF_PAD_HEIGHT]]

paddle1_vel = 0
paddle2_vel = 0

# the score
score = [0,0]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    if not direction:
        ball_vel = [-random.randrange(2,4),-random.randrange(1,3)]
    else:
        ball_vel = [random.randrange(2,4),-random.randrange(1,3)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    pos = random.randrange(0,2)
    if pos == 0:
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)
def draw(canvas):
    global score,score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel,paddle2_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # check to see if it collides
    if(ball_pos[1] >= HEIGHT-1-BALL_RADIUS or ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
        
    #check to see if it collides with gutters
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,4,"White","White")
    
    # update paddle's vertical position, keep paddle on the screen
    # the first paddle
    paddle1_pos[0][1] += paddle1_vel
    paddle1_pos[1][1] += paddle1_vel
    
    if paddle1_pos[0][1] < 0:
        paddle1_vel = 0
    elif paddle1_pos[1][1] >= HEIGHT:
        paddle1_vel = 0
    
    # the second paddle
    paddle2_pos[0][1] += paddle2_vel
    paddle2_pos[1][1] += paddle2_vel
    
    if paddle2_pos[0][1] < 0:
        paddle2_vel = 0
    elif paddle2_pos[1][1] >= HEIGHT:
        paddle2_vel = 0
    
    # draw paddles
    canvas.draw_line(paddle1_pos[0],paddle1_pos[1], 
                     PAD_WIDTH, 'White')
    canvas.draw_line(paddle2_pos[0],paddle2_pos[1],
                     PAD_WIDTH,"White")
    # determine whether paddle and ball collide
    if ball_pos[0] >= WIDTH-1-BALL_RADIUS-PAD_WIDTH or ball_pos[0] <= PAD_WIDTH+BALL_RADIUS:
        if ((ball_pos[0] < WIDTH/2) and (ball_pos[1] >= paddle1_pos[0][1] and ball_pos[1] <= paddle1_pos[1][1])):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = ball_vel[0] * 1.1
        elif((ball_pos[0] > WIDTH/2) and (ball_pos[1] >= paddle2_pos[0][1] and ball_pos[1] <= paddle2_pos[1][1])):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = ball_vel[0] * 1.1
        else:
            if ball_pos[0] >= WIDTH-1-BALL_RADIUS-PAD_WIDTH:
                score[0] += 1
            else:
                score[1] += 1
            spawn_ball(LEFT)
    # draw scores
    canvas.draw_text(str(score[0]),[WIDTH/2-40,40],40,"White","sans-serif")
    canvas.draw_text(str(score[1]),[WIDTH/2+20,40],40,"White","sans-serif")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    # for the first paddle
    if key == simplegui.KEY_MAP["w"]:
        if paddle1_pos[0][1] >= 0:
            paddle1_vel = -3
    elif key == simplegui.KEY_MAP["s"]:
        if paddle1_pos[1][1] < HEIGHT:
            paddle1_vel = 3
    # for the second paddle
    if key == simplegui.KEY_MAP["up"]:
        if paddle2_pos[0][1] >= 0:
            paddle2_vel = -3
    elif key == simplegui.KEY_MAP["down"]:
        if paddle2_pos[1][1] < HEIGHT:
            paddle2_vel = 3

def keyup(key):
    global paddle1_vel, paddle2_vel
    # for the fist paddle
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    # for the second paddle
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    
def reset():
    global score
    score[0] = 0
    score[1] = 0
    new_game()
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.add_button("Reset",reset,100)

# start frame
new_game()
frame.start()
