from Environments import ZetlinEnvironment
from LearningAutomatas import TsetlinAutomata

from AutomataGames import GurGame




def automata_demo():
    env = ZetlinEnvironment(0.1, 0.3)

    la = TsetlinAutomata(6)

    action_count = [0, 0]

    for i in range(5000):
        action = la.make_decision()

        action_count[action - 1] += 1
        penalty = env.penalty(action)

        print("State:", la.state, "Action:", action)

        if penalty:
            print("Penalty")
            la.penalize()
        else:
            print("Reward")
            la.reward()

        print("New State:", la.state)

    print("#Action 1: ", action_count[0], "#Action 2:", action_count[1])

if __name__ == "__main__":

    ggs = [GurGame(nr_of_states= 1 + 3*v , nr_of_rounds=5000, nr_of_games=50) for v in range(1)]

    for game in ggs:
        print(game.games_mean)






