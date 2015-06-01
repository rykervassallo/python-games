#Credit the Invent With Python book (http://inventwithpython.com)
#for doRectsOverlap and isPointInsideRect functions

#used to detect collisions in our game
def doRectsOverlap(rect1, rect2):
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        # Check if a's corners are inside b
        if ((isPointInsideRect(a.left, a.top, b)) or
            (isPointInsideRect(a.left, a.bottom, b)) or
            (isPointInsideRect(a.right, a.top, b)) or
            (isPointInsideRect(a.right, a.bottom, b))):
            return True

    return False

#used the by the doRectsOverlap function (won't be called directly from game code)
def isPointInsideRect(x, y, rect):
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
        return True
    else:
        return False

import pygame, sys, random
pygame.init()
screen = pygame.display.set_mode([640,480])
black = [0, 0, 0]
mode = 'menu'
topscores = []

#the game's variables

#open the top score file
with open('TOPSCORES.txt','r') as f:
    print "CURRENT TOP SCORES"
    for line in f:
        topscores.append(int(line))
        print line

#snake variables
snake_x = 0
snake_y = 0
snake_x_speed = 0
snake_y_speed = 0
snake_color = [40,250,96]
snake_size = 25
speed_multiplier = 5

snake_mini_x = 0
snake_mini_y = 0
snake_mini_x_speed = 0
snake_mini_y_speed = 0
snake_mini_color = snake_color
snake_mini_size = 10


#pellet variables
target_color = [255 , 0 , 0]
target_x = random.randint(1 , 640)
target_y = random.randint(1 , 480)
target_size = 10

#powerup 1 (invincibility) variables
power_x = 0
power_y = 0
power_time = 0   #when >0, on screen; when <0, powerup active
power_size = 10
power_color = [0,0,255]

#powerup2 (slow) variables
power2_x = 0
power2_y = 0
power2_time = 0
power2_size = 10
power2_color = [71,138,54]

score = 0



running = True
#game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and mode=='menu':
            mode='play'

        if event.type == pygame.KEYDOWN:
            #SECTION 3 - YOUR CODE HERE FOR WHEN A KEY IS PRESSED
            if event.key == pygame.K_LEFT:
                snake_x_speed = -1*speed_multiplier
                snake_y_speed = 0
            elif event.key == pygame.K_RIGHT:
                snake_x_speed = speed_multiplier
                snake_y_speed = 0
            elif event.key == pygame.K_UP:
                snake_y_speed = -1*speed_multiplier
                snake_x_speed = 0
            elif event.key == pygame.K_DOWN:
                snake_y_speed = speed_multiplier
                snake_x_speed = 0
            if event.key == pygame.K_x:
                snake_mini_x = snake_x
                snake_mini_y = snake_y

            
                
    #pause for 20 milliseconds
    pygame.time.delay(20)
    #make the screen completely black
    screen.fill(black)

    #logic for moving everything in the game and checking collisions

    if mode=='menu':
        pass

    if mode=='play':

        if power_time >= 0:         #if no active powerup

            #if a wall was hit
            if snake_y < 0 or snake_y > 480 or snake_x < 0 or snake_x > 640:
                print "YOU LOSE"
                topscores.append(score)
                topscores.sort()
                topscores.reverse()
                print 'TOP SCORES!!!'
                
                #save the scores
                with open('TOPSCORES.txt','wr') as f:
                    for x in topscores[0:3]:
                        print x
                        f.write(str(x)+'\n')
                
                break
        else:   #invincibility power up, bounce off the walls 
            if snake_y < 0:
                snake_y_speed = speed_multiplier
            elif snake_y > 480:
                snake_y_speed = -1*speed_multiplier
            elif snake_x < 0:
                snake_x_speed = speed_multiplier
            elif snake_x > 640:
                snake_x_speed = -1*speed_multiplier
            
        #update snake position
        snake_x = snake_x + snake_x_speed/1
        snake_y = snake_y + snake_y_speed/1

        #if overlap with pellet
        target_rect = pygame.Rect(target_x-target_size, target_y-target_size, target_size*2,target_size*2) 
        snake_rect = pygame.Rect(snake_x , snake_y , snake_size , snake_size)
        if doRectsOverlap(target_rect, snake_rect):     #if eat pellet
            target_x = random.randint(1 , 640)
            target_y = random.randint(1 , 480)
            score = score + 1
            if speed_multiplier < 7 and power2_time>=0:     #increase the speed
                speed_multiplier += .1
            print score
            if random.random() < .10 and power_time == 0:   #chance to make an invincibility powerup
                power_time = 30*1000
                power_x = random.randint(1 , 640)
                power_y = random.randint(1 , 480)
            if random.random() < .10 and power2_time == 0:  #chance to make a slow powerup
                power2_time = 30*1000
                power2_x = random.randint(1 , 640)
                power2_y = random.randint(1 , 480)
                

        if power_time > 0:  #if invincibility power pellet is on screen
            power_time = power_time - 20
            pygame.draw.circle(screen, power_color, [power_x, power_y], power_size)
            power_rect = pygame.Rect(power_x-power_size, power_y-power_size, power_size*2,power_size*2) 
            if doRectsOverlap(power_rect,snake_rect):   #eat power pellet
               power_time = -10*1000
               print "YOU HAVE A BOUNCE POWERUP!!!!!!!!!!!"
        elif power_time < 0:        #if power up is active
            power_time = power_time + 20
            if power_time == 0:     #if power up is done
                print "YOU LOST YOUR BOUNCE POWERUP!!!!!!"

        if power2_time > 0:  #if slow power up is on the screen 
            power2_time = power2_time - 20
            pygame.draw.circle(screen, power2_color, [power2_x, power2_y], power2_size)
            power2_rect = pygame.Rect(power2_x-power_size, power2_y-power_size, power_size*2,power_size*2) 
            if doRectsOverlap(power2_rect,snake_rect):  #eat power pellet, slow speed
               power2_time = -10*1000
               power2_oldspeed = speed_multiplier
               speed_multiplier = 4
               print "YOU HAVE A SLOW POWERUP!!!!!!!!!!!"
        elif power2_time < 0:       #if power up is active
            power2_time = power2_time + 20
            if power2_time == 0:    #if power up is done
                speed_multiplier = power2_oldspeed
                print "YOU LOST YOUR SLOW POWERUP!!!!!!"
        
        #draw snake/pellet on the screen
        pygame.draw.rect(screen , snake_color , (snake_x , snake_y , snake_size , snake_size))
        pygame.draw.circle(screen, target_color, [target_x, target_y], target_size)
        

    #update the entire display
    pygame.display.update()


pygame.quit()
