#@KnightEndall
import pygame as pg
from sys import exit
from random import randint, choice

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pg.image.load("graphics/Player/player_walk_1.png").convert_alpha()

        player_walk_2 = pg.image.load("graphics/Player/player_walk_2.png").convert_alpha()

        self.player_walk = [player_walk_1,player_walk_2]

        self.player_index = 0

        self.player_jump = pg.image.load("graphics/Player/Jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        
        self.jump_sound = pg.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.15)
    def player_input(self):
        if event.type == pg.FINGERDOWN and self.rect.bottom == 300:
            self.gravity = -21
            self.jump_sound.play()
            
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pg.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == "bird":
            bird_frame1 = pg.image.load("graphics/Bird/Bird.png").convert_alpha()
            bird_frame2 = pg.image.load("graphics/Bird/Bird2.png").convert_alpha()
            self.frames = [bird_frame1, bird_frame2]
            y_pos = 200
        else:
            creature_frame1 = pg.image.load("graphics/Creature/Creature.png").convert_alpha()
            creature_frame2 = pg.image.load("graphics/Creature/Creature2.png").convert_alpha()
            self.frames = [creature_frame1, creature_frame2]
            y_pos = 300
        
        self.animation_index = 0  
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
               
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()      
        self.rect.x -= 6  
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()          
            

def display_score():
    current_time = int((pg.time.get_ticks() / 1000)) - start_time
    score_surf = font1.render(f"SCORE: {current_time}", False, "black")
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time
  
    
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(creature_surf,obstacle_rect)
            else:
                screen.blit(bird_surf,obstacle_rect)
                    
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []
  
        
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): 
                return False
    return True
  
              
def collision_sprite():
    if pg.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True         

def player_animation():
    global player_surf, player_index
    
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]
    
        
            
                    
pg.init()

# create window
screen_width = 800
screen_height = 400
#screen = pg.display.set_mode((screen_width,screen_height))
screen = pg.display.set_mode((screen_width,screen_height), pg.SCALED | pg.FULLSCREEN)
screen.fill("Grey")

pg.display.set_caption("Runner")
clock = pg.time.Clock()
game_active = True
start_time = 0
font1 = pg.font.Font("font/AbyssalHorrors.ttf",50)
score = 0

# Background Music
bg_music = pg.mixer.Sound("audio/music.wav")
bg_music.set_volume(0.15)
bg_music.play(loops = -1)
# Groups

player = pg.sprite.GroupSingle()
player.add(Player())

obstacle_group = pg.sprite.Group()

sky_surf = pg.image.load("graphics/Sky.png").convert()
sky_surf = pg.transform.scale(sky_surf, (800, 700))
ground_surf = pg.image.load("graphics/Ground.png").convert()
ground_surf = pg.transform.scale(ground_surf, (800, 300))


# Creature
creature_frame1 = pg.image.load("graphics/Creature/Creature.png").convert_alpha()
creature_frame1 = pg.transform.rotozoom(creature_frame1,0,1.1)

creature_frame2 = pg.image.load("graphics/Creature/Creature2.png").convert_alpha()
creature_frame2 = pg.transform.rotozoom(creature_frame2,0,1.1)

creature_frames = [creature_frame1, creature_frame2]
creature_frame_index = 0
creature_surf = creature_frames[creature_frame_index]

# Bird
bird_frame1 = pg.image.load("graphics/Bird/Bird.png").convert_alpha()
bird_frame2 = pg.image.load("graphics/Bird/Bird2.png").convert_alpha()

bird_frames = [bird_frame1, bird_frame2]
bird_frame_index = 0
bird_surf = bird_frames[bird_frame_index]

obstacle_rect_list = [] 

player_walk_1 = pg.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_1 = pg.transform.scale(player_walk_1, (80, 80))

player_walk_2 = pg.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk_2 = pg.transform.scale(player_walk_2, (80, 80))

player_walk = [player_walk_1,player_walk_2]

player_index = 0

player_jump = pg.image.load("graphics/Player/Jump.png").convert_alpha()
player_jump = pg.transform.rotozoom(player_jump,0,1)

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

# Intro Screen
player_stand = pg.image.load("graphics/Player/Stand.png").convert_alpha()
player_stand = pg.transform.rotozoom(player_stand,0,2.25)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_title = font1.render("Fantasy Runner", False, "black")
game_title_rect = game_title.get_rect(center = (400,35))

game_message = font1.render("Touch Screen To Run", False, "black")
game_message_rect = game_message.get_rect(center = (400,360))

# Timer
obstacle_timer = pg.USEREVENT + 1
pg.time.set_timer(obstacle_timer, 1500)

creature_animation_timer = pg.USEREVENT + 2
pg.time.set_timer(creature_animation_timer, 300)

bird_animation_timer = pg.USEREVENT + 3
pg.time.set_timer(bird_animation_timer, 200)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)
    
        if game_active:
            fingers = {}
            if event.type == pg.FINGERDOWN and player_rect.bottom == 300:
                player_gravity = -21
        else:
            if event.type == pg.FINGERDOWN:
                game_active = True
                player_rect.right = 125
                start_time = int((pg.time.get_ticks() / 1000))
          
                
        if game_active:                   
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["bird", "creature", "creature", "creature"])))
                    
            if event.type == creature_animation_timer:
                if creature_frame_index == 0:
                    creature_frame_index = 1
                else:
                    creature_frame_index = 0
                creature_surf = creature_frames[creature_frame_index]
                    
            if event.type == bird_animation_timer:
                if bird_frame_index == 0:
                    bird_frame_index = 1
                else:
                    bird_frame_index = 0
                bird_surf = bird_frames[bird_frame_index]     
            

    if game_active:
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,300))  
        score = display_score()
    
        # Player    
        player.draw(screen)
        player.update()
        
        # Obstacle
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        # Collision
        game_active = collision_sprite()

        
        
    else:
        intro_surf = pg.image.load("graphics/Intro.png").convert_alpha()
        screen.blit(intro_surf,(0,0))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        
        score_message = font1.render(f"Your Score: {score}", False, "black")
        score_message_rect = score_message.get_rect(center = (400,360))
        screen.blit(game_title,game_title_rect)
        
        if score == 0: 
            screen.blit(game_message,game_message_rect)
        else: 
            screen.blit(score_message,score_message_rect)
            
            
    pg.display.flip()
    clock.tick(60)
