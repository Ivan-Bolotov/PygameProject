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
            if t == "ID":
                if not websocket.is_in_room:
                    for c in clients:
                        if c.id == msg:
                            if not c.is_in_room:
                                rooms.append([websocket, c])
                                print("Комната создана!")
                                await websocket.send("Room created")
                                await c.send("Room created")
                                websocket.is_in_room = True
                                c.is_in_room = True
                                break
            else:
                for i in rooms:
                    if websocket == i[0]:
                        await i[1].send(message)
                        break
                    elif websocket == i[1]:
                        await i[0].send(message)
                        break
    except ws.ConnectionClosedOK:
        for i in rooms:
            if websocket in i:
                i[0].is_in_room, i[1].is_in_room = False, False
                rooms.remove(i)
                break
        clients.remove(websocket)
        print("Close connection.")


async def main():
    async with ws.serve(handler, "localhost", 12345):  #вместо IP можно написать localhost
        print("Start serving...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
