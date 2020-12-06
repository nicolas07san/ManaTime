import pygame
import random
import sys
import zlib
import os


# Iniciando Pygame
pygame.init()
clock = pygame.time.Clock()


# Compressão e Descompressão
def compress():
    with open('data/images/background.png', 'rb') as imageFile:
        compressed = zlib.compress((imageFile.read()), 9)

    imagetxt = open('data/images/background.txt', 'wb')
    imagetxt.write(compressed)
    imagetxt.close()
    os.remove('data/images/background.png')


def descompress():
    read_file = open('data/images/background.txt', 'rb').read()

    decompressed = zlib.decompress(read_file)

    dimg = open('data/images/background.png', 'wb')
    dimg.write(decompressed)
    dimg.close()
    os.remove('data/images/background.txt')


# Configurando Tamanho da tela
screen_width = 1280
screen_height = 720
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
descompress()

# Logo e Nome da janela
logo = pygame.image.load('data/images/logo.png')
pygame.display.set_caption('ManaTime')
pygame.display.set_icon(logo)

# Escala da Tela
scale = 3
display = pygame.Surface((screen_width / scale, screen_height / scale))

# Timers
current_time = 0
dmg_time = 0
c_time = 0
l_time = 0

win = False
lose = False

pop_sound = pygame.mixer.Sound('data/sounds/pop.wav')


# Carregando Mapa
def load_map(path):
    f = open('data/' + path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for lin in data:
        game_map.append(list(lin))
    return game_map


game_map = load_map('map')


# Classes
class Tile(pygame.sprite.Sprite):
    def __init__(self, linha, coluna):
        super().__init__()
        self.image = pygame.image.load('data/images/tile.png')
        self.tile_size = 32
        x = coluna * self.tile_size
        y = linha * self.tile_size
        self.rect = pygame.Rect((x, y), (self.tile_size, self.tile_size))


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/images/background.png')
        self.rect = pygame.Rect((0, 0), (self.image.get_width(), self.image.get_height()))


class Ampulheta(pygame.sprite.Sprite):
    def __init__(self, linha, coluna):
        super().__init__()
        self.image = pygame.image.load('data/images/ampulheta.png')
        self.rect = pygame.Rect((coluna * (self.image.get_width()), linha * (self.image.get_height())),
                                (self.image.get_width(), self.image.get_height()))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, linha, coluna):
        pygame.sprite.Sprite.__init__(self)
        self.speedX = 1 * random.choice([-1, 1])
        self.current_sprite = 0
        self.anim_speed = 0.20
        self.distance = 0

        # Animção Inimigo
        self.anim = []
        self.anim.append(pygame.image.load('data/images/ghost_1.png'))
        self.anim.append(pygame.image.load('data/images/ghost_2.png'))
        self.image = self.anim[self.current_sprite]
        self.rect = pygame.Rect((coluna * (self.image.get_width()), linha * (self.image.get_height())),
                                (32, 32))

    def movement(self):
        self.distance += 1
        self.rect.x += self.speedX
        if self.distance > 90:
            self.speedX = self.speedX * -1
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
        self.image = pygame.image.load('data/images/bullet.png')
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
        self.damage = False
        self.current_sprite = 0
        self.anim_speed = 0.20

        self.j_sound = pygame.mixer.Sound('data/sounds/jump.wav')
        self.k_sound = pygame.mixer.Sound('data/sounds/kill.wav')
        self.s_sound = pygame.mixer.Sound('data/sounds/shoot.wav')

        # Carregando imagens
        self.idle = pygame.image.load('data/images/idle.png')
        self.air_shoot = pygame.image.load('data/images/jump_shoot.png')
        self.air = pygame.image.load('data/images/air.png')
        self.shoot = pygame.image.load('data/images/shoot.png')
        self.dmg = pygame.image.load('data/images/dmg.png')

        # Animação de correr
        self.run = []
        self.run.append(pygame.image.load('data/images/run_1.png'))
        self.run.append(pygame.image.load('data/images/run_2.png'))
        self.run.append(pygame.image.load('data/images/run_3.png'))

        self.image = self.idle
        self.rect = self.image.get_rect()
        self.intencao_pos = list(self.rect.center)
        self.intencao_pos = [64, 1312]

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
        self.jump -= 1
        self.j_sound.play()

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
        self.clean_image.fill('darkslategray4')
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


font = pygame.font.Font('data/pixelart.ttf', 48)
font2 = pygame.font.Font('data/pixelart.ttf', 16)

click = False

player = Player()


def draw_text(text, fonte, color, surface, x, y):
    textobj = fonte.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    global click, pop_sound, s

    while True:
        s = False
        screen.fill('darkslategray4')
        draw_text('MANA', font, 'white', screen, screen_width / 2, 100)
        draw_text('TIME', font, 'white', screen, screen_width / 2, 150)

        color_htp = 'gray50'
        color_pb = 'gray50'
        color_c = 'gray50'

        mx, my = pygame.mouse.get_pos()

        # Play Button
        pb = pygame.Rect(50, 50, 200, 50)
        pb2 = pygame.Rect(50, 50, 210, 60)
        pb.center = (screen_width / 2, (screen_height / 2 + 100))
        pb2.center = pb.center

        # Botão Como Jogar
        htp = pygame.Rect(50, 150, 200, 50)
        htp2 = pygame.Rect(50, 150, 210, 60)
        htp.center = (screen_width / 2, (screen_height / 2 + 200))
        htp2.center = htp.center

        # Botão Créditos
        cb = pygame.Rect(50, 150, 200, 50)
        cb2 = pygame.Rect(50, 150, 210, 60)
        cb.center = (screen_width / 2, (screen_height / 2 + 300))
        cb2.center = cb.center

        if pb.collidepoint(mx, my):
            color_pb = 'gray70'
            if click:
                pop_sound.play()
                game()

        if htp.collidepoint(mx, my):
            color_htp = 'gray70'
            if click:
                pop_sound.play()
                h2p()

        if cb.collidepoint(mx, my):
            color_c = 'gray70'
            if click:
                pop_sound.play()
                creditos()

        pygame.draw.rect(screen, 'gray9', pb2)
        pygame.draw.rect(screen, color_pb, pb)
        draw_text('Jogar', font2, 'white', screen, pb.centerx, pb.centery)

        pygame.draw.rect(screen, 'gray9', htp2)
        pygame.draw.rect(screen, color_htp, htp)
        draw_text('Como Jogar', font2, 'white', screen, htp.centerx, htp.centery)

        pygame.draw.rect(screen, 'gray9', cb2)
        pygame.draw.rect(screen, color_c, cb)
        draw_text('Créditos', font2, 'white', screen, cb.centerx, cb.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                compress()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = False

        pygame.display.flip()
        clock.tick(60)


def h2p():
    global click, pop_sound
    running = True
    while running:
        screen.fill('darkslategray4')

        mx, my = pygame.mouse.get_pos()

        color_b = 'gray50'

        # Botão Back
        back = pygame.Rect(50, 600, 200, 50)
        back2 = pygame.Rect(50, 150, 210, 60)
        back2.center = back.center

        if back.collidepoint(mx, my):
            color_b = 'gray70'
            if click:
                pop_sound.play()
                main_menu()

        pygame.draw.rect(screen, 'gray9', back2)
        pygame.draw.rect(screen, color_b, back)
        draw_text('Voltar', font2, 'white', screen, back.centerx, back.centery)

        draw_text('Como Jogar', font, 'white', screen, screen_width / 2, 50)

        draw_text('Seu objetivo é chegar ao topo da torre antes do tempo acabar', font2, 'white', screen,
                  screen_width / 2, 200)
        draw_text('Mate fantasmas para ganhar tempo, e evite-os para não perder tempo', font2, 'white', screen,
                  screen_width / 2,
                  250)
        draw_text('Utilize as setas direcionais para se mover e J para atirar', font2, 'white', screen,
                  screen_width / 2, 300)
        draw_text('E lembre-se atirar consome tempo', font2, 'white', screen, screen_width / 2, 350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                compress()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = False

        pygame.display.update()
        clock.tick(60)


def creditos():
    global click, pop_sound
    running = True
    while running:
        screen.fill('darkslategray4')

        mx, my = pygame.mouse.get_pos()

        color_b = 'gray50'

        # Botão Back
        back = pygame.Rect(50, 600, 200, 50)
        back2 = pygame.Rect(50, 150, 210, 60)
        back2.center = back.center

        if back.collidepoint(mx, my):
            color_b = 'gray70'
            if click:
                pop_sound.play()
                main_menu()

        pygame.draw.rect(screen, 'gray9', back2)
        pygame.draw.rect(screen, color_b, back)
        draw_text('Voltar', font2, 'white', screen, back.centerx, back.centery)

        draw_text('Créditos', font, 'white', screen, screen_width / 2, 50)

        draw_text('Programação: Nicolas Gonçalves', font2, 'white', screen, screen_width / 2, 200)
        draw_text('Arte: Lucas Canute', font2, 'white', screen, screen_width / 2, 250)
        draw_text('Musica: Misty Dungeon, from PlayOnLoop.com ', font2, 'white', screen, screen_width / 2, 300)
        draw_text('Licenciado sob Creative Commons por Atribuição 4.0 ', font2, 'white', screen, screen_width / 2, 350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                compress()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = False

        pygame.display.update()
        clock.tick(60)


def game():
    global bullet, l_time, dmg_time, current_time, click, win, lose

    music = pygame.mixer.Sound('data/sounds/game.wav')
    music.set_volume(10)
    music.play(-1)

    win = False
    lose = False

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
    amps = pygame.sprite.Group()

    player.intencao_pos = [64, 1312]
    time = 30

    def show_time(tx, ty, color):
        time_txt = font2.render("Tempo " + str(time), True, color)
        display.blit(time_txt, (tx, ty))

    click = False

    c = 'white'
    y = 0
    for lin in game_map:
        x = 0
        for tile in lin:
            if tile == 'C':
                tile = Tile(y, x)
                tile.add(tiles)
            if tile == 'E':
                enemy = Enemy(y, x)
                enemies.add(enemy)
            if tile == 'W':
                amp = Ampulheta(y, x)
                amps.add(amp)
            x += 1
        y += 1

    cam = Camera(player.rect.topleft, ((screen_width / scale), (screen_height / scale)))

    running = True
    while running:
        cam.start_drawing()
        cam.draw_group(bgs)
        cam.draw_group(tiles)
        cam.draw_group(bullets)
        cam.draw_group(enemies)
        cam.draw_group(amps)
        cam.draw_group(players)
        cam.paint(display)

        players.update()
        player.teste_colisao(tiles)
        bullets.update()
        enemies.update()
        cam.move(player.rect.center)

        if pygame.sprite.groupcollide(enemies, bullets, True, True):
            player.k_sound.play()
            time += 5
            c = 'green'

        if pygame.sprite.groupcollide(amps, players, False, False):
            win = True
            music.stop()
            running = False
            endgame()

        if current_time - dmg_time >= 4000:
            player.damage = False
            if pygame.sprite.groupcollide(players, enemies, False, False):
                dmg_time = pygame.time.get_ticks()
                player.damage = True
                time -= 10
                c = 'red'

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
            music.stop()
            lose = True
            running = False
            endgame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                compress()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.m_right = True
                if event.key == pygame.K_LEFT:
                    player.m_left = True
                if event.key == pygame.K_UP:
                    if player.jump > 0:
                        player.pular()
                if event.key == pygame.K_j:
                    if not player.damage:
                        bullet = Bullet(player)
                        bullet.rect.center = player.rect.center
                        bullets.add(bullet)
                        bullet.shoot = True
                        player.s_sound.play()
                        time -= 1
                        c = 'red'
                    if player.right:
                        bullet.speedX = 8
                    if player.left:
                        bullet.speedX = -8
                if event.key == pygame.K_ESCAPE:
                    music.stop()
                    main_menu()
                    running = False

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


def endgame():
    global click, win, lose
    running = True
    while running:
        screen.fill('darkslategray4')

        mx, my = pygame.mouse.get_pos()

        color_b = 'gray50'

        color_j = 'gray50'

        # Botão Back
        back = pygame.Rect(50, 600, 200, 50)
        back2 = pygame.Rect(0, 0, 210, 60)
        back2.center = back.center

        # Botão Jogar Novamente
        jn = pygame.Rect(930, 600, 300, 50)
        jn2 = pygame.Rect(0, 0, 310, 60)
        jn2.center = jn.center

        # Botão Menu
        if back.collidepoint(mx, my):
            color_b = 'gray70'
            if click:
                pop_sound.play()
                main_menu()

        # Botão Jogar Novamente
        if jn.collidepoint(mx, my):
            color_j = 'gray70'
            if click:
                pop_sound.play()
                game()

        # Draw Jogar Novamente
        pygame.draw.rect(screen, 'gray9', jn2)
        pygame.draw.rect(screen, color_j, jn)
        draw_text('Jogar Novamente', font2, 'white', screen, jn.centerx, jn.centery)

        # Draw Menu
        pygame.draw.rect(screen, 'gray9', back2)
        pygame.draw.rect(screen, color_b, back)
        draw_text('Menu', font2, 'white', screen, back.centerx, back.centery)

        # Mensagem de vitória
        if win:
            draw_text('PARABENS VOCÊ VENCEU!', font, 'white', screen, screen_width / 2, 50)
        if lose:
            draw_text('Que pena você perdeu...', font, 'white', screen, screen_width / 2, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                compress()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = False

        pygame.display.update()
        clock.tick(60)


main_menu()
