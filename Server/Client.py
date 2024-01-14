class Client:
    @staticmethod
    def createRoom(ID):
        return f"ID:{ID}"

    @staticmethod
    def sendCords(x: int, y: int):
        return f"Cords:{x}:{y}"

    @staticmethod
    def sendMessage(msg: str):
        return f"Message:{msg}"

    @staticmethod
    def sendMatrix(matrix: list[list[int]]):
        return f"Matrix:{matrix}"
