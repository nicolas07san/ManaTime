import pygame
import sys

pygame.init()
clock = pygame.time.Clock()
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)

font = pygame.font.Font('pixelart.ttf', 48)
font2 = pygame.font.Font('pixelart.ttf', 16)

click = False


def draw_text(text, fonte, color, surface, x, y):
    textobj = fonte.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    global click
    while True:

        screen.fill('darkslategray2')
        draw_text('MANA', font, 'white', screen, 1280 / 2, 100)
        draw_text('TIME', font, 'white', screen, 1280 / 2, 150)

        color_htp = 'gray50'
        color_pb = 'gray50'
        color_c = 'gray50'

        mx, my = pygame.mouse.get_pos()

        #Play Button
        pb = pygame.Rect(50, 50, 200, 50)
        pb2 = pygame.Rect(50, 50, 210, 60)
        pb.center = (1280 / 2, (720 / 2 + 100))
        pb2.center = pb.center

        #Botão Como Jogar
        htp = pygame.Rect(50, 150, 200, 50)
        htp2 = pygame.Rect(50, 150, 210, 60)
        htp.center = (1280 / 2, (720 / 2 + 200))
        htp2.center = htp.center

        # Botão Créditos
        cb = pygame.Rect(50, 150, 200, 50)
        cb2 = pygame.Rect(50, 150, 210, 60)
        cb.center = (1280 / 2, (720 / 2 + 300))
        cb2.center = cb.center

        if pb.collidepoint(mx, my):
            color_pb = 'gray70'
            if click:
                color_pb = 'gray30'
                game()

        if htp.collidepoint(mx, my):
            color_htp = 'gray70'
            if click:
                color_htp = 'gray30'
                h2p()

        if cb.collidepoint(mx, my):
            color_c = 'gray70'
            if click:
                color_c = 'gray30'
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
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = False

        pygame.display.flip()
        clock.tick(60)


def h2p():
    global click
    running = True
    while running:
        screen.fill('darkslategray2')

        mx, my = pygame.mouse.get_pos()

        color_b = 'gray50'

        # Botão Back
        back = pygame.Rect(50, 600, 200, 50)
        back2 = pygame.Rect(50, 150, 210, 60)
        back2.center = back.center

        if back.collidepoint(mx, my):
            color_b = 'gray70'
            if click:
                color_b = 'gray30'
                main_menu()

        pygame.draw.rect(screen, 'gray9', back2)
        pygame.draw.rect(screen, color_b, back)
        draw_text('Voltar', font2, 'white', screen, back.centerx, back.centery)

        draw_text('Como Jogar', font, 'white', screen, 1280 / 2, 50)

        draw_text('Seu objetivo é chegar ao topo da torre antes do tempo acabar', font2, 'white', screen, 1280/2, 200)
        draw_text('Mate fantasmas para ganhar tempo, e evite-os para não perder tempo', font2, 'white', screen, 1280/2,
                  250)
        draw_text('Utilize as setas direcionais para se mover e J para atirar', font2, 'white', screen, 1280/2, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = False

        pygame.display.update()
        clock.tick(60)


def creditos():
    global click
    running = True
    while running:
        screen.fill('darkslategray2')

        mx, my = pygame.mouse.get_pos()

        color_b = 'gray50'

        # Botão Back
        back = pygame.Rect(50, 600, 200, 50)
        back2 = pygame.Rect(50, 150, 210, 60)
        back2.center = back.center

        if back.collidepoint(mx, my):
            color_b = 'gray70'
            if click:
                color_b = 'gray30'
                main_menu()

        pygame.draw.rect(screen, 'gray9', back2)
        pygame.draw.rect(screen, color_b, back)
        draw_text('Voltar', font2, 'white', screen, back.centerx, back.centery)

        draw_text('Créditos', font, 'white', screen, 1280 / 2, 50)

        draw_text('Programação: Nicolas Gonçalves', font2, 'white', screen, 1280 / 2, 200)
        draw_text('Arte: Lucas Canute', font2, 'white', screen, 1280 / 2, 250)
        draw_text('Sons', font2, 'white', screen, 1280 / 2, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = False

        pygame.display.update()
        clock.tick(60)


def game():
    pass


main_menu()
