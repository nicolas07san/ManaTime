import pygame, sys, random

# Iniciando Pygame
pygame.init()
clock = pygame.time.Clock()

# Configurando Tamanho da tela
screen_width = 1280
screen_height = 720
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
logo = pygame.image.load('images/ampulheta.png')
pygame.display.set_caption('ManaTime')
pygame.display.set_icon(logo)

# Escala da Tela
scale = 2
display = pygame.Surface((screen_width / scale, screen_height / scale))

#Timer
current_time = 0
dmg_time = 0
c_time = 0
l_time = 0
time = 60

# Carregando Mapa
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for lin in data:
        game_map.append(list(lin))
    return game_map


game_map = load_map('map')


class Tile(pygame.sprite.Sprite):
    def __init__(self, linha, coluna):
        super().__init__()
        self.image = pygame.image.load('images/tile.png')
        self.tile_size = 32
        x = coluna * self.tile_size
        y = linha * self.tile_size
        self.rect = pygame.Rect((x, y), (self.tile_size, self.tile_size))

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/background.png')
        self.rect = pygame.Rect((0, 0), (self.image.get_width(), self.image.get_height()))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, linha, coluna):
        pygame.sprite.Sprite.__init__(self)
        self.speedX = 1 * random.choice([-1,1])
        self.current_sprite = 0
        self.anim_speed = 0.20
        self.distance = 0

        # Animção Inimigo
        self.anim = []
        self.anim.append(pygame.image.load('images/ghost_1.png'))
        self.anim.append(pygame.image.load('images/ghost_2.png'))
        self.image = self.anim[self.current_sprite]
        self.rect = pygame.Rect((coluna * (self.image.get_width()), linha * (self.image.get_height())),
                                ((self.image.get_width()), self.image.get_height()))

    def movement(self):
        self.distance += 1
        self.rect.x += self.speedX
        if self.distance > 90:
            self.speedX = self.speedX*-1
            self.distance = 0

        if self.speedX > 0:
            self.current_sprite += self.anim_speed
            if self.current_sprite >= len(self.anim):
                self.current_sprite = 0
            self.image = self.anim[int(self.current_sprite)]
            self.image = pygame.transform.flip(self.image, True, False)

        if self.speedX < 0:
            self.current_sprite += self.anim_speed
            if self.current_sprite >= len(self.anim):
                self.current_sprite = 0
            self.image = self.anim[int(self.current_sprite)]

    def update(self):
        self.movement()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, personagem):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bullet.png')
        self.rect = pygame.Rect(personagem.rect.center, (self.image.get_width(), self.image.get_height()))
        self.speedX = 0
        self.speedY = 0
        self.shoot = False

        if player.right:
            self.image = self.image
        if player.left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.rect.centerx += self.speedX


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speedX = 3
        self.speedY = 0
        self.gravity = 0.09
        self.jumping = False
        self.m_right = False
        self.m_left = False
        self.right = True
        self.left = False
        self.jump = 1
        self.collision = False
        self.jumping = True
        self.damage = False
        self.current_sprite = 0
        self.anim_speed = 0.20

        # Carregando imagens
        self.idle = pygame.image.load('images/idle.png')
        self.air_shoot = pygame.image.load('images/jump_shoot.png')
        self.air = pygame.image.load('images/air.png')
        self.shoot = pygame.image.load('images/shoot.png')
        self.dmg = pygame.image.load('images/dmg.png')

        # Animação de correr
        self.run = []
        self.run.append(pygame.image.load('images/run_1.png'))
        self.run.append(pygame.image.load('images/run_2.png'))
        self.run.append(pygame.image.load('images/run_3.png'))

        self.image = self.idle
        self.rect = self.image.get_rect()
        self.intencao_pos = list(self.rect.center)
        self.intencao_pos = [1000,100]

    def movement(self):
        if self.m_right:
            self.intencao_pos[0] += self.speedX
            self.left = False
            self.right = True
            self.current_sprite += self.anim_speed
            if self.current_sprite >= len(self.run):
                self.current_sprite = 0
            self.image = self.run[int(self.current_sprite)]

        elif self.m_left:
            self.intencao_pos[0] -= self.speedX
            self.left = True
            self.right = False
            self.current_sprite += self.anim_speed
            if self.current_sprite >= len(self.run):
                self.current_sprite = 0
            self.image = self.run[int(self.current_sprite)]
            self.image = pygame.transform.flip(self.image, True, False)

        if self.m_left == False and self.m_right == False and self.jumping == False and self.damage == False:
            if self.right:
                self.image = self.idle
            if self.left:
                self.image = self.idle
                self.image = pygame.transform.flip(self.image, True, False)

        if self.jumping == True and bullet.shoot == True:
            if self.right:
                self.image = self.air_shoot
            if self.left:
                self.image = self.air_shoot
                self.image = pygame.transform.flip(self.image, True, False)

        elif self.jumping:
            if self.right:
                self.image = self.air
            if self.left:
                self.image = self.air
                self.image = pygame.transform.flip(self.image, True, False)

        elif bullet.shoot:
            if self.right:
                self.image = self.shoot
            if self.left:
                self.image = self.shoot
                self.image = pygame.transform.flip(self.image, True, False)

        if self.damage:
            if self.right:
                self.image = self.dmg
            if self.left:
                self.image = self.dmg
                self.image = pygame.transform.flip(self.image, True, False)

        self.speedY += self.gravity
        if self.speedY > 3:
            self.speedY = 3
        self.intencao_pos[1] += self.speedY
        if int(self.speedY) != 0:
            self.jumping = True
        if int(self.speedY) == 0:
            self.jumping = False

    def pular(self):
        self.speedY = -3
        self.intencao_pos[1] += self.speedY

    def update(self):
        self.movement()

    def autorizar_movimento(self):
        self.rect.center = self.intencao_pos

    def recusar_movimento(self):
        self.intencao_pos = list(self.rect.center)
        if not self.jumping:
            self.intencao_pos = list(self.rect.center)

    # def testa_colisao_mask(self, spr1, spr2):
    #   return pygame.sprite.collide_mask(spr1,spr2)

    def teste_colisao(self, group):
        temp = self.rect.center
        self.rect.center = self.intencao_pos
        if pygame.sprite.spritecollide(self, group, False):
            self.rect.center = temp
            self.speedY = 0
            self.recusar_movimento()
            self.collision = True
            self.jump = 1
        else:
            self.autorizar_movimento()
            self.collision = False


class Camera:

    def __init__(self, position, tamanho):
        self.window = pygame.Rect(position, tamanho)
        self.position = position
        self.offset_x = 0
        self.offset_y = 0
        self.clean_image = pygame.Surface(self.window.size)
        self.clean_image.fill('black')
        self.draw_area = pygame.Surface(self.window.size)

    def in_viewport(self, r):
        return self.window.colliderect(r)

    def move(self, pos):
        self.window.center = pos
        self.offset_x = self.window.x
        self.offset_y = self.window.y

    def start_drawing(self):
        self.draw_area.blit(self.clean_image, (0, 0))

    def paint(self, tela):
        tela.blit(self.draw_area, self.position)
        # pygame.draw.rect(tela, 'red', (self.position, self.window.size), 2)

    def draw_group(self, group):
        for s in group:
            if self.in_viewport(s.rect):
                self.draw_area.blit(s.image, (s.rect.x - self.offset_x, s.rect.y - self.offset_y))

font = pygame.font.Font('pixelart.ttf', 20)
c = 'white'

def show_time(tx, ty, color):
    time_txt = font.render("Tempo " + str(time), True, color)
    display.blit(time_txt, (tx, ty))


player = Player()
bullet = Bullet(player)
players = pygame.sprite.Group()
player.add(players)
bg = Background()
bgs = pygame.sprite.Group()
bgs.add(bg)
tiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

y = 0
for lin in game_map:
    x = 0
    for tile in lin:
        if tile == '1' or tile == '2':
            tile = Tile(y, x)
            tile.add(tiles)
        if tile == '3':
            enemy = Enemy(y, x)
            enemies.add(enemy)
        x += 1
    y += 1


cam = Camera(player.rect.topleft, ((screen_width / scale), (screen_height / scale)))

while True:

    cam.start_drawing()
    cam.draw_group(bgs)
    cam.draw_group(tiles)
    cam.draw_group(bullets)
    cam.draw_group(enemies)
    cam.draw_group(players)
    cam.paint(display)

    players.update()
    player.teste_colisao(tiles)
    bullets.update()
    enemies.update()
    cam.move(player.rect.center)

    if pygame.sprite.groupcollide(enemies, bullets, True, True):
        time += 10
        c = 'green'

    if current_time - dmg_time >= 4000:
        player.damage = False
        if pygame.sprite.groupcollide(players, enemies, False, False):
            dmg_time = pygame.time.get_ticks()
            player.damage = True
            time -= 10
            c = 'red'
            print('damage')

    for bullet in bullets:
        if bullet.rect.centerx > (player.rect.centerx + ((screen_width / scale) / 2)):
            bullet.kill()
        if bullet.rect.centerx < (player.rect.centerx - ((screen_width / scale) / 2)):
            bullet.kill()

    if current_time - l_time >= 1000:
        c = 'white'
        l_time = current_time
        time -= 1
    if time <= 0:
       pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.m_right = True
            if event.key == pygame.K_LEFT:
                player.m_left = True
            if event.key == pygame.K_UP:
                if player.jump > 0:
                    player.pular()
                    player.jump -= 1
            if event.key == pygame.K_j:
                if not player.damage:
                    bullet = Bullet(player)
                    bullet.rect.center = player.rect.center
                    bullets.add(bullet)
                    bullet.shoot = True
                    time -= 1
                    c = 'red'
                if player.right:
                    bullet.speedX = 8
                if player.left:
                    bullet.speedX = -8
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.m_left = False
            if event.key == pygame.K_RIGHT:
                player.m_right = False
            if event.key == pygame.K_j:
                bullet.shoot = False

    show_time(30, 30, c)
    current_time = pygame.time.get_ticks()
    surf = pygame.transform.scale(display, screen_size)
    screen.blit(surf, (0, 0))
    pygame.display.flip()
    clock.tick(60)

