from mendeleev import element

dummyRate = 12
class Species:
    def __init__(self, aNum, aMass):
        self.aNum = aNum
        self.aMass = aMass

    def __hash__(self):
        return hash(self.aNum) ^ hash(self.aMass)
    def __eq__(self, other):
        return (self.aNum, self.aMass) == (other.aNum, other.aMass)
    def getElement(self):
        return element(self.aNum).symbol
    def getAtomicMass(self):
        return self.aMass
    def __str__(self):
        return "(" + self.getElement() + "," + str(self.getAtomicMass()) + ")"

class Reactions:
    def __init__(self, stuff, rate):
        self.stuff = stuff
        self.rate = rate

    def __hash__(self):
        return hash(self.stuff) ^ hash(self.rate)
    def getElements(self):
        return self.stuff
    def getRate(self):
        return self.rate
    def setRate(self, newRate):
        self.rate = newRate
    def __str__(self):
        temp = "["
        for x in self.stuff.keys():
            temp = temp + str(x) + ", "
        temp = temp + "]"
        return temp


dt = 100
m_h = 1.6726219 * 10**-27
rho = 15 #to be determined, assume density stays constant, dummy number for now
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
elements.append(Species(8, 15))
elements.append(Species(8, 16))
elements.append(Species(8, 17))
elements.append(Species(9, 17))
elements.append(Species(9, 18))
elements.append(Species(9, 19))
for i in range(10, 30, 2):
    elements.append(Species(i, 2*i))
production = {} #Reactions that produce some species i, only store the reactants
consumption = {} #Reactions that consume some species i, only store the OTHER reactants

mass_fractions = {}
for e in elements:
    mass_fractions[e] = [-1]*100
    mass_fractions[e][0] = 0
    production[e] = []
    consumption[e] = []

#Setting up pp chain

consumption[Species(1,1)].append(Reactions({Species(1,1): 1}, dummyRate))
production[Species(1,2)].append(Reactions({Species(1,1): 2}, dummyRate))

consumption[Species(1, 1)].append(Reactions({Species(1, 2): 1}, dummyRate))
consumption[Species(1, 2)].append(Reactions({Species(1, 1): 1}, dummyRate))
production[Species(2, 3)].append(Reactions({Species(1, 1): 1, Species(2, 2): 2}, dummyRate))

consumption[Species(2, 3)].append(Reactions({Species(2, 3): 1}, dummyRate))
production[Species(2, 4)].append(Reactions({Species(2, 3): 2}, dummyRate))
production[Species(1, 1)].append(Reactions({Species(2, 3): 2}, 2*dummyRate))

consumption[Species(2, 3)].append(Reactions({Species(2, 4): 1}, dummyRate))
consumption[Species(2, 4)].append(Reactions({Species(2, 3): 1}, dummyRate))
production[Species(4, 7)].append(Reactions({Species(2, 3): 1, Species(2, 4): 1}, dummyRate))

consumption[Species(2, 3)].append(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].append(Reactions({Species(2, 3): 1}, dummyRate))
production[Species(2, 4)].append(Reactions({Species(2, 3): 1, Species(1, 1): 1}, dummyRate))

consumption[Species(4, 7)].append(Reactions({}, dummyRate))
production[Species(3, 7)].append(Reactions({Species(4, 7): 1}, dummyRate))

consumption[Species(3, 7)].append(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].append(Reactions({Species(3, 7): 1}, dummyRate))
production[Species(2, 4)].append(Reactions({Species(3, 7): 1, Species(1, 1): 1}, 2*dummyRate))

consumption[Species(4, 7)].append(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].append(Reactions({Species(4, 7): 1}, dummyRate))
production[Species(5, 8)].append(Reactions({Species(1, 1): 1, Species(4, 7): 1}, dummyRate))

consumption[Species(5, 8)].append(Reactions({}, dummyRate))
production[Species(4, 8)].append(Reactions({Species(5, 8): 1}, dummyRate))

consumption[Species(4, 8)].append(Reactions({}, dummyRate))
production[Species(2, 4)].append(Reactions({Species(4, 8): 1}, 2 * dummyRate))

#Setting up Triple Alpha Process

consumption[Species(2,4)].append(Reactions({Species(2,4): 1}, dummyRate))
production[Species(4,8)].append(Reactions({Species(2,4): 2}, dummyRate))

consumption[Species(4,8)].append(Reactions({Species(2,4): 1}, dummyRate))
consumption[Species(2,4)].append(Reactions({Species(4,8): 1}, dummyRate))
production[Species(6,12)].append(Reactions({Species(2,4): 1, Species(4,8): 1}, dummyRate))

consumption[Species(6,12)].append(Reactions({Species(2,4): 1}, dummyRate))
consumption[Species(2,4)].append(Reactions({Species(6,12): 1}, dummyRate))
production[Species(8, 16)].append(Reactions({Species(2,4): 1, Species(6,12): 1}, dummyRate))

#Setting up Alpha Process

for i in range(12, 28, 2):
    consumption[Species(i, 2*i)].append(Reactions({Species(2, 4): 1}, dummyRate))
    consumption[Species(2, 4)].append(Reactions({Species(i, 2*i): 1}, dummyRate))
    production[Species(i+1, 2*i+2)].append(Reactions({Species(2,4): 1, Species(i, 2*i): 1}, dummyRate))





def memoizeComp(atomicNum, atomicMass, time):
    curr_species = Species(element(atomicNum), atomicMass)
    if mass_fractions[curr_species][time] > -1:
        return mass_fractions[curr_species][time]
    last = memoizeComp(atomicNum, atomicMass, time-1)
    coef = dt*rho * atomicNum/m_h
    for x in production[curr_species]:
        if x == (atomicNum, atomicMass):
            delta = 1
            temp = 0
            last += temp*coef
        else:
            delta = 0
            temp = 0
            last += temp*coef
    for x in consumption[curr_species]:
        if x == (atomicNum, atomicMass):
            delta = 1
            temp = 0
            last -= temp * coef
        else:
            delta = 0
            temp = 0
            last -= temp * coef
    mass_fractions[curr_species][time] = last
    return last



