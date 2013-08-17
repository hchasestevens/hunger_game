# ===Tit For Tat===
'''
General strategy:

- Infer identity across rounds via reputation.

- Start first round with good-faith cooperation.

- In subsequent rounds, reciprocate what was done in previous round.

'''

from math import sqrt
from random import randint

class Player(object):

    def __str__(self):
        return "TFT"


    def __repr__(self):
        return "TFT"


    def __init__(self):
        """
        Optional __init__ method is run once when your Player object is created before the
        game starts

        You can add other internal (instance) variables here at your discretion.

        You don't need to define food or reputation as instance variables, since the host
        will never use them. The host will keep track of your food and reputation for you
        as well, and return it through hunt_choices.
        """
        self.food = 0
        self.reputation = 0
        self.rounds_elapsed = 0
        self.player_histories = []
        self.last_responses = None
        self.decisions_made = 0
        self.id_ = randint(0, 10000)

    # All the other functions are the same as with the non object oriented setting (but they
    # should be instance methods so don't forget to add 'self' as an extra first argument).

    def hunt_choices(self, round_number, current_food, current_reputation, m,
            player_reputations):
        ''' 
        The main routine that plays each individual round.

        You must create an array of variables 'hunt_decisions' and assign an 'h' for hunt or
        an 's' for slack (i.e., not hunt) to each member of the array; the order of the hunt
        decisions in hunt_decisions should correspond to the order of opponents'
        reputations in player_reputations.

        Blank variables or errors will be assigned 's'.

        The variables passed in to hunt_choices for your use are:
            round_number: integer, the number round you are in.
            current_food: integer, the amount of food you have.
            current_reputation: float (python's representation of real numbers), your current reputation.
            m: integer, the threshold cooperation/hunting value for this round.
            player_reputations: list of floats, the reputations of all the remaining players in the game.
                                The ordinal positions of players in this list will be randomized each round.
        '''
        
        self.reputation = current_reputation
        self.player_histories.append(player_reputations)

        # [(int, bool)] where int = index of player_reputations and bool = cooperated last round:
        cooperators = map(lambda ((reputation, i), prev_action): (i, prev_action >= 0),
                                    zip(sorted((rep, i) for i, rep in enumerate(player_reputations)),
                                        self.last_responses if self.last_responses is not None else [1] * len(player_reputations)
                                        )
                                    )
        cooperators.sort()
        # [(float, bool)] where float = opponent_reputation and bool = cooperated last round:
        player_reputations = zip(player_reputations, (cooperated for i, cooperated in cooperators))

        return ['h' if previously_cooperated else 's' for _, previously_cooperated in player_reputations]


    def hunt_outcomes(self, food_earnings):
        '''
        hunt_outcomes is called after all hunts for the round are complete.

        Add any code you wish to modify your variables based on the outcome of the last round.

        The variable passed in to hunt_outcomes for your use is:
            food_earnings: list of integers, the amount of food earned from the last round's hunts.
                           The entries can be negative as it is possible to lose food from a hunt.
                           The amount of food you have for the next round will be current_food
                           + sum of all entries of food_earnings + award from round_end.
                           The list will be in the same order as the decisions you made in that round.
        '''

        self.decisions_made += len(food_earnings)
        self.last_responses = food_earnings

        # match results with reputations, order accordingly:
        self.player_histories[-1], self.last_responses = zip(*sorted(zip(self.player_histories[-1],
                                                                         self.last_responses)
                                                                     )
                                                             )


    def round_end(self, award, m, number_hunters):
        '''
        round_end is called after all hunts for the round are complete.

        award - the total amount of food you received due to cooperation in the round.
        can be zero if the threshold m was not reached.

        add any code you wish to modify your variables based on the cooperation that occurred in
        the last round.

        the variables passed in to round_end for your use are:
            award: integer, total food bonus (can be zero) you received due to players cooperating
                   during the last round. the amount of food you have for the next round will be
                   current_food (including food_earnings from hunt_outcomes this round) + award.
            number_hunters: integer, number of times players chose to hunt in the last round.
        '''

        self.rounds_elapsed += 1
