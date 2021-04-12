dt = 100
m_h = 1.6726219 * 10**-27
density = []
energy = []
elements = [[-1]*100] * 40

atomicNum = {"H":1, "He": 2, "Be": 4, "C": 6, "N": 7, "O": 8, "Ne": 10, "Mg": 12, "Si": 14, "S": 16, "Ar": 18,
             "Ca": 20, "Ti": 22, "Cr": 24, "Fe": 26, "Ni": 28}
def getElement(name, isotope):
    return atomicNum.get(name), isotope;

species = {(1,1): 0, (1,2): 1, (2,3): 2, (2,4): 3}
production = {}
consumption = {}


def memoizeComp(atomicNum, atomicMass, time):
    if(elements[species.get((atomicNum, atomicMass))][time] > -1):
        return elements[species.get((atomicNum, atomicMass))][time] > -1
    last = memoizeComp(atomicNum, atomicMass, time-1)
    coef = density[time-1] * atomicNum/m_h
    for x in production.get((atomicNum, atomicMass)):
        if x == (atomicNum, atomicMass):
            delta = 1
            temp = 0
            last += temp*coef
        else:
            delta = 0
            temp = 0
            last += temp*coef
    for x in consumption.get((atomicNum, atomicMass)):
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



