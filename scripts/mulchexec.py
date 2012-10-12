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
import re
import random
from filehelper import write_to_file
CURRDIR = os.getcwd() + '/'

unit_2_set = [
    ("Willem De Kooning","dekooning.1950.woman1.jpg"),
    ("Helen Frankenthaler","frankenthaler.1963.canal.jpg"),
    ("Arshile Gorky","gorky.1944.theLiverIsTheCocksComb.jpg"), 
    ("Hans Hofmann","hofmann.1962.sanctum.jpg"),
    ("Morris Louis","louis.1959.saraband.jpg"),
    ("Barnett Newman","newman.1948.onement.jpg"),
    ("Jackson Pollock","pollock.1950.autumnRhythm.jpg"),
    ("Ad Reinhardt","reinhardt.1960-66.abstractPainting.jpg"),
    ("Marc Rothko","rothko.1957.orangeAndYellow.jpg")
]

unit_3_set = [
    ("Jasper Johns","johns.1954.flag.jpg"),
    ("Richard Hamilton","hamilton.1956.justWhatIsItEtc.jpg"),
    ("Roy Lichtenstein","lichtenstein.1963.whaam.jpg"), 
    ("Claes Oldenburg","oldenburg.1962.floorCake.jpg"),
    ("Robert Rauschenberg","rauschenberg.55-9.monogram.jpg"),
    ("James Rosenquist","rosenquist.1964-5.f111.detail2.jpg"),
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

unit_5_set = [
("Judy Chicago","chicago.74-9.dinnerParty.jpg"),
("Carolee Schneemann","schneemann.1975.interiorScroll.jpg"),
("Ana Mendieta","mendieta.1977.treeOfLife.jpg"),
("Fred Wilson","wilson.1991.guardedView.jpg"),
("Kara Walker","walker.1994c.girlAndMan.jpg"),
("Carrie Mae Weems","weems.2008.theAssasinationOfMedgarMalcolmAndMartin.jpg"),
("Michael Ray Charles","charles.1994.beware.jpg"),
("Kerry James Marshall","marshall.1992.couldThisBeLove.jpg")
]

unit_7_set = [
("Jenny Holzer","holzer.1986.timesSquareTruisms.77-9.jpg"),
("Jeff Koons","koons.1988.michaelJacksonAndBubbles.jpg"),
("Jean Michel Basquiat","basquiat.1981.untitled.jpg"),
("Barbara Kruger","kruger.1987.shop.jpg"),
("Cindy Sherman","sherman.1982.sundress.jpg")

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
    
def make_exam(bank_set):
    """Creates a list of exam images to use from the bank set
    
    Images names are encoded with rot13 and cut to 10 characters. A file is printed
    with new names for reference, the terminal commands to copy the files into a
    new directory with the new names, and then the bank set is passed onto make_mulch
    to create the list of test questions as per usual.
    """
    conversion = []
    bash = []
    exam_bank = []
    for unit in bank_set:
        for item in unit:
            r13 = item[1].encode('rot13')
                # take out dates cut to 10 char max and return to jpg 
            r13 = re.sub('.wct','',r13)
            r13 = re.sub(r'\.\d+\-?\d*.\.','',r13)
            if  len(r13) > 10:
                r13 = r13[:10]
            r13 = r13 + '.jpg'
            conversion.append(item[1] + " --> " + r13)
            bash.append("cp " + item[1] + " _exam/" + r13)
            exam_bank.append((item[0],r13))
    file_name = "../images/_exam_notes.txt"
    title = "Exam Images Key:"
    write_to_file(conversion,file_name,title, mode='a')
    title = "Bash Commands for file rename:"
    write_to_file(bash,file_name,title, mode='a')
    make_mulch(exam_bank,[exam_bank])
    

make_mulch(unit_7_set,[unit_2_set,unit_3_set,unit_4_set,unit_5_set,unit_7_set])
#make_exam([unit_2_set,unit_3_set,unit_4_set,unit_5_set])