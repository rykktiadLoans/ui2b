import json, random, copy, math
import sys

class Fitness:
    def __init__(self, fitness, instructions):
        self.fitness = fitness
        self.instructions = instructions
#represantaion of a treasure on a grid
class Treasure:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#represatation of a field, treasure on it, and a finder guy.
class Field:
    def __init__(self, fieldfile):
        fieldJSON = fieldfile
        self.sizex = fieldJSON["size"]["x"]
        self.sizey = fieldJSON["size"]["y"]
        self.playerx = fieldJSON["start"]["x"]
        self.playery = fieldJSON["start"]["y"]
        self.treasure = []
        for i in fieldJSON["treasure"]:
            self.treasure.append(Treasure(i["x"], i["y"]))
        self.treasureCount = len(self.treasure)
        self.currentTreasure = 0
        self.steps = 0

    #print out the field to the standard output
    def print(self):
        output = ""
        for y in range(self.sizey):
            for x in range(self.sizex):
                isTreasure = False
                for t in self.treasure:
                    if(t.x == x and t.y == y):
                        isTreasure = True
                        output += "t"
                        break
                if(not isTreasure and self.playerx == x and self.playery == y):
                    output += "p"
                    continue
                if(not isTreasure):
                    output += " "
            output += "\n"
        print(output)

    #move the player up
    def up(self):
        if(self.playery != 0):
            self.playery -= 1
            self.treasureCheck()
            return True
        else:
            return False
    #move the player down
    def down(self):
        if(self.playery < self.sizey):
            self.playery += 1
            self.treasureCheck()
            return True
        else:
            return False
    #move the player right
    def right(self):
        if(self.playerx != 0):
            self.playerx += 1
            self.treasureCheck()
            return True
        else:
            return False
    #move the player left
    def left(self):
        if(self.playerx < self.sizex):
            self.playerx -= 1
            self.treasureCheck()
            return True
        else:
            return False
    #check whether we hit a treasure
    def treasureCheck(self):
        self.steps += 1
        for t in self.treasure:
            if(t.x == self.playerx and t.y == self.playery):
                self.treasure.remove(t)
                self.currentTreasure += 1
                break
    #read a direction and move in that direction
    def smartMoving(self, dir):
        val = False
        if(dir == "H"):
            val = self.up()
        if(dir == "D"):
            val = self.down()
        if(dir == "P"):
            val = self.right()
        if(dir == "L"):
            val = self.left()
        return val

#represantaion of the most basic ra machine ever made. computer scientists in the 1950 will weep
class Machine:
    def __init__(self):
        self.instructions = ["00000000" for x in range(64)]
        self.current = 0
        self.total = 0
        self.output = ""
        self.state = "a" # a-active d-done f-fail

    #do one instruction
    def next(self):
        if(self.state == "d" or self.state == "f"):
            return False
        adress = self.instructions[self.current][2:]
        action = self.instructions[self.current][:2]
        if(action == "00"):
            n = int(self.instructions[int(adress,2)], 2)
            n += 1
            if(n > 255):
                n = 0
            n = format(n, "b").zfill(8)
            self.instructions[int(adress, 2)] = n

            self.current += 1
        if(action == "01"):
            n = int(self.instructions[int(adress,2)], 2)
            n -= 1
            if(n < 0):
                n = 255 
            n = format(n, "b").zfill(8)
            self.instructions[int(adress, 2)] = n

            self.current += 1
        if(action == "10"):
            n = int(adress, 2)
            self.current = n
        if(action == "11"): 
            #  0
            # 1 2
            #  3
            n = int(adress[-2:], 2)
            if(n == 0):
                self.output += "H"
            if(n == 1):
                self.output += "L"
            if(n == 2):
                self.output += "P"
            if(n == 3):
                self.output += "D"
            self.current+= 1
        if(self.current > 63):
            self.state = "f"
            return False
        self.total += 1
        if(self.total >= 500):
            self.state = "f"
            return False
        return True

#initialize the machine with 16 random instructions
def initInstructions(machine):
    count = 32
    for i in range(count):
        out = ""
        for j in range(8):
            out += str(random.randint(0, 1))
        machine.instructions[i] = out
    return machine


#calculate fitness
def calcFitness(field):
    POINTFOUND = 50000 
    POINTSTEP = -1
    points = 500
    if(field.steps == 0):
        points -= 200
    points += POINTFOUND * field.currentTreasure + POINTSTEP * field.steps
    return points

#get output of a machine
def getOutput(machine):
    val = True
    while(val):
        val = machine.next()
    return machine.output

#get the result of a series of operations on a field
def runField(field, output):
    for i in output:
        field.smartMoving(i)
        if(field.currentTreasure == field.treasureCount):
            return field
    return field

def crossover(in1 : list[str], in2: list[str]):
    output1 = []
    output2 = []
    l = list(filter(lambda x: x != "00000000", in1))
    spot = random.randint(0, len(l) -1)
    output1 += in1[spot:]
    output2 += in2[spot:]
    output1 += in2[:spot]
    output2 += in1[:spot]
    return [output1, output2]

def mutate(inst: list[str]):
    # add, remove, clear, randomize, switch
    inst = inst
    available = maxmut
    while available > 0:
        sel = (random.randint(0, 99))
        if (sel < 30):
                output = ""
                index = inst.index("00000000") if "00000000" in inst else -1
                if(index == -1):
                    continue
                for i in range(8):
                    output += str(random.randint(0,1))
                inst[index] = output
                available -= 5 
        elif (sel < 50):
                index = random.randint(0,63)
                inst.pop(index)
                inst.append("00000000")
                available -= 10
        elif (sel < 60):
                index = random.randint(0,63)
                while(inst[index] == "00000000"):
                    index = random.randint(0,63)
                inst[index] = "00000000"
                available -= 5
        elif (sel < 20):
                output = ""
                index = random.randint(0, 63)
                for i in range(8):
                    output += str(random.randint(0,1))
                inst[index] = output
                available -=  5
        elif (sel < 99):
                index1 = random.randint(0, 63)
                index2 = random.randint(0, 63)
                while(index1 == index2):
                    index2 = random.randint(0, 63)
                inst[index1], inst[index2] = inst[index2], inst[index1]
                available -= 5
    return inst

def roulette(fitarr: list[Fitness]):
    output : list[Fitness]= []
    while(len(output) < SELECTSIZE):
        total = 0 
        for i in range(len(fitarr)):
            total += fitarr[i].fitness
        current = random.randint(0, total)
        index = 0 
        while(fitarr[index].fitness < current -1):
            current -= fitarr[index].fitness
            index += 1 
        output.append(fitarr[index])
        fitarr.remove(fitarr[index])
    return output

def tournament(fitarr: list[Fitness]):
    lists = []
    cur = []
    while(len(fitarr) > 0):
        i = random.randrange(0, len(fitarr))
        cur.append(fitarr[i])
        fitarr.pop(i)
        if(len(cur) > 2):
            cur.sort(key=lambda x: x.fitness, reverse=True)
            lists.append(cur[0])
            cur = []

    return lists

def construct(fitarr : list[Fitness], selection):
    fitarr = selection(fitarr)
    instr = [x.instructions for x in fitarr]
    newinstr = []
    while(len(newinstr) < POPULATION):
        i1 = random.randint(0, SELECTSIZE - 1)
        i2 = random.randint(0, SELECTSIZE - 1)
        while(i2 == i1):
            i2 = random.randint(0, SELECTSIZE - 1)
        res = crossover(instr[i1], instr[i2])
        newinstr += res
    mutres = [mutate(x) for x in newinstr]
    maken = []
    for i in mutres:
        t = Machine()
        t.instructions = i
        maken.append(t)
    return maken


POPULATION = 90
maxmut = 25
SELECTSIZE = 30

filename = "field.json"
jsonfile = json.load(open(filename, "r"))
machine = Machine()
machine = initInstructions(machine)
machines = [initInstructions(Machine()) for x in range(POPULATION)]
gen = 0
Field(jsonfile).print()
print("Genereation number : Maximum treasures found")
while(True):
    fields = [Field(jsonfile) for x in range(POPULATION)]
    instr = [copy.deepcopy(x.instructions) for x in machines]
    output = [getOutput(machines[x]) for x in range(POPULATION)]
    runned = [runField(fields[x], output[x]) for x in range(POPULATION)]
    fitnessdickinyourmouth = [calcFitness(runned[x]) for x in range(POPULATION)]

    found = 0 
    for i in range(POPULATION):
        found = runned[i].currentTreasure if runned[i].currentTreasure > found else found
    print("Gen", gen, ":", found, "\r", end="")
    gen += 1
    #maxmut = 25 + math.floor(gen / 100) * 10
    for i in runned:
        if(i.currentTreasure == i.treasureCount):
            print("\n")
            print("FOUND")
            sys.exit(0)
    
    sel = roulette 
    if(gen > 200):
        sel = tournament
    fitarr = [Fitness(fitnessdickinyourmouth[x], instr[x]) for x in range(POPULATION)]
    machines = construct(fitarr, sel)



