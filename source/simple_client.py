
import logging  # Gestion des logs
import pickle  # Sérialisation/désérialisation d'objets Python
import threading  # Gestion des threads pour l'interface utilisateur
import time  # Gestion des délais


from names_generator import generate_name # Génère un pseudo aléatoire
from pywebio.pin import put_input, pin_update, pin # Gestion des champs d'entrée
from pywebio.output import put_button, put_row, put_scrollable, put_text, put_scope # UI Web
from pywebio.session import register_thread  # Gestion de session
from pywebio.session import defer_call  # Gestion de session

from base_client import BaseClient  # Client de base pour la communication réseau


class SimpleClient:
    def __init__(self, host: str, send_port: int, broadcast_port: int, nick: str):
        self._client = BaseClient(host, send_port, broadcast_port) # Initialise le client réseau
        self._log = logging.getLogger(f"SimpleClient[{nick}]")  # Logger spécifique au client
        self._nick = nick # Nom du client
        self._running = True # Indique si le client est actif

    def send(self, frame:dict)->dict:
        packet = pickle.dumps(frame) # Sérialise le message
        response_packet = self._client.send(packet)  # Envoie le message
        if response_packet:
            return pickle.loads(response_packet) # Retourne la réponse désérialisée
        
    def start_server(self):
        
        def _inner():
            put_scrollable(put_scope('scrollable'), height=500, keep_bottom=True)  # Interface de chat
            put_row([
                put_text(self._nick),
                put_input('message_input', placeholder='Your message'),  # Champ de texte
                put_button("send", self._on_send ) # Bouton d'envoi
            ])

        t = threading.Thread(target=_inner) # Crée un thread pour l'interface
        register_thread(t) # Enregistre le thread auprès de PyWebIO
        defer_call(self.defer_callback)  # Exécute une fonction à la fermeture
        t.start() # Démarre l'interface


    def _on_send(self):
        # called when the button send is hit
        self._log.debug("send callback")  # Log sur l'action d'envoi
        message = pin['message_input'] # Récupère le texte du champ
        if message:
            self._log.debug("message : "+message)  # Log du message
            self.message(message)  # Envoie le message
            pin_update('message_input', value='')  # Réinitialise le champ
        
    def join(self):
        frame = {"type":"join", "nick":self._nick} # Demande de connexion
        response = self.send(frame)
        if response["response"] != "ok":
            raise Exception("Failed to join") # Erreur si refusé
        
    def leave(self):
        frame = {"type": "leave", "nick": self._nick}# Demande de déconnexion
        response = self.send(frame)
        if response["response"] != "ok":
            raise Exception("Failed to leave") # Erreur si refusé
        
    def message(self, message:str):
        frame = {"type": "message", "nick": self._nick, "message":message} # Message utilisateur
        response = self.send(frame)
        if response["response"] != "ok":
            raise Exception("Failed to send message")# Erreur si refusé
        
    def on_recv(self, packet: bytes):
        # callback of broadcast message
        frame = pickle.loads(packet)# Désérialise le message reçu
        self._log.debug(f"Received broadcast frame {frame}") # Log de réception
        if frame["type"] == "message":
            put_text(f"{frame['nick']} : {frame['message']}", scope='scrollable')# Affiche le message
        else:
            raise Exception(f"packet type '{frame['type']}' can't be handled")# Erreur si type inconnu
        
    def update(self):
        self._client.update(self.on_recv) # Vérifie les nouveaux messages

    def close(self):
        self._client.close() # Ferme le client proprement

    def defer_callback(self):
        # callback for closed windows
        self._running = False # Arrête l'exécution
        self._log.info("Window closed, quitting") # Log de fermeture

    def run(self):
        self.start_server() # Démarre l'interface
        self.join()# Se connecte au serveur

        try:
            while self._running:
                self.update() # Écoute les messages
                time.sleep(0.1) # Attente pour limiter la charge
        except KeyboardInterrupt:
            self._log.info("ctrl+c")# Log interruption clavier
        finally:
            self.leave()
            self.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG) # Active les logs détaillés
    client = SimpleClient("localhost", 6666, 6667, generate_name())# Initialise un client
    client.run() # Démarre le client
