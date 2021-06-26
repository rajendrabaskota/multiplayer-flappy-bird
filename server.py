import socket
import threading
import pickle
from game import Game


HEADER = 64
FORMAT = 'utf-8'
SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_ADDRESS, PORT))

GAMES = {}
ID_COUNT = 0


def initiate_game(msg, game_id):
    msg = msg.split()
    bird_width = int(msg[0])
    pipe_width = int(msg[1])
    pipe_height = int(msg[2])

    game = GAMES[game_id]
    game.bird_width = bird_width
    game.pipe_width = pipe_width
    game.pipe_height = pipe_height


def initiate_pipes(game_id):
    game = GAMES[game_id]

    for i in range(3):
        game.create_new_pipe()

    game.current_pipe = game.pipes[0]
    game.next_pipe = game.pipes[1]


def threaded_client(conn, player_id, game_id):
    global ID_COUNT
    print('Thread Started...')
    connected = True

    pipe_msg = conn.recv(64).decode('utf-8')
    initiate_game(pipe_msg, game_id)
    initiate_pipes(game_id)

    send_data = str(player_id)
    print(send_data)
    conn.send(str.encode(send_data))
    print(send_data)

    while connected:
        msg = conn.recv(64).decode('utf-8')
        print(msg)

        if not msg:
            break
        else:
            if game_id in GAMES:
                game = GAMES[game_id]
                bird = game.players[player_id]
                current_pipe = game.pipes[game.pipe_count - 3]

                if player_id == 0:
                    if current_pipe.x < 0 - 60:
                        game.create_new_pipe()
                        game.replace_current_next_pipe()

                if msg == "jump":
                    bird.jump()
                    return_data = pickle.dumps(game)
                elif msg == "move":
                    bird.move()
                    current_pipe.move()
                    game.collision_detection()
                    return_data = pickle.dumps(game)
                else:
                    return_data = pickle.dumps(game)

                conn.send(return_data)

    print('conn closed!!!')
    conn.close()
    ID_COUNT -= 1


def start():
    global ID_COUNT
    server.listen()
    while True:
        conn, addr = server.accept()
        print(conn)
        print(f'[CONNECTED TO] {addr}')

        ID_COUNT += 1
        game_id = (ID_COUNT - 1) // 2
        player_id = 0

        if ID_COUNT % 2 == 1:
            GAMES[game_id] = Game()
        else:
            player_id = 1
            GAMES[game_id].ready = True

        thread = threading.Thread(target=threaded_client, args=(conn, player_id, game_id))
        thread.start()


print("[STARTING] server is starting...")
start()
