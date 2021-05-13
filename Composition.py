from mendeleev import element
from pprint import pprint

dummyRate = 0.0001
class Species:
    def __init__(self, aNum, aMass):
        self.aNum = aNum
        self.aMass = aMass

    def __hash__(self):
        return hash(self.aNum) ^ hash(self.aMass)
    def __eq__(self, other):
        return self.aNum == other.aNum and self.aMass == other.aMass
    def getElement(self):
        return element(self.aNum).symbol
    def getAtomicNum(self):
        return self.aNum
    def getAtomicMass(self):
        return self.aMass
    def __str__(self):
        return "(" + self.getElement() + "," + str(self.getAtomicMass()) + ")"

class Reactions:
    def __init__(self, stuff, rate):
        self.stuff = stuff
        self.rate = rate

    def __hash__(self):
        return hash(len(self.stuff)) ^ hash(self.rate)

    def __eq__(self, other):
        if len(self.stuff) != len(other.stuff):
            return False
        for i in self.stuff:
            if i in other.stuff:
                if self.stuff[i] != other.stuff[i]:
                    return False
            else:
                return False
        if self.rate != other.rate:
            return False
        return True
    def getElementList(self):
        return list(self.stuff.keys())
    def getElement(self, index):
        if(len(self.stuff) == 1 and index == 1):
            return list(self.stuff.keys())[0]
        return list(self.stuff.keys())[index]
    def getRate(self):
        return self.rate
    def setRate(self, newRate):
        self.rate = newRate
    def __str__(self):
        temp = "["
        for x in self.stuff.keys():
            temp = temp + str(x) + ": " + str(self.stuff[x]) + ", "
        temp = temp + "]"
        return temp


dt = 100
m_h = 1.67 * 10**-24
rho = 10 ** -24 #to be determined, dummy number for now
energy = []

elements = []
elements.append(Species(1, 1))
elements.append(Species(1, 2))
elements.append(Species(2, 3))
elements.append(Species(2, 4))
elements.append(Species(3, 7))
elements.append(Species(4, 7))
elements.append(Species(4, 8))
elements.append(Species(5, 8))
elements.append(Species(6, 12))
elements.append(Species(6, 13))
elements.append(Species(7, 13))
elements.append(Species(7, 14))
elements.append(Species(7, 15))
elements.append(Species(8, 14))
elements.append(Species(8, 15))
elements.append(Species(8, 16))
elements.append(Species(8, 17))
elements.append(Species(8, 18))
elements.append(Species(9, 17))
elements.append(Species(9, 18))
elements.append(Species(9, 19))
elements.append(Species(10, 18))
elements.append(Species(10, 19))
elements.append(Species(11, 23))
elements.append(Species(12, 23))
for i in range(10, 30, 2):
    elements.append(Species(i, 2*i))

creation = {} #Reactions that produce some species i, only store the reactants
destruction = {} #Reactions that consume some species i, only store the OTHER reactants

mass_fractions = {}
for e in elements:
    mass_fractions[e] = [-1]*100
    mass_fractions[e][0] = 0
    creation[e] = set()
    destruction[e] = set()
mass_fractions[Species(1,1)][0] = 1

#Setting up pp chain

destruction[Species(1,1)].add(Reactions({Species(1,1): 1}, dummyRate))
creation[Species(1,2)].add(Reactions({Species(1,1): 2}, dummyRate))

destruction[Species(1, 1)].add(Reactions({Species(1, 2): 1}, dummyRate))
destruction[Species(1, 2)].add(Reactions({Species(1, 1): 1}, dummyRate))
creation[Species(2, 3)].add(Reactions({Species(1, 1): 1, Species(1, 2): 2}, dummyRate))

destruction[Species(2, 3)].add(Reactions({Species(2, 3): 1}, dummyRate))
creation[Species(2, 4)].add(Reactions({Species(2, 3): 2}, dummyRate))
creation[Species(1, 1)].add(Reactions({Species(2, 3): 2}, 2*dummyRate))

destruction[Species(2, 3)].add(Reactions({Species(2, 4): 1}, dummyRate))
destruction[Species(2, 4)].add(Reactions({Species(2, 3): 1}, dummyRate))
creation[Species(4, 7)].add(Reactions({Species(2, 3): 1, Species(2, 4): 1}, dummyRate))

destruction[Species(2, 3)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(2, 3): 1}, dummyRate))
creation[Species(2, 4)].add(Reactions({Species(2, 3): 1, Species(1, 1): 1}, dummyRate))

destruction[Species(4, 7)].add(Reactions({}, dummyRate))
creation[Species(3, 7)].add(Reactions({Species(4, 7): 1}, dummyRate))

destruction[Species(3, 7)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(3, 7): 1}, dummyRate))
creation[Species(2, 4)].add(Reactions({Species(3, 7): 1, Species(1, 1): 1}, 2*dummyRate))

destruction[Species(4, 7)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(4, 7): 1}, dummyRate))
creation[Species(5, 8)].add(Reactions({Species(1, 1): 1, Species(4, 7): 1}, dummyRate))

destruction[Species(5, 8)].add(Reactions({}, dummyRate))
creation[Species(4, 8)].add(Reactions({Species(5, 8): 1}, dummyRate))

destruction[Species(4, 8)].add(Reactions({}, dummyRate))
creation[Species(2, 4)].add(Reactions({Species(4, 8): 1}, 2 * dummyRate))

# Setting up Triple Alpha Process

destruction[Species(2, 4)].add(Reactions({Species(2, 4): 1}, dummyRate))
creation[Species(4, 8)].add(Reactions({Species(2, 4): 2}, dummyRate))

destruction[Species(4, 8)].add(Reactions({Species(2, 4): 1}, dummyRate))
destruction[Species(2, 4)].add(Reactions({Species(4, 8): 1}, dummyRate))
creation[Species(6, 12)].add(Reactions({Species(2, 4): 1, Species(4, 8): 1}, dummyRate))

destruction[Species(6, 12)].add(Reactions({Species(2, 4): 1}, dummyRate))
destruction[Species(2, 4)].add(Reactions({Species(6, 12): 1}, dummyRate))
creation[Species(8, 16)].add(Reactions({Species(2, 4): 1, Species(6, 12): 1}, dummyRate))

# Setting up Alpha Process

for i in range(6, 28, 2):
    destruction[Species(i, 2 * i)].add(Reactions({Species(2, 4): 1}, dummyRate))
    destruction[Species(2, 4)].add(Reactions({Species(i, 2 * i): 1}, dummyRate))
    creation[Species(i + 2, 2 * i + 4)].add(Reactions({Species(2, 4): 1, Species(i, 2 * i): 1}, dummyRate))

# Set up Carbon Burning

destruction[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate))
creation[Species(10, 20)].add(Reactions({Species(6, 12): 2}, dummyRate))
creation[Species(2, 4)].add(Reactions({Species(6, 12): 2}, dummyRate))

destruction[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate))
creation[Species(11, 23)].add(Reactions({Species(6, 12): 2}, dummyRate))
creation[Species(1, 1)].add(Reactions({Species(6, 12): 2}, dummyRate))

destruction[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate))
creation[Species(12, 23)].add(Reactions({Species(6, 12): 2}, dummyRate))

destruction[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate))
creation[Species(12, 24)].add(Reactions({Species(6, 12): 2}, dummyRate))

destruction[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate))
creation[Species(8, 16)].add(Reactions({Species(6, 12): 2}, dummyRate))
creation[Species(2, 4)].add(Reactions({Species(6, 12): 2}, 2 * dummyRate))

# Set up CNO Cycle 1

destruction[Species(6, 12)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(6, 12): 1}, dummyRate))
creation[Species(7, 13)].add(Reactions({Species(1, 1): 1, Species(6, 12): 1}, dummyRate))

destruction[Species(7, 13)].add(Reactions({}, dummyRate))
creation[Species(6, 13)].add(Reactions({Species(7, 13): 1}, dummyRate))

destruction[Species(6, 13)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(6, 13): 1}, dummyRate))
creation[Species(7, 14)].add(Reactions({Species(1, 1): 1, Species(6, 13): 1}, dummyRate))

destruction[Species(7, 14)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(7, 14): 1}, dummyRate))
creation[Species(8, 15)].add(Reactions({Species(1, 1): 1, Species(7, 14): 1}, dummyRate))

destruction[Species(8, 15)].add(Reactions({}, dummyRate))
creation[Species(7, 15)].add(Reactions({Species(8, 15): 1}, dummyRate))

destruction[Species(7, 15)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(7, 15): 1}, dummyRate))
creation[Species(6, 12)].add(Reactions({Species(1, 1): 1, Species(7, 15): 1}, dummyRate))
creation[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(7, 15): 1}, dummyRate))

#Set up CNO Cycle 2

destruction[Species(7, 15)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(7, 15): 1}, dummyRate))
creation[Species(8, 16)].add(Reactions({Species(1, 1): 1, Species(7, 15): 1}, dummyRate))

destruction[Species(8, 16)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(8, 16): 1}, dummyRate))
creation[Species(9, 17)].add(Reactions({Species(1, 1): 1, Species(8, 16): 1}, dummyRate))

destruction[Species(9, 17)].add(Reactions({}, dummyRate))
creation[Species(8, 17)].add(Reactions({Species(9, 17): 1}, dummyRate))

destruction[Species(8, 17)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(8, 17): 1}, dummyRate))
creation[Species(7, 14)].add(Reactions({Species(1, 1): 1, Species(8, 17): 1}, dummyRate))
creation[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(8, 17): 1}, dummyRate))

destruction[Species(7, 14)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(7, 14): 1}, dummyRate))
creation[Species(8, 15)].add(Reactions({Species(1, 1): 1, Species(7, 14): 1}, dummyRate))

destruction[Species(8, 15)].add(Reactions({}, dummyRate))
creation[Species(7, 15)].add(Reactions({Species(8, 15): 1}, dummyRate))

#Set up CNO Cycle 3

destruction[Species(8, 17)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(8, 17): 1}, dummyRate))
creation[Species(9, 18)].add(Reactions({Species(1, 1): 1, Species(8, 17): 1}, dummyRate))

destruction[Species(9, 18)].add(Reactions({}, dummyRate))
creation[Species(8, 18)].add(Reactions({Species(9, 18): 1}, dummyRate))

destruction[Species(8, 18)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(8, 18): 1}, dummyRate))
creation[Species(7, 15)].add(Reactions({Species(1, 1): 1, Species(8, 18): 1}, dummyRate))
creation[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(8, 18): 1}, dummyRate))

destruction[Species(7, 15)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(7, 15): 1}, dummyRate))
creation[Species(8, 16)].add(Reactions({Species(1, 1): 1, Species(7, 15): 1}, dummyRate))

destruction[Species(8, 16)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(8, 16): 1}, dummyRate))
creation[Species(9, 17)].add(Reactions({Species(1, 1): 1, Species(8, 16): 1}, dummyRate))

destruction[Species(9, 17)].add(Reactions({}, dummyRate))
creation[Species(8, 17)].add(Reactions({Species(9, 17): 1}, dummyRate))

#Set up CNO Cycle 4

destruction[Species(8, 18)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(8, 18): 1}, dummyRate))
creation[Species(9, 19)].add(Reactions({Species(1, 1): 1, Species(8, 18): 1}, dummyRate))

destruction[Species(9, 19)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(9, 19): 1}, dummyRate))
creation[Species(8, 16)].add(Reactions({Species(1, 1): 1, Species(9, 19): 1}, dummyRate))
creation[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(9, 19): 1}, dummyRate))

destruction[Species(8, 16)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(8, 16): 1}, dummyRate))
creation[Species(9, 19)].add(Reactions({Species(1, 1): 1, Species(8, 16): 1}, dummyRate))

destruction[Species(9, 17)].add(Reactions({}, dummyRate))
creation[Species(8, 17)].add(Reactions({Species(9, 17): 1}, dummyRate))

destruction[Species(8, 17)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(8, 17): 1}, dummyRate))
creation[Species(9, 18)].add(Reactions({Species(1, 1): 1, Species(8, 17): 1}, dummyRate))

destruction[Species(9, 18)].add(Reactions({}, dummyRate))
creation[Species(8, 18)].add(Reactions({Species(9, 18): 1}, dummyRate))

#Set up HCNO 1

destruction[Species(7, 13)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(7, 13): 1}, dummyRate))
creation[Species(8, 14)].add(Reactions({Species(1, 1): 1, Species(7, 13): 1}, dummyRate))

destruction[Species(8, 14)].add(Reactions({}, dummyRate))
creation[Species(7, 14)].add(Reactions({Species(8, 14): 1}, dummyRate))

#Set up HCNO 2

destruction[Species(9, 17)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(9, 17): 1}, dummyRate))
creation[Species(10, 18)].add(Reactions({Species(1, 1): 1, Species(9, 17): 1}, dummyRate))

destruction[Species(10, 18)].add(Reactions({}, dummyRate))
creation[Species(9, 18)].add(Reactions({Species(10, 18): 1}, dummyRate))

destruction[Species(9, 18)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(9, 18): 1}, dummyRate))
creation[Species(8, 15)].add(Reactions({Species(1, 1): 1, Species(9, 18): 1}, dummyRate))
creation[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(9, 18): 1}, dummyRate))

#Set up HCNO 3

destruction[Species(9, 18)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(9, 18): 1}, dummyRate))
creation[Species(10, 19)].add(Reactions({Species(1, 1): 1, Species(9, 18): 1}, dummyRate))

destruction[Species(10, 19)].add(Reactions({}, dummyRate))
creation[Species(9, 19)].add(Reactions({Species(10, 19): 1}, dummyRate))

destruction[Species(9, 19)].add(Reactions({Species(1, 1): 1}, dummyRate))
destruction[Species(1, 1)].add(Reactions({Species(9, 19): 1}, dummyRate))
creation[Species(8, 16)].add(Reactions({Species(1, 1): 1, Species(9, 19): 1}, dummyRate))
creation[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(9, 19): 1}, dummyRate))



def memoizeComp(atomicNum, atomicMass, time):
    curr_species = Species(atomicNum, atomicMass)
    last = mass_fractions[curr_species][time-1]
    coef = 1.0 * dt*rho * atomicMass/m_h
    sum = 0
    for x in creation[curr_species]:
        if len(x.getElementList()) == 1:
            curr_key = Species(x.getElement(0).getAtomicNum(), x.getElement(0).getAtomicMass())
            if curr_key not in mass_fractions:
                print(f"curr_key {curr_key} not exist")
                return
            prevVal = mass_fractions[curr_key][time-1]
            sum += 0.5 * x.getRate() * prevVal * prevVal / (x.getElement(0).getAtomicMass() * x.getElement(0).getAtomicMass())
        else:
            curr_key = Species(x.getElement(0).getAtomicNum(), x.getElement(0).getAtomicMass())
            if curr_key not in mass_fractions:
                print(f"curr_key {curr_key} not exist")
                return
            prevVal0 = mass_fractions[Species(x.getElement(0).getAtomicNum(), x.getElement(0).getAtomicMass())][time-1]
            curr_key = Species(x.getElement(1).getAtomicNum(), x.getElement(1).getAtomicMass())
            if curr_key not in mass_fractions:
                print(f"curr_key {curr_key} not exist")
                return
            prevVal1 = mass_fractions[Species(x.getElement(1).getAtomicNum(), x.getElement(1).getAtomicMass())][time-1]
            sum += x.getRate() * prevVal0 * prevVal1 / (x.getElement(0).getAtomicMass() * x.getElement(1).getAtomicMass())

    for x in destruction[curr_species]:
        if(len(x.getElementList()) == 0):
            sum -= x.getRate() * last / atomicMass
        else:
            curr_key = Species(x.getElement(0).getAtomicNum(), x.getElement(0).getAtomicMass())
            if curr_key not in mass_fractions:
                print(f"curr_key {curr_key} not exist")
                return
            prevVal = mass_fractions[Species(x.getElement(0).getAtomicNum(), x.getElement(0).getAtomicMass())][time-1]
            sum -= x.getRate() * last * prevVal / (atomicMass * x.getElement(0).getAtomicMass())
    return last + coef * sum


for i in range(1,100):
    for e in elements:
        mass_fractions[e][i] = memoizeComp(e.getAtomicNum(), e.getAtomicMass(), i)

for e in elements:
    print(str(e) + ": " + str(mass_fractions[e]))

