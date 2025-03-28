import pickle
import time # Pour gérer les délais entre les requêtes
import random # Pour générer des pseudos aléatoires
import string # Pour choisir des caractères aléatoires
from base_client import BaseClient

def random_nick():
    """Génère un pseudo aléatoire"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def flood_server(host="localhost", send_port=6666, broadcast_port=6667, count=1000, delay=0.01):
    """Envoie massivement des requêtes 'join' pour saturer le serveur"""
    client = BaseClient(host, send_port, broadcast_port)

    for _ in range(count):
        nick = random_nick()# Génère un pseudo unique pour chaque requête
        frame = {"type": "join", "nick": nick} # Prépare la requête de connexion
        packet = pickle.dumps(frame)# Sérialise la requête
        
        response = client.send(packet) #Envoie la requête au serveur et récupère la réponse
        print(f"Tried to join with {nick}, response: {pickle.loads(response)}")# Affiche le retour du serveur
        
        time.sleep(delay)  # Petit délai pour éviter un crash du script
    
    client.close()

if __name__ == "__main__":
    flood_server()# Lance le test de charge du serveur
