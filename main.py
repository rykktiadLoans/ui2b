import json, random

class Treasure:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Field:
    def __init__(self, fieldfile):
        fieldJSON = json.load(open(fieldfile))
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
    def up(self):
        if(self.playery != 0):
            self.playery -= 1
            self.treasureCheck()
            return True
        else:
            return False
    def down(self):
        if(self.playery < self.sizey):
            self.playery += 1
            self.treasureCheck()
            return True
        else:
            return False
    def right(self):
        if(self.playerx != 0):
            self.playerx += 1
            self.treasureCheck()
            return True
        else:
            return False
    def left(self):
        if(self.playerx < self.sizex):
            self.playerx -= 1
            self.treasureCheck()
            return True
        else:
            return False

    def treasureCheck(self):
        self.steps += 1
        for t in self.treasure:
            if(t.x == self.playerx and t.y == self.playery):
                self.treasure.remove(t)
                self.currentTreasure += 1
                break
    
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

class Machine:
    def __init__(self):
        self.instructions = ["00000000" for x in range(64)]
        self.current = 0
        self.total = 0
        self.output = ""
        self.state = "a" # a-active d-done f-fail
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

def initInstructions(machine):
    count = 16
    for i in range(count):
        out = ""
        for j in range(8):
            out += str(random.randint(0, 1))
        machine.instructions[i] = out
    return machine


def calcFitness(field):
    POINTFOUND = 100 
    POINTSTEP = -1
    points = 500
    points += POINTFOUND * field.currentTreasure + POINTSTEP * field.steps
    return points

def getOutput(machine):
    val = True
    while(val):
        val = machine.next()
    return machine.output

def runField(field, output):
    for i in output:
        field.smartMoving(i)
        if(field.currentTreasure == field.treasureCount):
            return field
    return field


POPULATION = 20

filename = "field.json"
field = Field(filename)
field.print()
machine = Machine()
machine = initInstructions(machine)
fields = [Field(filename) for x in range(POPULATION)]
machines = [initInstructions(Machine()) for x in range(POPULATION)]
output = [getOutput(machines[x]) for x in range(POPULATION)]
runned = [runField(fields[x], output[x]) for x in range(POPULATION)]
fitnessdickinyourmouth = [calcFitness(runned[x]) for x in range(POPULATION)]
for i in range(POPULATION):
    print(runned[i].currentTreasure, ":", runned[i].steps, ":", fitnessdickinyourmouth[i])
