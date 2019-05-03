import re
numberOfLayer = 1
zPosition = 0
data = open("Gcode/two.gcode","r")
for x in data:
    #print(x)
    if "Z" in x and not re.search(r"\A;",x):
        zData= re.search(r"\bZ(\d*.\d*)",x)
        #a = re.search(r"^;.*",x)
        if float(zData[1]) > zPosition:
            numberOfLayer = numberOfLayer + 1
            zPosition = float(zData[1])
        elif float(zData[1]) < zPosition:
            numberOfLayer = numberOfLayer - 1
            zPosition = float(zData[1])
        else:
            zPosition = float(zData[1])
            pass
        print(x,numberOfLayer)

