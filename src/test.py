#!/usr/bin/env python3

import socket
import select
import sys
import argparse
import time

from agent import Agent
from planner import Planner
from state import State
from actions.actions import ACTIONS
from goals.goals import GOALS
from goals.goals import SurviveGoal


def parse_args():
    parser = argparse.ArgumentParser(description="Zappy AI Client", add_help=False)
    parser.add_argument("-p", type=int, required=True, help="port number")
    parser.add_argument("-n", type=str, required=True, help="team name")
    parser.add_argument("-h", type=str, default="localhost", help="server host")
    return parser.parse_args()


def connect_to_server(host, port, team_name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    sock.setblocking(True)

    buffer = ""

    def recv_line():
        nonlocal buffer
        while '\n' not in buffer:
            data = sock.recv(4096).decode()
            if not data:
                raise ConnectionError("Connexion fermée par le serveur")
            buffer += data
        line, buffer = buffer.split('\n', 1)
        return line.strip(), buffer

    line, buffer = recv_line()
    if line != "WELCOME":
        raise RuntimeError(f"[ERROR] Protocole inattendu : attendu 'WELCOME', reçu '{line}'")

    sock.sendall((team_name + "\n").encode())

    client_num_line, buffer = recv_line()
    try:
        client_num = int(client_num_line)
        if client_num <= 0:
            raise RuntimeError(f"[ERROR] Pas de slot disponible pour l'équipe '{team_name}'")
    except ValueError:
        raise RuntimeError(f"[ERROR] Réponse client_num invalide : {client_num_line}")

    map_line, buffer = recv_line()
    try:
        x, y = map(int, map_line.strip().split())
    except ValueError:
        raise RuntimeError(f"[ERROR] Dimensions de carte invalides : '{map_line}'")

    print(f"[INFO] Connecté. Carte: {x}x{y} | Slots restants: {client_num}", file=sys.stderr)

    sock.setblocking(False)
    return sock, x, y, buffer



def main():
    args = parse_args()

    try:
        sock, world_width, world_height, leftover_buffer = connect_to_server(args.h, args.p, args.n)
    except Exception as e:
        print(f"[CRITICAL] Échec connexion : {e}", file=sys.stderr)
        return

    state = State(world_width=world_width, world_height=world_height)
    agent = Agent(state, Planner(ACTIONS))
    agent.set_goal(SurviveGoal())

    buffer = leftover_buffer

    while True:
        try:
                agent.tick()

                readable, _, _ = select.select([sock], [], [], 0.01)
                for s in readable:
                    data = s.recv(4096).decode()
                    if not data:
                        print("[ERROR] Connexion perdue", file=sys.stderr)
                        return
                    buffer += data
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        agent.receive_message(line.strip())
                        print(line, file=sys.stderr)

                if agent.has_command() and agent.waiting_for_response:
                    cmd = agent.next_command()
                    if cmd:
                        try:
                            sock.sendall((cmd + "\n").encode())
                            print(f"[DEBUG] Commande envoyée : {cmd}", file=sys.stderr)
                        except Exception as e:
                            print(f"[ERROR] Envoi échoué : {e}", file=sys.stderr)

                time.sleep(0.005)

        except KeyboardInterrupt:
            print("[INFO] Interruption utilisateur", file=sys.stderr)
            break
        except Exception as e:
            print(f"[CRASH] Exception non gérée : {e}", file=sys.stderr)
            break


if __name__ == "__main__":
    main()

