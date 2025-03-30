import msgpack
import logging
from simple_server import SimpleServer

class RogueServer(SimpleServer):
    def __init__(self, recv_port: int, broadcast_port: int) -> None:
        super().__init__(recv_port, broadcast_port)
        self._serial_function = msgpack.packb
        self._deserial_function = msgpack.unpackb
        logging.basicConfig(level=logging.DEBUG)

    def on_message(self, packet: bytes, frame: dict):
        if frame["nick"] not in self._clients:
            self._log.error(f"Client '{frame['nick']}' n'est pas connecté")
            return None, self._serial_function({"response": "ko"})

        logging.info(f"Avant la modification : {frame.get('message', '')}")

        try:
            if "message" in frame:
                original_message = frame["message"]
                modified_message = " Ce message a été altéré"
                frame["message"] = modified_message

            modified_packet = self._serial_function(frame) #sérialisation
            logging.info(f"Message après modification : {modified_message}")
            return modified_packet, self._serial_function({"response": "ok"})
        
        except Exception as e:
            self._log.error(f"Erreur: {e}")
            return None, self._serial_function({"response": "ko"})

if __name__ == "__main__":
    server = RogueServer(6666, 6667)

    try:
        logging.info("RogueServer en marche... Attente de messages...")
        while True:
            server.update()
    except KeyboardInterrupt:
        logging.info("Extinction du serveur malveillant...")
    finally:
        server.close()