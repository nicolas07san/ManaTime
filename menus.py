import pygame, sys

pygame.init()
clock = pygame.time.Clock()
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)

font = pygame.font.Font('pixelart.ttf', 20)

click = False


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    global click
    while True:

        screen.fill('black')
        draw_text('Main Menu', font, 'white', screen, 10, 10)

        color_game = 'gray18'
        color_opt = 'gray18'

        mx, my = pygame.mouse.get_pos()

        opt_buttom = pygame.Rect(50, 50, 100, 50)
        game_buttom = pygame.Rect(50, 150, 100, 50)

        if opt_buttom.collidepoint(mx, my):
            color_opt = 'gray60'
            if click == True:
                color_opt = 'gray30'
        if game_buttom.collidepoint(mx, my):
            color_game = 'gray60'
            if click == True:
                color_game = 'gray30'

        pygame.draw.rect(screen, color_opt, opt_buttom)
        pygame.draw.rect(screen, color_game, game_buttom)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = False


        pygame.display.flip()
        clock.tick(60)


main_menu()
