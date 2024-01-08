import asyncio
import websockets as ws


class Client:
    def __init__(self, conn, my=((0,) * 10,) * 10, op=((0,) * 10,) * 10):
        self.MyMatrix = list[list[int]](my)
        self.OpponentMatrix = list[list[int]](op)
        self.messages = []
        self.websocket = conn

    async def createRoom(self, ID):
        if self.websocket is not None:
            if not self.websocket.closed:
                await self.websocket.send(f"ID:{ID}")
            else:
                print("Connection is already closed!")
        else:
            print("You are still not connected!")

    def setConnection(self, websocket):
        self.websocket = websocket

    async def sendCords(self, x, y):
        if self.websocket is not None:
            if not self.websocket.closed:
                await self.websocket.send(f"Cords:{x}:{y}")
            else:
                print("Connection is already closed!")
        else:
            print("You are still not connected!")

    async def sendMessage(self, msg):
        if self.websocket is not None:
            if not self.websocket.closed:
                await self.websocket.send(f"Message:{msg}")
            else:
                print("Connection is already closed!")
        else:
            print("You are still not connected!")

    async def recv(self):
        if self.websocket is not None:
            if not self.websocket.closed:
                return await self.websocket.recv()
            else:
                print("Connection is already closed!")
        else:
            print("You are still not connected!")

    async def sendRes(self, res):
        if self.websocket is not None:
            if not self.websocket.closed:
                await self.websocket.send(f"Res:{res}")
            else:
                print("Connection is already closed!")
        else:
            print("You are still not connected!")
