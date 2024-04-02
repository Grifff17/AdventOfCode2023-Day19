traitMap = {
    "x":0,
    "m":1,
    "a":2,
    "s":3
}

def solvepart1():
    #read in data
    data = fileRead("input.txt")
    partsReached = False
    workflows = {}
    parts = []
    for rawRow in data:
        row = rawRow.strip()
        if row == "":
            partsReached = True
            continue
        if not partsReached:
            line = row.split("{")
            name = line[0]
            steps = line[1][:-1].split(",")
            workflows[name] = tuple(steps)
        else:
            vals = row[1:-1].split(",")
            parts.append((int(vals[0][2:]),int(vals[1][2:]),int(vals[2][2:]),int(vals[3][2:])))

    #determine whether each part should be rejected or not
    sum = 0
    for part in parts:
        valid = acceptOrRejectPart(part, workflows)
        if valid:
            sum = sum + (part[0] + part[1] + part[2] + part[3])
    print(sum)

#goes through workflows and determines whether a part should be rejected or not
def acceptOrRejectPart(part, workflows):
    currentWorkflow = "in"
    while (currentWorkflow not in ("R","A")):
        rules = workflows[currentWorkflow]
        for rule in rules:
            if ("<" not in rule) and (">" not in rule):
                currentWorkflow = rule
                break
            comp, dest = rule.split(":")
            if "<" in comp:
                trait, amount = comp.split("<")
                if part[traitMap[trait]] < int(amount):
                    currentWorkflow = dest
                    break
            else:
                trait, amount = comp.split(">")
                if part[traitMap[trait]] > int(amount):
                    currentWorkflow = dest
                    break

    if currentWorkflow == "A":
        return True
    return False

def solvepart2():
    #read in data
    data = fileRead("input.txt")
    workflows = {}
    parts = []
    for rawRow in data:
        row = rawRow.strip()
        if row == "":
            break
        line = row.split("{")
        name = line[0]
        steps = line[1][:-1].split(",")
        workflows[name] = tuple(steps)

    #run recursive function to determine the number of possible parts
    numParts = acceptOrRejectRange(((1,4001),(1,4001),(1,4001),(1,4001)), "in", workflows)
    print(numParts)

    #determine whether each part should be rejected or not
    
#recursively takes a range through the workflow, splitting it into multiple ranges as necessary
#returns number of possible accepted parts
def acceptOrRejectRange(partRange, currentWorkflow, workflows):
    if (currentWorkflow == "R"):
        return 0
    if (currentWorkflow == "A"):
        print(partRange, (partRange[0][1] - partRange[0][0]) * (partRange[1][1] - partRange[1][0]) * (partRange[2][1] - partRange[2][0]) * (partRange[3][1] - partRange[3][0]))
        return (partRange[0][1] - partRange[0][0]) * (partRange[1][1] - partRange[1][0]) * (partRange[2][1] - partRange[2][0]) * (partRange[3][1] - partRange[3][0])
    
    sum = 0
    curPartRange = list(partRange)
    rules = workflows[currentWorkflow]
    for rule in rules:
        if ("<" not in rule) and (">" not in rule):
            sum = sum + acceptOrRejectRange(curPartRange, rule, workflows)
            break
        comp, dest = rule.split(":")
        if "<" in comp:
            trait, splitPos = comp.split("<")
            splitPos = int(splitPos)
            newPartRange = curPartRange.copy()
            print("<", newPartRange[traitMap[trait]], splitPos)
            newPartRange[traitMap[trait]] = (newPartRange[traitMap[trait]][0], splitPos)
            curPartRange[traitMap[trait]] = (splitPos, curPartRange[traitMap[trait]][1])
            sum = sum + acceptOrRejectRange(tuple(newPartRange), dest, workflows)
        else:
            trait, splitPos = comp.split(">")
            splitPos = int(splitPos)
            newPartRange = curPartRange.copy()
            print(">", newPartRange[traitMap[trait]], splitPos)
            newPartRange[traitMap[trait]] = (splitPos+1, newPartRange[traitMap[trait]][1])
            curPartRange[traitMap[trait]] = (curPartRange[traitMap[trait]][0], splitPos+1)
            sum = sum + acceptOrRejectRange(tuple(newPartRange), dest, workflows)
    return sum

def fileRead(name):
    data = []
    f = open(name, "r")
    for line in f:
        data.append(line);
    return data


solvepart2()