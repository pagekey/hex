import os
import socket

from hex import Params

SOCKET_PATH = "./user_input.sock"


def run(params: Params) -> dict[str, str]:
    prompt = params.inputs["prompt"]

    # Clean up existing socket file if it exists
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(SOCKET_PATH)
        server.listen(1)

        print(f"{prompt}: (waiting on socket {SOCKET_PATH})", end="", flush=True)

        conn, _ = server.accept()
        with conn:
            data = b""
            while not data.endswith(b"\n"):
                chunk = conn.recv(1024)
                if not chunk:
                    break
                data += chunk

    # Clean up socket file after use
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    user_input = data.decode().rstrip("\n")

    return {"user_input": user_input}
