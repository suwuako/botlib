import websocket
import asyncio
import json

class socket_lib():
    def hello(self):
        gateway_pointer = f"{discord}/gateway"
        ws.connect(gateway_pointer)

        response = json.loads(ws.recv())
        heartbeat = response["d"]["heartbeat_interval"] / 1000
        print(f"opcode : {response['op']} | Heartbeat: {heartbeat}ms")

        if response["op"] != 10: # if not opcode 10 (hello)
            print("opcode not 10?")
            return 0

        return heartbeat

    async def heartbeat(self, heartbeat_interval):
        print("----------------------Heartbeat----------------------")
        print(f"Beginning heartbeat ({heartbeat_interval}s)")

        dump = {
            "op" : 1,
            "d" : "null"
        }

        print("sending heartbeat...")
        self.gateway_send(dump)
        
        heartbeat_ack = json.loads(ws.recv())
        print(heartbeat_ack)

        if heartbeat_ack["op"] != 11:
            print("HELP HELP HELP heartbeat not 11? breaking")
            exit()

        print(f"Heartbeat sent successfully! opcode correct: {heartbeat_ack['op']}")
        print("-----------------------------------------------------\n")

        await asyncio.sleep(heartbeat_interval)

    async def identify(self, TOKEN_TYPE, token):
            print("-----------------------Identify----------------------")
            print(f"Identifying self with token type {TOKEN_TYPE} and with token {token}")

            dump_json = {
                "op" : 2,
                "d" : {
                    "token" : token,
                    "properties" : {
                        "os" : "windows",
                        "browser" : "firefox",
                        "device" : "pc"
                    }
                }
            }

            self.gateway_send(dump_json)

            print("identify success!")
            print("-----------------------------------------------------\n")

    def gateway_send(self, dump):
        ws.send(json.dumps(dump))

    async def gateway_event(self):
        try:

            event = ws.recv()
            event_json = json.loads(event)

            with open("out.txt", 'w') as output:
                json.dump(event_json, output, indent=4)

            print(f"{event_json['d']}")
        except Exception as error:
            print(f"event failed because of {error}")



class main():
    def __init__(self) -> None:
        pass

    def read_token(self, TOKEN_TYPE):

        token_path = "supersecret.json"
        token = json.load(open(token_path, 'r'))

        return token[TOKEN_TYPE]

    async def keep_alive(self):
        print("hello world!")

        sl = socket_lib()
        TOKEN_TYPE = "selfbot_token"
        never_ran = True

        heartbeat_interval = sl.hello()
        token = self.read_token(TOKEN_TYPE)

        heartbeat = asyncio.create_task(
            sl.heartbeat(heartbeat_interval)
        )

        identify = asyncio.create_task(
            sl.identify(TOKEN_TYPE, token)
        )

        event = asyncio.create_task(
            sl.gateway_event()
        )

        print("entering heartbeat loop")
        while True:
            await heartbeat

            if never_ran:
                await identify
                never_ran = False

            print("-------------printing event-----------")
            await event
            print("-----------------------------------------------------\n")

            


        

if __name__ == "__main__":
    discord = "wss://gateway.discord.gg"
    ws = websocket.WebSocket()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(main().keep_alive())
    