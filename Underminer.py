# ===UNDERMINER===
'''
General strategy:

- Assume other players are inferring identity via reputation as described
 below.

- Assume (at least some of) these other players are employing tit-for-tat.

- If in a position with a slightly better reputation than some opponent
 and the ability to decrease own reputation to be slightly below the 
 projected lower bound of said opponent's next-round reputation, do so,
 thereby assuming their identity (and making gains) while simultaneously
 offloading some repercussions.

- Otherwise, act as a (forgiving) tit-for-tat bot. To link players between
 rounds, assume that ordering of player reputations is largely preserved
 between rounds.

'''

from math import sqrt
from math import ceil
from random import randint
from random import random

class Player(object):

    def __str__(self):
        return "Underminer (conf: %s | forg: %s | lim: %s)" %(str(self.confidence_interval), str(self.forgiveness_rate), str(self.cooperation_limit))


    def __repr__(self):
        return "Underminer"
    

    def __init__(self, confidence_interval=1.96, forgiveness_rate=0.01, cooperation_limit=5):
        """
        Optional __init__ method is run once when your Player object is created before the
        game starts
        """

        self.food = 0
        self.reputation = 0
        self.rounds_elapsed = 0
        self.player_histories = []
        self.last_responses = None
        self.decisions_made = 0

        # Chosen via empirical testing:
        self.confidence_interval = 1.318668962 #1.0 = 85%, 1.96 = 95%
        self.forgiveness_rate = 0.009708212
        self.cooperation_limit = 2

        # For debugging:
        self.id_ = randint(0, 10000)


    def hunt_choices(self, round_number, current_food, current_reputation, m,
            player_reputations):
        ''' 
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

        if round_number <= self.cooperation_limit:
            return ['h' for _ in player_reputations]

        _, lower_bound = self._get_reputation_bounds(len(player_reputations))

        opponents_projected = map(lambda rep: self._confidence(rep, len(player_reputations)),
                                  filter(lambda rep: rep < current_reputation, player_reputations)
                                  )
        underminables = filter(lambda (_, projected): projected > lower_bound, enumerate(opponents_projected))
        if underminables:
            # Hunting with the players we undermine overall confers an advantage, if players == 1
            return ['s' if len(underminables) > 1 or underminables[0][0] == index else 'h' 
                    for index, projected in
                    enumerate(player_reputations)]
            
        else:
            # Forgiving tit-for-tat, based off reasonable assumption that player reputation rankings are
            #  mostly static after a few rounds (see above).

            # [(int, bool)] where int = index of player_reputations and bool = cooperated last round:
            cooperators = map(lambda ((reputation, i), prev_action): (i, prev_action >= 0),
                                      zip(sorted((rep, i) for i, rep in enumerate(player_reputations)),
                                          self.last_responses if self.last_responses is not None else [1] * len(player_reputations)
                                          )
                                      )
            cooperators.sort()

            # [(float, bool)] where float = opponent_reputation and bool = cooperated last round:
            player_reputations = zip(player_reputations, (cooperated for i, cooperated in cooperators))

            return ['h' if previously_cooperated or self.forgiveness_rate > random() else 's' 
                for _, previously_cooperated in 
                player_reputations]


    def hunt_outcomes(self, food_earnings):
        '''
        The variable passed in to hunt_outcomes for your use is:
            food_earnings: list of integers, the amount of food earned from the last round's hunts.
                           The entries can be negative as it is possible to lose food from a hunt.
                           The amount of food you have for the next round will be current_food
                           + sum of all entries of food_earnings + award from round_end.
                           The list will be in the same order as the decisions you made in that round.
        '''

        self.decisions_made += len(food_earnings)
        self.last_responses = food_earnings

        # Match results with reputations, order accordingly:
        self.player_histories[-1], self.last_responses = zip(*sorted(zip(self.player_histories[-1],
                                                                         self.last_responses)
                                                                     )
                                                             )


    def round_end(self, award, m, number_hunters):
        '''
        the variables passed in to round_end for your use are:
            award: integer, total food bonus (can be zero) you received due to players cooperating
                   during the last round. the amount of food you have for the next round will be
                   current_food (including food_earnings from hunt_outcomes this round) + award.
            number_hunters: integer, number of times players chose to hunt in the last round.
        '''

        self.rounds_elapsed += 1


    def _get_reputation_bounds(self, n_players, reputation=None, past=None):
        '''
        Returns tuple of (upper_bound, lower_bound) possible given specified number of decisions
        available in the current round.
        '''

        if reputation == None:
            reputation = self.reputation
        if past == None:
            past = self.decisions_made
        
        hunts = self._get_past_hunts(reputation, past)
        return ((hunts + n_players) / (past + n_players)), (hunts / (past + n_players))


    def _confidence(self, reputation, n_players):
        '''
        Returns lower bound of a player's reputation at end-of-round with confidence_interval
        confidence.
        '''
        if not self.decisions_made:
            return 0
        prob_hunt = self._calc_confidence(reputation, self.decisions_made, self.confidence_interval)

        # Return how prob_hunt affects likely rep at end of this round
        hunts = self._get_past_hunts(reputation, self.decisions_made)
        return (hunts + round(prob_hunt * n_players)) / (self.decisions_made + n_players)


    @staticmethod
    def _calc_confidence(reputation, n, z):
        '''
        Get lower bound of william score interval (i.e. lower bound of "true" liklihood to hunt).
        Taken from http://stackoverflow.com/questions/10029588/python-implementation-of-the-wilson-score-interval.
        '''
        return ((reputation + z * z/(2 * n) - z * sqrt((reputation * (1 - reputation) + z * z / (4 * n)) / n)) / (1 + z * z / n))


    @staticmethod
    def _get_past_hunts(reputation, past):
        return int(ceil(reputation * past))

