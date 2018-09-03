from Environments import GurGameEnvironment
from LearningAutomatas import TsetlinAutomata

import random

from collections import defaultdict


class GurGame:
    """
    Download and installPythonfromhttp://www.python.org

    Implement the following program and justify your results:

    1. Create 5 Tsetlin Automata with actions No and Yes
    2. Count the number of Tsetlin Automata that outputs a Yes-action
    3. If the number of Yes-actions is M Then:
        * If M = 0 OR 1 OR 2 OR 3: Give each Automaton a reward with probability M*0.2, otherwise a penalty
        * If M = 4 OR 5 : Give each Automaton a reward with probability 0.6-(M-3)*0.2, otherwise a penalty
    4. Goto 2

    Remark:Generate the rewards independently for each automaton

    ----------

    NOTES:

    - started the nr of states at 3. this did yield around half of the runs to be the optimal nr of yes votes (3).

    Todo:

    -add extra outer loop that runs the gur game x amount of times.
    -calculate and plot stats for different nr_of_states config... (maybe 3,6,9,12......huge number)
     and nr of steps in each gur game
    -....



    """

    action_desc = {0: "No", 1: "Yes"}
    nr_of_states = 3
    players = None
    games_mean = 0

    def __init__(self, nr_of_states=3, nr_of_rounds=500, nr_of_games=1):
        self.gg_environment = GurGameEnvironment()
        self.nr_of_games = nr_of_games
        self.games = [{
            "round_votes": defaultdict(lambda: [0, 0]),
            "round_votes_summarized": [0, 0, 0, 0, 0, 0],
            "mean_nr_of_yes": 0
        } for n in range(self.nr_of_games)]
        self.nr_of_states = nr_of_states
        self.nr_of_rounds = nr_of_rounds
        self.players = [TsetlinAutomata(self.nr_of_states) for i in range(1, 6)]
        self.run_games()

    def get_mean(self, prev_mean, x, n):
        return ((prev_mean *
                 n + x) /
                (n + 1))

    def run_games(self):
        means = defaultdict(lambda: 0)
        for j in range(self.nr_of_games):
            self.run_game(game_nr=j)
            means[j] = sum([x[1] for i, x in enumerate(list(self.games[j]["round_votes"].values()))])/self.nr_of_rounds
        means = list(means.values())
        self.games_mean = sum(means)/self.nr_of_games

    def run_game(self, game_nr):

        for i in range(self.nr_of_rounds):
            nr_of_pos_votes = 0

            for j, p in enumerate(self.players):
                # player votes
                vote = p.make_decision()
                self.games[game_nr]["round_votes"][i][vote] += 1
                nr_of_pos_votes += vote

            self.games[game_nr]["round_votes_summarized"][nr_of_pos_votes] += 1
            self.games[game_nr]["mean_nr_of_yes"] = \
                self.get_mean(prev_mean=self.games[game_nr]["mean_nr_of_yes"], x=nr_of_pos_votes, n=i)

            # Calculate chance for reward and reward/penalize players
            reward_prob = self.gg_environment.get_reward_prob(nr_of_pos_votes)
            for j, p in enumerate(self.players):
                # player is rewarded or penalized
                reward = random.random() <= reward_prob
                if reward:
                    p.reward()
                else:
                    p.penalize()
