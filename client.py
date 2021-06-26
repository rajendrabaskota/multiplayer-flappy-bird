import pygame
from network import Network

pygame.font.init()

WIDTH = 700
HEIGHT = 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND_IMG = pygame.image.load("imgs/bg.png")

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load("images/bird1.bmp")),
    pygame.transform.scale2x(pygame.image.load("images/bird2.bmp")),
    pygame.transform.scale2x(pygame.image.load("images/bird3.bmp")),
    pygame.transform.scale2x(pygame.image.load("images/bird2.bmp"))
]

BUTTOM_PIPE_IMG = pygame.image.load("images/pipe.bmp")
TOP_PIPE_IMG = pygame.transform.flip(BUTTOM_PIPE_IMG, False, True)
BASE_IMG = pygame.image.load("imgs/base.png")


def blur_surface(image, amount):
    scale = 1.0 / float(amount)
    surf_size = image.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(image, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf


def draw_background(to_be_blurred):
    background_img = BACKGROUND_IMG

    if to_be_blurred:
        background_img = blur_surface(background_img, 10)

    win.blit(background_img, (0, 0))


def draw_pipe(pipe, to_be_blurred):
    top_pipe_img = TOP_PIPE_IMG
    buttom_pipe_img = BUTTOM_PIPE_IMG

    if to_be_blurred:
        top_pipe_img = blur_surface(top_pipe_img, 5)
        buttom_pipe_img = blur_surface(buttom_pipe_img, 5)

    win.blit(top_pipe_img, (pipe.x, pipe.top_pipe_pos))
    win.blit(buttom_pipe_img, (pipe.x, pipe.bottom_pipe_pos))


def draw_bird(bird, to_be_blurred):
    bird.image_index = (bird.image_count // bird.ANIMATION_TIME) % 4
    bird_img = BIRD_IMGS[bird.image_index]

    if bird.tilt < -80:
        bird_img = BIRD_IMGS[1]

    if to_be_blurred:
        bird_img = blur_surface(bird_img, 5)

    win.blit(pygame.transform.rotate(bird_img, bird.tilt), (bird.x, bird.y))

    bird.image_count += 1


def redraw_window(game, player_id, my_bird, opponent_bird, current_pipe, next_pipe):
    to_be_blurred = any(game.if_collided)

    if not game.connected():
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render('Waiting for another player..', 1, (255, 0, 0))
        win.blit(text, (100, 100))
    else:
        win.fill((128, 128, 128))
        draw_background(to_be_blurred)
        draw_pipe(current_pipe, to_be_blurred)
        draw_pipe(next_pipe, to_be_blurred)
        draw_bird(my_bird, to_be_blurred)
        draw_bird(opponent_bird, to_be_blurred)

    if any(game.if_collided):
        if game.if_collided[0] and player_id == 0 or game.if_collided[1] and player_id == 1:
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render('You Lost!!', 1, (255, 0, 0))
            win.blit(text, (100, 100))
        else:
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render('You Won!!', 1, (255, 0, 0))
            win.blit(text, (100, 100))

    pygame.display.update()


def get_player_id(network):
    bird_width = BIRD_IMGS[0].get_width()
    pipe_width = BUTTOM_PIPE_IMG.get_width()
    pipe_height = BUTTOM_PIPE_IMG.get_height()
    player_id = network.connect(bird_width, pipe_width, pipe_height)
    return player_id


def main():
    run = True
    network = Network()
    player_id = get_player_id(network)
    game = network.send("get")
    my_bird = game.players[player_id]
    opponent_bird = game.players[(player_id + 1) % 2]
    current_pipe = game.current_pipe
    next_pipe = game.next_pipe
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if game.connected():
                if not any(game.if_collided):
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            network.send("jump")

        if game.connected() and not any(game.if_collided):
            network.send("move")

        redraw_window(game, player_id, my_bird, opponent_bird, current_pipe, next_pipe)

        game = network.send("get")
        my_bird = game.players[player_id]
        opponent_bird = game.players[(player_id + 1) % 2]
        current_pipe = game.current_pipe
        next_pipe = game.next_pipe


def main_menu():
    run = True

    while run:
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click To Play!!", 1, (255, 0, 0))
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


main_menu()
