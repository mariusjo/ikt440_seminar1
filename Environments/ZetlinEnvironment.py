import random


class ZetlinEnvironment:

    def __init__(self, c_1, c_2):
        self.c_1 = c_1
        self.c_2 = c_2

    def penalty(self, action):
        if action == 1:
            if random.random() <= self.c_1:
                return True
            else:
                return False
        elif action == 2:
            if random.random() <= self.c_2:
                return True
            else:
                return False
