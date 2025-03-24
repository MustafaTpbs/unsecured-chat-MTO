# Question 1 : Les données ne sont pas confidentiels vis à vis du serveur car on voit les messages, ils ne sont pas cryptés, on voit également les informations du clients. 

# Question 2 : pickle est risqué car il peut exécuter du code malveillant lors de la désérialisation, n'est pas interopérable avec d'autres langages, peut générer des fichiers volumineux et lents à traiter, et perd la compatibilité lorsque la structure des objets change, ce qui le rend moins fiable et sécurisé que des alternatives comme JSON ou Protocol Buffers.

# Question 3 : JSON et MessagePack sont sécurisés car ils ne permettent pas d'exécuter du code arbitraire lors de la désérialisation, contrairement à pickle qui peut invoquer des fonctions via des objets malveillants.





