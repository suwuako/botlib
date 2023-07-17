import requests
import json
import asyncio
import websocket

discord = "wss://gateway.discord.gg"
ws = websocket.WebSocket()

async def establish_connection():
    gateway_pointer = f"{discord}/gateway/bot"
    ws.connect(gateway_pointer)

    recv = json.loads(ws.recv())
    heartbeat = recv["d"]["heartbeat_interval"]
    print(f"recieved opcode: {recv['op']} | Heartbeat: {heartbeat}ms")
    print(recv)

    if recv["op"] == 10: # opcode 10 (hello)
        pass


class main():
    def __init__(self) -> None:
        pass

    def run(self):
        print("Hello World!")
        asyncio.run(establish_connection())
        pass

if __name__ == "__main__":
    main().run()