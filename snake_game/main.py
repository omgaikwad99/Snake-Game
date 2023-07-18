import pygame
from pygame.locals import *
import time
import random

size = 40

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.apple_x = size*3
        self.apple_y = size*3

    def draw(self):
        self.parent_screen.blit(self.image,(self.apple_x, self.apple_y))#blit copies from one surface to another enabling the block to move      
        pygame.display.flip() #To modify the above changes

    def move(self):
        self.apple_x = random.randint(1,29)*size # 30 coz x screen is 1200 and size of apple is 40, so 1200/40=30
        self.apple_y = random.randint(1,19)*size 
    

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert() #Loads our block image
        self.direction = 'down'
        
        self.length = length
        self.block_x = [40]*length
        self.block_y = [40]*length
        
    def increase_length(self):
        self.length += 1
        self.block_x.append(-1)
        self.block_y.append(-1)
    
    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'
    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'
        
    def walk(self):

        for i in range(self.length-1,0,-1):     # To update body
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]

        if self.direction == 'left':
            self.block_x[0] -= size
        if self.direction == 'right':
            self.block_x[0] += size
        if self.direction == 'up':
            self.block_y[0] -= size
        if self.direction == 'down':
            self.block_y[0] += size

        self.draw()

    def draw(self):
        self.parent_screen.fill((0,255,0)) # So that when the block moves, the previous surface goes back to original

        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.block_x[i], self.block_y[i]))#blit copies from one surface to another enabling the block to move      
        pygame.display.flip() #To modify the above changes
        

        

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and Apple Game")

        pygame.mixer.init()  # To initialize music and sounds to the code
        self.background_music()
        self.surface = pygame.display.set_mode((1200, 800)) #Creates a screen
        self.surface.fill((0,255,0)) #Fills color in the screen
        self.snake = Snake(self.surface, 1) #The class Snake is inside class Game
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def collision(self, x1, y1, x2, y2):     
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def background_music(self):
        pygame.mixer.music.load("resources/bella_ciao.mp3")
        pygame.mixer.music.play()
        
    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

         #Snake colliding with apple
        if self.collision(self.snake.block_x[0], self.snake.block_y[0], self.apple.apple_x, self.apple.apple_y):
           sound = pygame.mixer.Sound("resources/chew.mp3")
           pygame.mixer.Sound.play(sound)
           self.snake.increase_length()
           self.apple.move()

        for i in range(1,self.snake.length):  #Sanke colliding with itself
            if self.collision(self.snake.block_x[0],self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i]):
                sound = pygame.mixer.Sound("resources/meow.mp3")
                pygame.mixer.Sound.play(sound)
                raise "Collision Occured"

    def show_game_over(self):
        self.surface.fill((0,255,0))
        font = pygame.font.SysFont('aerial',50)
        line1 = font.render(f"Game is over!! Your score is {(self.snake.length-1)*10}",True,(255,255,255))
        self.surface.blit(line1, (170,300)) #To display this msg at the center of the screen
        line2 = font.render(f" Play Again? - Press Enter       Exit? - Press Esc",True,(255,255,255))
        self.surface.blit(line2, (170,350))
        pygame.display.flip()

        pygame.mixer.music.pause()
     

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {(self.snake.length-1)*10}", True, (255,0,0)) # Score=(length of the snake -1) *10
        self.surface.blit(score, (1000,10)) # To display score
   
    def run(self):
        
        running = True
        pause = False
        
        while running:
             for event in pygame.event.get(): #gets event from the queue
                 if event.type == KEYDOWN:   #Keydown to use various keys

                     if event.key == K_ESCAPE:
                         running = False
                         pygame.quit()
                     if event.key == K_RETURN:
                         self.background_music()
                         pause = False
                         
                       # For the block to move
                     if not pause:
                         if event.key == K_UP:
                             self.snake.move_up()
                         if event.key == K_DOWN:
                             self.snake.move_down()
                         if event.key == K_LEFT:
                             self.snake.move_left()
                         if event.key == K_RIGHT:
                             self.snake.move_right()
                     
                 elif event.type == QUIT:
                     running = False   # Quits the game on clicking x
                     pygame.quit()

             try:
                 if not pause:
                     self.play()
                     
             except Exception as e:
                 self.show_game_over()
                 pause = True
                 self.reset()
                 
             if (self.snake.length-1)*10 > 50:
                 time.sleep(0.1)
             elif (self.snake.length-1)*10 > 100:
                 time.sleep(0.05)
             elif (self.snake.length-1)*10 > 200:
                 time.sleep(0.01)
             else:
                 time.sleep(0.2)
             
         
    

if __name__ =="__main__":
    game=Game()
    game.run()
   

    
    
