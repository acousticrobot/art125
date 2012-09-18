#!/usr/bin/env python

# Name: Image Indexer
# Author: Jonathan Gabel
# version: 0.9.1
# (c) GPL 2012
# URL: http://jonathangabel.com
# Image Indexer is a command line utility to deal with artist image repositories.
# It works with images named with the following naming convention:
# artist.date.Title.Subtitle.jpg
# It expects a file in the directory named __whos_who.txt with the following dictionary
# format, one artists per line:
# artist : FirstName LastName


import re
import subprocess
import datetime
import codecs # codecs.open() handles unicode
from unidecode import unidecode
import operator # for sorting dict in menu()
import os # check if directory is valid in change_dir()

CURRDIR = os.getcwd() + '/'
FOO = "bar"

DEFCOLOR = 'COLOR_LIGHT_BLUE'
C_N = '$none'
C_LG = '$lgreen'
C_G = '$green'
C_B = '$blue'
C_LB = '$lblue'
C_R = '$red'
C_GY = '$gray'
C_P = '$purple'
C_LP = '$lpurple'
C_Y = '$yellow'

#-------------- FORMATTING AND WRITING TO TERMINAL  -------------------------#

def pretty_string(s):
    # split camelCase, then make pretty
    lowers = [  'a', 'an', 'and', 'da', 'du', 'is', 'in', 'on', 
                'of', 'the', 'to']
    exceptions = [  ('I I I', 'III'), ('I I', 'II'), (' W ',' with '),
                    (r'^[l|L]$',"l'"), (r'[i|I]m ',"I'm "),('O ',"O'"),
                    (r'[w|W]hos ','Who\'s'),('D I A','DIA'),
                    ('N Y C','NYC'),('N Y'),('NY'),('L A', 'LA'),
                    ('freuds','freud\'s'),
                    ('T N'),('TN'),('Didnt','Didn\'t'),('Dont','Don\'t'),('Lets','Let\'s'),
                    ('Im','I\'m'),('Jaspers','Jasper\'s'),('Platos','Plato\s'),
                    ('Sambos','Sambo\'s'),]
    title = re.sub(r'([a-z]*)([A-Z])', r'\1 \2', s)
    title = re.sub(r'([a-z]+)([0-9])', r'\1 \2', title)
    for l in lowers:
        l1 = ' ' + l.capitalize() + ' '
        l2 = ' ' + l + ' '
        title = re.sub(l1,l2,title)
    for e in exceptions:
        title = re.sub(e[0],e[1],title)
    title = title[0].upper() + title[1:]
    return title


def pretty_file_name(l, artist = '', display = False):
    """Makes a human readable string from image file."""
    file_name = list_to_dotstring(l)
    if artist == '':
        artist = pretty_string(l[0])
    date = l[1]
    title = pretty_string(l[2])
    if len(l) > 4:
        sub_title = ''
        for s in l[3:-1]:
            sub_title += pretty_string(s) 
        title += ' (' + sub_title + ')'
    if display:
        s1 = s2 = ' '
        if len(artist) < 12:
            s1 += (12 - len(artist)) * ' '
        if len(date) < 8:
            s2 += (9  - len(date)) * ' '
        cprint(C_Y,artist,s1,C_B,date,s2,C_P,title)
    return artist, date, title, file_name


def color(s = ""):
    if s == '$none':
        c = '${COLOR_NC}\c'
    elif s == '$white':
        c = '${COLOR_WHITE}\c'
    elif s == '$black':
        c = '${COLOR_BLACK}\c'
    elif s == '$blue':
        c = '${COLOR_BLUE}\c'
    elif s == '$lblue':
        c = '${COLOR_LIGHT_BLUE}\c'
    elif s == '$green':
        c = '${COLOR_GREEN}\c'
    elif s == '$cyan':
        c = '${COLOR_CYAN}\c'
    elif s == '$lgreen':
        c = '${COLOR_LIGHT_GREEN}\c'
    elif s == '$lcyan':
        c = '${COLOR_LIGHT_CYAN}\c'
    elif s == '$red':
        c = '${COLOR_RED}\c'
    elif s == '$lred':
        c = '${COLOR_LIGHT_RED}\c'
    elif s == '$purple':
        c = '${COLOR_PURPLE}\c'
    elif s == '$lpurple':
        c = '${COLOR_LIGHT_PURPLE}\c'
    elif s == '$brown':
        c = '${COLOR_BROWN}\c'
    elif s == '$yellow':
        c = '${COLOR_YELLOW}\c'
    elif s == '$gray':
        c = '${COLOR_GRAY}\c'
    elif s == '$lgray':
        c = '${COLOR_LIGHT_GRAY}\c'
    else:
        c = '${' + DEFCOLOR + '}\c'
    call = 'echo "' + c + '"'
    subprocess.call(call, shell = True)


def cprint(*print_list):
    """Take a list of strings, print them to terminal in color.
    
    Send a list of strings, if strings are color keywords, terminal color
    is changed.
    """
    for s in print_list:
        s = str(s)
        if len(s) > 0 and s[0] == '$':
            color(s)
        else:
            call = 'echo "' + s + '\c"'
            subprocess.call(call, shell = True)
    color()
    print ""
    return


def cprint_list(color,l,pretty=False):
    color(color)
    for item in l:
        if pretty:
            print pretty_string(item)
        else:
            print item
    color()


def section(heading='*****'):
    cprint( '\n', C_Y,'***** ',C_B, heading.upper(), C_Y, ' *****')


def menu(d,prompt='true'): 
    """Take a dictionary, and turns it into a menu"""  
    keys = []
    try:
        title = d.pop('TITLE')
        section(title)
    except KeyError:
        section()
    sorted_d = sorted(d.items())
    for key in sorted_d:
        row = [C_LB,'  {0:10}'.format(key[0]),' : ',C_LG,'{}\n'.format(key[1])]
        keys.extend(row)
    cprint(*keys)
    if prompt:
        return raw_input('Enter Selection: ')


#-------------- WRITING TO FILE  --------------------------------------------#

def write_list(l,f):
    """Writes list l, one item per line, to file f."""
    count = 0
    for item in l:
        try:
            f.write(item)
        except UnicodeDecodeError:
            cprint(C_R, 'error on {}'.format(item))
        f.write('\n')
        count += 1
    return count


def write_dict(l,f):
    count = 0
    for k, v in sorted(l.items()):
        item = k + ', ' + v
        f.write(item)
        f.write('\n')
        count += 1
    return count


def write_to_file(l,file_name,title,o_type='list', mode='w'):
    """Save a list to a file"""
    file_path = CURRDIR + file_name
    cprint(C_G, "file saving mode: ", mode)
    f = codecs.open(file_path, encoding='utf-8', mode=mode)
    count = 0
    now = str(datetime.datetime.now())
    now_stamp = '##### Generated: ' + now + '\n\n'
    hash_title = '# ' + title
    f.write(hash_title)
    f.write('\n')
    f.write(now_stamp)
    if o_type == 'list':
        count = write_list(l,f)
    elif o_type == 'dict':
        count = write_dict(l,f)
    end_title = """
##### end generated log
##### total items = """ + str(count) + '\n\n'
    f.write(end_title)
    f.close()
    cprint (C_G, 'Saved ', C_P, title, C_G, ' to file ', C_LG, file_path)
    return


def write_titles(args,split=True):
    """Save titles to file from image directory.
    
    Assumes format: name.date.title.etc.jpg
    args passed as a string and can contain the following:
         -fx : from x in alphabet forward
         -tx : to x in alphabet forward
         -p2 : target position 2 (name is position 0)
    split is optional, splits titles simply at capitals 
    """
    frm, thru, pos = '0', 'z', 2
    args = re.split(r' ',args)
    for arg in args:
        if arg[:2] == '-f':
            frm = arg[2]
        if arg[:2] == '-t':
            thru = arg[2]
        if arg[:2] == '-p':
            pos == int(arg[2])
    titles = []
    images = load_images_as_lists()
    for image in images:
        i = list(image) #necessary?
        if len(i) > pos + 1:
            if i[pos][0] >= frm and i[pos][0] <= thru:
                title = i[2]
                if split:
                    title = re.sub(r'([A-Z])', r' \1', title);
                titles.append(title)
    title_set = sorted(set(titles))
    cprint(C_P,"Titles {f} through {t}".format(f = frm, t = thru))
    color(C_LP)
    for title in title_set:
        print title
    color()
    sel = raw_input('Save Selection? [Y/N]: ')
    if sel in ('y','Y'):
        f = 'Image Titles From {f} Through {t} at Position {p}'.format(
                f = frm, t = thru, p = pos)
        write_to_file(title_set,'_titles.txt', f, 'list','a') 
    else:
        print "Exiting without saving..."


#-------------- LOADING FROM FILES AND DIRECTORY ----------------------------#

def change_dir(s):
    global CURRDIR
    s = s.strip()
    if os.path.isdir(s):
        CURRDIR = s + '/'
        return True
    else:
        cprint(C_R,'Directory ', C_P, s, C_R, " Not Found.")
        return None
 
def nav_dir_menu():
    "Create a help menu used to navigate the directories"
    menu_args = {
        'TITLE': 'ENTER DIRECTORY CHANGES',
        'RETURN': 'Return with current directory',
        '/new_dir' : 'change to /new_dir',
        'new_dir' : 'current directory/new_dir',
        '..' : 'current parent directory',
        'Q' : 'Quit Program'
    }
    menu(menu_args,False)
    

def nav_dir(sel=False):
    print sel
    """Validate the current global directory"""
    valid_dir = os.path.isdir(CURRDIR)
    cprint(C_B,'NAVIGATE CURRENT DIRECTORY ([h]elp)')
    while True:
        color(C_G)
        if not sel:      
            sel = raw_input(CURRDIR + " cd> ")
        if sel in ('h','H'):
            nav_dir_menu()
        elif sel in ('q','Q'):
            return None
        elif not sel or sel == '':
            if valid_dir:
                cprint ('Saving current directory: ', C_G, CURRDIR)
                return True
            else:
                cprint(C_R,'You must pick a valid directory')
        elif sel == '..':
            sel = os.path.dirname(CURRDIR[:-1])
        elif sel[0] != '/':
            sel = CURRDIR + sel.strip()
        else:
            sel = sel.strip()
        valid_dir = change_dir(sel)
        sel = False


def load_directory_as_list(dir):
    """Load files in directory into list."""
    ls_comm = 'ls -R ' + dir
    try:
        d = subprocess.check_output(ls_comm, shell=True)
    except subprocess.CalledProcessError:
        cprint(C_R,"Error finding Directory {}".format(dir))
        return None
    dir_list = re.split(r'\s',d)
    return dir_list


def compare_directories(dir1='',dir2=''):
    d1 = load_directory_as_list(dir1)
    d2 = load_directory_as_list(dir2)
    if not d1 or not d2:
        cprint(C_R,"Undable to compare Directories")
        return None
    d1, d2 = set(d1), set(d2)
    in1 = sorted(d1 - d2)
    in2 = sorted(d2 - d1)
    diff = ["--------> Unique to {}".format(dir1)]
    diff.extend(in1)
    diff.append("<-------- Unique to {}".format(dir2))
    diff.extend(in2)
    title = "Directory Comparison {} {}".format(dir1,dir2)
    file_name = "_xdir.txt"
    write_to_file(diff, file_name, title, o_type='list', mode='a')
    
def load_file_as_list(file_name):
    """Transfer lines from a file into a list"""
    l = []
    path = CURRDIR + file_name
    print "Loading File {}...".format(file_name)
    if os.path.exists(path):
        with codecs.open(path, encoding='utf-8') as f:
            for ln in f:
                    if (ln[0] != '#') and (ln != '\n'):
                        l.append(ln[0:-1])
    else:
        sel = ''
        while sel not in ('y','n'):
            s = raw_input('No file {} found, create new? [Y/N]: '.format(file_name))
            sel = s.lower()
            if sel == 'y':
                write_to_file([],file_name,"NEW {}".format(file_name))  
            elif sel == 'n':
                cprint(C_R,"No {} created".format(file_name))
                return None
    return l


def load_file_as_dict(f):
    """Load dictionary from file and returns python dict
    
    File should have one entry per line: key: value"""
    l = load_file_as_list(f)
    if not l:
        cprint(C_R,"Empty file or unloadable as dictionary.")
        return
    a = []
    for line in l:
        line = re.split(r':',line)
        if len(line) != 2:
            cprint(C_R, "Skipping line: {}, Invalid Format for Dictionary".format(line))
        else:
            for i in range(len(line)):
                line[i] = line[i].strip()
            a.append(line)
    d = dict(a)
    return d


def add_file_to_list(file_name,l):
    """Append lines from a file into a list"""
    with codecs.open( CURRDIR + file_name, encoding='utf-8') as f:
        for ln in f:
                if (ln[0] != '#') and (ln != '\n'):
                    l.append(ln[0:-1])
    return l


def load_images_as_lists():
    """Make list from directory images, split each on dots into list."""
    directory = load_directory_as_list(CURRDIR)
    i_list = []
    for item in directory:
        i_list.append(re.split(r'\.',item))
    for i in list(i_list):
        if 'jpg' not in i:
            i_list.remove(i)
    return i_list


def list_to_dotstring(l):
    """Put a file name back together from the list version"""
    build = ''
    for section in l:
        build += '.' + section 
    return build[1:]


def load_artists_in_dir():
    """Return list of artist from current directory
    
    no titles or dates retained"""
    image_list = load_images_as_lists()
    artists = []
    for i in image_list:
        if i[0] not in artists:
            artists.append(i[0])
    return artists


def find(args,split=True):
    images = load_images_as_lists()
    srch, pos, typ, search_all = [], 2, 'intersection', False
    args = re.split(r' ',args)
    for arg in args:
        if arg == '-u':
            typ = 'union'
        elif arg == '-i':
            typ = 'intersection'
        elif arg == '-a':
            pos = 0
        elif arg == '-t':
            pos = 2
        elif arg == '-e':
            search_all = True
        elif arg[:2] == '-p':
            pos = arg[3]
        elif arg != '':
            srch.append(arg.lower())
    results = []
    cprint(C_GY,"Search Type: ", C_LG, typ)
    if search_all:
        cprint(C_GY,"Searching all Positions...")
    else:
        cprint(C_GY,"Search Position: ",C_LG, pos)
    if typ == 'intersection':
        refined_results = []
    for i in range(len(srch)):
        cprint(C_GY,"Searching: ",C_LG, srch[i])
        if i == 0 or typ == 'union':
            targets = images
            collection = results
        else:
            targets = results
            collection = refined_results
        for target in targets:
            if search_all:
                for item in target:
                    if srch[i] in item.lower() and target not in collection:
                        collection.append(target)
            else:
                if target[pos] and srch[i] in target[pos].lower():
                    if target not in collection:
                        collection.append(target)
        if i > 0 and typ == 'intersection':
            results = list(refined_results)
    for item in results:
        pretty_file_name(item,display = True)
    menu_args = {'TITLE': 'Save Options',
                    'F': 'Full file name',
                    'T':'Title Only',
                    '[0-9]':'Title at Position',
                    'P':'Title as Search Position',
                    'Return':'Return Without Save'}
    sel = menu(menu_args)
    res = []
    if sel == '' or sel[0] in ('r','R'):
        cprint(C_R,'Returning without save')
        return
    if sel in ('F','f'):
        for f in results:
            res.append(list_to_dotstring(f))
    elif sel in ('p', 'P'):
        sel = pos # next if, we save only the position from the find
    elif sel in ('t','T'):
        sel = 2
    else:
        try:
            sel = int(sel)
        except ValueError, TypeError:
            cprint(C_R,"Not a valid value, skipping save...")
            return 
    if sel in range(0,9):
        for f in results:
            if f[sel]:
                s = f[sel]
                if split:
                    s = re.sub(r'([A-Z])', r' \1', s);
                res.append(s)
    t = 'File from {t} search: {s} at position {p}'.format(
            t = typ, s = srch, p = sel )
    write_to_file(res,'_titles.txt', t, mode='a') 
        
    


#-------------- CLEANING ODD FILES ------------------------------------------#

def write_names():
    """Match names from images to whos_who, print all to file.
    
    DEPRECIATED: load_whos_who is now load_file_as_dict()
    Keeping as is for historical documentation."""
    quicknames = load_artists_in_dir()
    ww = load_whos_who('__whos_who.txt')
    names = []
    for artist in quicknames:
        if artist in ww:
            n = u'{quickname}, {fullname}'.format(
                                quickname = artist,fullname = ww[artist])
            names.append(n)
        else:
            n = u'{quickname}, ** {title}'.format(
                                quickname = artist, title = artist.title())
            names.append(n)
    write_to_file(names,'_names.txt','Artist Names and Quicknames')


def gather_artists():
    """Load and combine artist names from files '_artists_logged.txt' and '_artists_add.txt'."""
    artists = []
    for f in ('_artists.txt', '_add.txt'):
        add_file_to_list(f,artists)
    a_set = sorted(set(artists))
    return a_set


def under_to_camel():
    """Clean up the image file names: my_title to myTitle
    
    titles with underscores replace with camel
    NOTE: for safety, this function only prints the mv commands,
    review and then copy / paste into terminal"""
    images = load_images_as_lists()
    for image in images:
        i = list(image)
        change = False
        if len(i) > 3 and '_' in i[2]:
            new_title = ''
            name = re.split(r'_',i[2])
            for n in name:
                n = n[0].upper() + n[1:]
                new_title += n
            new_title = new_title[0].lower() + new_title[1:]
            i[2] = new_title
            change = True
        if change:
            old_image = list_to_dotstring(image)
            new_image = list_to_dotstring(i)
            print_bash_rename(old_image, new_image)


def add_dots():
    """Read in titles with added dots from file, make alterations"""
    images = load_images_as_lists()
    titles = load_file_as_list('_titles.txt')
    for title in titles:
        s = re.split(r'\.',title)
        strip = ''
        for word in s:
            strip += word
        for image in images:
            if len(image) > 3 and image[2] == strip:
                old_image = list_to_dotstring(image)
                i = list(image)
                i[2] = title
                new_image = list_to_dotstring(i)
                print_bash_rename(old_image, new_image)


def make_quicknames(artists):
    """Get artist's names from file with format: last, first
    
    return list with format: [('quickname','first last')]"""
    registry = []
    for artist in artists:
        a = re.split(r', ',artist)
        quickname = unidecode(a[0].lower())
        if len(a) == 1:
            full_name = a[0]
        else:
            full_name = a[1] + ' ' + a[0]
        registry.append((quickname,full_name))       
    return registry


def artist_dict_from_files():
    """Turn artist list from files into a dictionary.
    
    input form: last name, first name
    returns: quickname, Full Name"""
    artists_list = gather_artists()
    registry = make_quicknames(artists_list)
    return dict(registry)


#-------------- RENAMING IMAGES ---------------------------------------------#

def print_bash_rename(old_name, new_name):
    rename = 'mv ' + CURRDIR + old_name + ' ' + CURRDIR + new_name
    cprint(C_R, 'mv ', C_GY, old_name, ' ', C_B, new_name)
    return rename


def execute_bash_rename(f='_rename.txt'):
    l = load_file_as_list(f)
    for item in l:
        if item[:3] == "mv ":
            subprocess.check_call(item, shell=True)
            cprint(C_Y, "executing: ", C_R, item)
    return


def alter_txt(text,operation,pattern,add=''):
    """Alter text with a regex, pivot on a group.
    
    see examples in alter_file_names below"""
    m = re.search(pattern,text)
    new_text = ''
    if m and m.groups() > 0:
        if operation == 'prepend':
            new_text = text[0:m.start(1)] + add + text[m.start(1):len(text)]
        elif operation == 'append':
            new_text = text[0:m.end(1)] + add + text[m.end(1):len(text)]
        elif operation == 'remove':
            new_text = text[0:m.start(1)] + text[m.end(1):len(text)]
        elif operation == 'replace':
            new_text = text[0:m.start(1)] + add + text[m.end(1):len(text)]
        return new_text
    else:
        return None


def alter_file_names(objective,pattern,replacement=''):
    """Find offending names and print an mv command.
    
    regex expects at least one group
    examples:
        'prepend', r'\.(\d\d)\.','19' : 47 to 1947
        'append', r'\.(1900)\.','s' : 1900 to 1900s
        'slice', r'(1900\.)19\d+' : 1900.1947 to 1947
        'replace', r'(__)', '.' : __detail to .detail
    """
    directory = load_directory_as_list(CURRDIR)
    p = re.compile(pattern)
    r = re.compile(replacement)
    for f in directory:
        if p.search(f) != None:
            new_name = alter_txt(f, objective, p, replacement)
            print_bash_rename(f, new_name)         


def lower_first_character():
    """Clean up the file name sections: MyName.FirstChar to myName.firstChar.
    
    NOTE: for safety, this function only prints the mv commands to 
    file _rename.txt, review and then [X] EXECUTE in terminal."""
    images = load_images_as_lists()
    renames = []
    for image in images:
        new = list(image)
        change = False
        for i in range(len(new)):
            if new[i][0].isupper():
                new[i] = new[i][0].lower() + new[i][1:]
                change = True
        if change:
            old_name = list_to_dotstring(image)
            new_name = list_to_dotstring(new)
            renames.append(print_bash_rename(old_name, new_name))
    write_to_file(renames,'_rename.txt','Rename Commands') 
    print 'Review _rename.txt and then press X to EXECUTE'


def space_rinse_and_repeat(pos = 2):
    """Reads new titles from file, finds old file and prints bash mv.
    
    Save list of titles and open file. Split with spaces where it
    should be capitalized, and save as _titles.txt.  This function takes the
    file, makes a camel version of title,finds the original in the directory,
    and writes out the rename commands to _rename.txt. Review the rename    
    commands and copy / paste into the terminal. 
    Assumes file format: name.date.title.etc.jpg. Change pos to target other 
    than title position.
    """  
    images = load_images_as_lists()
    news = load_file_as_list('_titles.txt')
    renames = []
    for n in news:
        old = re.sub(' ', '', n)
        new = n.title()
        new = re.sub(' ', '', new)
        new = new[0].lower() + new[1:]
        for image in images:
            if len(image) > pos + 1 and image[pos] == old:
                old_image = list_to_dotstring(image)
                ni = list(image)
                ni[2] = new
                new_image = list_to_dotstring(ni)
                renames.append(print_bash_rename(old_image, new_image))
                break
    write_to_file(renames,'_rename.txt','Rename Commands') 
    print 'Review _rename.txt and then press X to EXECUTE'


def encode_str(str = 'andre.1999.AluminumDoubleTwelver.3versions'):
    """TODO: make a title coder / decoder """
    str = 'andre.1999.AluminumDoubleTwelver.3versions'
    str = str.encode('base-64','strict')
    print 'Encoded String: ' + str;
    print 'Decoded String: ' + str.decode('base-64','strict') 


#------------- ASSEMBLE THE ARMY  -------------------------------------------#

def check_whos_who():
    print "Loading images..."
    images = load_images_as_lists()
    ww = load_file_as_dict('__whos_who.txt')
    if not ww:
        cprint(C_R,"Returning without loading Who's Who")
        return None
    unkn_artist = []
    for image in images:
        if image[0] not in ww and image[0] + ' : ' not in unkn_artist:
            print 'No record of: {}'.format(image[0])
            unkn_artist.append(image[0] + ' : ')
    if unkn_artist:
        cprint(C_R,"Unknown Artists Found")
        unkn_artist.append("# Add artist full name and update who\'s who. For example: zorn: John Zorn")
        write_to_file(unkn_artist,'_whos_new.txt','Add The Following:','list','a')
    else:
        cprint(C_G, 'Who\'s Who up to date.')


def update_whos_who():
    """Save whos_who to _whos_old and add whos_new to whos_who."""
    ww = load_file_as_dict('__whos_who.txt')
    wn = load_file_as_dict('_whos_new.txt')
    write_to_file(ww,'_whos_old.txt',"Who's Who Archive",'dict','a')
    new_ww = dict(ww.items() + wn.items())
    write_to_file(new_ww,'__whos_who.txt',
        "Who's Who: Quickname and Full Name",'dict')


def md_title_link(l):
    """Makes a Markdown Title linked to an image.
    
    Takes a list style image, returns md string"""
    artist, date, title, file_name = pretty_file_name(l,display = False)
    link = '[' + title + '](' + CURRDIR + file_name + ')'
    return link

           
def md_index():
    """Print image directory as markdown"""
    print "Loading Images..."
    images = load_images_as_lists()
    print "Loading Who's Who..."
    ww = load_file_as_dict('__whos_who.txt')   
    print "Saving File..."
    md = list(('## Image Index\n','\n'))
    
        # print alphabet-index:
    head = ''
    for i in range(65, 91):
        head += '[' + chr(i) + '][] '
    md.append(head)
    c = 64  # current index letter
    j = 0
    last = ''
    
    while j < len(images):
            # check artist name from file against who's who
        quickname = images[j][0]
        if images[j][0] not in ww:
            print 'Error on {num}, No record of: {image}'.format(
                        num = j, image = images[j] )
            print 'Please update Who\'s Who'
            j += 1
            continue
        md_name = '### ' + ww[images[j][0]] + '\n'
        year = images[j][1]
        if year == '1990s': # generic year, don't list
            md_title = md_title_link(images[j]) + '\n'
        else:
            md_title = md_title_link(images[j]) + ', ' + year + '\n'
        curr_c = quickname[0]
        if ord(curr_c) > c + 32: # a to A etc.
            c = ord(curr_c) - 32
            md.append('-----\n')
            md.append('*[---back to top---][Artist Names and Images]*\n')
            md.append('#### ' + chr(c))
            md.append('\n-----\n')
        if quickname != last:
            last = quickname
            md.append(md_name)
        md.append(md_title)
        j += 1
    write_to_file(md,'_index.md','Artist Names and Images')
    print "Contverting to HTML..."
    md = CURRDIR + '_index.md'
    html = CURRDIR + '_index.html'
    # pandoc = 'pandoc -f markdown -t html -o {} {}'.format(md, html)
    # d = subprocess.check_output(pandoc, shell=True)
    # print d
    # except CalledProcessError: 
    #     cprint(C_R,'Unable to Save html', d)


def init_dir():
    if not nav_dir():
        return None
    check_whos_who()
    return True   


def init():
    """Run a loop with program possibilities."""
    
    section('Initializing')
    if not init_dir():
        cprint(C_R,"Quitting on error loading directory")
        return
    section('Image Indexer')
    sel = ''
    while sel != 'Q':
        menu_args = {'TITLE':'Please Enter one of the following',
                    'md': 'Create markdown INDEX',
                    'title -f0 -tz -p2':
                        'Create TITLES list -from -to -file.name.position)',
                    'find -a/-t/-p -i/-u': 
                        'FIND files by artist/title/file.name.position intersetion/union',
                    'R': 'RINSE titles',
                    'L': 'LOWER-CASE titles',
                    'W': 'Update WHO\'S WHO\'S',
                    'X': 'EXECUTE rename commands',
                    'cd': 'change DIRECTORY',
                    'xd': 'cross directory comparison',
                    'Q' : 'Quit'}
        sel = menu(menu_args)
        if not sel:
            continue
        elif sel.lower() == 'md':
            print 'Creating Markdown Index...'
            md_index()
        elif sel[0:4].lower() == 'find':
            print 'Find files...'
            find(sel[4:])
        elif sel[0:5].lower == 'title':
            print '\nWriting Titles to File...\n'
            write_titles(sel[5:])   
        elif sel in ('r','R'):
            print '\nWriting Title Rename Commands to File...\n'
            space_rinse_and_repeat()
        elif sel in ('l','L'):
            print '\nWriting Title Rename Commands to File...\n'
            lower_first_character()
        elif sel in ('w','W'):
            print 'Updating Who\'s Who...'
            update_whos_who()
        elif sel in ('x','X'):
            print '\nExecuting Bash Renames...\n'
            execute_bash_rename()
        elif sel[0:2].lower() == 'cd':
            print '\nChanging Directory...\n'
            sel = sel[2:].strip()
            nav_dir(sel)
            check_whos_who()
        elif sel[0:2].lower() == 'xd':
            sel = sel[2:].strip()
            dirs = re.split(" ",sel)
            print dirs
            dir1 = dirs[0].strip()
            dir2 = dirs[1].strip()
            try:
                compare_directories(dir1,dir2)
            except IndexError, subprocess.CalledProcessError:
                cprint(C_R,"Not valid Directories")
        elif sel in ('Q','q'):
            print 'Exiting...'
            sel = 'Q'
            


init()