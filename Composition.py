from mendeleev import element


class Species:
    def __init__(self, element, aMass):
        self.element = element
        self.isotope = aMass

    def __hash__(self):
        return hash(self.element) ^ hash(self.isotope)

    def getElement(self):
        return self.element.symbol
    def getAtomicMass(self):
        return self.isotope
    def toString(self):
        return "(" + self.getElement() + "," + str(self.getAtomicMass()) + ")"

class Reactions:
    def __init__(self, reactants, products, rate):
        self.reactants = reactants
        self.products = products
        self.rate = rate

    def __hash__(self):
        return hash(self.reactants) ^ hash(self.products)
    def getReactants(self):
        return self.reactants
    def getProducts(self):
        return self.products
    def getRate(self):
        return self.rate
    def setRate(self, newRate):
        self.rate = newRate


dt = 100
m_h = 1.6726219 * 10**-27
rho = 15 #to be determined, assume density stays constant, dummy number for now
energy = []

elements = []
elements.append(Species(element(1), 1))
elements.append(Species(element(1), 2))
elements.append(Species(element(2), 3))
elements.append(Species(element(2), 4))
elements.append(Species(element(4), 8))
elements.append(Species(element(6), 12))
elements.append(Species(element(6), 13))
elements.append(Species(element(7), 13))
elements.append(Species(element(7), 14))
elements.append(Species(element(7), 15))
elements.append(Species(element(8), 15))
elements.append(Species(element(8), 16))
elements.append(Species(element(8), 17))
elements.append(Species(element(9), 17))
elements.append(Species(element(9), 18))
elements.append(Species(element(9), 19))
for i in range(10, 30, 2):
    elements.append(Species(element(i), 2*i))
production = {}
consumption = {}

mass_fractions = {}
for e in elements:
    mass_fractions[e] = [-1]*100
    mass_fractions[e][0] = 0
for x in mass_fractions:
    print(x.toString() + " " + str(mass_fractions[x]))


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
    elements[species.get((atomicNum, atomicMass))][time] = last
    return last



