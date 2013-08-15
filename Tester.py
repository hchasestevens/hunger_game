import random


class RandBot:
    def __str__(self):
        return "RandBot Mk. IV (" + str(self.p) + ")"
    def __repr__(self):
        return self.__str__()

    
    def __init__(self, p):
        self.p = p

    def hunt_choices(self,
                     round_number,
                     current_food,
                     current_reputation,
                     m,
                     player_reputations):
        return ['s' if random.random() > self.p else 'h' for x in player_reputations]
    
    def hunt_outcomes(self, food_earnings):
        pass
    
    def round_end(self, award, m, number_hunters):
        pass

def insertself(list, index):
    return list[0:index] + ['X'] + list[index:]
    
LVL_NONE = 0
LVL_LOW = 1
LVL_REGULAR = 2
LVL_DBG = 3

BOT_I = 0
FOOD_I = 1
REP_I = 2

def rungame(bots, dbg_lvl, seed=None):
    seed and random.seed(seed)
    
    #(bot, current food, amount of hunts made)
    entries = [[bot,300*(len(bots)-1),0] for bot in bots]

    round = 1
    
    bonus_food_bound = 999999
    tot_hunts = 0.0
    
    while len(entries)> 1:
        p = len (entries)
        
        round_hunts = 0        
        m=random.randint(1,p*(p-1)-1)
        
        dead_bots = 0

        if dbg_lvl >= LVL_DBG:
            print ""
            print "Round " + str(round) + ", FIGHT!"

        random.shuffle(entries)
        if dbg_lvl >= LVL_DBG:
            print "Post-shuffle entries: " + entries.__str__()

        reps = map (lambda e:e[REP_I]/(tot_hunts if tot_hunts > 0 else 1.0), entries)

        if dbg_lvl >= LVL_DBG:
            print "reps: " + reps.__str__()
        
        choices = [insertself(bot.hunt_choices(round, food, rep, m, reps[0:index] + reps[index+1:]),index)
                   for ([bot, food, rep], index)
                   in zip (entries, range(0,p))
                   ]
        
        if dbg_lvl >= LVL_DBG:
            print "Choices made: ["
            for l in choices:
                print l
            print "]"

        #drain food
        for i in range(0,p):
            for j in range(0,p):
                if choices[i][j] == 'h':
                    entries[i][REP_I] += 1
                    entries[i][FOOD_I] -= 3
                    entries[j][FOOD_I] += 3
                    round_hunts += 1
                if choices[i][j] == 's':
                    entries[i][FOOD_I] -= 2

        #hunt_outcomes
        for i in range(0,p):
            outcomes = []
            for j in range(0,p):
                if i != j:
                    index = j if j<i else j-1
                    outcomes.append(-2)
                    if(choices[i][j]=='h'):
                        outcomes[index] -= 1
                    if(choices[i][j]=='h'):
                        outcomes[index] += 3
            entries[i][BOT_I].hunt_outcomes(outcomes)

        if round_hunts >= m:
            if dbg_lvl >= LVL_DBG:
                print "Hunt goal reached in round " + str(round) + ", bonus food will be awarded"
            for e in entries:
                e[FOOD_I] += 2*(p-1)
        
        for e in entries:
            if dbg_lvl >= LVL_REGULAR and e[FOOD_I] <= 0:
                print e[BOT_I].__str__() + " failed at not starving in round " + str(round)
                dead_bots = 1

        entries = filter (lambda e:e[FOOD_I]>0, entries)

        if dead_bots and dbg_lvl >= LVL_REGULAR:
            print "Current state: " + entries.__str__()

        #round_end
        for e in entries:
            e[BOT_I].round_end(2*(p-1) if round_hunts >= m else 0, m, round_hunts)
        
        round += 1
        tot_hunts += p-1

        if round >= 2000 and random.random() > 0.99:
            if dbg_lvl >= LVL_LOW:
                print "Game ended due to timeout"
                break


    
    if dbg_lvl >= LVL_LOW:
        print "REMAINING BOTS: " + (entries.__str__() if entries else "None")
        print "=============== Game Finished ==============="
    
rungame([RandBot(1), RandBot(0.5), RandBot(0.5), RandBot(0)], LVL_REGULAR, 1234567890)