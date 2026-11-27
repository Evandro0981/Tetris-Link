from config.configuracoes import *
import threading
import socket
import random
import json
import time

clientes = []

ultimo_id_peca = {"EQUIPE_1": 0, "EQUIPE_2": 0}

# Várias threads enviam para o mesmo socket: sem trava, mensagens grandes se misturam
trava_envio = threading.Lock()

# Estado global do fim de partida
fim_de_jogo = {
    "pontos": {"EQUIPE_1": None, "EQUIPE_2": None},
    "revanche": set(),        # ids dos jogadores que já clicaram
    "total_jogadores": MAX_JOGADORES_MULTIPLAYER,
}

def lidar_com_cliente(conn, endereco):
    print(f"[NOVA CONEXÃO] {endereco} conectado.")
    buffer = ""
    
    while True:
        try:
            dados = conn.recv(MAX_BUFFER_MENSAGEM).decode(CODIFICACAO)
            
            if not dados:
                break

            buffer += dados
            
            while '\n' in buffer:
                linha, buffer = buffer.split('\n', 1)
                linha = linha.strip()
                
                if not linha:
                    continue

                try:
                    msg = json.loads(linha)
                
                except json.JSONDecodeError:
                    continue

                tipo = msg.get("tipo")

                if tipo in ("FIM_JOGO_REPORT", "PEDIR_REVANCHE", "VOLTAR_INICIO"):
                    if tipo == "FIM_JOGO_REPORT":
                        equipe = msg.get("equipe")
                        fim_de_jogo["pontos"][equipe] = msg.get("pontos", 0)
                        
                        if all(v is not None for v in fim_de_jogo["pontos"].values()):
                            enviar_para_todos(json.dumps({
                                "tipo": "RESULTADO_FINAL",
                                "pontos_eq1": fim_de_jogo["pontos"]["EQUIPE_1"],
                                "pontos_eq2": fim_de_jogo["pontos"]["EQUIPE_2"],
                            }) + '\n')

                    elif tipo == "PEDIR_REVANCHE":
                        fim_de_jogo["revanche"].add(msg.get("id"))
                        
                        enviar_para_todos(json.dumps({
                            "tipo": "ESPERA_REVANCHE",
                            "confirmados": len(fim_de_jogo["revanche"]),
                            "total": fim_de_jogo["total_jogadores"],
                        }) + '\n')

                        if len(fim_de_jogo["revanche"]) >= fim_de_jogo["total_jogadores"]:
                            _iniciar_partida()

                    elif tipo == "VOLTAR_INICIO":
                        _voltar_todos_ao_inicio()

                    continue

                fazer_broadcast(linha + '\n', remetente=conn)

                if tipo == "GRID_SYNC":
                    equipe = msg.get("equipe")
                    id_peca = msg.get("id_peca", 0)
                    
                    if id_peca > ultimo_id_peca.get(equipe, 0):
                        ultimo_id_peca[equipe] = id_peca
                        
                        enviar_para_todos(json.dumps({
                            "tipo": "NOVA_PECA",
                            "equipe": equipe,
                            "peca": random.choice(TETROMINOS[0])
                        }) + '\n')

        except Exception as e:
            print(f"[ERRO] {e}")
            break

    print(f"[DESCONECTADO] Cliente {endereco} desconectou.")
    fim_de_jogo['total_jogadores'] = len(clientes)

    with trava_envio:
        if conn in clientes:
            clientes.remove(conn)
    conn.close()


def fazer_broadcast(mensagem, remetente):
    dados = mensagem.encode(CODIFICACAO)

    with trava_envio:
        for cliente in list(clientes):
            if cliente != remetente:
                try:
                    cliente.sendall(dados)
                except Exception:
                    pass

def enviar_para_todos(mensagem):
    dados = mensagem.encode(CODIFICACAO)

    with trava_envio:
        for cliente in list(clientes):
            try:
                cliente.sendall(dados)
            except Exception:
                pass

def _resetar_estado_fim_de_jogo():
    fim_de_jogo["pontos"] = {"EQUIPE_1": None, "EQUIPE_2": None}
    fim_de_jogo["revanche"] = set()
    ultimo_id_peca["EQUIPE_1"] = 0
    ultimo_id_peca["EQUIPE_2"] = 0

def _iniciar_partida():
    """Sorteia novos papéis/peças e envia INICIAR_JOGO para todos (revanche)."""
    papeis_eq1 = ["EQUIPE_1_MOVIMENTO", "EQUIPE_1_ROTACAO"]
    random.shuffle(papeis_eq1)

    papeis_eq2 = ["EQUIPE_2_MOVIMENTO", "EQUIPE_2_ROTACAO"]
    random.shuffle(papeis_eq2)

    atribuicoes = [papeis_eq1[0], papeis_eq1[1], papeis_eq2[0], papeis_eq2[1]]

    pecas_iniciais_eq1 = [random.choice(TETROMINOS[0]) for _ in range(TOTAL_PECAS_SORTEADAS)]
    pecas_iniciais_eq2 = [random.choice(TETROMINOS[0]) for _ in range(TOTAL_PECAS_SORTEADAS)]

    for idx, cliente_conn in enumerate(list(clientes)):
        msg_inicio = json.dumps({
            "tipo": "INICIAR_JOGO",
            "papel": atribuicoes[idx],
            "id": idx,
            "pecas_eq1": pecas_iniciais_eq1,
            "pecas_eq2": pecas_iniciais_eq2
        }) + '\n'

        try:
            with trava_envio:
                cliente_conn.sendall(msg_inicio.encode(CODIFICACAO))
        except Exception as e:
            print(f"Erro ao enviar início para o jogador {idx}: {e}")



def _voltar_todos_ao_inicio():
    enviar_para_todos(json.dumps({"tipo": "VOLTAR_INICIO_FORCADO"}) + '\n')
    _resetar_estado_fim_de_jogo()

def iniciar_servidor():
    global ultimo_id_peca

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen(MAX_JOGADORES_MULTIPLAYER)
    print(f"[INICIANDO] Servidor escutando no IP {HOST}:{PORT}")

    while True:
        if len(clientes) >= 4:
            time.sleep(5)  # evita laço ocupando 100% da CPU com a sala cheia
            continue

        conn, addr = servidor.accept()
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        with trava_envio:
            clientes.append(conn)

        thread = threading.Thread(target=lidar_com_cliente, args=(conn, addr), daemon=True)
        thread.start()

        if len(clientes) == 4:
            print("[SERVIDOR CHEIO] 4 jogadores conectados. Sorteando funções e gerando peças...")
            ultimo_id_peca = {"EQUIPE_1": 0, "EQUIPE_2": 0}

            _iniciar_partida()

if __name__ == "__main__":
    iniciar_servidor()