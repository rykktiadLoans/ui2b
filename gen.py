import json, math, random
x = int(input("SizeX: "))
y = int(input("SizeY: "))
tc = int(input("TreasureCount: "))

xp = random.randrange(0, x)
yp = random.randrange(0, y)
ar = []
setx = set()
sety = set()
for i in range(tc):
    tx = random.randrange(0, x)
    ty = random.randrange(0, y)
    while(tx in setx):
        tx = random.randrange(0, x)
    while(ty in sety):
        ty = random.randrange(0, y)
    setx.add(tx)
    sety.add(ty)
    td = {
            "x": tx,
            "y": ty
            }
    ar.append(td)
dict = {
    "size": {
        "x": x,
        "y": y
    },
    "start": {
        "x": xp,
        "y": yp
    },
    "treasure": ar 
}
file = open("field.json", "w")
j = json.dumps(dict)
file.write(j)
file.flush()
file.close()

