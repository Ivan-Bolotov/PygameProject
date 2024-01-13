class Client:
    @staticmethod
    def createRoom(ID):
        return f"ID:{ID}"

    @staticmethod
    def sendCords(x, y):
        return f"Cords:{x}:{y}"

    @staticmethod
    def sendMessage(msg):
        return f"Message:{msg}"

    @staticmethod
    def sendRes(res):
        return f"Res:{res}"
