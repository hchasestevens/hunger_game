# ===SAMPLE PLAYER===
# Might want to use following for prediction of opponents? http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
# ptyhon implementation (as by reddit) here: http://stackoverflow.com/questions/10029588/python-implementation-of-the-wilson-score-interval
# NB comment in above saying 95% confidence should be z = 1.96, not z = 1.6

##OOP version:
#Seems like a good idea to use this approach, for ease of testing/competition simulation

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
        pass # do nothing
