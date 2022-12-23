import random
import pygame
pygame.init()
clock = pygame.time.Clock()
from pygame import mixer
mixer.init()



FPS = 60
GRAVITY = 0.5
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
screen_width = 1800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))



coin_collision = False
walking_left = False
walking_right = False
jumping_up = False
attack = False

city = pygame.image.load('city.jpg').convert_alpha()
city_transformed = pygame.transform.scale(city, (screen_width, screen_height))
city_rect = city_transformed.get_rect()
city_flipped = pygame.transform.flip(city_transformed, True, False)
is_alive = True
clicked_start = False
font_style = pygame.font.Font('greed.ttf', 30)
def menu_func():
    if clicked_start == False:
        screen.fill('black')
        start_bitton = pygame.Rect(660,373,500,70)
        menu_colour = (0,255,0)
        game_title = font_style.render('[ press space to start] ', False, 'white')
        menu_rect = game_title.get_rect(center=(screen_width/2, screen_height / 2))
        pygame.draw.rect(screen, menu_colour, start_bitton)
        screen.blit(game_title, menu_rect)





mixer.music.load("main.wav")
mixer.music.set_volume(0.5)
mixer.music.play(-1)





level_map = [
    '                           ',
    '                          ',
    '       B              C      XXXXXXXX            XXXX XXXXXXX XXXXXXXXXXXXX',
    ' XX   XXX            XX    XXXX XXX     XXXXX  XXXXXXXXXXX    XXXXXXXXXXXXXXXXX    XXXXXXXXXXXXX     XX',
    ' XX CC  XXXXXX         XXXXXXXXXXXXXXXXXXXXXXXXXXXX    X XXXXXXXXXXX XXXXXXXXXXXX XXXXXXXXX X X  '      
    '   XXXXXX  PP    CC XXXXXXX          XXXX  P XXXXXXXXXXXX  XXXXX  XXXXXXXXXXXXXX XXXXXXXXXXXXXX X  X X  XXXXXXXXXXXX XXXXXX XXXXXXXXXXXX XXXXXXX X X  X X XXXXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX X X   XXXXXXXXXX    X X           X X X   XXXXXXXXX        XXXXXXXXXXXXXX X X       XXXXXXXXXXXXXX X X             X X X         XXXXXXXXXXXX X X X XXXXXXXXXX X X     X   XXXXXXXXXXX XX',
    'XXXXX          XX P     XXCCX         XCCXXX   XXXXXX     XXXXXX      XXXXXXXXX     P XXX XXXXXXXXXXX  XXXXXXXXXXXXX X XX       X XX X X X  XXXXXXXXXXXX XXXXXXXXXX XXXXXXXXXXXXX X  X XXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXX X  XXXXXXXXXXXX XXXXXXXXXX X XXXXXXXXXXX X X       XXXXXXXXXXXXXXXXXXXXX X  X XXXXXXXXXXXXXXXXXX',
    'XXXXX       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     CC    CC   XXXXXXXXXXX     XXXXXXXXXXXXXX     XXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXX  XXXXXXX  CCCCCC',
    ' LLLLLLLLLLLLLLLLLLLLLLLLL     '
    '             LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL']


if walking_right:
    dojo=pygame.image.load('other.png').convert_alpha()
    dojo=pygame.transform.scale(dojo,(screen_width,screen_height))
else:
    dojo = pygame.image.load('dojo.png').convert_alpha()
    dojo = pygame.transform.scale(dojo, (screen_width, screen_height))
def draw_background():
    screen.blit(dojo, (xv-dojo.get_rect().width,0))

x=0


class Tiles(pygame.sprite.Sprite):
    def __init__(self, data):
        pygame.sprite.Sprite.__init__(self)
        self.offsetX = 0
        self.offsetY = 0
        self.world_shift_y =5
        self.world_shift = 0
        self.is_alive = True
        self.platforms = []
        self.score_value = 0
        self.dirt_bg = pygame.image.load('rock tile.png').convert_alpha()
        self.lava = pygame.image.load("lava.jpg").convert_alpha()
        y_position = 0

        # this for loop reads each value in the level_map list and appends an image at the location of the value 'X' in the list

        for row in data:
            x_position = 0
            for tile in row:
                if tile == 'X':
                    self.dirt_bg = pygame.transform.scale(self.dirt_bg, (154, 154))
                    self.dirt_bg_rect = self.dirt_bg.get_rect()
                    self.dirt_bg_rect.x = x_position * 104
                    self.dirt_bg_rect.y = y_position * 104
                    block = (self.dirt_bg, self.dirt_bg_rect)
                    self.platforms.append(block)

                x_position += 1
            y_position += 1

    def draw_tile(self, player):
        if clicked_start == True:
            for tile_1 in self.platforms:
                screen.blit(tile_1[0], tile_1[1])
                #tile_1[1] represents the rect of the tile and we increment the x position of the tile by a number
                tile_1[1].x += self.world_shift


    def scroll_x(self, player):
        if player_create.is_Player == True:
            player_x = player.rect.centerx
            direction_x = player.direction.x

            if player_x < 100 and direction_x < 0 and walking_left:
                self.world_shift = 8
                player.movement_speed = 0

            elif player_x > 1600 and direction_x > 0 and walking_right:
                self.world_shift = -8
                player.movement_speed = 0

            else:
                self.world_shift = 0
                player.movement_speed = 8


    def game_text(self, player):

        # this functions handles the crucial text within the game while it is running

        font_style = pygame.font.Font('greed.ttf', 50)
        game_title = font_style.render('Greed Island', False, 'Red')
        game_title_rect = game_title.get_rect(center=(screen_width / 2, screen_height / 6))
        screen.blit(game_title, game_title_rect)

        score = font_style.render("Score: " + str(self.score_value), True, 'Black')
        screen.blit(score, (1500, 50))

        font_style2 = pygame.font.Font('greed.ttf', 40)
        health = font_style2.render('Health', False, 'Black')
        screen.blit(health, (20, 20))

tile = Tiles(level_map)

class Nen(pygame.sprite.Sprite):
    def __init__(self, data):
        self.offsetX = 0
        self.list_of_animation_in_array = []
        self.offsetY = 0
        self.action = 0
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        self.world_shift = 0
        pygame.sprite.Sprite.__init__(self)
        self.platforms = []
        self.lava = pygame.image.load("book1.png").convert_alpha()
        self.lava = pygame.transform.scale(self.lava,(102,102))

        y_position = 0
        for row in data:
            x_position = 0
            for tile in row:
                if tile == 'B':
                    self.dirt_bg = pygame.transform.scale(self.lava, (102, 102))
                    self.lava_rect = self.lava.get_rect()
                    self.lava_rect.x = x_position * 102
                    self.lava_rect.y = y_position * 102
                    lava = (self.lava, self.lava_rect)
                    self.platforms.append(lava)

                x_position += 1
            y_position += 1


    def draw_tile(self, player):
        if clicked_start == True:

            for tile_1 in self.platforms:
                screen.blit(tile_1[0], tile_1[1])
                tile_1[1].x += self.world_shift

    def scroll_x(self, player):


            if player_create.is_Player == True:
                player_x = player.rect.centerx
                direction_x = player.direction.x

                if player_x < 100 and direction_x < 0 and walking_left:
                    self.world_shift = 8
                    player.movement_speed = 0
                elif player_x > 1600 and direction_x > 0 and walking_right:
                    self.world_shift = -8
                    player.movement_speed = 0
                else:
                    self.world_shift = 0
                    player.movement_speed = 8
upgrades_create = Nen(level_map)

class Lava(Tiles):
    def __init__(self, data):
        self.offsetX = 0
        self.offsetY = 0
        self.world_shift = 0
        pygame.sprite.Sprite.__init__(self)
        self.platforms = []
        self.lava = pygame.image.load("lava.jpg").convert_alpha()

        y_position = 0
        for row in data:
            x_position = 0
            for tile in row:
                if tile == 'L':
                    self.dirt_bg = pygame.transform.scale(self.lava, (102, 102))
                    self.lava_rect = self.lava.get_rect()
                    self.lava_rect.x = x_position * 102
                    self.lava_rect.y = y_position * 102
                    lava = (self.lava, self.lava_rect)
                    self.platforms.append(lava)

                x_position += 1
            y_position += 1

    def draw_tile(self, player):
        if clicked_start:

            for tile_1 in self.platforms:
                screen.blit(tile_1[0], tile_1[1])
                tile_1[1].x += self.world_shift

    def scroll_x(self, player):

            player_x = player.rect.centerx
            direction_x = player.direction.x

            if player_x < 100 and direction_x < 0 and walking_left:
                self.world_shift = 8
                player.movement_speed = 0

            elif player_x > 1600 and direction_x > 0 and walking_right:
                self.world_shift = -8
                player.movement_speed = 0

            else:
                self.world_shift = 0
                player.movement_speed = 8

lava_create = Lava(level_map)

class Coins(pygame.sprite.Sprite):
    def __init__(self, data):
        pygame.sprite.Sprite.__init__(self)
        self.platforms = []

        self.coins_bg = pygame.image.load('4.png').convert_alpha()

        y_position = 0
        for row in data:
            x_position = 0
            for tile in row:
                if tile == 'P':
                    self.enemy = pygame.transform.scale(self.coins_bg, (30, 30))
                    self.enemy_rect = self.enemy.get_rect()
                    self.enemy_rect.x = x_position * 102
                    self.enemy_rect.y = y_position * 102
                    enemy = (self.enemy, self.enemy_rect)

                    self.platforms.append(enemy)

                x_position += 1
            y_position += 1

    def draw_tile(self, player, tiles):
        if clicked_start == True:

            for tile_1 in self.platforms:
                screen.blit(tile_1[0], tile_1[1])
                tile_1[1].x += tiles.world_shift
coin_create = Coins(level_map)


class Player(pygame.sprite.Sprite):
    def __init__(self, p_or_e, x, y, displacement):
        pygame.sprite.Sprite.__init__(self)
        self.list_of_animation_in_array = []
        self.movement_speed = 10
        self.current_choice = 0
        self.is_Player = False
        self.list_choice = 0
        self.jump = 0
        self.lava_dead = False
        self.is_alive = True
        self.move_delay = 0
        self.cooldown_time_Animation = 0
        self.direction = pygame.math.Vector2(0, 0)
        self.status = 'Idle'
        self.times_walk = 0
        self.angry_state = False
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.p_or_e = p_or_e
        self.flip_image = False
        self.health = 200
        self.axis = 1
        self.displacement = displacement

        self.update_time = pygame.time.get_ticks()
       # each animation group list is given its own my_list
        my_list = []
        self.current_x = 0
        self.attack = True
        # here, a for loop is used is used to loop through a collection of files within the game
        for i in range(4):
            character = pygame.image.load(f"{p_or_e}{i}idle.png").convert_alpha()
            character = pygame.transform.scale(character, (100, 150))
            my_list.append(character)
        # the list  is appended into a greater animation list
        self.list_of_animation_in_array.append(my_list)

        my_list = []
        for i in range(5):
            character = img = pygame.image.load(f'{p_or_e}{i}run.png').convert_alpha()
            character = pygame.transform.scale(character, (100, 150))
            my_list.append(character)

        self.list_of_animation_in_array.append(my_list)

        my_list = []
        for i in range(1,2):
            character = img = pygame.image.load(f'{p_or_e}attack{i}.png').convert_alpha()
            character = pygame.transform.scale(character, (100, 150))
            my_list.append(character)
        self.list_of_animation_in_array.append(my_list)

        my_list = []
        for i in range(2,4):
            character = pygame.image.load(f'{p_or_e}{i}angry.png').convert_alpha()
            character = pygame.transform.scale(character, (100, 550))
            my_list.append(character)
        self.list_of_animation_in_array.append(my_list)

        my_list = []
        for i in range(3,4):
            character = pygame.image.load(f'{p_or_e}1attack{i}.png').convert_alpha()
            character = pygame.transform.scale(character, (100, 550))
            my_list.append(character)
        self.list_of_animation_in_array.append(my_list)

        # the characters image is set to the index of the animation list and the list choice. This will allow for the image to constantly change depending on the character's actions
        self.image = self.list_of_animation_in_array[self.current_choice][self.list_choice]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        if self.p_or_e == 'p':
            self.is_Player = True
        else:
            self.is_Player = False

    def movement(self, walking_left, walking_right):
        if clicked_start:
            if walking_left == True:
                # the players' x value which they are being displayed on, is incremented by the speed of the player
                self.rect.x -= self.movement_speed
                self.flip_image = True
                self.axis = -1
                self.direction.x = -1
            if walking_right == True:
                self.rect.x += self.movement_speed

                self.flip_image = False
                self.axis = 1
                self.direction.x = 1

    def jumping(self):
        if jumping_up == True:
            self.jump = -5
            self.rect.y += self.jump
            self.rect.y += self.jump - 15
        if self.rect.y == 600:
            self.rect.y = 600

    def update_animation(self):
        # i have two different animation cooldowns for my character when he has collected an upgrade
        if self.angry_state == False:
            self.cooldown_time_Animation = 100 # here its 100
            self.image = self.list_of_animation_in_array[self.current_choice][self.list_choice]
            if pygame.time.get_ticks() - self.update_time > self.cooldown_time_Animation:
                self.update_time = pygame.time.get_ticks()
                self.list_choice += 1
            if self.list_choice >= len(self.list_of_animation_in_array[self.current_choice]):
                self.list_choice = 0
            if self.on_ground and self.on_right:
                self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
            elif self.on_ground and self.on_left:
                self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
            elif self.on_ground:
                self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            elif self.on_ceiling and self.on_right:
                self.rect = self.image.get_rect(topright=self.rect.topright)
            elif self.on_ceiling and self.on_left:
                self.rect = self.image.get_rect(topleft=self.rect.topleft)
            elif self.on_ceiling:
                self.rect = self.image.get_rect(midtop=self.rect.midtop)
        else:
            # there is a "delay" between animations which judges how slow the transition between one sprite image and the next
            self.cooldown_time_Animation = 250 # here its 250
            self.image = self.list_of_animation_in_array[self.current_choice][self.list_choice]
            if pygame.time.get_ticks() - self.update_time > self.cooldown_time_Animation:
                self.update_time = pygame.time.get_ticks()
                self.list_choice += 1
            if self.list_choice >= len(self.list_of_animation_in_array[self.current_choice]):
                self.list_choice = 0

            # Using a series of if statements, the players coordinates are set to certain values if a certian condition if met.
            if self.on_ground and self.on_right:
                self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
            elif self.on_ground and self.on_left:
                self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
            elif self.on_ground:
                self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            elif self.on_ceiling and self.on_right:
                self.rect = self.image.get_rect(topright=self.rect.topright)
            elif self.on_ceiling and self.on_left:
                self.rect = self.image.get_rect(topleft=self.rect.topleft)
            elif self.on_ceiling:
                self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def override_currentAction(self, new_action):
        if new_action != self.current_choice:
            self.current_choice = new_action
            self.list_choice = 0
            self.update_time = pygame.time.get_ticks()

    # This function handles the collision in the x-axis by using an iterative loop to check what the player is colliding with. Furthermore, it sets the player's x value to the right hand side or the left hand side of the block depeneding on the player's direction
    def collision_x(self, tiles):

        for tile_1 in tiles.platforms:
            if tile_1[1].colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = tile_1[1].right
                    self.on_left = True
                    self.current_x = self.rect.left
                elif self.direction.x > 0:
                    self.rect.right = tile_1[1].left
                    self.on_right = True
                    self.current_x = self.rect.right
        if self.on_left and (self.rect.left < self.current_x or self.direction.x >= 0):
            self.on_left = False
        if self.on_right and (self.rect.right > self.current_x or self.direction.x <= 0):
            self.on_right = False

    # This function handles the collision in the y-axis by using an iterative loop to check through the tile map and using a series of conditions to reassign new new values to the player's coordinates
    def collison_y(self, tiles):
        self.direction.y += GRAVITY
        self.rect.y += self.direction.y

        for tile_1 in tiles.platforms:
            if tile_1[1].colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile_1[1].top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:
                    self.rect.top = tile_1[1].bottom
                    self.direction.y = 0
                    self.on_ceiling = True
        if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
            self.on_ground = False
        if self.on_ceiling and self.direction.y > 0:
            self.on_ceiling = False
#this is similar to the previous collision functions however the character doesnt have to split it into x and y axis. The players health is decremented by 5 as it collides with the lava
    def collison_y_lava(self, lava):

        for tile_1 in lava.platforms:
            if tile_1[1].colliderect(self.rect):
                self.health -= 5
                self.lava_dead = True

               # self.health -= 1
                if self.direction.y > 0:
                    self.rect.bottom = tile_1[1].top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:
                    self.rect.top = tile_1[1].bottom
                    self.direction.y = 0
                    self.on_ceiling = True
            else:
                self.lava_dead = False
        if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
            self.on_ground = False
        if self.on_ceiling and self.direction.y > 0:
            self.on_ceiling = False

    def collison_coins(self, coins, tiles):
        for tile_1 in (coins.platforms):
            if tile_1[1].colliderect(self.rect):
                tiles.score_value += 1
                coins.platforms.remove(tile_1)
                self.angry_state = False


    def collision_book(self,nen):
        for tile_1 in nen.platforms:
            if tile_1[1].colliderect(self.rect):
                nen.platforms.remove(tile_1)
                self.angry_state = True

   # def collison_with_enemy(self,enemy):
       # if self.rect.colliderect(enemy.rect):
        #    self.health -=1

    def player_health(self):
        pygame.draw.rect(screen, 'red', (20, 70, 200, 5))
        pygame.draw.rect(screen, 'green', (20, 70, self.health, 5))
        if self.rect.y> screen_height:
            self.health= 0
            self.rect.y = random.randint(0,screen_height-200)


    def create_bullet(self,player):
        if player_create.angry_state == False:
            return Bullet(self.rect.x+100,self.rect.y+50)
        else:
            now = pygame.time.get_ticks()
            if now - self.cooldown_time_Animation:
                self.cooldown_time_Animation = now
                return Bullet(self.rect.x+50,self.rect.y+430)

    def create_enemy(self):
        if is_alive:
            return Enemy(random.randint(0,screen_width),0)



    def draw(self):
        if clicked_start == True:
            #if self.health>0:
                screen.blit(pygame.transform.flip(self.image, self.flip_image, False), self.rect)



player_create = Player('p', 1350, 500, 400)



class Bullet(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load("bullet1.png")
        self.image = pygame.transform.scale(self.image,(64,64))
        self.rect =  self.image.get_rect(center = (x_pos,y_pos))

    def update(self,player,tiles):

        self.rect.x +=14
        self.rect.y+=1




        if self.rect.x >= screen_width +200:
            self.kill()

        for tile_1 in tiles.platforms:
            if self.rect.colliderect(tile_1[1]):
                if player_create.angry_state == False:
                    self.kill()
                else:
                    tiles.platforms.remove(tile_1)




        if player_create.angry_state == True:
            self.image = pygame.image.load("bigger_bullet.png")
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.rect.x+=14
            self.rect.y+=1

bullet_group = pygame.sprite.Group()




class Enemy(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load("e0idle.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.direction = pygame.math.Vector2(0,0)
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.speed = 5

    def update(self, player, tiles):

        #self.rect.x += 14
        self.rect.y += 1

        if self.rect.x >= screen_width + 200:
            self.kill()



        for tile_1 in tiles.platforms:
            if tile_1[1].colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = tile_1[1].right
                    self.on_left = True
                    self.current_x = self.rect.left
                elif self.direction.x > 0:
                    self.rect.right = tile_1[1].left
                    self.on_right = True
                    self.current_x = self.rect.right
        if self.on_left and (self.rect.left < self.current_x or self.direction.x >= 0):
            self.on_left = False
        if self.on_right and (self.rect.right > self.current_x or self.direction.x <= 0):
            self.on_right = False

        # This function handles the collision in the y-axis by using an iterative loop to check through the tile map and using a series of conditions to reassign new new values to the player's coordinates


        self.direction.y += GRAVITY
        self.rect.y += self.direction.y
        for tile_1 in tiles.platforms:
            if tile_1[1].colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile_1[1].top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:
                    self.rect.top = tile_1[1].bottom
                    self.direction.y = 0
                    self.on_ceiling = True
        if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
            self.on_ground = False
        if self.on_ceiling and self.direction.y > 0:
            self.on_ceiling = False


            # The enemy has a very simple ai where it follows the player and attacks when in close proximity with the player depending on the players' direction. This is done through a series of if statements to check the player's positiion relative to the enemy
        if self.rect.x < player_create.rect.x + 150 and player_create.direction.x == 1:
                self.rect.x += self.speed

                self.flip_image = False
        elif self.rect.x > player_create.rect.x + 150 and player_create.direction.x == 1:
                self.rect.x -= self.speed
                self.flip_image = True
        elif self.rect.x < player_create.rect.x + 150 and player_create.direction.x == -1:
                self.rect.x += self.speed
                self.flip_image = False
        else:

            if self.rect.x > player_create.rect.x + 150 and player_create.direction.x == -1:
                    self.rect.x -= self.speed
                    self.flip_image = True

        if pygame.sprite.groupcollide(bullet_group,enemy_group,False,True):
            player_create.health -=1





enemy_group = pygame.sprite.Group()
if is_alive == False:
    clicked_start = True

while True:



    xv = x % dojo.get_rect().width

    if xv < screen_width:
        screen.blit(dojo, (xv, 0))

    draw_background()
    x -= 1

    menu_func()



    clock.tick(FPS)
    # uses an interative loop to check if an event has happened
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                walking_left = True

                flip_image = True
            if event.key == pygame.K_d:
                walking_right = True
            if event.key == pygame.K_w:
                jumping_up = True
                jump_sfx = True
            if event.key == pygame.K_SPACE:
                if clicked_start == False:
                    clicked_start = True


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                walking_left = False
            if event.key == pygame.K_d:
                walking_right = False
            if event.key == pygame.K_w:
                jumping_up = False
            if event.key == pygame.K_e:
                attack = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_create.flip_image == False:
                attack = True
                bullet_group.add(player_create.create_bullet(player_create))
                enemy_group.add(player_create.create_enemy())


        if event.type == pygame.MOUSEBUTTONUP:
            attack = False




# calls to functions within classes
    player_create.draw()
    player_create.update_animation()
    player_create.movement(walking_left, walking_right)
    player_create.jumping()
    player_create.collision_x(tile)
    player_create.collison_y(tile)
    player_create.collison_y_lava(lava_create)
    player_create.collison_coins(coin_create, tile)
    player_create.collision_book(upgrades_create)
    player_create.player_health()
    player_create.create_enemy()
   # player_create.collison_with_enemy()
    #player_create.healthfunction()

    tile.draw_tile(player_create)
    tile.scroll_x(player_create)
    tile.update()
    tile.game_text(player_create)



    lava_create.draw_tile(player_create)
    #lava_create.scroll_x(player_create, attacker_create)

    upgrades_create.draw_tile(player_create)
    upgrades_create.scroll_x(player_create)

    coin_create.draw_tile(player_create, tile)

    bullet_group.draw(screen)
    bullet_group.update(player_create, tile)

    enemy_group.draw(screen)
    enemy_group.update(player_create,tile)
    #enemy_group.c


# The players' animation state is changed if a certain if confition is met. This is done inside the while loop so that the player's animation state can be "instantly" updated after meeting a condition
    if player_create.angry_state == True and attack == True:
        player_create.override_currentAction(4)
    elif player_create.angry_state == True and attack!= True :
        player_create.override_currentAction(3)

    elif walking_left or walking_right:
        player_create.override_currentAction(1)

    elif attack == True and walking_right == False :
        player_create.override_currentAction(2)
    elif attack == False:
        player_create.override_currentAction(0)

    else:
         player_create.override_currentAction(0)

    if player_create.health <= 0:
        clicked_start = False
        player_create.rect.x = random.randint(500,screen_width)

        player_create.health = 200





    pygame.display.update()
