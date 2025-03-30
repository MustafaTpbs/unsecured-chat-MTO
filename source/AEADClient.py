import logging
import base64
import os
from typing import Tuple
import msgpack
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.fernet import Fernet
from pywebio.output import put_text
from names_generator import generate_name
from simple_client import SimpleClient

class AEADClient(SimpleClient):
    def __init__(self, host: str, send_port: int, broadcast_port: int, nick: str, password: str):
        super().__init__(host, send_port, broadcast_port, nick)
        self._password = password.encode()
        self._salt = os.urandom(16)
        self._key = self.derive_key_from_password(self._password, self._salt)

    def derive_key_from_password(self, password: bytes, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt_message(self, message: str) -> Tuple[bytes, bytes, bytes]:
        fernet = Fernet(self._key)
        encrypted_message = fernet.encrypt(message.encode())

        hmac = HMAC(self._key, hashes.SHA256())
        hmac.update(encrypted_message)
        tag = hmac.finalize()

        return self._salt, encrypted_message, tag

    def decrypt_message(self, encrypted_message: bytes, salt: bytes, tag: bytes, nick: str) -> str:
        key = self.derive_key_from_password(self._password, salt)
        fernet = Fernet(key)

        hmac = HMAC(key, hashes.SHA256())
        hmac.update(encrypted_message)
        try:
            hmac.verify(tag)
        except Exception as e:
            logging.error("Erreur HMAC : Message modifié ou invalide.")
            return "[Message corrompu]"

        try:
            return fernet.decrypt(encrypted_message).decode()
        except Exception as e:
            logging.error(f"Erreur de déchiffrement : {e}")
            return "[Message corrompu]"

    def send(self, frame: dict) -> dict:
        try:
            packet = msgpack.packb(frame)
            response_packet = self._client.send(packet)
            return msgpack.unpackb(response_packet)
        except Exception as e:
            logging.error(f"Erreur d'envoi : {e}")
            return {}

    def message(self, message: str):
        salt, encrypted_message, tag = self.encrypt_message(message)
        frame = {"type": "message", "nick": self._nick, "message": encrypted_message, "salt": salt, "tag": tag}
        self.send(frame)

    def on_recv(self, packet: bytes):
        try:
            frame = msgpack.unpackb(packet)
            decrypted_message = self.decrypt_message(frame["message"], frame["salt"], frame["tag"], frame["nick"])
            put_text(f"{frame['nick']} : {decrypted_message}", scope='scrollable')
        except Exception as e:
            logging.error(f"Erreur de réception : {e}")

    def join(self):
        frame = {"type": "join", "nick": self._nick}
        response = self.send(frame)

        if response is None:
            raise Exception("Aucune réponse du serveur lors de la connexion")

        if response.get("response") != "ok":
            raise Exception(f"Échec de connexion: {response}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    client = AEADClient("localhost", 6666, 6667, generate_name(), "Best_Secr3t_ever_!")
    
    try:
        client.run()
    except KeyboardInterrupt:
        logging.info("Arrêt du client...")
