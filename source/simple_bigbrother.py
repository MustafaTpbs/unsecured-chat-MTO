import zmq
import pickle
import logging

def main():
    logging.basicConfig(level=logging.INFO) # Configuration du niveau de log
    log = logging.getLogger("BigBrother")# Création d'un logger spécifique
    
    context = zmq.Context()
    broadcast_socket = context.socket(zmq.SUB)
    broadcast_socket.connect("tcp://localhost:6667")
    broadcast_socket.setsockopt(zmq.SUBSCRIBE, b"")
    
    log.info("BigBrother is listening to all conversations...")
    
    try:
        while True:
            packet = broadcast_socket.recv()# Réception
            frame = pickle.loads(packet)# Désérialisation
            if frame["type"] == "message":# Vérification du type
                log.info(f"[SPY] {frame['nick']}: {frame['message']}")# Affichage du message intercepté
    except KeyboardInterrupt:
        log.info("BigBrother is shutting down...")
    finally:
        broadcast_socket.close()
        context.term()

if __name__ == "__main__":
    main()
