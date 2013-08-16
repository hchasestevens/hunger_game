# ===Tit For Tat===
'''
General strategy:

- Infer identity across rounds via reputation.

- Start first round with good-faith cooperation.

- In subsequent rounds, reciprocate what was done in previous round.

'''

from math import sqrt

class Player:
    def __str__(self):
        return "TFT"
    def __repr__(self):
        return "TFT"
    def __init__(self):
        #dict sending (scrambled) position to the last response from there 
        self.responses = None
        #dict sending sorted position to scrambled position
        self.positions = None

    # All the other functions are the same as with the non object oriented setting (but they
    # should be instance methods so don't forget to add 'self' as an extra first argument).

    def hunt_choices(self, round_number, current_food, current_reputation, m,
            player_reputations):

        sorted_reps = sorted(zip(player_reputations,range(len(player_reputations))))
        self.positions = {new_i : old_i for ((_,old_i),new_i)in zip(sorted_reps, range(len(sorted_reps)))}
        
        return [self._get_last_response(i) for i in range(len(player_reputations))]


    def hunt_outcomes(self, food_earnings):
        self.responses = { self._get_sorted_position(i) : 'h' if food >= 0 else 's' for (food, i) in zip(food_earnings,range(len(food_earnings)))}

    def _get_last_response(self, scrambled_pos):
        if self.responses == None:
            return 'h'
        return self.responses[self._get_sorted_position(scrambled_pos)]

    def _get_sorted_position(self, scrambled_pos):
        if self.positions == None:
            return scrambled_pos
        return self.positions[scrambled_pos]
                          
    def round_end(self, award, m, number_hunters):
        pass

