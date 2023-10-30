import json 

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
    def __init__(self, field):
        self.field = field
        self.instructions = ["00000000" for x in range(64)]
        self.current = 0
        self.total = 0
        self.state = "a" # a-active d-done f-fail
    def next(self):
        if(self.state == "d" or self.state == "f"):
            return False
        full = self.instructions[self.current]
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
            success = False 
            if(n == 0):
                success = field.up()
            if(n == 1):
                success = field.left()
            if(n == 2):
                success = field.right()
            if(n == 3):
                success = field.down()
            if(success):
                self.current+= 1
            else:
                self.state = "f"
                return False
        if(self.current > 63):
            self.state = "f"
            return False
        self.total += 1
        if(self.total >= 500):
            self.state = "f"
            return False
        if(len(self.field.treasure) == 0):
            self.state = "d"
            return True
        return True







filename = "field.json"
field = Field(filename)
field.print()
machine = Machine(field)
machine.instructions[0] = "10111000"
machine.instructions[56] = "11000000"
machine.instructions[57] = "11000000"
machine.instructions[58] = "11000000"
machine.instructions[59] = "11000000"
machine.instructions[60] = "11000000"
machine.instructions[61] = "11000000"
machine.instructions[62] = "11000000"
machine.instructions[63] = "11000000"
val = True
while val:
    print(machine.current)
    val = machine.next()
    machine.field.print()

