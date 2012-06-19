import random

# define artsits and image set lists by unit

u1set = [	"Willem De Kooning","Helen Frankenthaler","Arshile Gorky","Hans Hofmann",
						"Morris Louis","Barnett Newman","Jackson Pollock","Ad Reinhardt","Marc Rothko"]
u1img = [	"dekooning.50.woman1.jpg", "frankenthaler.63.canal.jpg","gorky.44.theLiverisTheCocksComb.jpg", 
					"hofmann.62.sanctum.jpg", "louis.59.saraband.jpg","newman.48.onement.jpg",
					"pollock.50.autumnRhythm.jpg","reinhardt.60-66.abstractpainting.jpg","rothko.57.orangeandyellow.jpg"]

# define bank of artists

abank = []

# load units into abank

for artist in u1set:
	abank.append(artist)

alen = len(abank) - 1

def unique_list(seq):
	#not order preserving
	# http://www.peterbe.com/plog/uniqifiers-benchmark
	set = Set(seq)
	return list(set)

def random_artists(aset,iset):
	qlist = ["B.","C.", "D."]
	for x in range(len(aset)):
		print "Q: This Artwork is by:"
		print "A.", aset[x]
		rand = []
		for p in range(len(qlist)):
			while True:
				r = random.randint(0, alen)
				if (r not in rand) and (r != x):
					rand.append(r)
					break; 
		for q in range(len(qlist)):
			print qlist[q], abank[rand[q]]
		print "Answer: A"
		print "POINTS: 5"
		print "TYPE: MC"
		print "IMAGE: http://jonathangabel.com/images/art125/"+ iset[x]
		print
				
random_artists(u1set,u1img)