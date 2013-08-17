import random
from tit_for_tat import Player as Tft
from tit_for_tat_forgiveness import Player as Tftf
from underminer import Player as Underminer
from tkFileDialog import asksaveasfile

class RandBot:
    def __str__(self):
        return "RandBot (" + str(self.p) + ")"
    def __repr__(self):
        return self.__str__()

    
    def __init__(self, p):
        self.p = p
        self.id_ = random.randint(0,10000)

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
    

class Verbosity():
    NONE, LOW, REGULAR, DBG, CSV = range(5)


class Index():
    BOT, FOOD, REP = range(3)


def rungame(bots, verbosity, seed=None):

    output = ""

    seed and random.seed(seed)
    
    if verbosity == Verbosity.CSV:
        output += ','.join("round bot_id bot_type bot_details food reputation".split()) + '\n'

    #(bot, current food, amount of hunts made)
    entries = [[bot,300*(len(bots)-1),0] for bot in bots]

    round = 1
    
    bonus_food_bound = 999999
    tot_hunts = 0.0
    
    while len(entries)> 1:
        p = len (entries)
        
        round_hunts = 0        
        m = random.randint(1,p*(p-1)-1)
        
        dead_bots = 0

        if verbosity >= Verbosity.DBG:
            print ""
            print "Round " + str(round) + ", FIGHT!"

        random.shuffle(entries)
        if verbosity == Verbosity.DBG:
            print "Post-shuffle entries: " + entries.__str__()

        reps = map (lambda e:e[Index.REP]/(tot_hunts if tot_hunts > 0 else 1.0), entries)

        if verbosity == Verbosity.DBG:
            print "reps: " + reps.__str__()
        
        choices = [insertself(bot.hunt_choices(round, food, rep, m, reps[0:index] + reps[index+1:]),index)
                   for ([bot, food, rep], index)
                   in zip (entries, range(0,p))
                   ]
        
        if verbosity == Verbosity.DBG:
            print "Choices made: ["
            for l in choices:
                print l
            print "]"

        #drain food
        for i in range(0,p):
            for j in range(0,p):
                if choices[i][j] == 'h':
                    entries[i][Index.REP] += 1
                    entries[i][Index.FOOD] -= 3
                    entries[j][Index.FOOD] += 3
                    round_hunts += 1
                if choices[i][j] == 's':
                    entries[i][Index.FOOD] -= 2

        #hunt_outcomes
        for i in range(0,p):
            outcomes = []
            for j in range(0,p):
                if i != j:
                    index = j if j<i else j-1
                    outcomes.append(-2)
                    if(choices[i][j]=='h'):
                        outcomes[index] -= 1
                    if(choices[j][i]=='h'):
                        outcomes[index] += 3
            entries[i][Index.BOT].hunt_outcomes(outcomes)

        if round_hunts >= m:
            if Verbosity.CSV > verbosity >= Verbosity.DBG:
                print "Hunt goal reached in round " + str(round) + ", bonus food will be awarded"
            for entry in entries:
                entry[Index.FOOD] += 2*(p-1)
        
        for entry in entries:
            if Verbosity.CSV > verbosity >= Verbosity.REGULAR and entry[Index.FOOD] <= 0:
                print entry[Index.BOT].__str__() + " failed at not starving in round " + str(round)
                dead_bots = 1

        entries = filter (lambda e:e[Index.FOOD]>0, entries)

        if dead_bots and Verbosity.CSV > verbosity >= Verbosity.REGULAR:
            print "Current state: " + entries.__str__()

        #round_end
        for entry in entries:
            entry[Index.BOT].round_end(2*(p-1) if round_hunts >= m else 0, m, round_hunts)
        
        round += 1
        tot_hunts += p-1

        # CSV output
        if verbosity == Verbosity.CSV:
            for entry in entries:
                output += ','.join(
                                   map(str,[round,
                                    entry[Index.BOT].id_,
                                    str(entry[Index.BOT]).split()[0]
                                    ]) + map(str,entry[:-1] + [entry[-1] / tot_hunts])
                                   ) + '\n'

        if round >= 50 and random.random() > 0.99:
            if Verbosity.CSV > verbosity >= Verbosity.LOW:
                print "Game ended due to timeout"
            break
    
    if Verbosity.CSV > verbosity >= Verbosity.LOW:
        print "REMAINING BOTS: " + (sorted(entries,key=(lambda e:-e[Index.FOOD])).__str__() if entries else "None")
        print "=============== Game Finished ==============="

    with asksaveasfile() as f:
        f.write(output)
 
        
def main():
    rungame(
            [RandBot(random.random()) for _ in xrange(2)] + 
            [Tft() for _ in xrange(1)] + 
            [Tftf(random.random()) for _ in xrange(1)] + 
            [Underminer(random.random() * 2) for _ in xrange(1)] + 
            [Underminer(1.96)]
            , Verbosity.CSV, 1234567890)

           
if __name__ == "__main__":        
    main()
    raw_input("Enter to exit.")


