# Question 1 : Les données ne sont pas confidentiels vis à vis du serveur car on voit les messages, ils ne sont pas cryptés, on voit également les informations du clients. 

# Question 2 : pickle est risqué car il peut exécuter du code malveillant lors de la désérialisation, n'est pas interopérable avec d'autres langages, peut générer des fichiers volumineux et lents à traiter, et perd la compatibilité lorsque la structure des objets change, ce qui le rend moins fiable et sécurisé que des alternatives comme JSON ou Protocol Buffers.

# Question 3 : JSON et MessagePack sont sécurisés car ils ne permettent pas d'exécuter du code arbitraire lors de la désérialisation, contrairement à pickle qui peut invoquer des fonctions via des objets malveillants.

# Question 4 : Le chiffrement seul est insuffisant car il protège les données contre l'espionnage, mais ne garantit pas leur intégrité, ce qui permettrait à un attaquant de modifier le message sans être détecté.

# Question 5 : En Python, la fonction os.urandom() permet de générer un salt avec une qualité cryptographique, car elle génère des nombres aléatoires sécurisés pour un usage cryptographique.

# Question 6 : Oui, le salt devra être envoyé en clair dans le paquet message, car il est nécessaire pour dériver la clé de chiffrement lors de la réception.

# Question 7 : J'ai modifié les variables _serial_function et _deserial_function dans le constructeur pour utiliser msgpack.packb et msgpack.unpackb

# Question 8 : Le serveur relaie uniquement des messages chiffrés sans pouvoir les lire, les clients étant responsables du déchiffrement.

# Question 9 : Le serveur malveillant peut modifier ou injecter des messages chiffrés sans pouvoir les lire, perturbant ainsi la communication entre les clients.

# Question 10 : Pour éviter l’action du Rogue Server, il faut authentifier et vérifier l’intégrité des messages avec des signatures numériques (ex. HMAC)

# Question 11 : Une solution simple mais sous-optimale consiste à concaténer la variable nick avec le message avant de le chiffrer avec Fernet, puis à vérifier après déchiffrement que nick correspond bien à l'expéditeur attendu, ce qui ajoute une couche de validation sans garantir une authentification forte.


