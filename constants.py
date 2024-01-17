from dataclasses import dataclass


FPS = 60
SCREEN_SIZE = (800, 600)


@dataclass
class COLORS:
    WHITE: tuple[int] = (255, 255, 255)
    BLACK: tuple[int] = (0, 0, 0)
    RED: tuple[int] = (255, 0, 0)
    GREEN: tuple[int] = (0, 255, 0)
    BLUE: tuple[int] = (0, 0, 255)
    GRAY: str = "gray"
