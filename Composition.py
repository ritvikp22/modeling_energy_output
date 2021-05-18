from mendeleev import element
import math
from pprint import pprint

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
    def __init__(self, stuff, rate, energy):
        self.stuff = stuff
        self.rate = rate
        self.energy = 0 if energy == None else energy

    def __hash__(self):
        return hash(len(self.stuff)) ^ hash(self.rate)

    def __eq__(self, other):
        if len(self.stuff) != len(other.stuff):
            return False
        if self.energy != other.energy:
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
    def setRate(self, oldT, newT):
        oldFactor = 1.0
        oldFactor *= (oldT ** (-2.0 / 3.0))
        oldFactor *= math.exp(-1.0 * oldT ** (-1.0 / 3.0))
        newFactor = 1.0
        newFactor *= (newT ** (-2.0 / 3.0))
        newFactor *= math.exp(-1.0 * newT ** (-1.0 / 3.0))
        self.rate /= oldFactor
        self.rate *= newFactor

    def getEnergy(self):
        return self.energy
    def __str__(self):
        temp = "["
        for x in self.stuff.keys():
            temp = temp + str(x) + ": " + str(self.stuff[x]) + ", "
        temp = temp + "]"
        return temp


dt = 86400
m_h = 1.67 * 10**-24
stefan = 5.670374419 * 10 ** -8
radius = 6.5 * 6.957 * 10 ** 8
mass = 1.98847 * 10 ** 33
Temperature = 29850.0
rho = mass * 3.0 / (4.0 * math.pi * radius * radius * radius)
rrc = 4.0 / (3 ** 2.5)
rrc /= (math.pi * math.pi)
rrc *= (6.62607015 * 10 ** -31)
rrc /= m_h
rrc /= (math.e * math.e)
rrc *= (Temperature ** (-2.0/3.0))
rrc *= math.exp(-1.0 * Temperature ** (-1.0/3.0))

#Putting in value for S(E_0), found based on calculations with the sun

rrc /= (3 * 10 ** 30)
rrc *= (3.828 / 3.19635)

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
    mass_fractions[e] = [-1]*1000000
    mass_fractions[e][0] = 0
    creation[e] = set()
    destruction[e] = set()
total = 1.0*1*10**12+4*10**10.92+12*10**8.26+14*10**7.62+16*10**8.43+20*10**8.26+24*10**7.60+28*10**7.14+52*10**7.30
mass_fractions[Species(1,1)][0] = 1.0 * (10**12) / total
mass_fractions[Species(2,4)][0] = 4.0 * (10**10.92) / total
mass_fractions[Species(6,12)][0] = 12.0 * (10**8.26) / total
mass_fractions[Species(7,14)][0] = 14.0 * (10**7.62) / total
mass_fractions[Species(8,16)][0] = 16.0 * (10**8.43) / total
mass_fractions[Species(10,20)][0] = 20.0 * (10**8.26) / total
mass_fractions[Species(12,24)][0] = 24.0 * (10**7.60) / total
mass_fractions[Species(14,28)][0] = 28.0 * (10**7.14) / total
mass_fractions[Species(26,52)][0] = 52.0 * (10**7.30) / total
reactions = set()

energy = [0] * 1000000
temperature = [0] * 1000000

temperature[0] = Temperature
temperature[1] = Temperature

def findFactor(a, b):
    temp = 1.0
    temp *= a.getAtomicNum()
    temp *= a.getAtomicMass()
    temp *= b.getAtomicNum()
    temp *= b.getAtomicMass()
    temp /= (a.getAtomicMass() + b.getAtomicMass())
    return temp


#Setting up pp chain

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(1,1))
destruction[Species(1,1)].add(Reactions({Species(1,1): 1}, dummyRate, 0))
creation[Species(1,2)].add(Reactions({Species(1,1): 2}, dummyRate, 1.442))


dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(1,2))
destruction[Species(1, 1)].add(Reactions({Species(1, 2): 1}, dummyRate, 0))
destruction[Species(1, 2)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
creation[Species(2, 3)].add(Reactions({Species(1, 1): 1, Species(1, 2): 1}, dummyRate, 5.493))


dummyRate = 1.0 * rrc / findFactor(Species(2,3), Species(2,3))
destruction[Species(2, 3)].add(Reactions({Species(2, 3): 1}, dummyRate, 0))
creation[Species(2, 4)].add(Reactions({Species(2, 3): 2}, dummyRate, 0))
creation[Species(1, 1)].add(Reactions({Species(2, 3): 2}, 2*dummyRate, 12.859))


dummyRate = 1.0 * rrc / findFactor(Species(2,3), Species(2,4))
destruction[Species(2, 3)].add(Reactions({Species(2, 4): 1}, dummyRate, 0))
destruction[Species(2, 4)].add(Reactions({Species(2, 3): 1}, dummyRate, 0))
creation[Species(4, 7)].add(Reactions({Species(2, 3): 1, Species(2, 4): 1}, dummyRate, 1.59))


dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(2,3))
destruction[Species(2, 3)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(2, 3): 1}, dummyRate, 0))
creation[Species(2, 4)].add(Reactions({Species(2, 3): 1, Species(1, 1): 1}, dummyRate, 19.795))


dummyRate = 1.0 * rrc / 28.0
destruction[Species(4, 7)].add(Reactions({}, dummyRate, 0))
creation[Species(3, 7)].add(Reactions({Species(4, 7): 1}, dummyRate, 0.383))


dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(3,7))
destruction[Species(3, 7)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(3, 7): 1}, dummyRate, 0))
creation[Species(2, 4)].add(Reactions({Species(3, 7): 1, Species(1, 1): 1}, 2*dummyRate, 17.35))


dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(4,7))
destruction[Species(4, 7)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(4, 7): 1}, dummyRate, 0))
creation[Species(5, 8)].add(Reactions({Species(1, 1): 1, Species(4, 7): 1}, dummyRate, 0))


dummyRate = 1.0 * rrc / 40.0
destruction[Species(5, 8)].add(Reactions({}, dummyRate, 0))
creation[Species(4, 8)].add(Reactions({Species(5, 8): 1}, dummyRate, 0))


dummyRate = 1.0 * rrc / 32.0
destruction[Species(4, 8)].add(Reactions({}, dummyRate, 0))
creation[Species(2, 4)].add(Reactions({Species(4, 8): 1}, 2 * dummyRate, 0))


# Setting up Triple Alpha Process

dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(2,4))
destruction[Species(2, 4)].add(Reactions({Species(2, 4): 1}, dummyRate, 0))
creation[Species(4, 8)].add(Reactions({Species(2, 4): 2}, dummyRate, -0.0918))


dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(4,8))
destruction[Species(4, 8)].add(Reactions({Species(2, 4): 1}, dummyRate, 0))
destruction[Species(2, 4)].add(Reactions({Species(4, 8): 1}, dummyRate, 0))
creation[Species(6, 12)].add(Reactions({Species(2, 4): 1, Species(4, 8): 1}, dummyRate, 7.367))


dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(6,12))
destruction[Species(6, 12)].add(Reactions({Species(2, 4): 1}, dummyRate, 0))
destruction[Species(2, 4)].add(Reactions({Species(6, 12): 1}, dummyRate, 0))
creation[Species(8, 16)].add(Reactions({Species(2, 4): 1, Species(6, 12): 1}, dummyRate, 7.162))


# Setting up Alpha Process

for i in range(6, 28, 2):
    dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(i, 2 * i))
    destruction[Species(i, 2 * i)].add(Reactions({Species(2, 4): 1}, dummyRate, 0))
    destruction[Species(2, 4)].add(Reactions({Species(i, 2 * i): 1}, dummyRate, 0))

dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(8,16))
creation[Species(10, 20)].add(Reactions({Species(2, 4): 1, Species(8, 16): 1}, dummyRate, 4.73))

dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(10,20))
creation[Species(12, 24)].add(Reactions({Species(2, 4): 1, Species(10, 20): 1}, dummyRate, 9.32))

dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(12,24))
creation[Species(14, 28)].add(Reactions({Species(2, 4): 1, Species(12, 24): 1}, dummyRate, 9.98))

dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(14,28))
creation[Species(16, 32)].add(Reactions({Species(2, 4): 1, Species(14, 28): 1}, dummyRate, 6.95))

dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(16,32))
creation[Species(18, 36)].add(Reactions({Species(2, 4): 1, Species(16, 32): 1}, dummyRate, 6.64))

dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(18,36))
creation[Species(20, 40)].add(Reactions({Species(2, 4): 1, Species(18, 36): 1}, dummyRate, 7.04))

dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(20,40))
creation[Species(22, 44)].add(Reactions({Species(2, 4): 1, Species(20, 40): 1}, dummyRate, 5.13))

dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(22,44))
creation[Species(24, 48)].add(Reactions({Species(2, 4): 1, Species(22, 44): 1}, dummyRate, 7.70))

dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(24,48))
creation[Species(26, 52)].add(Reactions({Species(2, 4): 1, Species(24, 48): 1}, dummyRate, 7.94))

dummyRate = 1.0 * rrc / findFactor(Species(2,4), Species(26,52))
creation[Species(28, 56)].add(Reactions({Species(2, 4): 1, Species(26, 52): 1}, dummyRate, 8.00))


# Set up Carbon Burning

dummyRate = 1.0 * rrc / findFactor(Species(6,12), Species(6,12))
destruction[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate, 0))
creation[Species(10, 20)].add(Reactions({Species(6, 12): 2}, dummyRate, 4.617))
creation[Species(2, 4)].add(Reactions({Species(6, 12): 2}, dummyRate, 4.617))

dummyRate = 1.0 * rrc / findFactor(Species(6,12), Species(6,12))
destruction[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate, 0))
creation[Species(11, 23)].add(Reactions({Species(6, 12): 2}, dummyRate, 2.241))
creation[Species(1, 1)].add(Reactions({Species(6, 12): 2}, dummyRate, 2.241))

dummyRate = 1.0 * rrc / findFactor(Species(6,12), Species(6,12))
destruction[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate, 0))
creation[Species(12, 23)].add(Reactions({Species(6, 12): 2}, dummyRate, -2.599))

dummyRate = 1.0 * rrc / findFactor(Species(6,12), Species(6,12))
destruction[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate, 0))
creation[Species(12, 24)].add(Reactions({Species(6, 12): 2}, dummyRate, 13.933))

dummyRate = 1.0 * rrc / findFactor(Species(6,12), Species(6,12))
destruction[Species(6, 12)].add(Reactions({Species(6, 12): 1}, dummyRate, 0))
creation[Species(8, 16)].add(Reactions({Species(6, 12): 2}, dummyRate, -0.113))
creation[Species(2, 4)].add(Reactions({Species(6, 12): 2}, 2 * dummyRate, -0.113))


# Set up CNO Cycle 1

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(6,12))
destruction[Species(6, 12)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(6, 12): 1}, dummyRate, 0))
creation[Species(7, 13)].add(Reactions({Species(1, 1): 1, Species(6, 12): 1}, dummyRate,1.95))

dummyRate = 1.0 * rrc / 91.0
destruction[Species(7, 13)].add(Reactions({}, dummyRate, 0))
creation[Species(6, 13)].add(Reactions({Species(7, 13): 1}, dummyRate, 1.20))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(6,13))
destruction[Species(6, 13)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(6, 13): 1}, dummyRate, 0))
creation[Species(7, 14)].add(Reactions({Species(1, 1): 1, Species(6, 13): 1}, dummyRate, 7.54))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(7,14))
destruction[Species(7, 14)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(7, 14): 1}, dummyRate, 0))
creation[Species(8, 15)].add(Reactions({Species(1, 1): 1, Species(7, 14): 1}, dummyRate, 7.35))

dummyRate = 1.0 * rrc / 120.0
destruction[Species(8, 15)].add(Reactions({}, dummyRate, 0))
creation[Species(7, 15)].add(Reactions({Species(8, 15): 1}, dummyRate, 1.73))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(7,15))
destruction[Species(7, 15)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(7, 15): 1}, dummyRate, 0))
creation[Species(6, 12)].add(Reactions({Species(1, 1): 1, Species(7, 15): 1}, dummyRate, 4.96))
creation[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(7, 15): 1}, dummyRate, 4.96))


#Set up CNO Cycle 2

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(7,15))
destruction[Species(7, 15)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(7, 15): 1}, dummyRate, 0))
creation[Species(8, 16)].add(Reactions({Species(1, 1): 1, Species(7, 15): 1}, dummyRate, 12.13))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(8,16))
destruction[Species(8, 16)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(8, 16): 1}, dummyRate, 0))
creation[Species(9, 17)].add(Reactions({Species(1, 1): 1, Species(8, 16): 1}, dummyRate, 0.60))

dummyRate = 1.0 * rrc / 1.0*9*17
destruction[Species(9, 17)].add(Reactions({}, dummyRate, 0))
creation[Species(8, 17)].add(Reactions({Species(9, 17): 1}, dummyRate, 2.76))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(8,17))
destruction[Species(8, 17)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(8, 17): 1}, dummyRate, 0))
creation[Species(7, 14)].add(Reactions({Species(1, 1): 1, Species(8, 17): 1}, dummyRate, 1.19))
creation[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(8, 17): 1}, dummyRate, 1.19))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(7,14))
destruction[Species(7, 14)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(7, 14): 1}, dummyRate, 0))
creation[Species(8, 15)].add(Reactions({Species(1, 1): 1, Species(7, 14): 1}, dummyRate, 7.35))

dummyRate = 1.0 * rrc / 120.0
destruction[Species(8, 15)].add(Reactions({}, dummyRate, 0))
creation[Species(7, 15)].add(Reactions({Species(8, 15): 1}, dummyRate, 2.75))


#Set up CNO Cycle 3

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(8,17))
destruction[Species(8, 17)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(8, 17): 1}, dummyRate, 0))
creation[Species(9, 18)].add(Reactions({Species(1, 1): 1, Species(8, 17): 1}, dummyRate, 5.61))

dummyRate = 1.0 * rrc / 1.0 * 9 * 18
destruction[Species(9, 18)].add(Reactions({}, dummyRate, 0))
creation[Species(8, 18)].add(Reactions({Species(9, 18): 1}, dummyRate, 1.656))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(8,18))
destruction[Species(8, 18)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(8, 18): 1}, dummyRate, 0))
creation[Species(7, 15)].add(Reactions({Species(1, 1): 1, Species(8, 18): 1}, dummyRate, 3.98))
creation[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(8, 18): 1}, dummyRate, 3.98))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(7,15))
destruction[Species(7, 15)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(7, 15): 1}, dummyRate, 0))
creation[Species(8, 16)].add(Reactions({Species(1, 1): 1, Species(7, 15): 1}, dummyRate, 12.13))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(8,16))
destruction[Species(8, 16)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(8, 16): 1}, dummyRate, 0))
creation[Species(9, 17)].add(Reactions({Species(1, 1): 1, Species(8, 16): 1}, dummyRate, 0.60))

dummyRate = 1.0 * rrc / 1.0 * 9 * 17
destruction[Species(9, 17)].add(Reactions({}, dummyRate, 0))
creation[Species(8, 17)].add(Reactions({Species(9, 17): 1}, dummyRate, 2.76))


#Set up CNO Cycle 4

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(8,18))
destruction[Species(8, 18)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(8, 18): 1}, dummyRate, 0))
creation[Species(9, 19)].add(Reactions({Species(1, 1): 1, Species(8, 18): 1}, dummyRate, 7.994))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(9,19))
destruction[Species(9, 19)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(9, 19): 1}, dummyRate, 0))
creation[Species(8, 16)].add(Reactions({Species(1, 1): 1, Species(9, 19): 1}, dummyRate, 8.114))
creation[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(9, 19): 1}, dummyRate, 8.114))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(8,16))
destruction[Species(8, 16)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(8, 16): 1}, dummyRate, 0))
creation[Species(9, 19)].add(Reactions({Species(1, 1): 1, Species(8, 16): 1}, dummyRate, 0.60))

dummyRate = 1.0 * rrc / 9.0 * 17
destruction[Species(9, 17)].add(Reactions({}, dummyRate, 0))
creation[Species(8, 17)].add(Reactions({Species(9, 17): 1}, dummyRate, 2.76))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(8,17))
destruction[Species(8, 17)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(8, 17): 1}, dummyRate, 0))
creation[Species(9, 18)].add(Reactions({Species(1, 1): 1, Species(8, 17): 1}, dummyRate, 5.61))

dummyRate = 1.0 * rrc / 9.0 * 18
destruction[Species(9, 18)].add(Reactions({}, dummyRate, 0))
creation[Species(8, 18)].add(Reactions({Species(9, 18): 1}, dummyRate, 1.656))


#Set up HCNO 1

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(7,13))
destruction[Species(7, 13)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(7, 13): 1}, dummyRate, 0))
creation[Species(8, 14)].add(Reactions({Species(1, 1): 1, Species(7, 13): 1}, dummyRate, 4.63))

dummyRate = 1.0 * rrc / 8.0 * 14
destruction[Species(8, 14)].add(Reactions({}, dummyRate, 0))
creation[Species(7, 14)].add(Reactions({Species(8, 14): 1}, dummyRate, 5.14))


#Set up HCNO 2

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(9,17))
destruction[Species(9, 17)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(9, 17): 1}, dummyRate, 0))
creation[Species(10, 18)].add(Reactions({Species(1, 1): 1, Species(9, 17): 1}, dummyRate, 3.92))

dummyRate = 1.0 * rrc / 10.0 * 18
destruction[Species(10, 18)].add(Reactions({}, dummyRate, 0))
creation[Species(9, 18)].add(Reactions({Species(10, 18): 1}, dummyRate, 4.44))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(9,18))
destruction[Species(9, 18)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(9, 18): 1}, dummyRate, 0))
creation[Species(8, 15)].add(Reactions({Species(1, 1): 1, Species(9, 18): 1}, dummyRate, 2.88))
creation[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(9, 18): 1}, dummyRate, 2.88))


#Set up HCNO 3

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(9,18))
destruction[Species(9, 18)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(9, 18): 1}, dummyRate, 0))
creation[Species(10, 19)].add(Reactions({Species(1, 1): 1, Species(9, 18): 1}, dummyRate, 6.41))

dummyRate = 1.0 * rrc / 10.0 * 19
destruction[Species(10, 19)].add(Reactions({}, dummyRate, 0))
creation[Species(9, 19)].add(Reactions({Species(10, 19): 1}, dummyRate, 3.32))

dummyRate = 1.0 * rrc / findFactor(Species(1,1), Species(9,19))
destruction[Species(9, 19)].add(Reactions({Species(1, 1): 1}, dummyRate, 0))
destruction[Species(1, 1)].add(Reactions({Species(9, 19): 1}, dummyRate, 0))
creation[Species(8, 16)].add(Reactions({Species(1, 1): 1, Species(9, 19): 1}, dummyRate, 8.11))
creation[Species(2, 4)].add(Reactions({Species(1, 1): 1, Species(9, 19): 1}, dummyRate, 8.11))


for e in creation:
    for r in creation[e]:
        reactions.add(r)



def dpComp(atomicNum, atomicMass, time):
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

def dpEnergy(time):
    sum = 0
    for r in reactions:
        if len(r.getElementList()) == 1:
            species1 = r.getElement(0)
            temp = 1.0 * (mass_fractions[species1][time-1] ** 2) / (species1.getAtomicMass() ** 2)
            temp *= r.getRate()
            temp *= r.getEnergy()
            sum += temp
        else:
            species1 = r.getElement(0)
            species2 = r.getElement(1)
            temp = 0.5 * mass_fractions[species1][time-1] * mass_fractions[species2][time-1]
            temp /= species1.getAtomicMass()
            temp /= species2.getAtomicMass()
            temp *= r.getRate()
            temp *= r.getEnergy()
            sum += temp
    sum *= rho
    sum /= (m_h * m_h)
    sum *= dt
    sum *= 15
    sum *= mass
    return sum

def dpTemperature(time):
    q = 1.0 * energy[time] / dt
    q /= (4 * math.pi)
    q /= stefan
    q /= (radius * radius)
    T = q ** 0.25
    return T



for i in range(1,10):
    for e in elements:
        mass_fractions[e][i] = dpComp(e.getAtomicNum(), e.getAtomicMass(), i)
    energy[i] = dpEnergy(i)
    energy[i]*= (1.6021773 * 10 ** -13)
    if i > 1:
        temperature[i] = dpTemperature(i)
    print(energy[i])
    print(temperature[i])








