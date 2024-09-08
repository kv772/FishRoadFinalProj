import pygame, random
from log import Log

class River:
    # Define constant values
    SIZE = (600, 30)
    SCREEN_DIM = 600, 500

    # Creates a Log object
    def __init__(self, river_height: int, direction: str, number_of_logs: int):
        # River Information
        self.rect = pygame.Rect((0, river_height), River.SIZE)
        self.logs = []
        # Add Logs
        self.add_logs(direction, number_of_logs, river_height + 15)

    # This function randomizes an X position until there is no other Log 30 pixels infront and 30 pixels behind them
    # Ensures logs do not stack on top of one another
    def add_logs(self, direction: str, number_of_logs: int, river_height: int):
        dp = []
        for _ in range(number_of_logs):
            while True:
                x_pos = random.randint(30, 570)
                valid = True
                for i in range(x_pos - 60, x_pos + 60):
                    if i in dp:
                        valid = False
                if valid:
                    dp.append(x_pos)
                    break
            self.logs.append(Log((x_pos, river_height), direction))