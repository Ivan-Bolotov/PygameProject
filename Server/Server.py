import asyncio
import websockets as ws


async def handler(conn, url):
    print("New connection!")
    while True:
        data = conn.recv()
        print(f"{data} from {url}")


async def main():
    await ws.serve(handler, "127.0.0.1", 12345)

if __name__ == '__main__':
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
