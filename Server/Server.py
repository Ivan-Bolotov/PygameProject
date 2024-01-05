import asyncio
import websockets as ws


clients = []
rooms = []


async def handler(websocket: ws.WebSocketServerProtocol, addr: str):
    try:
        clients.append(websocket)
        await websocket.send("Your ID:" + str(websocket.id))
        while True:
            message = await websocket.recv()
            t, msg = message.split(":")
            if t == "ID":
                for c in clients:
                    if c.id == msg:
                        rooms.append([websocket, c])
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
    async with ws.serve(handler, "localhost", 12345):
        print("Start serving...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
