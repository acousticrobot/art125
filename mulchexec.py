#!/usr/bin/python

# Make Multiple Choice takes in lists of artists and corresponding images

import random

# define sets: ("artist", image.jpg, "title, date")

u2set = [	"Willem De Kooning","Helen Frankenthaler","Arshile Gorky","Hans Hofmann",
						"Morris Louis","Barnett Newman","Jackson Pollock","Ad Reinhardt","Marc Rothko"]
u2img = [	"dekooning.50.woman1.jpg", "frankenthaler.63.canal.jpg","gorky.44.theLiverisTheCocksComb.jpg", 
					"hofmann.62.sanctum.jpg", "louis.59.saraband.jpg","newman.48.onement.jpg",
					"pollock.50.autumnRhythm.jpg","reinhardt.60-66.abstractpainting.jpg","rothko.57.orangeandyellow.jpg"]

u22set = [
	("Willem De Kooning","dekooning.50.woman1.jpg","Woman 1, 1950"),
	("Helen Frankenthaler","frankenthaler.63.canal.jpg","Canal, 1963"),
	("Arshile Gorky","gorky.44.theLiverisTheCocksComb.jpg","The Liver is the Cocks Comb, 1944"), 
	("Hans Hofmann","hofmann.62.sanctum.jpg","Sanctum, 1962"),
	("Morris Louis","louis.59.saraband.jpg","Saraband, 1959"),
	("Barnett Newman","newman.48.onement.jpg","Onement 1948"),
	("Jackson Pollock","pollock.50.autumnRhythm.jpg","Autumn Rhythm.jpg"),
	("Ad Reinhardt","reinhardt.60-66.abstractpainting.jpg"),
	("Marc Rothko","rothko.57.orangeandyellow.jpg")
]

def load_bank(alists):
	#adbank = list to fill
	# alists = list of artist lists to include
	abank = []
	for alist in alists:
		for artist in alist:
			abank.append(artist)
	return abank
	
def make_mulch(aset,iset):
	outgroup = file ("md/_multichoice.txt",'w')
	qlist = ["B.","C.", "D."]
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
	# bank_set = [u1set,u2set,...]
	# test_set = u2set
	bank = load_bank(bank_set)
	blen = len(bank) - 1	
	outgroup = file ("md/_multichoice.txt",'w')
	qlist = ["B.","C.", "D."]
	for x in range(len(test_set)):
		outgroup.write("Q: This Artwork is by:\n")
		outgroup.write("A."+ test_set[x][0]+"\n")
		rand = []
		for p in range(len(qlist)):
			while True:
				r = random.randint(0, blen)
				if (r not in rand) and (r != x):
					rand.append(r)
					break; 
		for q in range(len(qlist)):
			outgroup.write( qlist[q] + bank[rand[q]][0] + "\n" )
		outgroup.write("Answer: A\n")
		outgroup.write("POINTS: 5\n")
		outgroup.write("TYPE: MC\n")
		outgroup.write("IMAGE: http://jonathangabel.com/images/art125/"+ test_set[x][1]+"\n")
		outgroup.write("\n")

# define artists bank

#abank = load_bank([u2set])			
#alen = len(abank) - 1

make_mulch2(u22set,[u22set])
# outgroup = file ("md/_multichoice.txt",'w')
# for x in range(len(u22set)):
# 	outgroup.write("A."+ u22set[x][0]+"\n")


