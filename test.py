import requests
import time
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
    
async def ws_heartbeat(heartbeat):
    print(f"Beginning heartbeat ({heartbeat})")

    dump = {
        "op" : 1,
        "d" : "null"
    }

    while True:
        print("sending heartbeat...")
        gateway_send(dump)
        
        heartbeat_ack = json.loads(ws.recv())

        if heartbeat_ack["op"] != 11:
            print("HELP HELP HELP heartbeat not 11? breaking")
            break

        print(f"Heartbeat sent successfully! opcode {heartbeat_ack['op']}")
        time.sleep(heartbeat)

async def identify():
    pass

def establish_connection():
    hello = gateway_hello()

    if hello["op"] != 10: # if not opcode 10 (hello)
        print("opcode not 10?")
        return 0
    
    heartbeat = hello["d"]["heartbeat_interval"] / 1000
    return (hello, heartbeat)


class main():
    def __init__(self) -> None:
        tokenfile = open("supersecret.json", "r")
        self.token = json.load(tokenfile)
        print(self.token)
        pass

    def run(self):
        print("Hello World!")
        hello = establish_connection()

        loop = asyncio.get_event_loop()
        task = loop.create_task(ws_heartbeat(hello[1]))

        loop.run_forever()

        pass

if __name__ == "__main__":
    main().run()