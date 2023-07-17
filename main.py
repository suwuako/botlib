import requests
import json
import asyncio
import websocket

discord = "wss://gateway.discord.gg"
ws = websocket.WebSocket()

def gateway_hello():
    gateway_pointer = f"{discord}/gateway"
    ws.connect(gateway_pointer)

    recv = json.loads(ws.recv())
    heartbeat = recv["d"]["heartbeat_interval"]
    print(f"opcode : {recv['op']} | Heartbeat: {heartbeat}ms")
    print(recv)

    return recv

def gateway_send(dump):
    ws.send(json.dumps(dump))
    
async def ws_heartbeat(hello, heartbeat):
    print(f"Beginning heartbeat ({heartbeat})")

    dump = {
        "op" : 1,
        "d" : "null"
    }

    while True:
        print(ws.recv())
        await asyncio.sleep(1)
       
        gateway_send(dump)

        print("Heartbeat sent")




async def establish_connection():
    hello = gateway_hello()

    if hello["op"] != 10: # if not opcode 10 (hello)
        return 0
    
    heartbeat = hello["d"]["heartbeat_interval"] / 1000
    await ws_heartbeat(hello, heartbeat)


    
        


class main():
    def __init__(self) -> None:
        pass

    def run(self):
        print("Hello World!")
        asyncio.run(establish_connection())
        pass

if __name__ == "__main__":
    main().run()