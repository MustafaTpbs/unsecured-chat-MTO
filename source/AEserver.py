import msgpack  # Utilisation de msgpack pour la sérialisation
import logging
from simple_server import SimpleServer

class AEServer(SimpleServer):
    def __init__(self, recv_port: int, broadcast_port: int) -> None:
        super().__init__(recv_port, broadcast_port)  # Appel du constructeur parent avec super
        
        # Modification des fonctions de sérialisation/désérialisation /possible avec python 
        self._serial_function = msgpack.packb  # Convertit les objets en bytes avec msgpack
        self._deserial_function = msgpack.unpackb  # Convertit les bytes en objets avec msgpack

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)  # Activation des logs en mode debug
    server = AEServer(6666, 6667)  # Création du serveur AEServer
    
    try:
        while True:
            server.update()  # Boucle principale du serveur
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
