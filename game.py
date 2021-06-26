import random


class Game:
    def __init__(self):
        self.ready = False
        self.if_collided = [False, False]
        self.bird_width = 0
        self.pipe_width = 0
        self.pipe_height = 0
        self.players = [Bird(200, 350, 0), Bird(200, 350, 1)]
        self.pipes = {}
        self.pipe_count = 0
        self.current_pipe = None
        self.next_pipe = None

    def connected(self):
        return self.ready

    def create_new_pipe(self):
        self.pipes[self.pipe_count] = Pipe(700, self.pipe_height)
        self.pipe_count += 1

    def replace_current_next_pipe(self):
        self.current_pipe = self.next_pipe
        self.next_pipe = self.pipes[self.pipe_count - 2]

    def collision_detection(self):
        bird1 = self.players[0]
        bird2 = self.players[1]
        pipe = self.current_pipe

        if pipe.x <= bird1.x + self.bird_width <= pipe.x + self.pipe_width and bird1.y <= pipe.height:
            self.if_collided[0] = True
        elif pipe.x <= bird1.x + self.bird_width <= pipe.x + self.pipe_width and bird1.y >= pipe.bottom_pipe_pos:
            self.if_collided[0] = True
        elif pipe.x <= bird2.x + self.bird_width <= pipe.x + self.pipe_width and bird2.y <= pipe.height:
            self.if_collided[1] = True
        elif pipe.x <= bird2.x + self.bird_width <= pipe.x + self.pipe_width and bird2.y >= pipe.bottom_pipe_pos:
            self.if_collided[1] = True


class Bird:
    MAX_ROTATION = 25
    ROTATION_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.vel = 0
        self.height = y
        self.tick_count = 0
        self.tilt = 0
        self.image_count = 0
        self.image_index = 0
        self.player = player
        self.image_width = 0
        # self.image = BIRD_IMAGES[self.player]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 15:
            d = 15

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0:
            self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VEL


class Pipe:
    def __init__(self, x, image_height):
        self.x = x
        self.height = 0
        self.top_pipe_pos = 0
        self.bottom_pipe_pos = 0
        self.vel = 5
        self.gap = 200
        self.image_height = image_height
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top_pipe_pos = self.height - self.image_height
        self.bottom_pipe_pos = self.height + self.gap

    def move(self):
        self.x -= self.vel
