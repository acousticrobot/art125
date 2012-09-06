#!/usr/bin/env python

# Name: Image Indexer
# Author: Jonathan Gabel
# version: 0.9
# (c) GPL 2012
# URL: http://jonathangabel.com
# Make Multiple Choice takes in lists of artists and corresponding images
# For each artists in the test set, it generates one multiple choice question
# Answers are appended to the md/_multichoice.md file

import os
import random
from filehelper import write_to_file
CURRDIR = os.getcwd() + '/'


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

unit_3_set = [
    ("Jasper Johns","johns.1954.flag.jpg"),
    ("Richard Hamilton","hamilton.1956.todaysHomes.jpg"),
    ("Roy Lichtenstein","lichtenstein.1963.whaam.jpg"), 
    ("Claes Oldenburg","oldenburg.1962.floorCake.jpg"),
    ("Robert Rauschenberg","rauschenberg.55-9.monogram.jpg"),
    ("James Rosenquist","rosenquist.64-5.f111.detail2.jpg"),
    ("Andy Warhol","warhol.1962.marilynDyptych.jpg"),
    ("Chuck Close","close.1967.bigSelfPortrait.jpg"),
    ("Duane Hanson","hanson.1970.supermarketShopper.jpg")
]

unit_4_set = [
("David Smith","smith.1964.cubiXIX.jpg"),
("Louise Nevelson","nevelson.1958.skyCathedral.2.jpg"),
("Donald Judd","judd.1968.1900s.jpg"),
("Dan Flavin","flavin.1977.untitled.inhonorharoldjoachim.jpg"),
("Frank Stella","stella.1962.grandCairo.jpg"),
("Sol Lewitt","lewitt.60s.123454321.jpg"),
("Robert Morris","morris.1961.boxForStanding.empty.jpg"),
("Robert Smithson","smithson.1970.spiralJetty.jpg"),
("Richard Serra","serra.2006.band.jpg"),
("James Turrell","turrell.77-2002.rodenCratersEye.jpg")
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

def make_mulch(test_set, bank_set):
    """Creates a list of artists from unit lists of artists/image tuples
    
    test_set is the unit set to test, example: u2set
    bank_set is a list of all units to draw answers from, ex: [u1set,u2set,...]
    """
    bank = load_bank(bank_set)
    blen = len(bank) - 1    
    file_name = "../md/_multichoice.txt"
    title = "Multiple Choice"
    l = []
    qlist = ["A.","B.","C.", "D."]
    for x in range(len(test_set)):
        l.append("Q: This Artwork is by:")
        answer_set = [test_set[x][0]]
            # load unique artists names into answer_set
        for p in range(len(qlist) - 1):
            while True:
                r = random.randint(0, blen)
                if (bank[r] not in answer_set):
                    answer_set.append(bank[r])
                    break; 
        for q in range(len(qlist)):
            l.append( qlist[q] + answer_set[q] )
        l.append("Answer: A")
        l.append("POINTS: 5")
        l.append("TYPE: MC")
        l.append("IMAGE: $COURSE_PATH$images/"+ test_set[x][1])
        l.append("\n")
    write_to_file(l,file_name,title, mode='a')

make_mulch(unit_4_set,[unit_2_set,unit_3_set,unit_4_set])
