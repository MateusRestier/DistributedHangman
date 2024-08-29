import socket
import threading

# Função para lidar com cada jogador
def handle_client(client_socket, addr, game_state):
    print(f"Conexão estabelecida com {addr}")
    
    while True:
        try:
            # Recebe a mensagem do cliente
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            command, *args = message.split()

            if command == "START":
                game_state['word'] = args[0]
                game_state['guesses'] = ['_'] * len(game_state['word'])
                client_socket.send("Jogo iniciado!".encode('utf-8'))

            elif command == "GUESS":
                letter = args[0]
                if letter in game_state['word']:
                    for i, l in enumerate(game_state['word']):
                        if l == letter:
                            game_state['guesses'][i] = letter
                    response = f"Correto! Estado atual: {' '.join(game_state['guesses'])}"
                else:
                    game_state['attempts'] -= 1
                    response = f"Errado! Tentativas restantes: {game_state['attempts']}"

                client_socket.send(response.encode('utf-8'))

                if '_' not in game_state['guesses']:
                    client_socket.send("Vitória! Você adivinhou a palavra.".encode('utf-8'))
                    break
                elif game_state['attempts'] == 0:
                    client_socket.send(f"Derrota! A palavra era: {game_state['word']}".encode('utf-8'))
                    break

            elif command == "END":
                client_socket.send("Conexão encerrada!".encode('utf-8'))
                break

        except ConnectionResetError:
            print(f"Conexão com {addr} perdida.")
            break

    client_socket.close()

# Função principal do servidor
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(2)
    print("Servidor aguardando conexões...")

    game_state = {
        'word': '',
        'guesses': [],
        'attempts': 6
    }

    # Aceita conexões de dois jogadores
    client1, addr1 = server_socket.accept()
    thread1 = threading.Thread(target=handle_client, args=(client1, addr1, game_state))
    thread1.start()

    client2, addr2 = server_socket.accept()
    thread2 = threading.Thread(target=handle_client, args=(client2, addr2, game_state))
    thread2.start()

    thread1.join()
    thread2.join()

    server_socket.close()

if __name__ == "__main__":
    start_server()
