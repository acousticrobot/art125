#!/usr/bin/python

# Make Multiple Choice takes in 

import random

# define artsits and image set lists by unit

u2set = [	"Willem De Kooning","Helen Frankenthaler","Arshile Gorky","Hans Hofmann",
						"Morris Louis","Barnett Newman","Jackson Pollock","Ad Reinhardt","Marc Rothko"]
u2img = [	"dekooning.50.woman1.jpg", "frankenthaler.63.canal.jpg","gorky.44.theLiverisTheCocksComb.jpg", 
					"hofmann.62.sanctum.jpg", "louis.59.saraband.jpg","newman.48.onement.jpg",
					"pollock.50.autumnRhythm.jpg","reinhardt.60-66.abstractpainting.jpg","rothko.57.orangeandyellow.jpg"]


def load_bank(abank,alists):
	#adbank = list to fill
	# alists = list of artist lists to include
	for alist in alists:
		for artist in alist:
			abank.append(artist)
	
def unique_list(seq):
	# don't repeat an artist
	# from:
	# http://www.peterbe.com/plog/uniqifiers-benchmark
	set = Set(seq)
	return list(set)

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


# define artists bank

abank = []
load_bank(abank,[u2set])			
alen = len(abank) - 1
random_artists(u2set,u2img)