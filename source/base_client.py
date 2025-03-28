import logging
from typing import Callable

import zmq# Bibliothèque pour la communication entre processus et réseaux

class BaseClient:
    def __init__(self, host:str, send_port:int, broadcast_port:int) -> None:
        self._context = zmq.Context()
        self._send_socket = self._context.socket(zmq.REQ) # Socket pour envoyer des requêtes
        self._send_socket.connect(f"tcp://{host}:{send_port}") # Connexion au serveur
        self._broadcast_socket = self._context.socket(zmq.SUB)# Socket pour recevoir des messages diffusés
        self._broadcast_socket.connect(f"tcp://{host}:{broadcast_port}")# Connexion au canal de diffusion
        self._broadcast_socket.setsockopt(zmq.SUBSCRIBE, b"")
        self._log = logging.getLogger("BaseClient")

    def send(self, message:bytes)->bytes:
        self._send_socket.send(message) # Envoi du message au serveur
        response = self._send_socket.recv() # Attente et réception de la réponse
        self._log.debug(f"Send '{message}', recv '{response}'")
        return response
    
    def update(self, on_recv:Callable):
        try:
            while True:
                broadcast_message = self._broadcast_socket.recv(flags=zmq.NOBLOCK)
                self._log.debug(f"Recv from broadcast '{broadcast_message}'")# Log du message reçu
                try:
                    on_recv(broadcast_message)
                except Exception as e:
                     self._log.error(f"Exception raised on message '{broadcast_message}' ({e})")
        except zmq.Again as e:
            pass # no message

    def close(self):
        self._log.info("closing socket")
        self._send_socket.close()
        self._broadcast_socket.close()
