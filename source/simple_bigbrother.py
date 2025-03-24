import zmq
import pickle
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger("BigBrother")
    
    context = zmq.Context()
    broadcast_socket = context.socket(zmq.SUB)
    broadcast_socket.connect("tcp://localhost:6667")
    broadcast_socket.setsockopt(zmq.SUBSCRIBE, b"")
    
    log.info("BigBrother is listening to all conversations...")
    
    try:
        while True:
            packet = broadcast_socket.recv()
            frame = pickle.loads(packet)
            if frame["type"] == "message":
                log.info(f"[SPY] {frame['nick']}: {frame['message']}")
    except KeyboardInterrupt:
        log.info("BigBrother is shutting down...")
    finally:
        broadcast_socket.close()
        context.term()

if __name__ == "__main__":
    main()
