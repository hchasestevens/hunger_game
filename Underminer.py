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

class Player:
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
        self.confidence_interval = 1.0 #1.0 = 85%, 1.6 = 95%
        self.rounds_elapsed = 0
        self.player_histories = None
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
        hunt_decisions = ['h' for x in player_reputations] # replace logic with your own
        return hunt_decisions


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
        pass # do nothing


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
        pass # do nothing


    def _confidence(self, reputation):
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
        return self._calc_confidence(reputation, self.decisions_made, self.confidence_interval)


    @staticmethod
    def _calc_confidence(reputation, n, z):
        '''
        Get lower bound of william score interval (i.e. lower bound of "true" liklihood to hunt).
        Taken from http://stackoverflow.com/questions/10029588/python-implementation-of-the-wilson-score-interval.
        '''
        return ((reputation + z*z/(2*n) - z * sqrt((reputation*(1-reputation)+z*z/(4*n))/n))/(1+z*z/n))

