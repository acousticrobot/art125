artists = ['Joseph Albers', 'Morris Louis', 'Ad Reinhardt', 'Willem De Kooning', 'Hans Hoffmann', 'Robert Motherwell', 'Marc Rothko', 'Helen  Frankenthaler', 'Franz Kline', 'Barnet Newman', 'Clifford Still', 'Arshile Gorky', 'Lee Krasner', 'Jackson Pollock']

import re
import subprocess

#---------------------------------------- MAKING FILE NAMES PRETTY --------------#

def old_rename_artists(artists):
	# works well except for changing case only:
	for artist in artists:
		x = "ls | perl -ne 'chomp; next unless -e; $o = $_; s/" + artist[0] + "/" + artist[1] + "/; next if -e; rename $o, $_';"
		print x
		
def rename_artists(artists):
	for artist in artists:
		x = "mv " + artist[0] + " " + artist[1]
		print x
		
#---------------------------------------- MAKING PRETTY DIRECTORY  --------------#

def get_image_directory():
	dirList = subprocess.check_output("ls")
	image = r"\w+\.\d+-*\d*\.\w+\.jpg"
	directory = re.findall(image,dirList)
	return directory
		
def last_names_registry():
	registry = []
	for artist in artists:
		a = re.split(r" ",artist)
		surname = a[-1].lower()
		registry.append((surname,artist))		
	return registry

rawnames = []
def collect_rawname(s,image):
	newS = re.sub(r'\w+_','',s)
	newS = re.sub(r'\w+-','',s)
	newS = newS.lower()
	mv = []
	mv = re.sub(s,newS,image)
	if s != newS:
		rawnames.append([image,mv])

def get_full_name(s,artists,image):
	for artist in artists:
		if s == artist[0]:
			return artist[1]
	collect_rawname(s,image)
	return s.lower()

def make_title(s):
	# split camelCase, then make pretty
	lowers = ["a","an","the","is","on","of","du"]
	title = re.sub(r'([a-z]*)([A-Z])',r'\1 \2',s)
	for	l in lowers:
		r1 = " " + l.capitalize()
		r2 = " " + l
		title = re.sub(r1,r2,title)
		title = title[0].upper() + title[1:]
		return title

def make_pretty(images,artists):
	works = []
	for image in images:
		raw = re.split(r"\.",image)
		name = get_full_name(raw[0],artists,image)
		date = raw[1]
		title = make_title(raw[2])
		works.append([name,title,date])
	
registry = last_names_registry()
directory = get_image_directory()
make_pretty(directory,registry)
rename_artists(rawnames)
