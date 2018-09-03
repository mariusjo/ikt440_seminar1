import random


class GurGameEnvironment:

    def get_reward_prob(self, nr_of_yes):
        if nr_of_yes <= 3:
            return nr_of_yes * 0.2
        elif nr_of_yes <= 5:
            return 0.6 - (nr_of_yes - 3) * 0.2
        else:
            raise ValueError