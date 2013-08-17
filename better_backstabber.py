from random import randint

class Player(object):

    def __str__(self):
        return "'Better'_Backstabber"


    def __repr__(self):
        return "'Better'_Backstabber"

    def __init__(self): 
        self.ROUND_THRESHOLD= 1000
        self.REPUTATION_THRESHOLD = 0.55
        self.REP_MULTIPLIER = 1.0
        self.SUCKERS = 0.2
        self.id_ = randint(0, 10000)

    # Basic strategy:
    # 1. Maintain average reputation at all times. Do this by selecting average_rep
    #    fraction of the players you are paired with to hunt with. Slack off on all
    #    other missions.
    # 2. People with really low reputations are not valuable, so slack off when
    #    paired with them each time, to cause them to die faster.
    # 3. People with really high reputations are considered "self.SUCKERS" -- they hunt
    #    too much, so we take advantage of them by slacking off with them
    #    frequently. If they are intelligent, they will drop down their reputation,
    #    and we'll do the same with the next set of self.SUCKERS. If not, they will die.
    #    Either choice is cool with us :)
    # 4. Hunt with people who are not self.SUCKERS or low reputation.

    def hunt_choices(self, round_number, current_food, current_reputation, m,
                     player_reputations):

        avg_reputation = float(sum(player_reputations))/len(player_reputations)
        # Reputations are weird in the beginning, set a minimum reputation for the
        # first few rounds.
        if round_number <= self.ROUND_THRESHOLD:
            avg_reputation = max(avg_reputation, self.REPUTATION_THRESHOLD)
        players_to_trust = self.REP_MULTIPLIER * (avg_reputation * len(player_reputations))
        players_to_backstab = self.SUCKERS * len(player_reputations)
        # Find the upper and lower bound of the reputation which we want to
        # hunt with (anything higher than upper is a sucker, anything lower than
        # lower is too lazy).
        lower_bound = int(min(players_to_backstab, len(player_reputations)-1))
        upper_bound = int(min(players_to_trust+players_to_backstab, len(player_reputations)))
    
        reps = zip(range(len(player_reputations)), list(player_reputations))
        reps.sort(key=lambda tup: tup[1], reverse=True)
        # The set off people who maintain middle reputation (these are the ones we
        # want to hunt with).
        anti_SUCKERS = [r[0] for r in reps[lower_bound:upper_bound]]

        """
        # DEBUG INFO
        if round_number == 200:
            print "avg_reputation", avg_reputation
            print "players_to_trust", players_to_trust
            print "players_to_backstab", players_to_backstab
            print anti_self.SUCKERS
        """
    
        hunt_decisions = list()
        for i in xrange(len(player_reputations)):
            if i in anti_SUCKERS:
                hunt_decisions.append('h')
            else:
                hunt_decisions.append('s')
        return hunt_decisions


    # We don't care what other people did, since we can't track who is who in the
    # long run anyway.
    def hunt_outcomes(self, food_earnings):
        pass # do nothing


    # m is not really relevant until the very end game, since nothing we do will
    # influence it much.
    def round_end(self, award, m, number_hunters):
        pass # do nothing