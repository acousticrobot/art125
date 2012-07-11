#!/usr/bin/env python

# Make Multiple Choice takes in lists of artists and corresponding images

import random

# define sets: ("artist", image.jpg, "title, date")


unit_2_set = [
    ("Willem De Kooning","dekooning.50.woman1.jpg"),
    ("Helen Frankenthaler","frankenthaler.63.canal.jpg"),
    ("Arshile Gorky","gorky.44.theLiverisTheCocksComb.jpg"), 
    ("Hans Hofmann","hofmann.62.sanctum.jpg"),
    ("Morris Louis","louis.59.saraband.jpg"),
    ("Barnett Newman","newman.48.onement.jpg"),
    ("Jackson Pollock","pollock.50.autumnRhythm.jpg"),
    ("Ad Reinhardt","reinhardt.60-66.abstractpainting.jpg"),
    ("Marc Rothko","rothko.57.orangeandyellow.jpg")
]

def load_bank(unit_sets):
    """Creates a list of artists from unit lists of artists/image tuples

    unit_sets = list of unit lists containing artists/image tuples
    [unit1,unit2,...]: unit1 = [(artist,image),(artist,image)...]
    returns bank, a list of artists only, no images"""
    bank = []
    for unit in unit_sets:
        for artist in unit:
            bank.append(artist[0])
    return bank


def make_mulch(aset,iset):
    for x in range(len(aset)):
        outgroup.write("Q: This Artwork is by:\n")
        outgroup.write("A."+aset[x]+"\n")
        rand = []
        for p in range(len(qlist)):
            while True:
                r = random.randint(0, alen)
                if (r not in rand) and (r != x):
                    rand.append(r)
                    break; 
        for q in range(len(qlist)):
            outgroup.write( qlist[q] + abank[rand[q]] + "\n" )
        outgroup.write("Answer: A\n")
        outgroup.write("POINTS: 5\n")
        outgroup.write("TYPE: MC\n")
        outgroup.write("IMAGE: http://jonathangabel.com/images/art125/"+ iset[x]+"\n")
        outgroup.write("\n")


def make_mulch2(test_set, bank_set):
    """Creates a list of artists from unit lists of artists/image tuples
    
    test_set is the unit set to test, example: u2set
    bank_set is a list of all units to draw answers from, ex: [u1set,u2set,...]
    """
    bank = load_bank(bank_set)
    blen = len(bank) - 1    
    outgroup = file ("md/_multichoice.txt",'w')
    qlist = ["A.","B.","C.", "D."]
    for x in range(len(test_set)):
        outgroup.write("Q: This Artwork is by:\n")
        answer_set = [test_set[x][0]]
            # load unique artists names into answer_set
        for p in range(len(qlist) - 1):
            while True:
                r = random.randint(0, blen)
                if (bank[r] not in answer_set):
                    answer_set.append(bank[r])
                    break; 
        for q in range(len(qlist)):
            outgroup.write( qlist[q] + answer_set[q] + "\n" )
        outgroup.write("Answer: A\n")
        outgroup.write("POINTS: 5\n")
        outgroup.write("TYPE: MC\n")
        outgroup.write("IMAGE: http://jonathangabel.com/images/art125/"+ test_set[x][1]+"\n")
        outgroup.write("\n")

# define artists bank

#abank = load_bank([u2set])         
#alen = len(abank) - 1

make_mulch2(unit_2_set,[unit_2_set])
# outgroup = file ("md/_multichoice.txt",'w')
# for x in range(len(u22set)):
#   outgroup.write("A."+ u22set[x][0]+"\n")


