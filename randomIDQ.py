import random


# define artsits and image set lists by unit

u1set = [	"Helen Frankenthaler","Arshile Gorky","Hans Hofmann","Willem De Kooning",
						"Morris Louis","Barnett Newman","Jackson Pollock","Ad Reinhardt","Marc Rothko"]
u1img = [	"Frankenthaler.","Gorky.","Hofmann.","DeKooning.",
					"Louis.","Newman.","Pollock.","Reinhardt.","Rothko."]

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
		print "Question: This Artwork is by:"
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