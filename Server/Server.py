import asyncio
import websockets as ws


clients = []
rooms = []
counter = 0


async def handler(websocket: ws.WebSocketServerProtocol, addr: str):
    global counter

    try:
        websocket.id = str(counter)
        websocket.is_in_room = False
        counter += 1
        clients.append(websocket)
        await websocket.send("Your ID:" + str(websocket.id))
        while True:
            message = await websocket.recv()
            t, msg = message.split(":")
            if t == "ID" and not websocket.is_in_room:
                for c in clients:
                    if c.id == msg:
                        if not c.is_in_room:
                            print("Комната создана!")
                            rooms.append([websocket, c])
                            websocket.is_in_room = True
                            c.is_in_room = True
                            break
            else:
                for i in rooms:
                    if websocket == i[0]:
                        i[1].send(message)
                    elif websocket == i[1]:
                        i[0].send(message)
    except ws.ConnectionClosedOK:
        print("Close connection.")


async def main():
    async with ws.serve(handler, "26.234.107.47", 12345):
        print("Start serving...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
