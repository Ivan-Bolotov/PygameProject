class Client:
    @staticmethod
    def createRoom(ID: int | str):
        return f"ID:{ID}"

    @staticmethod
    def sendCords(x: int, y: int):
        return f"Cords:{x}:{y}"

    @staticmethod
    def sendMessage(msg: str):
        return f"Message:{msg}"

    @staticmethod
    def sendRes(res: bool):
        return f"Res:{res}"
