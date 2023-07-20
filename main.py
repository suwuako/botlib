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

    print(1)
    print(ws.recv())
    print(ws.recv_data())
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
    return (hello, heartbeat)


class main():
    def __init__(self) -> None:
        pass

    def run(self):
        print("Hello World!")
        hello = asyncio.run(establish_connection())
        loop.run_until_complete(ws_heartbeat(hello[0], hello[1]))
        pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    main().run()