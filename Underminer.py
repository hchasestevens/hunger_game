# ===UNDERMINER===
'''
General strategy:

- Assume other players are inferring identity via reputation.

- Assume (at least some of) these other players are employing tit-for-tat.

- If in a position with a slightly better reputation than some opponent
 and the ability to decrease own reputation to be slightly below the 
 projected lower bound of said opponent's next-round reputation, do so,
 thereby assuming their identity (and making gains) while simultaneously
 offloading some repercussions.

'''

from math import sqrt
from math import ceil


class Player:
    def __str__(self):
        return "MegaMagiTech MechaMech Mk. III"
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
        self.confidence_interval = 1.0 #1.0 = 85%, 1.96 = 95%
        self.rounds_elapsed = 0
        self.player_histories = []
        self.last_responses = None
        self.decisions_made = 0

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

        # TODO: until _is_distinguishable, choose non-undermining strat to enact
        #  e.g. tit-for-tat, tit-for-tat with forgiveness? Something else?
        # The aim here would be to get in a position where many will be underminable,
        #  so want to have high rep without
        #   A) dying
        #   B) overshooting majority of population 

        _, lower_bound = self._get_reputation_bounds(len(player_reputations))

        opponents_projected = map(lambda rep: self._confidence(rep, len(player_reputations)),
                                  filter(lambda rep: rep < current_reputation, player_reputations)
                                  )
        underminable = filter(lambda projected: projected > lower_bound, opponents_projected)
        if underminable:
            # The following are purely informational, maybe useful for debug?:
            aim = min(underminable)
            hunts_allowed = len(player_reputations) - self._get_slacks_needed(aim, len(player_reputations))

            return ['s' for _ in player_reputations]
            
        else:
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


    def _is_distinguishable(self, n_players):
        return (lambda : (2 ** (self.rounds_elapsed * n_players)) >= n_players)()


    def _get_slacks_needed(self, reputation_aim, decisions, current_reputation=None):
        '''
        Get number of slacks necessary to end the round with a reputation below the given reputation aim.
        Note that this number is not neccesarily in [0,decisions]. If it is larger, we need to dive for more than
        one round to reach our target. If it is negative, we will end the round below the target regardless of our
        actions.
        '''

        if current_reputation == None:
            current_reputation = self.reputation
        
        hunts = self._get_past_hunts(current_reputation, self.decisions_made)

        return int(ceil(hunts + decisions - (self.decisions_made + decisions) * reputation_aim))


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
        # TODO: Third argument of following should be calculated from self.confidence_interval 
        #  using p-value of normal distribution for a confidence level between 0-1 (i.e. .95
        #  confidence interval would be 95% confidence, as expected. To do this, probably want
        #  to re-write ruby's statistics2 pnormaldist func, found here as 'pnorm':
        #  http://blade.nagaokaut.ac.jp/~sinara/ruby/math/statistics2/statistics2-0.53/statistics2.rb
        #  Usage example: Statistics2.pnormaldist(1-(1-(.95))/2) == 1.96
        #  Alternatively, try using either scipy.stats.norm.sf(.95) or 
        #  scipy.stats.stats.zprob(.95) or scipy.special.ndtr(.95) (it's unclear from 
        #  http://stackoverflow.com/questions/3496656/convert-z-score-z-value-standard-score-to-p-value-for-normal-distribution-in
        #  which of these we might want). 
        prob_hunt = self._calc_confidence(reputation, self.decisions_made, self.confidence_interval)

        # return how prob_hunt affects likely rep at end of this round
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

