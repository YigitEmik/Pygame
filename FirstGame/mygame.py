#--------------------------------------------------------------------------------------------------------------------------------------
# keys = pygame.key.get_pressed()
# player_rect.colliderect(snail_rect) # Check if there is a collision (between 2 rectangle)
# mouse_pos = pygame.mouse.get_pos() # Get mouse pos(x,y) || event.pos also gets mouse position if we use in event loop with MOUSEMOTION
# player_rect.collidepoint(mouse_pos): # Check if there is a collision (x,y)
# pygame.mouse.get_pressed() # Check if the mouse clicked (left, mid ,right)
#--------------------------------------------------------------------------------------------------------------------------------------
import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk1,player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect =  self.image.get_rect(midbottom =(80,300))
        self.gravity = 0 
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300
        
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
            
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image=self.frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100 :
            self.kill()

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    to_sec = int(current_time / 1000)
    score_surf = font.render(f'Score: {to_sec}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 100))
    screen.blit(score_surf,score_rect)
    return to_sec


def collisions(player,obstacles):
    if obstacles:
        for rectangle in obstacles:
            if player.colliderect(rectangle):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

def player_animation():
    global player_surf, player_index
    

    
    
pygame.init() # Initialize pygame.
screen = pygame.display.set_mode((800, 400)) #Creating screen.
pygame.display.set_caption("Runner") # Title
clock = pygame.time.Clock()
font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0
high_score = 0


#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()




#Tutorial Text.
tutorial_surf = font.render('Press \'Space\' to Jump', True, (64,64,64))
tutorial_rect = tutorial_surf.get_rect(center = (400,50))
tutorial_surf2 = font.render('Press \'Space\' to Run', True, (64,64,64))
tutorial_rect2 = tutorial_surf.get_rect(center = (410,300))

# Game Over text.
gameover_text = font.render('Pixel Runner', True, (64,64,64))
gameover_rect = gameover_text.get_rect(center = (400,50))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,200)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer,200)
 

#Surfaces
ground_surface = pygame.image.load("graphics\ground.png").convert()
sky_surface = pygame.image.load("graphics\sky.png").convert()

# Intro/End game screen
player_surface2 = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_surface2 = pygame.transform.scale(player_surface2,(200,200)) #Transform Player_surface2
player_rect2 = player_surface2.get_rect(center =(400,175))


#Main game loop.
while True: 
    #Event handler.
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #Lets us quit the game.
            pygame.quit()
            exit()
            
        else: #If game ends for whatever reason.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
        if game_active:        
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
                # if randint(0,2):
                #     obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100),300)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900,1100),210)))
                
    
    
    
    
    if game_active:    
        #Drawing Surfaces on screen.            
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        pygame.draw.rect(screen,"#c0e8ec",tutorial_rect)
        screen.blit(tutorial_surf,tutorial_rect)
        score = display_score()
        
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        
        #Collision
        game_active = collision_sprite()
    
    else: # Game Over Screen
        screen.fill((94, 129, 162))
        screen.blit(gameover_text, gameover_rect)
        screen.blit(tutorial_surf2, tutorial_rect2)
        screen.blit(player_surface2, player_rect2)

        score_message = font.render(f"Score: {score}", False, (64, 64, 64))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(score_message, score_message_rect)

        if score >= high_score:
            high_score = score
        score_message3 = font.render(f"Highest Score: {high_score}", False, (64, 64, 64))
        score_message_rect3 = score_message3.get_rect(center=(400, 360))
        screen.blit(score_message3, score_message_rect3)


            
        
        
        
    pygame.display.update() #Updates Screen.
    clock.tick(60)
    
    
    
    
    