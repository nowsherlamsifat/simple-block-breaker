import pygame,sys,random
from pygame.locals import *

pygame.init()

SCREEN_HEIGHT=600
SCREEN_WIDTH=800
PADDLE_HEIGHT=10
PADDLE_WIDTH=100
BALL_SIZE=20

screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Block breaker')
bg_color=pygame.Color('grey12')
clock=pygame.time.Clock()

"""paddle"""
paddle=Rect(int(SCREEN_WIDTH/2)-40,SCREEN_HEIGHT-30,PADDLE_WIDTH,PADDLE_HEIGHT)
paddle_color=pygame.Color('red2')
paddle_speed=0
paddle_move=2

def paddle_movement():
    if paddle.x<0:
        paddle.x=0
    if paddle.x>SCREEN_WIDTH-PADDLE_WIDTH:
        paddle.x=SCREEN_WIDTH-PADDLE_WIDTH
    paddle.x+=paddle_speed
    
"""ball"""
ball=Rect((int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2),BALL_SIZE,BALL_SIZE))
ball_color=pygame.Color('yellow')
ball_dx=1
ball_dy=1
ball_hit_wall=False

"""score"""
score=0
text=pygame.font.SysFont('comicsansms',20)


"""block"""

block_number=8
BLOCK_HEIGHT=10
BLOCK_WIDTH=60
SPACE=100
block_box=[]
BLUE=pygame.Color('blue')

for i in range(block_number):
    if i*SPACE<SCREEN_WIDTH:
        block_box.append(pygame.Rect(i*SPACE,0,BLOCK_WIDTH,BLOCK_HEIGHT))

    if i*SPACE<SCREEN_WIDTH:
        block_box.append(pygame.Rect(i*SPACE,50,BLOCK_WIDTH,BLOCK_HEIGHT))
    

        


def ball_movement():
    global ball_dx,ball_dy,ball_hit_wall,paddle_speed,score
    """horizontal"""
    
    if ball.x<0:
        ball_dx*=-1
        
    if ball.x>SCREEN_WIDTH-BALL_SIZE:
        ball_dx*=-1
    ball.x+=ball_dx
    
    """vertical"""
    if ball.y<0:
        ball_dy*=-1
        
    if ball.y>SCREEN_HEIGHT-BALL_SIZE:
        ball.y=paddle.y-20
        ball_dy=0
        ball.x=paddle.x+int(PADDLE_WIDTH/2)-10
        ball_dx=0
        ball_hit_wall=True
        score-=1
        
    ball.y+=ball_dy
    
    """ball paddle collide"""
    if not ball_hit_wall:
        if ball.y>paddle.y-10 and ball.x>paddle.x and ball.x<paddle.x+PADDLE_WIDTH:
            ball_dy*=-1
    
    """ball after hiting wall moving with paddle"""
    if paddle.x<0:
        paddle_speed=0
        
    if paddle.x>SCREEN_WIDTH-PADDLE_WIDTH:
        paddle_speed=0
    
    if ball_hit_wall:
        ball.x+=paddle_speed
        
    for i in range(len(block_box)):
        if ball.y<block_box[i].y+10 and ball.y>block_box[i].y-10 and ball.x>block_box[i].x-15 and ball.x<block_box[i].x+BLOCK_WIDTH+15:
            block_box[i].x=-100
            ball_dy*=-1
            score+=1
        
            
def draw_all():
    pygame.draw.rect(screen,paddle_color,paddle)
    pygame.draw.ellipse(screen,ball_color,ball)
    
    """drawing block"""
    for i in block_box:
        pygame.draw.rect(screen,BLUE,i)
    
    show_score=text.render(f'{score}',True,paddle_color)
    screen.blit(show_score,(paddle.x+45,paddle.y+5))
    
def game_over():
    global block_box
    
    if score==len(block_box):
        sys.exit()

while True:
    screen.fill(bg_color)
    for event in pygame.event.get():
        if event.type==QUIT:
            sys.exit()
            
        if event.type==KEYDOWN:
            if event.key==K_LEFT:
                paddle_speed=-paddle_move
                if ball_hit_wall:
                    ball.x-=paddle_move
                
            if event.key==K_RIGHT:
                paddle_speed=paddle_move
            
            if event.key==K_SPACE:
                if ball_hit_wall:
                    ball_dy=-1
                    x=[1,-1]
                    ball_dx=random.choice(x)
                    ball_hit_wall=False
                
        
        if event.type==KEYUP:
            paddle_speed=0
    
   
    draw_all()
    paddle_movement()
    ball_movement()
    game_over()
    
    clock.tick(500)
    pygame.display.update()
