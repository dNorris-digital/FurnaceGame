from enum import Enum

class Card(Enum):
    p1 = 'p1'
    p2 = 'p2'
    p3 = 'p3'
    p4 = 'p4'
    p5 = 'p5'
    c1 = 'c1'
    c2 = 'c2'
    c3 = 'c3'
    c4 = 'c4'
    c5 = 'c5'
    c6 = 'c6'
    c7 = 'c7'
    c8 = 'c8'
    c9 = 'c9'
    c10 = 'c10'
    c11 = 'c11'
    c12 = 'c12'
    c13 = 'c13'
    c14 = 'c14'
    c15 = 'c15'
    c16 = 'c16'
    o1 = 'o1'
    o2 = 'o2'
    o3 = 'o3'
    s1 = 's1'
    s2 = 's2'
    s3 = 's3'
    s4 = 's4'
    s5 = 's5'
    s6 = 's6'
    s7 = 's7'
    s8 = 's8'
    s9 = 's9'
    s10 = 's10'
    s11 = 's11'
    s12 = 's12'
    s13 = 's13'
    s14 = 's14'
    s15 = 's15'
    t1 = 't1'
    t2 = 't2'

class Res():
    def __init__(self, o=0, c=0, s=0, t=0, m=0, a=False, **kwargs):
        self.oil=o
        self.coal=c
        self.steel=s
        self.tool=t
        self.coin=m
        self.advance=a

    def IsNotEmpty(self):
        if self.oil == 0 and self.coal == 0 and self.steel == 0 and self.tool == 0 and self.coin == 0:
            return False
        return True


def NewCard(name,
            rSource=Res(),
            rVal=Res(),
            pSource=Res(),
            pVal=Res(),
            pCount=1,
            aSource=Res(),
            aVal=Res(),
            aCount=1,
            **kwargs):
    outData = {}
    outData['name'] = name
    outData['ResourceSource'] = rSource
    outData['ResourceValue'] = rVal
    outData['PrimarySource'] = pSource
    outData['PrimaryValue'] = pVal
    outData['PrimaryCount'] = pCount
    outData['AdvancedSource'] = aSource
    outData['AdvancedValue'] = aVal
    outData['AdvancedCount'] = aCount
    return outData

CardDeck = {}
CardDeck[Card.o1] = NewCard('o1', rVal=Res(c=2), pSource=Res(o=1), pVal=Res(m=4), pCount=1, aVal=Res(c=3))
CardDeck[Card.o2] = NewCard('o2', rSource=Res(s=1), rVal=Res(o=1), pSource=Res(o=1), pVal=Res(m=4), pCount=1, aVal=Res(s=1, c=2))
CardDeck[Card.o3] = NewCard('o3', rSource=Res(c=1), rVal=Res(t=1), pSource=Res(o=1), pVal=Res(m=4), pCount=1, aVal=Res(c=3))
CardDeck[Card.t1] = NewCard('t1', rVal=Res(c=2), pSource=Res(t=1), pVal=Res(m=5), pCount=1, aVal=Res(c=3))
CardDeck[Card.t2] = NewCard('t2', rVal=Res(s=1), pSource=Res(t=1), pVal=Res(m=5), pCount=1, aVal=Res(s=2))
CardDeck[Card.c1] = NewCard('c1', rVal=Res(c=2), pVal=Res(c=2), aVal=Res(c=3))
CardDeck[Card.c2] = NewCard('c2', rSource=Res(s=1), rVal=Res(o=1), pVal=Res(c=2), aVal=Res(o=1))
CardDeck[Card.c3] = NewCard('c3', rVal=Res(c=2), pVal=Res(c=2), aSource=Res(s=1), aVal=Res(m=2), aCount=4)
CardDeck[Card.c4] = NewCard('c4', rVal=Res(c=2), pVal=Res(c=2), aSource=Res(s=1, o=1), aVal=Res(m=7), aCount=2)
CardDeck[Card.c5] = NewCard('c5', rVal=Res(c=2), pVal=Res(c=2), aSource=Res(t=1), aVal=Res(m=5), aCount=2)
CardDeck[Card.c6] = NewCard('c6', rVal=Res(c=2), pVal=Res(c=2), aSource=Res(o=1), aVal=Res(m=4), aCount=2)
CardDeck[Card.c7] = NewCard('c7', rSource=Res(c=2), rVal=Res(o=1), pSource=Res(c=2), pVal=Res(m=2), pCount=2, aVal=Res(s=2))
CardDeck[Card.c8] = NewCard('c8', rVal=Res(s=1), pSource=Res(c=2), pVal=Res(m=2), pCount=2, aVal=Res(o=1))
CardDeck[Card.c9] = NewCard('c9', rSource=Res(o=1), rVal=Res(s=3), pSource=Res(c=2), pVal=Res(m=2), pCount=2, aSource=Res(c=1), aVal=Res(s=1), aCount=4)
CardDeck[Card.c10] = NewCard('c10', rSource=Res(o=1), rVal=Res(s=3), pSource=Res(c=2), pVal=Res(o=1), pCount=2, aSource=Res(c=1, s=1), aVal=Res(m=4), aCount=3)
CardDeck[Card.c11] = NewCard('c11', rSource=Res(c=2), rVal=Res(o=1), pSource=Res(c=2), pVal=Res(o=1), pCount=2, aVal=Res(t=1))
CardDeck[Card.c12] = NewCard('c12', rSource=Res(c=2), rVal=Res(o=1), pSource=Res(c=1), pVal=Res(o=1), pCount=1, aSource=Res(c=1, s=1), aVal=Res(m=4), aCount=3)
CardDeck[Card.c13] = NewCard('c13', rSource=Res(s=1), rVal=Res(t=1), pVal=Res(c=2), aSource=Res(s=1), aVal=Res(m=2), aCount=4)
CardDeck[Card.c14] = NewCard('c14', rVal=Res(s=1), pVal=Res(c=2), aSource=Res(s=1), aVal=Res(m=2), aCount=4)
CardDeck[Card.c15] = NewCard('c15', rSource=Res(c=2), rVal=Res(o=1), pSource=Res(c=2), pVal=Res(m=2), pCount=2, aVal=Res(o=1))
CardDeck[Card.c16] = NewCard('c16', rVal=Res(s=1), pVal=Res(c=2), aSource=Res(o=1), aVal=Res(m=4), aCount=2)
CardDeck[Card.s1] = NewCard('s1', rVal=Res(s=1), pVal=Res(s=1), aSource=Res(c=1, o=1), aVal=Res(m=6), aCount=2)
CardDeck[Card.s2] = NewCard('s2', rVal=Res(s=1), pVal=Res(s=1), aSource=Res(o=1), aVal=Res(m=4), aCount=2)
CardDeck[Card.s3] = NewCard('s3', rVal=Res(c=1), pVal=Res(s=1), aSource=Res(c=1), aVal=Res(s=1), aCount=4)
CardDeck[Card.s4] = NewCard('s4', rVal=Res(s=1), pVal=Res(s=1), aSource=Res(t=1), aVal=Res(m=5), aCount=2)
CardDeck[Card.s5] = NewCard('s5', rVal=Res(s=1), pVal=Res(s=1), aVal=Res(s=2))
CardDeck[Card.s6] = NewCard('s6', rSource=Res(s=1), rVal=Res(t=1), pSource=Res(s=1), pVal=Res(t=1), aSource=Res(c=3), aVal=Res(m=4), aCount=3)
CardDeck[Card.s7] = NewCard('s7', rSource=Res(s=1), rVal=Res(o=1), pSource=Res(s=1), pVal=Res(o=1), pCount=2, aVal=Res(o=1))
CardDeck[Card.s8] = NewCard('s8', rSource=Res(s=1), rVal=Res(o=1), pSource=Res(s=1), pVal=Res(t=1), aSource=Res(s=1), aVal=Res(m=2), aCount=4)
CardDeck[Card.s9] = NewCard('s9', rVal=Res(s=1), pSource=Res(s=1), pVal=Res(o=1), pCount=2, aSource=Res(c=3), aVal=Res(m=4), aCount=3)
CardDeck[Card.s10] = NewCard('s10', rVal=Res(s=1), pSource=Res(s=1), pVal=Res(t=1), aSource=Res(s=1, o=1), aVal=Res(m=7), aCount=2)
CardDeck[Card.s11] = NewCard('s11', rVal=Res(c=2), pSource=Res(s=1), pVal=Res(m=2), pCount=2, aVal=Res(c=3))
CardDeck[Card.s12] = NewCard('s12', rSource=Res(s=1), rVal=Res(c=4), pSource=Res(s=1), pVal=Res(c=4), aVal=Res(t=1))
CardDeck[Card.s13] = NewCard('s13', rSource=Res(s=1), rVal=Res(c=4), pSource=Res(s=1), pVal=Res(c=4), aSource=Res(t=1), aVal=Res(m=5), aCount=2)
CardDeck[Card.s14] = NewCard('s14', rVal=Res(c=2), pVal=Res(s=1), aSource=Res(c=1, o=1), aVal=Res(m=6), aCount=2)
CardDeck[Card.s15] = NewCard('s15', rVal=Res(c=2), pVal=Res(s=1), aSource=Res(o=1), aVal=Res(m=4), aCount=2)
CardDeck[Card.p1] = NewCard('p1', rVal=Res(c=1, s=1), pSource=Res(c=2), pVal=Res(m=2), pCount=2, aSource=Res(t=1, c=1), aVal=Res(a=True))
CardDeck[Card.p2] = NewCard('p2', rVal=Res(c=1, s=1), pSource=Res(o=1), pVal=Res(m=4), aSource=Res(t=1, c=1), aVal=Res(a=True))
CardDeck[Card.p3] = NewCard('p3', rVal=Res(c=2), pSource=Res(c=3), pVal=Res(m=4), aSource=Res(t=1, c=1), aVal=Res(a=True))
CardDeck[Card.p4] = NewCard('p4', rVal=Res(c=2), pSource=Res(s=1), pVal=Res(m=2), pCount=2, aSource=Res(t=1, c=1), aVal=Res(a=True))
CardDeck[Card.p5] = NewCard('p5', rVal=Res(t=1), pSource=Res(c=1, s=1), pVal=Res(m=4), aSource=Res(t=1, c=1), aVal=Res(a=True))
