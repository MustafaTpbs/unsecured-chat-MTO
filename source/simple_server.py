import pickle# Sérialisation et désérialisation des objets Python
from typing import Tuple# Définition des types pour les retours de fonction
import logging # Gestion des logs pour suivre les événements du serveur

from base_server import BaseServer

class SimpleServer:
    def __init__(self, recv_port: int, broadcast_port: int) -> None:
        self._server = BaseServer(recv_port, broadcast_port) # Création du serveur
        self._log = logging.getLogger(self.__class__.__name__)# Logger pour surveiller l'activité
        self._clients = set() # Stocke les clients connectés
        # can be overrided
        # serial : expect a direct, return bytes
        self._serial_function = pickle.dumps# Convertit les objets Python en bytes
        # deserial : expect bytes, return dict
        self._deserial_function = pickle.loads# Convertit les bytes en objets Python

    def update(self):
        self._server.update(self.on_recv) # Écoute les messages et les traite avec `on_recv`

    def on_recv(self, packet: bytes) -> Tuple[bytes, bytes]:
        callbacks = { # Dictionnaire associant un type de requête à une fonction
            "join" : self.on_join,
            "leave" : self.on_leave,
            "message" : self.on_message,
            "list": self.on_list
        }
        frame = self._deserial_function(packet) # Décode le message reçu
        return callbacks[frame["type"]](packet, frame) # Appelle la fonction appropriée
        
    def on_join(self, packet:bytes, frame: dict) -> Tuple[bytes, bytes]:
        if frame["nick"] in self._clients:
            self._log.error(f"Client '{frame['nick']}' is already joined")
            return None, self._serial_function({"response": "ko"})
        else:
            self._clients.add(frame["nick"]) # Ajoute le client à la liste
            self._log.info(f"Client '{frame['nick']}' join")
            return None, self._serial_function({"response": "ok"})

    def on_leave(self, packet:bytes, frame: dict) -> Tuple[bytes, bytes]:
        if frame["nick"] not in self._clients:
            self._log.error(f"Client '{frame['nick']}' doesn't joined")
            return None, self._serial_function({"response": "ko"})
        else:
            self._clients.remove(frame["nick"])# Supprime le client de la liste
            self._log.info(f"Client '{frame['nick']}' left")
            return None, self._serial_function({"response": "ok"})

    def on_message(self, packet:bytes, frame: dict) -> Tuple[bytes, bytes]:
        if frame["nick"] not in self._clients:
            self._log.error(f"Client '{frame['nick']}' didn't join, can't send message")
            return None, self._serial_function({"response": "ko"})
        else:
            self._log.info(f"Client '{frame['nick']}' sent message '{frame['message']}'")
            return packet, self._serial_function({"response": "ok"}) # Diffuse le message
        
    def on_list(self, packet: bytes, frame: dict) -> Tuple[bytes, bytes]:
        self._log.info(f"List requested") # Journalise la requête
        return None, self._serial_function({"response": list(self._clients)})# Renvoie la liste des clients

    def close(self):
        self._server.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG) # Active les logs en mode debug
    server = SimpleServer(6666, 6667) # Initialise le serveur avec les ports spécifiés

    try:
        while True:
            server.update()# Boucle principale qui écoute les requêtes
    except KeyboardInterrupt:
        pass # Ignore l'interruption clavier
    finally:
        server.close()