import socket

# Função principal do cliente
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print("Conectado ao servidor!")

    while True:
        command = input("Digite um comando (START, GUESS, END): ")
        
        if command.upper().startswith("START"):
            word = input("Escolha a palavra para o jogo: ")
            client_socket.send(f"START {word}".encode('utf-8'))
        
        elif command.upper().startswith("GUESS"):
            letter = input("Escolha uma letra: ")
            client_socket.send(f"GUESS {letter}".encode('utf-8'))
        
        elif command.upper().startswith("END"):
            client_socket.send("END".encode('utf-8'))
            break
        
        # Recebe a resposta do servidor
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Servidor: {response}")
        
        if "Vitória" in response or "Derrota" in response:
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
