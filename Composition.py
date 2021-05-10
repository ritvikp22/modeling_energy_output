from mendeleev import element
import pprint

dummyRate = 12
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
    elements.append(Species(i+1, 2*i + 2))
    if i > 20:
        elements.append(Species(i - 1, 2 * i))
        elements.append(Species(i - 2, 2 * i))
production = {} #Reactions that produce some species i, only store the reactants
consumption = {} #Reactions that consume some species i, only store the OTHER reactants

mass_fractions = {}
for e in elements:
    mass_fractions[e] = [-1]*100
    mass_fractions[e][0] = 0
    production[e] = set()
    consumption[e] = set()
mass_fractions[Species(1,1)][0] = 1

#Setting up pp chain

consumption[Species(1,1)].add(Reactions({Species(1,1): 1}, dummyRate))
production[Species(1,2)].add(Reactions({Species(1,1): 2}, dummyRate))

consumption[Species(1, 1)].add(Reactions({Species(1, 2): 1}, dummyRate))
consumption[Species(1, 2)].add(Reactions({Species(1, 1): 1}, dummyRate))
production[Species(2, 3)].add(Reactions({Species(1, 1): 1, Species(2, 2): 2}, dummyRate))

consumption[Species(2, 3)].add(Reactions({Species(2, 3): 1}, dummyRate))
production[Species(2, 4)].add(Reactions({Species(2, 3): 2}, dummyRate))
production[Species(1, 1)].add(Reactions({Species(2, 3): 2}, 2*dummyRate))

consumption[Species(2, 3)].add(Reactions({Species(2, 4): 1}, dummyRate))
consumption[Species(2, 4)].add(Reactions({Species(2, 3): 1}, dummyRate))
production[Species(4, 7)].add(Reactions({Species(2, 3): 1, Species(2, 4): 1}, dummyRate))

consumption[Species(2, 3)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(2, 3): 1}, dummyRate))
production[Species(2, 4)].add(Reactions({Species(2, 3): 1, Species(1, 1): 1}, dummyRate))

consumption[Species(4, 7)].add(Reactions({}, dummyRate))
production[Species(3, 7)].add(Reactions({Species(4, 7): 1}, dummyRate))

consumption[Species(3, 7)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(3, 7): 1}, dummyRate))
production[Species(2, 4)].add(Reactions({Species(3, 7): 1, Species(1, 1): 1}, 2*dummyRate))

consumption[Species(4, 7)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(4, 7): 1}, dummyRate))
production[Species(5, 8)].add(Reactions({Species(1, 1): 1, Species(4, 7): 1}, dummyRate))

consumption[Species(5, 8)].add(Reactions({}, dummyRate))
production[Species(4, 8)].add(Reactions({Species(5, 8): 1}, dummyRate))

consumption[Species(4, 8)].add(Reactions({}, dummyRate))
production[Species(2, 4)].add(Reactions({Species(4, 8): 1}, 2 * dummyRate))

# Setting up Triple Alpha Process

consumption[Species(2, 4)].add(Reactions({Species(2, 4): 1}, dummyRate))
production[Species(4, 8)].add(Reactions({Species(2, 4): 2}, dummyRate))

consumption[Species(4, 8)].add(Reactions({Species(2, 4): 1}, dummyRate))
consumption[Species(2, 4)].add(Reactions({Species(4, 8): 1}, dummyRate))
production[Species(6, 12)].add(Reactions({Species(2, 4): 1, Species(4, 8): 1}, dummyRate))

consumption[Species(6, 12)].add(Reactions({Species(2, 4): 1}, dummyRate))
consumption[Species(2, 4)].add(Reactions({Species(6, 12): 1}, dummyRate))
production[Species(8, 16)].add(Reactions({Species(2, 4): 1, Species(6, 12): 1}, dummyRate))

# Setting up Alpha Process

for i in range(12, 28, 2):
    consumption[Species(i, 2 * i)].add(Reactions({Species(2, 4): 1}, dummyRate))
    consumption[Species(2, 4)].add(Reactions({Species(i, 2 * i): 1}, dummyRate))
    production[Species(i + 1, 2 * i + 2)].add(Reactions({Species(2, 4): 1, Species(i, 2 * i): 1}, dummyRate))
    if i > 20:
        consumption[Species(i, 2 * i)].add(Reactions({}, dummyRate))
        production[Species(i - 1, 2 * i)].add(Reactions({Species(i, 2 * i): 1}, dummyRate))
        consumption[Species(i - 1, 2 * i)].add(Reactions({}, dummyRate))
        production[Species(i - 2, 2 * i)].add(Reactions({Species(i - 1, 2 * i): 1}, dummyRate))

# Set up Carbon Burning

consumption[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate))
production[Species(10, 20)].add(Reactions({Species(6, 12): 2}, dummyRate))
production[Species(2, 4)].add(Reactions({Species(6, 12): 2}, dummyRate))

consumption[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate))
production[Species(11, 23)].add(Reactions({Species(6, 12): 2}, dummyRate))
production[Species(1, 1)].add(Reactions({Species(6, 12): 2}, dummyRate))

consumption[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate))
production[Species(12, 23)].add(Reactions({Species(6, 12): 2}, dummyRate))

consumption[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate))
production[Species(12, 24)].add(Reactions({Species(6, 12): 2}, dummyRate))

consumption[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate))
production[Species(8, 16)].add(Reactions({Species(6, 12): 2}, dummyRate))
production[Species(2, 4)].add(Reactions({Species(6, 12): 2}, 2 * dummyRate))

# Set up CNO Cycle 1

consumption[Species(6, 12)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(6, 12): 1}, dummyRate))
production[Species(7, 13)].add(Reactions({Species(1, 1): 1, Species(6, 12): 1}, dummyRate))

consumption[Species(7, 13)].add(Reactions({}, dummyRate))
production[Species(6, 13)].add(Reactions({Species(7, 13): 1}, dummyRate))

consumption[Species(6, 13)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(6, 13): 1}, dummyRate))
production[Species(7, 14)].add(Reactions({Species(1, 1): 1, Species(6, 13): 1}, dummyRate))

consumption[Species(7, 14)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(7, 14): 1}, dummyRate))
production[Species(8, 15)].add(Reactions({Species(1, 1): 1, Species(7, 14): 1}, dummyRate))

consumption[Species(8, 15)].add(Reactions({}, dummyRate))
production[Species(7, 15)].add(Reactions({Species(8, 15): 1}, dummyRate))

consumption[Species(7, 15)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(7, 15): 1}, dummyRate))
production[Species(6, 12)].add(Reactions({Species(1, 1): 1, Species(7, 15): 1}, dummyRate))
production[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(7, 15): 1}, dummyRate))

#Set up CNO Cycle 2

consumption[Species(7, 15)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(7, 15): 1}, dummyRate))
production[Species(8, 16)].add(Reactions({Species(1, 1): 1, Species(7, 15): 1}, dummyRate))

consumption[Species(8, 16)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(8, 16): 1}, dummyRate))
production[Species(9, 17)].add(Reactions({Species(1, 1): 1, Species(8, 16): 1}, dummyRate))

consumption[Species(9, 17)].add(Reactions({}, dummyRate))
production[Species(8, 17)].add(Reactions({Species(9, 17): 1}, dummyRate))

consumption[Species(8, 17)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(8, 17): 1}, dummyRate))
production[Species(7, 14)].add(Reactions({Species(1, 1): 1, Species(8, 17): 1}, dummyRate))
production[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(8, 17): 1}, dummyRate))

consumption[Species(7, 14)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(7, 14): 1}, dummyRate))
production[Species(8, 15)].add(Reactions({Species(1, 1): 1, Species(7, 14): 1}, dummyRate))

consumption[Species(8, 15)].add(Reactions({}, dummyRate))
production[Species(7, 15)].add(Reactions({Species(8, 15): 1}, dummyRate))

#Set up CNO Cycle 3

consumption[Species(8, 17)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(8, 17): 1}, dummyRate))
production[Species(9, 18)].add(Reactions({Species(1, 1): 1, Species(8, 17): 1}, dummyRate))

consumption[Species(9, 18)].add(Reactions({}, dummyRate))
production[Species(8, 18)].add(Reactions({Species(9, 18): 1}, dummyRate))

consumption[Species(8, 18)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(8, 18): 1}, dummyRate))
production[Species(7, 15)].add(Reactions({Species(1, 1): 1, Species(8, 18): 1}, dummyRate))
production[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(8, 18): 1}, dummyRate))

consumption[Species(7, 15)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(7, 15): 1}, dummyRate))
production[Species(8, 16)].add(Reactions({Species(1, 1): 1, Species(7, 15): 1}, dummyRate))

consumption[Species(8, 16)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(8, 16): 1}, dummyRate))
production[Species(9, 17)].add(Reactions({Species(1, 1): 1, Species(8, 16): 1}, dummyRate))

consumption[Species(9, 17)].add(Reactions({}, dummyRate))
production[Species(8, 17)].add(Reactions({Species(9, 17): 1}, dummyRate))

#Set up CNO Cycle 4

consumption[Species(8, 18)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(8, 18): 1}, dummyRate))
production[Species(9, 19)].add(Reactions({Species(1, 1): 1, Species(8, 18): 1}, dummyRate))

consumption[Species(9, 19)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(9, 19): 1}, dummyRate))
production[Species(8, 16)].add(Reactions({Species(1, 1): 1, Species(9, 19): 1}, dummyRate))
production[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(9, 19): 1}, dummyRate))

consumption[Species(8, 16)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(8, 16): 1}, dummyRate))
production[Species(9, 19)].add(Reactions({Species(1, 1): 1, Species(8, 16): 1}, dummyRate))

consumption[Species(9, 17)].add(Reactions({}, dummyRate))
production[Species(8, 17)].add(Reactions({Species(9, 17): 1}, dummyRate))

consumption[Species(8, 17)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(8, 17): 1}, dummyRate))
production[Species(9, 18)].add(Reactions({Species(1, 1): 1, Species(8, 17): 1}, dummyRate))

consumption[Species(9, 18)].add(Reactions({}, dummyRate))
production[Species(8, 18)].add(Reactions({Species(9, 18): 1}, dummyRate))

#Set up HCNO 1

consumption[Species(7, 13)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(7, 13): 1}, dummyRate))
production[Species(8, 14)].add(Reactions({Species(1, 1): 1, Species(7, 13): 1}, dummyRate))

consumption[Species(8, 14)].add(Reactions({}, dummyRate))
production[Species(7, 14)].add(Reactions({Species(8, 14): 1}, dummyRate))

#Set up HCNO 2

consumption[Species(9, 17)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(9, 17): 1}, dummyRate))
production[Species(10, 18)].add(Reactions({Species(1, 1): 1, Species(9, 17): 1}, dummyRate))

consumption[Species(10, 18)].add(Reactions({}, dummyRate))
production[Species(9, 18)].add(Reactions({Species(10, 18): 1}, dummyRate))

consumption[Species(9, 18)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(9, 18): 1}, dummyRate))
production[Species(8, 15)].add(Reactions({Species(1, 1): 1, Species(9, 18): 1}, dummyRate))
production[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(9, 18): 1}, dummyRate))

#Set up HCNO 3

consumption[Species(9, 18)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(9, 18): 1}, dummyRate))
production[Species(10, 19)].add(Reactions({Species(1, 1): 1, Species(9, 18): 1}, dummyRate))

consumption[Species(10, 19)].add(Reactions({}, dummyRate))
production[Species(9, 19)].add(Reactions({Species(10, 19): 1}, dummyRate))

consumption[Species(9, 19)].add(Reactions({Species(1, 1): 1}, dummyRate))
consumption[Species(1, 1)].add(Reactions({Species(9, 19): 1}, dummyRate))
production[Species(8, 16)].add(Reactions({Species(1, 1): 1, Species(9, 19): 1}, dummyRate))
production[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(9, 19): 1}, dummyRate))



def memoizeComp(atomicNum, atomicMass, time):
    curr_species = Species(atomicNum, atomicMass)
    if mass_fractions[curr_species][time] > -1:
        return mass_fractions[curr_species][time]
    last = memoizeComp(atomicNum, atomicMass, time-1)
    placeHolder = last
    coef = dt*rho * atomicNum/m_h
    for x in production[curr_species]:
        print(x)
        temp = 0
        if len(x.getElements()) == 1:
            delta = 2
            query = memoizeComp(list(x.getElements())[0].getAtomicNum(), list(x.getElements())[0].getAtomicMass(), time-1)
            temp += query ** 2 / (delta * list(x.getElements())[0].getAtomicMass() ** 2)
            temp *= x.getRate()
        else:
            delta = 1
            query1 = memoizeComp(x.getElements()[0].getAtomicNum(), x.getElements()[0].getAtomicMass(), time-1)
            query2 = memoizeComp(x.getElements()[1].getAtomicNum(), x.getElements()[1].getAtomicMass(), time-1)
            temp += query1 * query2
            temp /= list(x.getElements())[0].getAtomicMass() * list(x.getElements())[1].getAtomicMass()
            temp *= x.getRate()
        last += coef * temp
    for x in consumption[curr_species]:
        temp = 0
        query1 = memoizeComp(list(x.getElements())[0].getAtomicNum(), list(x.getElements())[0].getAtomicMass(), time-1)
        temp += query1 / list(x.getElements())[0].getAtomicMass()
        temp *= x.getRate()
        temp *= placeHolder
        temp /= curr_species.getAtomicMass()
        last -= coef * temp
    mass_fractions[curr_species][time] = last
    return last
pprint.pprint(production[elements[0]])
for i in range(1, 100):
    for e in elements:
        memoizeComp(e.getAtomicNum(), e.getAtomicMass(), i)

